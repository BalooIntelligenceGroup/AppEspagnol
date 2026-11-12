import re
p='/home/claude/appespagnol/index.html';h=open(p,encoding='utf8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:60],h.count(a));h=h.replace(a,b)

# 1. Offre Famille : constantes + calcul selon la date d'abonnement (préparation, rien n'est payant)
rep("const ALL_UNITS=UNITS.slice();",
"""const ALL_UNITS=UNITS.slice();
/* ---------- Offre Famille (v23, affichage seulement : rien n'est payant pour l'instant) ----------
   Les 15 leçons de ACTIVE restent gratuites pour toujours. L'abonnement ajoutera FAM_PER_MONTH leçons
   par mois, comptées à partir de la date d'abonnement de chaque famille (famOpen). FAM_PREVIEW = leçons
   montrées verrouillées sur la carte (elles existent déjà dans le code). */
const FAM_PER_MONTH=5,FAM_PREVIEW=['zoo','juguetes','playa','cocinar','bosque'];
function famOpen(start,today){/* nombre de leçons Famille ouvertes : 5 le jour de l'abonnement, +5 à chaque mois entier */
  if(!start)return 0;const a=new Date(start+'T12:00:00'),b=new Date((today||dayPlus(0))+'T12:00:00');if(b<a)return 0;
  let m=(b.getFullYear()-a.getFullYear())*12+b.getMonth()-a.getMonth();if(b.getDate()<a.getDate())m--;
  return FAM_PER_MONTH*(m+1)}""")

# 2. Carte : bloc « Offre Famille » verrouillé après la coupe
rep("""<em>Termine les ${UNITS.length} leçons</em></div></div>`;
}""","""<em>Termine les ${UNITS.length} leçons</em></div>${famMap()}</div>`;
}
let famMsg=false;
function famMap(){
  const us=FAM_PREVIEW.map(id=>ALL_UNITS.find(u=>u.id===id)).filter(Boolean);
  return `<div class="tier fam"><b>Offre Famille ⭐</b><span>Bientôt : 5 nouvelles leçons chaque mois</span></div>`+
   us.map((u,i)=>`<button class="node locked famn" style="transform:translateX(${Math.round(Math.sin((UNITS.length+i)*1.1)*70)}px)" data-act="fam" aria-label="Leçon Famille : ${esc(tx(u.es,u.fr))}">
     <span class="disc">🔒</span><b>${esc(u.es)}</b><em>${esc(tx(u.es,u.fr))}</em><span class="ctag fam">⭐ Famille</span></button>${i===0&&famMsg?`<p class="hint-bubble">🌟 Ces leçons arriveront bientôt avec l'offre Famille. En attendant, profite de tes 15 leçons gratuites !</p>`:''}`).join('')}""")

rep("""  else if(a==='unit'){const i=+b.dataset.i;""","""  else if(a==='fam'){famMsg=true;say('¡Muy pronto!');render();const h=document.querySelector('.hint-bubble');if(h)h.scrollIntoView({block:'center',behavior:'smooth'})}
  else if(a==='unit'){const i=+b.dataset.i;""")

# 3. Espace parent : encadré d'information, sans prix
rep("""  ${PROMISE}
  <div class="set" style="background:var(--good-bg)"><b>🔒 Sans publicité""","""  ${PROMISE}
  <div class="set famset"><b>⭐ Offre Famille (bientôt)</b><p class="note" style="color:var(--ink);margin:0">Les 15 premières leçons (Niveaux 1 à 3) sont gratuites, pour toujours.</p><p class="note" style="color:var(--ink);margin:0">L'offre Famille ajoutera 5 nouvelles leçons chaque mois, à partir de la date d'abonnement de votre famille : votre enfant avance à son rythme, sans tout ouvrir d'un coup.</p><p class="note" style="margin:0">Rien n'est payant pour l'instant. Les leçons de l'offre sont visibles, verrouillées, sur la carte.</p></div>
  <div class="set" style="background:var(--good-bg)"><b>🔒 Sans publicité""")

# 4. Styles
rep(""".hint-bubble{position:relative;""",""".tier.fam b{background:var(--sun);color:var(--ink)}
.node.famn{opacity:.75}.node.famn .disc{filter:grayscale(.6)}
.ctag.fam{background:var(--sun);color:var(--ink)}
.famset{border:3px dashed var(--sun);display:grid;gap:6px}
.hint-bubble{position:relative;""")

# 5. Texte de nouveauté (les 3 demandes de la version 23)
rep('''23:"Nouveau : une boutique avec plein d'accessoires, des skins, des univers, 2 nouveaux jeux, des décors et des bonus à gagner avec tes pièces !",''',
'''23:"Nouveau : une boutique avec plein d'accessoires, des skins, des univers, 2 nouveaux jeux, des décors et des bonus à gagner avec tes pièces ! L'espace parent est mieux protégé, et de nouvelles leçons se préparent.",''')

# 6. Traductions de l'interface et des titres des leçons montrées
ui={
 "Nouveau : une boutique avec plein d'accessoires, des skins, des univers, {0} nouveaux jeux, des décors et des bonus à gagner avec tes pièces ! L'espace parent est mieux protégé, et de nouvelles leçons se préparent. Ta progression est gardée.":
  ["New: a shop full of accessories, skins, worlds, {0} new games, backgrounds and bonuses to win with your coins! The parent area is better protected, and new lessons are on the way. Your progress is saved.",
   "Novità: un negozio pieno di accessori, skin, mondi, {0} nuovi giochi, sfondi e bonus da vincere con le tue monete! Lo spazio genitori è più protetto e nuove lezioni sono in arrivo. I tuoi progressi sono salvati."],
 "Offre Famille ⭐":["Family plan ⭐","Offerta Famiglia ⭐"],
 "Bientôt : {0} nouvelles leçons chaque mois":["Coming soon: {0} new lessons every month","Presto: {0} nuove lezioni ogni mese"],
 "⭐ Famille":["⭐ Family","⭐ Famiglia"],
 "🌟 Ces leçons arriveront bientôt avec l'offre Famille. En attendant, profite de tes {0} leçons gratuites !":
  ["🌟 These lessons are coming soon with the Family plan. Until then, enjoy your {0} free lessons!","🌟 Queste lezioni arriveranno presto con l'offerta Famiglia. Nel frattempo, goditi le tue {0} lezioni gratuite!"],
 "⭐ Offre Famille (bientôt)":["⭐ Family plan (coming soon)","⭐ Offerta Famiglia (in arrivo)"],
 "Les {0} premières leçons (Niveaux {1} à {2}) sont gratuites, pour toujours.":["The first {0} lessons (Levels {1} to {2}) are free, forever.","Le prime {0} lezioni (Livelli da {1} a {2}) sono gratuite, per sempre."],
 "L'offre Famille ajoutera {0} nouvelles leçons chaque mois, à partir de la date d'abonnement de votre famille : votre enfant avance à son rythme, sans tout ouvrir d'un coup.":
  ["The Family plan will add {0} new lessons every month, counted from your family's subscription date: your child moves at their own pace, without unlocking everything at once.",
   "L'offerta Famiglia aggiungerà {0} nuove lezioni ogni mese, a partire dalla data di abbonamento della vostra famiglia: vostro figlio avanza al suo ritmo, senza aprire tutto in una volta."],
 "Rien n'est payant pour l'instant. Les leçons de l'offre sont visibles, verrouillées, sur la carte.":
  ["Nothing is paid for now. The plan's lessons are visible, locked, on the map.","Per ora non c'è nulla a pagamento. Le lezioni dell'offerta sono visibili, bloccate, sulla mappa."],
 "Leçon Famille : {0}":["Family lesson: {0}","Lezione Famiglia: {0}"],
}
import json
add=','.join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(v,ensure_ascii=False) for k,v in ui.items())
rep("const UI={","const UI={"+add+",")
trx={"En el zoo":["At the zoo","Allo zoo"],"Mis juguetes":["My toys","I miei giocattoli"],"En la playa":["At the beach","Al mare"],
 "¡A cocinar!":["Let's bake a cake","Facciamo una torta"],"En el bosque":["In the forest","Nel bosco"]}
add=','.join(json.dumps(k,ensure_ascii=False)+':'+json.dumps(v,ensure_ascii=False) for k,v in trx.items())
rep("const TRX={","const TRX={"+add+",")
open(p,'w',encoding='utf8').write(h);print('ok')
