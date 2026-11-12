import json
p='/home/claude/appespagnol/index.html';h=open(p,encoding='utf8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:70],h.count(a));h=h.replace(a,b)
J=lambda x:json.dumps(x,ensure_ascii=False)
h=h.replace("👭","👧")   # pas d'image 3D pour 👭

# toutes les leçons déjà créées, regroupées en Niveaux 5 à 7 (offre Ultimate seulement)
rep("const FAM_PREVIEW=FAM_UNITS.slice(0,5).map(u=>u.id);","""const FAM_PREVIEW=FAM_UNITS.slice(0,5).map(u=>u.id);
/* Offre Ultimate (v25) : toutes les leçons déjà écrites qui ne sont pas sur la carte gratuite, rangées par difficulté
   en Niveaux 5 (mots), 6 (quotidien) et 7 (phrases). Copies : l'id (et donc les étoiles) ne change pas. */
const EXTRA_UNITS=ALL_UNITS.filter(u=>!ACTIVE.includes(u.id)&&!u.phr).map(u=>Object.assign({},u,{tier:4+Math.min(3,Math.max(1,u.tier||1))})).sort((a,b)=>a.tier-b.tier);""")
rep("  for(let k=UNITS.length-1;k>=0;k--)if(UNITS[k].tier===4)UNITS.splice(k,1);","  for(let k=UNITS.length-1;k>=0;k--)if(UNITS[k].tier>=4)UNITS.splice(k,1);")
rep("  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famUltimate()?FAM_UNITS.length:famOpen(famStart())));",
    "  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famUltimate()?FAM_UNITS.length:famOpen(famStart())));\n  if(famUltimate())UNITS.push(...EXTRA_UNITS);")
rep("4:['Niveau 4','Dans la vraie vie']};","4:['Niveau 4','Dans la vraie vie'],5:['Niveau 5','Encore des mots'],6:['Niveau 6','Encore mon quotidien'],7:['Niveau 7','Encore des phrases']};")
# avec le code, tout est ouvert : ni ordre, ni évaluation, ni « une nouvelle leçon par jour » (le temps d'écran reste)
rep("""const unlocked=i=>{
  const u=UNITS[i];""","""const unlocked=i=>{
  const u=UNITS[i];if(famUltimate())return true;""")
rep("""function newGate(i){
  if(""","""function newGate(i){
  if(famUltimate())return null;
  if(""")
# texte de l'espace parent
rep("margin:0\">Code bêta-testeur : toutes les leçons et tous les bonus sont ouverts sur ce téléphone. Le fonctionnement reste le même (une nouvelle leçon par jour, temps d'écran).",
    "margin:0\">Code bêta-testeur : toutes les leçons créées et tous les bonus sont ouverts sur ce téléphone, dans n'importe quel ordre. Le temps d'écran reste le même.")
ui={"Encore des mots":["More words","Altre parole"],"Encore mon quotidien":["More of my everyday life","Ancora la mia giornata"],"Encore des phrases":["More sentences","Altre frasi"],
 "Code bêta-testeur : toutes les leçons créées et tous les bonus sont ouverts sur ce téléphone, dans n'importe quel ordre. Le temps d'écran reste le même.":
 ["Beta-tester code: all lessons created so far and all bonuses are open on this phone, in any order. Screen time stays the same.","Codice beta-tester: tutte le lezioni create e tutti i bonus sono aperti su questo telefono, in qualsiasi ordine. Il tempo davanti allo schermo resta lo stesso."]}
rep("const UI={","const UI={"+','.join(J(k)+':'+J(v) for k,v in ui.items())+",")
open(p,'w',encoding='utf8').write(h);print('ok')
