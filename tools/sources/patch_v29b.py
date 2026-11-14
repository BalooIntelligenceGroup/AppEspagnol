import json,sys
sys.path.insert(0,'/home/claude')
from content_v29b import GAPS,SONGS,SONG_TR
P='/home/claude/appespagnol/index.html'
s=open(P,encoding='utf8').read()
J=lambda x:json.dumps(x,ensure_ascii=False)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
# phrases à trou + récitations des niveaux Famille en anglais / italien
i=s.index('const TG_SONGS=');j=s.index(';\n',i)+2
s=s[:j]+"/* v29 : leçons Famille (Niveaux 4 et 5) en anglais et en italien : phrases à trou, récitations des Niveaux 4 et 5 */\n"+ \
  "Object.assign(TG_GAPS.en,"+J(GAPS['en'])+");Object.assign(TG_GAPS.it,"+J(GAPS['it'])+");\n"+ \
  "TG_SONGS.en.push(..."+J(SONGS['en'])+");TG_SONGS.it.push(..."+J(SONGS['it'])+");\n"+s[j:]
# setTarget : les leçons Famille changent de langue comme les 15 gratuites
rep("ALL_UNITS.forEach(u=>{if(!u._o)u._o={es:u.es,words:u.words,talk:u.talk,gaps:u.gaps};const o=u._o;\n    if(t==='es'||!ACTIVE.includes(u.id)){",
    "const TGU=new Set([...ACTIVE,...FAM_UNITS.map(f=>f.id)]);   /* leçons qui existent dans les 3 langues : les 15 gratuites et les leçons Famille */\n  ALL_UNITS.forEach(u=>{if(!u._o)u._o={es:u.es,words:u.words,talk:u.talk,gaps:u.gaps};const o=u._o;\n    if(t==='es'||!TGU.has(u.id)){")
rep("SONGS.filter(s=>s.tier<=3).forEach((s,k)=>{const n=t==='es'?null:(TG_SONGS[t]||[])[k];","SONGS.filter(s=>s.tier<=5).forEach((s,k)=>{const n=t==='es'?null:(TG_SONGS[t]||[])[k];")
# offre Famille dans les 3 langues ; les anciennes leçons (Ultimate) restent en espagnol
rep("  if(TGT!=='es')return;\n  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famUltimate()?FAM_UNITS.length:famOpen(famStart())));\n  if(famUltimate())UNITS.push(...EXTRA_UNITS);",
    "  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famUltimate()?FAM_UNITS.length:famOpen(famStart())));   /* même offre Famille dans les 3 langues (v29) */\n  if(famUltimate()&&TGT==='es')UNITS.push(...EXTRA_UNITS);   /* anciennes leçons : espagnol seulement pour l'instant */")
rep("  if(TGT!=='es')return `<div class=\"tier fam\"><b>Bientôt ⭐</b><span>De nouvelles leçons arrivent bientôt !</span></div>`;\n","")
# sens des nouvelles récitations
rep("const SONG_TR={","const SONG_TR={"+J(SONG_TR)[1:-1]+",")
open(P,'w',encoding='utf8').write(s);print('ok')
