import json
p='/home/claude/appespagnol/index.html';h=open(p,encoding='utf8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:90],h.count(a));h=h.replace(a,b)
J=lambda x:json.dumps(x,ensure_ascii=False)

# ---------- 1. Langue des traductions = langue du téléphone, sans écran au démarrage ----------
rep("const st=wStep||(!S.target?'target':!S.name?(S.lang?'name':'lang'):!S.gender?'gender':'theme');\n  if(st==='target'){",
    "const st=wStep||(!S.target?'target':!S.name?'name':!S.gender?'gender':'theme');\n  if(st==='target'){")
rep("const st=wStep||(!S.target?'target':!S.name?(S.lang?'name':'lang'):!S.gender?'gender':'theme');\n    if(st==='lang'){wStep='target'}\n    else if(st==='name'){readName();wStep='lang'}",
    "const st=wStep||(!S.target?'target':!S.name?'name':!S.gender?'gender':'theme');\n    if(st==='lang'){wStep='target'}\n    else if(st==='name'){readName();wStep='target'}")
rep("else if(a==='settarget'){S.target=b.dataset.t;if(S.lang===S.target)S.lang='fr';setTarget(S.target);famSync();save();wStep='lang';render()}",
    "else if(a==='settarget'){S.target=b.dataset.t;const sl=sysLang();if(!S.lang)S.lang=sl!==S.target?sl:'fr';if(S.lang===S.target)S.lang='fr';setTarget(S.target);famSync();save();wStep='name';render()}")

# ---------- 2. Plusieurs langues par enfant : une progression par langue ----------
rep("function setTarget(t){","""/* Un enfant peut apprendre plusieurs langues (v27) : les champs de progression de la langue en cours sont à la racine de S,
   ceux des autres langues sont rangés dans S.L[langue]. Partagés : prénom, univers, pièces, garde-robe, temps d'écran, série. */
const PL=['stars','words','evals','opened','seq','newDay','seanceDay','xp'];
const langsOf=s=>{const a=[(s&&s.target)||'es',...Object.keys((s&&s.L)||{})];return a.filter((v,i)=>a.indexOf(v)===i)};
function switchTarget(t){if(!TARGETS[t]||t===(S.target||'es'))return;S.L=S.L||{};const cur={};PL.forEach(k=>{if(S[k]!==undefined)cur[k]=S[k]});S.L[S.target||'es']=cur;
  const nx=S.L[t]||{},d=def();delete S.L[t];PL.forEach(k=>{S[k]=nx[k]!==undefined?nx[k]:(d[k]!==undefined?JSON.parse(JSON.stringify(d[k])):undefined)});
  S.target=t;if(S.lang===t)S.lang='fr';save();setTarget(t);famSync();pickVoice()}
function langsView(){const ls=langsOf(S),starsOf=t=>Object.keys((t===S.target?S.stars:(S.L[t]||{}).stars)||{}).length;
  app.innerHTML=`<div class="head"><button class="icon-btn" data-act="home" aria-label="Retour">←</button><h2>Mes langues</h2></div>
  <div class="center" style="justify-content:flex-start;padding-top:0">
    <div style="width:100%;display:grid;gap:12px">${ls.map(t=>`<button class="btn ${t===S.target?'sun':'ghost'} big2" data-act="golang" data-t="${t}">${TARGETS[t][1]} ${TARGETS[t][2]} <small style="font-weight:700"> · ${starsOf(t)} leçon${starsOf(t)>1?'s':''}</small></button>`).join('')}</div>
    ${Object.keys(TARGETS).filter(t=>!ls.includes(t)).length?`<p class="say">Apprendre une autre langue (avec un parent) :</p>
    <div style="width:100%;display:grid;gap:12px">${Object.keys(TARGETS).filter(t=>!ls.includes(t)).map(t=>`<button class="btn ghost" data-act="addlang" data-t="${t}">➕ ${TARGETS[t][1]} ${TARGETS[t][2]}</button>`).join('')}</div>`:''}
    <p class="note">Chaque langue garde sa propre progression. Les pièces, la garde-robe et le temps d'écran sont partagés.</p></div>`}
function setTarget(t){""")
rep("if(view==='duel')duel();else if(view==='duel2')duel2();else","if(view==='duel')duel();else if(view==='duel2')duel2();else if(view==='langs')langsView();else")
rep("""<div class="hello"><small>${esc(G().title)} te dit :</small><h1>¡Hola, ${esc(S.name)}!</h1></div>""",
    """<div class="hello"><small>${esc(G().title)} te dit :</small><h1>¡Hola, ${esc(S.name)}!</h1></div>
    <button class="icon-btn langchip" data-act="langs" aria-label="Mes langues">${TARGETS[S.target||'es'][1]}</button>""")
rep("  else if(a==='settarget'){","""  else if(a==='langs'){view='langs';render()}
  else if(a==='golang'){switchTarget(b.dataset.t);view='home';render()}
  else if(a==='addlang'){openGate({act:'addlang',t:b.dataset.t})}
  else if(a==='settarget'){""")
rep("  if(g&&g.act==='pick'){loadProfile(g.id);","  if(g&&g.act==='addlang'){switchTarget(g.t);view='home';render();return}\n  if(g&&g.act==='pick'){loadProfile(g.id);")
rep("""<b>${esc(s.name||'Nouveau joueur')} ${s.name?TARGETS[s.target||'es'][1]:''}</b><small>${n} leçon""","""<b>${esc(s.name||'Nouveau joueur')} ${s.name?langsOf(s).map(t=>TARGETS[t][1]).join(''):''}</b><small>${n} leçon""")
rep("""<span class="acc-t"><b>${esc(s.name||'Nouveau joueur')} ${s.name?TARGETS[s.target||'es'][1]:''}</b>""","""<span class="acc-t"><b>${esc(s.name||'Nouveau joueur')} ${s.name?langsOf(s).map(t=>TARGETS[t][1]).join(''):''}</b>""")

# ---------- 3. Abonnements par langue : Solo (1 enfant) ou Famille (tous les enfants) ----------
rep("const famStart=()=>{const f=famInfo();return f&&f.start||null};","""/* Abonnements (v27, préparation : rien n'est payant) : un abonnement = une langue.
   Solo = un enfant (pid), Famille = tous les enfants de la famille. Liste dans hola-lola-subs, écrite plus tard par le compte parent :
   [{lang:'es',offer:'solo'|'famille',pid,start:'AAAA-MM-JJ',period:'month'|'year'}]. L'ancienne clé hola-lola-fam (aperçu) vaut Famille espagnol. */
const SUBS_KEY='hola-lola-subs',OFFERS={solo:{n:'Solo',who:'1 enfant, 1 langue',m:'3,99',y:'43,09'},famille:{n:'Famille',who:'tous les enfants, 1 langue',m:'5,99',y:'64,69'}};
function subs(){let a=[];try{a=JSON.parse(localStorage.getItem(SUBS_KEY)||'[]')||[]}catch(e){}const f=famInfo();if(f&&f.start&&f.plan!=='ultimate')a=a.concat([{lang:'es',offer:'famille',start:f.start,preview:!!f.preview}]);return a}
const subFor=(pid,lang)=>subs().find(s=>s.lang===lang&&(s.offer==='famille'||s.pid===pid))||null;
const famStart=()=>{const f=famInfo();if(f&&f.plan==='ultimate')return f.start||null;const s=subFor(P.cur,TGT);return s?s.start:null};""")
rep("const famActive=()=>{const f=famInfo();return !!(f&&f.start&&(f.plan!=='ultimate'||famUltimate()))};",
    "const famActive=()=>famUltimate()||!!subFor(P.cur,TGT);")
# espace parent : statut de chaque langue de l'enfant + tarifs
rep("""      <div class="limit"><b>🎓 Langue apprise : ${TARGETS[s.target||'es'][1]} ${TARGETS[s.target||'es'][0]}</b><p class="note">Pour apprendre une autre langue, ajoutez un profil : chaque langue garde sa propre progression.</p></div>""",
"""      <div class="limit"><b>🎓 Langues apprises</b>${langsOf(s).map(t=>{const sb=subFor(p.id,t);return `<p class="note" style="margin:0;color:var(--ink)">${TARGETS[t][1]} ${TARGETS[t][0]} : ${famUltimate()?'Ultimate (bêta-testeur)':sb?`⭐ ${OFFERS[sb.offer].n} depuis le ${sb.start.split('-').reverse().join('/')}`:'Gratuit (15 leçons)'}</p>`}).join('')}
        <p class="note">Pour ajouter une langue : drapeau en haut de l'accueil de l'enfant, puis le code parent. Chaque langue garde sa propre progression.</p></div>""")
rep("""<div class="set famset"><b>⭐ Offre Famille (bientôt)</b><p class="note" style="color:var(--ink);margin:0">Les 15 premières leçons (Niveaux 1 à 3) sont gratuites, pour toujours.</p>""",
"""<div class="set famset"><b>⭐ Abonnements (bientôt)</b><p class="note" style="color:var(--ink);margin:0">Les 15 premières leçons (Niveaux 1 à 3) sont gratuites, pour toujours, dans chaque langue.</p>
  <div class="offers">${Object.values(OFFERS).map(o=>`<div class="offer"><b>${o.n}</b><small>${o.who}</small><span class="price">${o.m} €<small>/mois</small></span><small>ou ${o.y} €/an (−10 %)</small></div>`).join('')}</div>
  <p class="note" style="margin:0">Un abonnement par langue, sans engagement.</p>""")
rep(".famset{",""".langchip{font-size:26px}
.offers{display:grid;grid-template-columns:1fr 1fr;gap:10px}.offer{display:grid;gap:2px;background:var(--card);border:3px solid var(--line);border-radius:16px;padding:10px 12px;color:var(--ink)}
.offer .price{font-weight:900;font-size:22px;color:var(--lagoon-d)}.offer .price small{font-size:13px;font-weight:700}.offer small{color:var(--muted);font-weight:700}
.famset{""")

ui={"Mes langues":["My languages","Le mie lingue"],"Apprendre une autre langue (avec un parent) :":["Learn another language (with a parent):","Impara un'altra lingua (con un genitore):"],
 "Chaque langue garde sa propre progression. Les pièces, la garde-robe et le temps d'écran sont partagés.":["Each language keeps its own progress. Coins, wardrobe and screen time are shared.","Ogni lingua ha i suoi progressi. Monete, guardaroba e tempo davanti allo schermo sono condivisi."],
 "· {0} leçon":["· {0} lesson","· {0} lezione"],"· {0} leçons":["· {0} lessons","· {0} lezioni"],
 "🎓 Langues apprises":["🎓 Languages learnt","🎓 Lingue studiate"],"Gratuit ({0} leçons)":["Free ({0} lessons)","Gratis ({0} lezioni)"],"Ultimate (bêta-testeur)":["Ultimate (beta tester)","Ultimate (beta tester)"],
 "Pour ajouter une langue : drapeau en haut de l'accueil de l'enfant, puis le code parent. Chaque langue garde sa propre progression.":["To add a language: the flag at the top of the child's home screen, then the parent code. Each language keeps its own progress.","Per aggiungere una lingua: la bandiera in alto nella schermata del bambino, poi il codice genitore. Ogni lingua ha i suoi progressi."],
 "⭐ Abonnements (bientôt)":["⭐ Subscriptions (coming soon)","⭐ Abbonamenti (in arrivo)"],
 "Les {0} premières leçons (Niveaux {1} à {2}) sont gratuites, pour toujours, dans chaque langue.":["The first {0} lessons (Levels {1} to {2}) are free, forever, in every language.","Le prime {0} lezioni (Livelli da {1} a {2}) sono gratuite, per sempre, in ogni lingua."],
 "Solo":["Solo","Solo"],"Famille":["Family","Famiglia"],"{0} enfant, {1} langue":["{0} child, {1} language","{0} bambino, {1} lingua"],"tous les enfants, {0} langue":["all the children, {0} language","tutti i bambini, {0} lingua"],
 "/mois":["/month","/mese"],"ou {0} €/an (−{1} %)":["or €{0}/year (−{1}%)","o {0} €/anno (−{1}%)"],"Un abonnement par langue, sans engagement.":["One subscription per language, no commitment.","Un abbonamento per lingua, senza vincoli."]}
rep("const UI={","const UI={"+','.join(J(k)+':'+J(v) for k,v in ui.items())+",")
open(p,'w',encoding='utf8').write(h);print('ok')
