import json,os,re,sys
sys.path.insert(0,'/home/claude');from content_v24 import FAM,MONTHLY,T
R='/home/claude/appespagnol/';p=R+'index.html';h=open(p,encoding='utf8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:70],h.count(a));h=h.replace(a,b)
J=lambda x:json.dumps(x,ensure_ascii=False)

# ---------- images : listes FX / FXL ----------
keys=sorted(f[:-5] for f in os.listdir(R+'fx') if f.endswith('.webp'))
h=re.sub(r"const FX=new Set\('[^']*'",lambda m:"const FX=new Set('"+' '.join(keys)+"'",h,count=1)
sw=open(R+'sw.js',encoding='utf8').read()
sw=re.sub(r"const FXL='[^']*'",lambda m:"const FXL='"+' '.join(keys)+"'",sw,count=1)
open(R+'sw.js','w',encoding='utf8').write(sw)

# ---------- leçons Famille et Bonus du mois ----------
def unit_js(u,tier,extra=''):
    talk=','.join('{l:%s,f:%s,p:%s,o:%s}'%(J(d['l']),J(d['f']),J(d['p']),J(d['o'])) for d in u['talk'])
    return '{id:%s,tier:%d,conv:true,phr:true,%ses:%s,fr:%s,e:%s,words:%s,talk:[%s],gaps:%s}'%(J(u['id']),tier,extra,J(u['es']),J(u['fr']),J(u['e']),J(u['words']),talk,J(u['gaps']))
fam_js='const FAM_UNITS=[\n '+',\n '.join(unit_js(u,4) for u in FAM)+'];'
mon_js='const MONTHLY=[\n '+',\n '.join('{m:%s,u:%s}'%(J(m),unit_js(u,4,'bonus:true,where:%s,'%J(u['where']))) for m,u in MONTHLY)+'];'
rep("const FAM_PER_MONTH=5,FAM_PREVIEW=['zoo','juguetes','playa','cocinar','bosque'];",
"""const FAM_PER_MONTH=5;
/* Leçons Famille (v24) : 10 phrases par leçon (conv + phr), de plus en plus complexes ; Niveau 4 = « Dans la vraie vie ».
   Bonus du mois (v24) : une leçon de culture (Espagne + Amérique latine) par mois (clé AAAA-MM), réservée à l'offre Famille,
   montrée sur la carte juste après la leçon en cours de l'enfant, quelle que soit sa progression. */
"""+fam_js+"\n"+mon_js+"""
ALL_UNITS.push(...FAM_UNITS,...MONTHLY.map(b=>b.u));
const FAM_PREVIEW=FAM_UNITS.slice(0,5).map(u=>u.id);
/* Abonnement Famille : date de début rangée par téléphone (clé hola-lola-fam), écrite plus tard par le compte parent.
   Aperçu de test : adresse terminée par #famille, hors du site Netlify (aperçu Claude). */
const FAM_KEY='hola-lola-fam';
function famInfo(){try{return JSON.parse(localStorage.getItem(FAM_KEY)||'null')}catch(e){return null}}
const famStart=()=>{const f=famInfo();return f&&f.start||null};
const famActive=()=>!!famStart();
const monthBonus=()=>{const m=new Date();const k=m.getFullYear()+'-'+String(m.getMonth()+1).padStart(2,'0');return MONTHLY.find(b=>b.m===k)||null};
function famSync(){
  try{if(location.hash==='#famille'&&!/netlify\\.app$/.test(location.hostname)&&!famActive())localStorage.setItem(FAM_KEY,JSON.stringify({start:dayPlus(0),preview:1}))}catch(e){}
  for(let k=UNITS.length-1;k>=0;k--)if(UNITS[k].tier===4)UNITS.splice(k,1);
  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famOpen(famStart())));
}""")
rep("const TIERS={1:['Niveau 1','Premiers mots'],2:['Niveau 2','Mon quotidien'],3:['Niveau 3','Premières phrases']};",
    "const TIERS={1:['Niveau 1','Premiers mots'],2:['Niveau 2','Mon quotidien'],3:['Niveau 3','Premières phrases'],4:['Niveau 4','Dans la vraie vie']};")

# traductions des contenus (anglais, italien)
rep("const TRX={","const TRX={"+','.join(J(k)+':'+J(v) for k,v in T.items())+",")
# les phrases des leçons servent aussi de traduction française (phrases à trou, « Traduis »)
rep("ALL_UNITS.forEach(u=>(u.talk||[]).forEach(d=>{if(d.f)TRM[d.l]=d.f;d.o.forEach(o=>{if(o.length>2)TRM[o[0]]=o[1]})}));",
    "ALL_UNITS.forEach(u=>{(u.talk||[]).forEach(d=>{if(d.f)TRM[d.l]=d.f;d.o.forEach(o=>{if(o.length>2)TRM[o[0]]=o[1]})});if(u.phr)u.words.forEach(w=>{if(!TRM[w[0]])TRM[w[0]]=w[1]})});")
# le prénom de l'enfant dans les phrases ({name})
rep("const W=w=>({es:gx(w[0],S.gender),fr:gx(tx(w[0],w[1]),S.gender),","const W=w=>({es:gx(nameFill(w[0]),S.gender),fr:gx(nameFill(tx(w[0],w[1])),S.gender),")
# mots des Bonus réussis : dans le dico et la révision
rep("function wordMap(){const m={};UNITS.forEach(u=>","function wordMap(){const m={};UNITS.concat(MONTHLY.map(b=>b.u).filter(u=>S.stars[u.id])).forEach(u=>")

# ---------- exercices plus difficiles pour les leçons à phrases ----------
rep("""function buildSteps(u,n){
  const c=[...u.talk.map(d=>({s:d.o.find(isOk)[0],p:d.p||''})),...u.gaps.map(g=>({s:g[0].replace('_',g[1]),p:g[3]}))]
    .filter(x=>{const k=tilesOf(x.s).length;return k>=3&&k<=7});
  return shuffle(c).slice(0,n).map(x=>{
    const ws=tilesOf(x.s),wn=ws.map(nw);
    const extra=u.tier>1?shuffle(u.words.flatMap(w=>tilesOf(w[0])).filter(y=>!wn.includes(nw(y)))).slice(0,1):[];
    return {t:'build',sent:x.s,p:x.p,target:ws,tiles:shuffle([...ws,...extra]),used:[]}});
}""","""function buildSteps(u,n,fr){
  const c=[...u.talk.map(d=>({s:d.o.find(isOk)[0],p:d.p||''})),...u.gaps.map(g=>({s:g[0].replace('_',g[1]),p:g[3]})),...(u.phr?u.words.map(w=>({s:w[0],p:w[2]})):[])]
    .filter(x=>{const k=tilesOf(x.s).length;return k>=3&&k<=(u.phr?8:7)});
  const seen=new Set();
  return shuffle(c).filter(x=>!seen.has(x.s)&&seen.add(x.s)).slice(0,n).map(x=>{
    const ws=tilesOf(x.s),wn=ws.map(nw);
    const extra=u.tier>1?shuffle(u.words.flatMap(w=>tilesOf(w[0])).filter(y=>!wn.includes(nw(y)))).slice(0,u.phr?2:1):[];
    return {t:'build',sent:x.s,p:x.p,target:ws,tiles:shuffle([...ws,...extra]),used:[],fr:!!fr}});
}""")
rep("""  buildSteps(u,2).forEach(s=>steps.push(s));
  shuffle(words.slice()).slice(0,u.tier>1?3:2).forEach(w=>steps.push({t:'speak',w}));""","""  if(u.phr){const bs=buildSteps(u,5);bs.forEach((s,k)=>{if(k<2)s.fr=true;steps.push(s)})}   /* phrases : 3 à écouter, 2 à traduire */
  else buildSteps(u,2).forEach(s=>steps.push(s));
  shuffle(words.slice()).slice(0,u.tier>1?3:2).forEach(w=>steps.push({t:'speak',w}));""")
# startUnit accepte une leçon hors de la carte (Bonus du mois)
rep("""function startUnit(i){
  const u=UNITS[i],""","""function startUnit(i,uo){
  const u=uo||UNITS[i],""")
rep("L={unit:i,kind:'unit',steps:mix(u.id,learn,steps),","L={unit:uo?-1:i,u:uo||null,kind:'unit',steps:mix(u.id,learn,steps),")
rep("""  if(L.unit>=0){const id=UNITS[L.unit].id;newUnit=!S.stars[id];S.stars[id]=Math.max(S.stars[id]||0,stars);if(newUnit)S.newDay=dayPlus(0)}""",
"""  if(L.unit>=0){const id=UNITS[L.unit].id;newUnit=!S.stars[id];S.stars[id]=Math.max(S.stars[id]||0,stars);if(newUnit)S.newDay=dayPlus(0)}
  if(L.u){S.stars[L.u.id]=Math.max(S.stars[L.u.id]||0,stars)}   /* Bonus du mois : étoiles gardées, ne compte pas comme la nouvelle leçon du jour */""")
rep("const coins=L.kind==='chat'?3:L.unit>=0?(5+(L.mistakes===0?3:0)):5;","const coins=L.kind==='chat'?3:(L.unit>=0||L.u)?(5+(L.mistakes===0?3:0)):5;")
# « Traduis la phrase » : la phrase française est donnée, le son ne vient qu'après la réponse
rep("""    body=`<div class="ask">Construis la phrase<small>Écoute ${G().es}, puis touche les mots dans le bon ordre.</small></div>
    <div class="buildtop">${s.p?`<div class="prop">${esc(s.p)}</div>`:''}<button class="speaker sm" data-act="hear" aria-label="Écouter la phrase">🔊</button></div>${trRow(fill(tr(s.sent)))}""",
"""    body=s.fr?`<div class="ask">Traduis la phrase<small>Dis-la en espagnol : touche les mots dans le bon ordre.</small></div>
    <div class="buildtop">${s.p?`<div class="prop">${pic(s.p)}</div>`:''}<div class="frsent">${esc(fill(tr(s.sent)))}</div>${a?'<button class="speaker sm" data-act="hear" aria-label="Écouter la phrase">🔊</button>':''}</div>`
    :`<div class="ask">Construis la phrase<small>Écoute ${G().es}, puis touche les mots dans le bon ordre.</small></div>
    <div class="buildtop">${s.p?`<div class="prop">${esc(s.p)}</div>`:''}<button class="speaker sm" data-act="hear" aria-label="Écouter la phrase">🔊</button></div>${trRow(fill(tr(s.sent)))}""")
rep("settle(s,ok,`« ${esc(fill(s.sent))} »`,()=>({t:'build',sent:s.sent,p:s.p,target:s.target,tiles:shuffle(s.tiles.slice()),used:[]}));",
    "settle(s,ok,`« ${esc(fill(s.sent))} »`,()=>({t:'build',sent:s.sent,p:s.p,target:s.target,tiles:shuffle(s.tiles.slice()),used:[],fr:s.fr}));")

# ---------- carte : Niveau 4 si abonné, Bonus du mois à la leçon en cours ----------
rep("""${last?evalNode(u.tier,evalCur===u.tier):''}`}).join('');""","""${last&&u.tier<=3?evalNode(u.tier,evalCur===u.tier):''}${i===cur?bonusNode(i):''}`}).join('');""")
rep("""<div class="map">${nodes}<div class="node"><span class="disc" style""","""<div class="map">${nodes}${cur<0?bonusNode(UNITS.length):''}<div class="node"><span class="disc" style""")
rep("""let famMsg=false;
function famMap(){
  const us=FAM_PREVIEW.map(id=>ALL_UNITS.find(u=>u.id===id)).filter(Boolean);
  return `<div class="tier fam"><b>Offre Famille ⭐</b><span>Bientôt : 5 nouvelles leçons chaque mois</span></div>`+
   us.map((u,i)=>`<button class="node locked famn" style="transform:translateX(${Math.round(Math.sin((UNITS.length+i)*1.1)*70)}px)" data-act="fam" aria-label="Leçon Famille : ${esc(tx(u.es,u.fr))}">
     <span class="disc">🔒</span><b>${esc(u.es)}</b><em>${esc(tx(u.es,u.fr))}</em><span class="ctag fam">⭐ Famille</span></button>${i===0&&famMsg?`<p class="hint-bubble">🌟 Ces leçons arriveront bientôt avec l'offre Famille. En attendant, profite de tes 15 leçons gratuites !</p>`:''}`).join('')}""",
"""let famMsg='';
const FAM_BUBBLE=`<p class="hint-bubble">🌟 Ces leçons arriveront bientôt avec l'offre Famille. En attendant, profite de tes 15 leçons gratuites !</p>`;
function famMap(){
  const on=famActive(),us=on?FAM_UNITS.filter(u=>!UNITS.includes(u)):FAM_PREVIEW.map(id=>ALL_UNITS.find(u=>u.id===id)).filter(Boolean);
  if(!us.length)return on?`<div class="tier fam"><b>Offre Famille ⭐</b><span>De nouvelles leçons arrivent bientôt !</span></div>`:'';
  return `<div class="tier fam"><b>${on?'Bientôt ⭐':'Offre Famille ⭐'}</b><span>${on?'5 nouvelles leçons chaque mois':'Bientôt : 5 nouvelles leçons chaque mois'}</span></div>`+
   us.slice(0,5).map((u,i)=>`<button class="node locked famn" style="transform:translateX(${Math.round(Math.sin((UNITS.length+i)*1.1)*70)}px)" data-act="${on?'famsoon':'fam'}" data-w="m" aria-label="Leçon Famille : ${esc(tx(u.es,u.fr))}">
     <span class="disc">🔒</span><b>${esc(u.es)}</b><em>${esc(tx(u.es,u.fr))}</em><span class="ctag fam">${on?'🗓️ Le mois prochain':'⭐ Famille'}</span></button>${i===0&&famMsg==='m'?(on?`<p class="hint-bubble">🗓️ Ces leçons s'ouvriront le mois prochain. Patience !</p>`:FAM_BUBBLE):''}`).join('')}
/* Bonus du mois : posé juste après la leçon en cours de l'enfant (ou à la fin de la carte) */
function bonusNode(i){
  const b=monthBonus();if(!b)return '';const u=b.u,on=famActive(),st=S.stars[u.id]||0;
  return `<button class="node bonusn ${on?(st?'done':''):'locked'}" style="transform:translateX(${Math.round(Math.sin((i+.5)*1.1)*70)}px)" data-act="${on?'mbonus':'fam'}" data-w="b" aria-label="Bonus du mois : ${esc(tx(u.es,u.fr))}">
    <span class="btag">🎁 Bonus du mois</span><span class="disc">${on?u.e:'🔒'}</span>
    <span class="stars">${st?'⭐'.repeat(st)+'<span style="opacity:.25">'+'⭐'.repeat(3-st)+'</span>':''}</span>
    <b>${esc(u.es)}</b><em>${esc(tx(u.es,u.fr))}</em><small class="where">${esc(u.where)}</small><span class="ctag fam">${on?'⭐ Famille':'🔒 Famille'}</span></button>${famMsg==='b'&&!on?FAM_BUBBLE:''}`}""")
rep("""  else if(a==='fam'){famMsg=true;say('¡Muy pronto!');render();""","""  else if(a==='mbonus'){const b=monthBonus();if(!b||!famActive())return;if(!guard())return;startUnit(-1,b.u);speakStep()}
  else if(a==='famoff'){try{localStorage.removeItem(FAM_KEY)}catch(e){}famSync();render()}
  else if(a==='fam'||a==='famsoon'){famMsg=b.dataset.w||'m';say('¡Muy pronto!');render();""")

# ---------- Memory : dos de cartes aux couleurs des univers ----------
rep("const DECORS=[","const MBACK_PRICE=40;   /* dos de cartes du Memory : un par univers, à acheter avec des pièces quand on a l'univers */\nconst DECORS=[")
rep("""return `<button class="mcard ${up?'up':''} ${g.done.includes(c.w.es)?'ok':''}" data-act="gmem" data-k="${i}" aria-label="${up?esc(c.k==='t'?c.w.es:c.w.fr):'Carte cachée'}">${up?(c.k==='t'?`<b>${esc(c.w.es)}</b>`:pic(c.w.e)):'❓'}</button>`""",
"""const mb=!up&&S.mback&&THEMES[S.mback];return `<button class="mcard ${up?'up':''} ${g.done.includes(c.w.es)?'ok':''} ${mb?'mb':''}" ${mb?`style="background:linear-gradient(135deg,${mb.c.lagoon},${mb.c.coral});box-shadow:0 5px 0 ${mb.c['lagoon-d']}"`:''} data-act="gmem" data-k="${i}" aria-label="${up?esc(c.k==='t'?c.w.es:c.w.fr):'Carte cachée'}">${up?(c.k==='t'?`<b>${esc(c.w.es)}</b>`:pic(c.w.e)):mb?mb.e:'❓'}</button>`""")
rep("""  <div class="dunit">🎁 Bonus</div><div class="shop">${Object.entries(BONUS)""","""  <div class="dunit">🃏 Dos de cartes du Memory</div><p class="note">Un dos de cartes par univers. Débloque d'abord l'univers dans la boutique.</p><div class="shop">
    <button class="item ${!S.mback?'on':''}" data-act="mback" data-k="" data-p="0"><span>❓</span><b>Classique</b><small>${!S.mback?'Choisi ✓':'Choisir'}</small></button>
    ${Object.entries(THEMES).map(([k,t])=>{const has=(S.mbacks||[]).includes(k),on=S.mback===k,ok=hasTheme(k);
    return `<button class="item ${on?'on':''} ${!has&&(!ok||(S.coins||0)<MBACK_PRICE)?'poor':''}" data-act="mback" data-k="${k}" data-p="${MBACK_PRICE}" ${ok||has?'':'aria-disabled="true"'}><span class="mbprev" style="background:linear-gradient(135deg,${t.c.lagoon},${t.c.coral})">${t.e}</span><b>${esc(t.name)}</b><small>${on?'Choisi ✓':has?'Choisir':ok?`🪙 ${MBACK_PRICE}`:'🔒 Univers'}</small></button>`}).join('')}</div>
  <div class="dunit">🎁 Bonus</div><div class="shop">${Object.entries(BONUS)""")
rep("""  else if(a==='decor'){""","""  else if(a==='mback'){const k=b.dataset.k;S.mbacks=S.mbacks||[];shopMsg='';
    if(k&&!S.mbacks.includes(k)){if(!hasTheme(k)){shopMsg="Débloque d'abord cet univers dans la boutique.";render();return}if(!spend(MBACK_PRICE)){render();return}S.mbacks.push(k);shopMsg='Acheté !'}S.mback=k;save();render()}
  else if(a==='decor'){""")

# ---------- espace parent : abonnement ----------
rep("""<p class="note" style="color:var(--ink);margin:0">L'offre Famille ajoutera 5 nouvelles leçons chaque mois, à partir de la date d'abonnement de votre famille : votre enfant avance à son rythme, sans tout ouvrir d'un coup.</p><p class="note" style="margin:0">Rien n'est payant pour l'instant. Les leçons de l'offre sont visibles, verrouillées, sur la carte.</p></div>""",
"""<p class="note" style="color:var(--ink);margin:0">L'offre Famille ajoutera 5 nouvelles leçons chaque mois, à partir de la date d'abonnement de votre famille : votre enfant avance à son rythme, sans tout ouvrir d'un coup. Les nouvelles leçons font apprendre des phrases de la vie de tous les jours (commander au café, se présenter…).</p><p class="note" style="color:var(--ink);margin:0">🎁 Chaque mois, une leçon Bonus sur la culture d'Espagne et d'Amérique latine, ouverte à tous les abonnés, quelle que soit la progression de l'enfant.</p><p class="note" style="color:var(--ink);margin:0">Abonnement au mois ou à l'année, sans engagement : il se renouvelle automatiquement et s'arrête quand vous voulez. Avec le compte parent (bientôt, votre e-mail), vous retrouverez les profils et la progression de vos enfants, même après une pause.</p><p class="note" style="margin:0">Rien n'est payant pour l'instant. Les leçons de l'offre sont visibles, verrouillées, sur la carte.</p>${famInfo()&&famInfo().preview?`<p class="note" style="color:var(--coral-d);margin:0">Aperçu de l'offre Famille activé sur ce téléphone (test).</p><button class="tool" data-act="famoff" style="justify-content:center">Désactiver l'aperçu</button>`:''}</div>""")

# ---------- styles ----------
rep(".famset{",""".bonusn .disc{background:var(--coral);box-shadow:0 7px 0 var(--coral-d)}.bonusn.locked .disc{background:var(--line);box-shadow:0 7px 0 var(--muted)}
.where{font-weight:700;font-size:13px;color:var(--muted)}
.btag{background:var(--coral);color:#fff;font-weight:800;font-size:13px;border-radius:999px;padding:3px 10px;margin-bottom:4px}
.frsent{flex:1;min-width:0;background:var(--card);border:3px solid var(--line);border-radius:16px;padding:10px 12px;font-weight:800;font-size:18px;line-height:1.3;color:var(--ink);text-wrap:balance}
.mcard.mb{font-size:38px}.mbprev{display:grid;place-items:center;width:48px;height:48px;border-radius:12px;font-size:28px}
.famset{""")

# ---------- démarrage : leçons Famille ouvertes ----------
rep("loadProfile(P.list.some(x=>x.id===P.cur)?P.cur:P.list[0].id);","famSync();\nloadProfile(P.list.some(x=>x.id===P.cur)?P.cur:P.list[0].id);")

# ---------- traductions de l'interface ----------
ui={
 "Dans la vraie vie":["In real life","Nella vita vera"],
 "Traduis la phrase":["Translate the sentence","Traduci la frase"],
 "Dis-la en espagnol : touche les mots dans le bon ordre.":["Say it in Spanish: tap the words in the right order.","Dilla in spagnolo: tocca le parole nell'ordine giusto."],
 "🎁 Bonus du mois":["🎁 Bonus of the month","🎁 Bonus del mese"],
 "Bonus du mois : {0}":["Bonus of the month: {0}","Bonus del mese: {0}"],
 "⭐ Famille":["⭐ Family","⭐ Famiglia"],"🔒 Famille":["🔒 Family","🔒 Famiglia"],
 "Bientôt ⭐":["Coming soon ⭐","In arrivo ⭐"],
 "{0} nouvelles leçons chaque mois":["{0} new lessons every month","{0} nuove lezioni ogni mese"],
 "De nouvelles leçons arrivent bientôt !":["New lessons are coming soon!","Nuove lezioni in arrivo!"],
 "🗓️ Le mois prochain":["🗓️ Next month","🗓️ Il mese prossimo"],
 "🗓️ Ces leçons s'ouvriront le mois prochain. Patience !":["🗓️ These lessons will open next month. Be patient!","🗓️ Queste lezioni si apriranno il mese prossimo. Pazienza!"],
 "🃏 Dos de cartes du Memory":["🃏 Memory card backs","🃏 Dorsi delle carte del Memory"],
 "Un dos de cartes par univers. Débloque d'abord l'univers dans la boutique.":["One card back per world. Unlock the world in the shop first.","Un dorso per ogni mondo. Prima sblocca il mondo nel negozio."],
 "Classique":["Classic","Classico"],"🔒 Univers":["🔒 World","🔒 Mondo"],
 "Débloque d'abord cet univers dans la boutique.":["Unlock this world in the shop first.","Prima sblocca questo mondo nel negozio."],
 "L'offre Famille ajoutera {0} nouvelles leçons chaque mois, à partir de la date d'abonnement de votre famille : votre enfant avance à son rythme, sans tout ouvrir d'un coup. Les nouvelles leçons font apprendre des phrases de la vie de tous les jours (commander au café, se présenter…).":
  ["The Family plan will add {0} new lessons every month, counted from your family's subscription date: your child moves at their own pace, without unlocking everything at once. The new lessons teach everyday sentences (ordering at a café, introducing yourself…).",
   "L'offerta Famiglia aggiungerà {0} nuove lezioni ogni mese, a partire dalla data di abbonamento della vostra famiglia: vostro figlio avanza al suo ritmo, senza aprire tutto in una volta. Le nuove lezioni insegnano frasi di tutti i giorni (ordinare al bar, presentarsi…)."],
 "🎁 Chaque mois, une leçon Bonus sur la culture d'Espagne et d'Amérique latine, ouverte à tous les abonnés, quelle que soit la progression de l'enfant.":
  ["🎁 Every month, a Bonus lesson about the culture of Spain and Latin America, open to all subscribers whatever the child's progress.",
   "🎁 Ogni mese, una lezione Bonus sulla cultura della Spagna e dell'America Latina, aperta a tutti gli abbonati, qualunque sia il percorso del bambino."],
 "Abonnement au mois ou à l'année, sans engagement : il se renouvelle automatiquement et s'arrête quand vous voulez. Avec le compte parent (bientôt, votre e-mail), vous retrouverez les profils et la progression de vos enfants, même après une pause.":
  ["Monthly or yearly subscription, no commitment: it renews automatically and stops whenever you want. With the parent account (coming soon, your e-mail), you'll find your children's profiles and progress again, even after a break.",
   "Abbonamento mensile o annuale, senza vincoli: si rinnova automaticamente e si interrompe quando volete. Con l'account genitore (in arrivo, la vostra e-mail), ritroverete i profili e i progressi dei vostri figli, anche dopo una pausa."],
 "Aperçu de l'offre Famille activé sur ce téléphone (test).":["Family plan preview turned on on this phone (test).","Anteprima dell'offerta Famiglia attiva su questo telefono (test)."],
 "Désactiver l'aperçu":["Turn off the preview","Disattiva l'anteprima"],
 "Espagne":["Spain","Spagna"],"Espagne · Mexique":["Spain · Mexico","Spagna · Messico"],"Espagne · Amérique latine":["Spain · Latin America","Spagna · America Latina"],
 "Commander au café":["Ordering at the café","Ordinare al bar"],
}
rep("const UI={","const UI={"+','.join(J(k)+':'+J(v) for k,v in ui.items())+",")
open(p,'w',encoding='utf8').write(h);print('ok')
