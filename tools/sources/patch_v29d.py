import json,sys
sys.path.insert(0,'/home/claude')
from content_v29d import G,OVR,SONGS,ST
P='/home/claude/appespagnol/index.html'
s=open(P,encoding='utf8').read()
J=lambda x:json.dumps(x,ensure_ascii=False)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]);s=s.replace(a,b)
i=s.index('TG_SONGS.en.push(');j=s.index('\n',s.index('TG_SONGS.en.push('))+1
s=s[:j]+"/* v29 : anciennes leçons (Niveaux 6 à 12, code bêta) en anglais et en italien : phrases à trou (émoji repris de l'espagnol), récitations des Niveaux 6 à 12 */\n"+ \
  "Object.assign(TG_GAPS.en,"+J(G['en'])+");Object.assign(TG_GAPS.it,"+J(G['it'])+");\n"+ \
  "TG_SONGS.en.push(..."+J(SONGS['en'])+");TG_SONGS.it.push(..."+J(SONGS['it'])+");\n"+s[j:]
i=s.index('Object.assign(TG_OVR.en,');j=s.index('\n',i)+1
s=s[:j]+"Object.assign(TG_OVR.en,"+J(OVR['en'])+");Object.assign(TG_OVR.it,"+J(OVR['it'])+");   /* anciennes leçons : l'Espagne devient le pays de la langue apprise */\n"+s[j:]
rep("const TGU=new Set([...ACTIVE,...FAM_UNITS.map(f=>f.id)]);   /* leçons qui existent dans les 3 langues : les 15 gratuites et les leçons Famille */\n  ALL_UNITS.forEach(",
    "const TGU=new Set([...ACTIVE,...FAM_UNITS.map(f=>f.id),...EXTRA_UNITS.map(f=>f.id)]);   /* leçons qui existent dans les 3 langues : gratuites, Famille et anciennes leçons (v29) */\n  [...ALL_UNITS,...EXTRA_UNITS].forEach(")
rep("u.gaps=(o.gaps||[]).map((g,k)=>{const n=G&&G[k];if(!n)return g;al(n[0].replace('_',n[1]),g[0].replace('_',g[1]));return n})});",
    "u.gaps=(o.gaps||[]).map((g,k)=>{const n=G&&G[k];if(!n)return g;al(n[0].replace('_',n[1]),g[0].replace('_',g[1]));return n.length<4?[...n,g[3]]:n})});")
rep("SONGS.filter(s=>s.tier<=5).forEach((s,k)=>{","SONGS.forEach((s,k)=>{")
rep("  if(famUltimate()&&TGT==='es')UNITS.push(...EXTRA_UNITS);   /* anciennes leçons : espagnol seulement pour l'instant */","  if(famUltimate())UNITS.push(...EXTRA_UNITS);   /* anciennes leçons, dans les 3 langues (v29) */")
rep("const SONG_TR={","const SONG_TR={"+J(ST)[1:-1]+",")
open(P,'w',encoding='utf8').write(s);print('ok')
