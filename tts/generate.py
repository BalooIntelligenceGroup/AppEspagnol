"""Génère la voix de synthèse tunisienne (Microsoft, voix « arabe de Tunisie ») pour chaque phrase de tts/phrases.json.
Lancé automatiquement par GitHub Actions (.github/workflows/voix.yml). Un fichier par phrase : audio/tts/<hash>.mp3,
où <hash> est le même FNV-1a 32 bits que hashOf() dans index.html (calculé sur le texte latin de la phrase)."""
import asyncio, json, os, struct
import edge_tts

VOICE = os.environ.get('VOICE', 'ar-TN-ReemNeural')
RATE = os.environ.get('RATE', '-10%')
OUT = 'audio/tts'

def hash_of(t):
    b = t.strip().encode('utf-16-le')
    h = 0x811c9dc5
    for cu in struct.unpack('<%dH' % (len(b) // 2), b):
        h ^= cu
        h = (h * 0x01000193) & 0xFFFFFFFF
    return '%08x' % h

async def main():
    os.makedirs(OUT, exist_ok=True)
    phrases = json.load(open('tts/phrases.json', encoding='utf-8'))
    try:
        prev = {x['h']: x.get('k') for x in json.load(open(OUT + '/index.json', encoding='utf-8'))}
    except Exception:
        prev = {}
    index, made, failed = [], 0, []
    for p in phrases:
        h, key = hash_of(p['t']), p['ar'] + '|' + VOICE + '|' + RATE
        f = f'{OUT}/{h}.mp3'
        if not (os.path.exists(f) and os.path.getsize(f) > 1000 and prev.get(h) == key):
            for attempt in range(4):
                try:
                    await edge_tts.Communicate(p['ar'], VOICE, rate=RATE).save(f)
                    break
                except Exception as e:
                    print('retry', p['t'], e)
                    await asyncio.sleep(3 * (attempt + 1))
            if os.path.exists(f) and os.path.getsize(f) > 1000:
                made += 1
            else:
                failed.append(p['t'])
                continue
        index.append({'h': h, 't': p['t'], 'k': key})
    keep = {x['h'] for x in index}
    for name in os.listdir(OUT):
        if name.endswith('.mp3') and name[:-4] not in keep:
            os.remove(os.path.join(OUT, name))
    json.dump(index, open(OUT + '/index.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'{len(index)} phrases avec voix, {made} générées, {len(failed)} en échec: {failed[:5]}')

asyncio.run(main())
