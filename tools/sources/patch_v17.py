import sys, json
SCR = '/tmp/claude-0/-home-claude/aa41b3f1-6410-5635-8215-dcdb8c4f13a8/scratchpad/'
TRX = json.load(open(SCR + 'tr_x.json'))
p = open('index.html').read()
def rep(o, n, cnt=1):
    global p
    c = p.count(o)
    if c != cnt: sys.exit(f'{c}x: {o[:110]}')
    p = p.replace(o, n)

# ================= 1. Langue de traduction (fr par défaut, en, it) =================
trx_js = json.dumps(TRX, ensure_ascii=False, separators=(',', ':'))
rep("const W=w=>({es:gx(w[0],S.gender),fr:gx(w[1],S.gender),",
    """/* Langue de traduction (réglée par enfant dans l'espace parent). TRX[espagnol] = [anglais, italien]. */
const LANGS={fr:['Français','🇫🇷'],en:['English','🇬🇧'],it:['Italiano','🇮🇹']};
const TRX=""" + trx_js + """;
const LF=()=>(LANGS[S.lang]||LANGS.fr)[1];
function tx(es,fr){if(!S.lang||S.lang==='fr')return fr;const t=TRX[es];return t?t[S.lang==='en'?0:1]:fr}
const W=w=>({es:gx(w[0],S.gender),fr:gx(tx(w[0],w[1]),S.gender),""")
rep("const W=w=>({es:gx(w[0],S.gender),fr:gx(tx(w[0],w[1]),S.gender),e:ABSTRACT.has(w[0])?'txt:'+gx(w[1],S.gender):w[2]});",
    "const W=w=>({es:gx(w[0],S.gender),fr:gx(tx(w[0],w[1]),S.gender),e:ABSTRACT.has(w[0])?'txt:'+gx(tx(w[0],w[1]),S.gender):w[2]});")
rep("['fâchée','fâché']];", "['fâchée','fâché'],['stanca','stanco']];")
rep("const tr=es=>trMap()[es]||'';\nconst trOpt=o=>o.length>2?o[1]:tr(o[0]);",
    "const tr=es=>tx(es,trMap()[es]||'');\nconst trOpt=o=>tx(o[0],o.length>2?o[1]:trMap()[o[0]]||'');")
rep("fillG(s.d.f||tr(s.d.l))", "fillG(tr(s.d.l))")
rep("${showT&&(d.f||tr(d.l))?`<div class=\"frq\">🇫🇷 ${esc(fillG(d.f||tr(d.l)))}</div>`:''}",
    "${showT&&tr(d.l)?`<div class=\"frq\">${LF()} ${esc(fillG(tr(d.l)))}</div>`:''}")
rep("`<p>🇫🇷 ${l?", "`<p>${LF()} ${l?")
rep("'<button class=\"tool\" data-act=\"trq\">🇫🇷 Traduire</button>'", "`<button class=\"tool\" data-act=\"trq\">${LF()} Traduire</button>`")
rep("`<div class=\"frq big\">🇫🇷 ${esc(t)}</div>`", "`<div class=\"frq big\">${LF()} ${esc(t)}</div>`")
rep("${showT?`<div class=\"fr\">🇫🇷 ${esc(s.w.fr)}</div>`:''}", "${showT?`<div class=\"fr\">${LF()} ${esc(s.w.fr)}</div>`:''}")
rep("<small>${esc(gx(w[1],S.gender))}</small></button>`).join('')}</div>`).join('')",
    "<small>${esc(gx(tx(w[0],w[1]),S.gender))}</small></button>`).join('')}</div>`).join('')")

# ================= 2. Étape → Niveau, niveau → leçon, comptines → récitations =================
rep("const TIERS={1:['Étape 1','Premiers mots'],2:['Étape 2','Mon quotidien'],3:['Étape 3','Premières phrases']};",
    "const TIERS={1:['Niveau 1','Premiers mots'],2:['Niveau 2','Mon quotidien'],3:['Niveau 3','Premières phrases']};")
rep("""aria-label="Niveau ${i+1} : ${esc(u.fr)}">""", """aria-label="Leçon ${li} : ${esc(tx(u.es,u.fr))}">""")
rep("""<em>${i+1}. ${esc(u.fr)}</em>""", """<em>Leçon ${li} · ${esc(tx(u.es,u.fr))}</em>""")
rep("""    const last=i===UNITS.length-1||UNITS[i+1].tier!==u.tier;""",
    """    const last=i===UNITS.length-1||UNITS[i+1].tier!==u.tier,li=UNITS.slice(0,i+1).filter(x=>x.tier===u.tier).length;""")
rep("<em>Termine les ${UNITS.length} niveaux</em>", "<em>Termine les ${UNITS.length} leçons</em>")
rep("""aria-label="Évaluation de l'étape ${t}">""", """aria-label="Évaluation du niveau ${t}">""")
rep("`Étape ${t} réussie : ${ev.pct} %`:`Étape ${t} · 80 % pour passer`", "`Niveau ${t} réussi : ${ev.pct} %`:`Niveau ${t} · 80 % pour passer`")
rep("📝 Évaluation de l'étape ${L.tier} ·", "📝 Évaluation du niveau ${L.tier} ·")
rep("`Étape ${R.tier} réussie !`", "`Niveau ${R.tier} réussi !`")
rep("`L'étape ${R.tier+1} est ouverte : ${esc(TIERS[R.tier+1][1])}. +20 points !`:'Tu as réussi toutes les étapes. Bravo !'",
    "`Le niveau ${R.tier+1} est ouvert : ${esc(TIERS[R.tier+1][1])}. +20 points !`:'Tu as réussi tous les niveaux. Bravo !'")
rep("Commencer l'étape ${R.tier+1} →", "Commencer le niveau ${R.tier+1} →")
rep("`Nouveau niveau débloqué : ${esc(next.es)} ${next.e}`", "`Nouvelle leçon débloquée : ${esc(next.es)} ${next.e}`")
rep(">Niveau suivant →</button>", ">Leçon suivante →</button>")
rep("Chaque niveau réussi débloque un épisode", "Chaque leçon réussie débloque un épisode")
rep("'Réussis le niveau « '+esc(u.es)+' »'", "'Réussis la leçon « '+esc(u.es)+' »'")
rep("'Termine ton premier niveau pour débloquer les jeux !'", "'Termine ta première leçon pour débloquer les jeux !'")
rep("doit d'abord réussir un niveau.", "doit d'abord réussir une leçon.")
rep("Termine le premier niveau pour remplir ton dico !", "Termine la première leçon pour remplir ton dico !")
rep("Version ${APP_VERSION} · ${UNITS.length} niveaux", "Version ${APP_VERSION} · ${UNITS.length} leçons")
rep("${n} niveau${n>1?'x':''} réussi${n>1?'s':''}", "${n} leçon${n>1?'s':''} réussie${n>1?'s':''}")
rep("`Étape ${t} : ${(s.evals||{})[t].pct} %`", "`Niveau ${t} : ${(s.evals||{})[t].pct} %`")
rep("<small>niveaux réussis</small>", "<small>leçons réussies</small>")
rep("<h2>Étape 2 sur 3</h2>", "<h2>2 / 3</h2>")
rep("'Étape 3 sur 3'", "'3 / 3'")
# récitations
rep("""<button class="fun" data-act="songs"><span>🎵</span>Comptines</button>""", """<button class="fun" data-act="songs"><span>📜</span>Récitations</button>""")
rep("""head('🎵 Comptines')+`<p class="note" style="margin-bottom:12px">Écoute, puis chante avec ${esc(G().es)}. Chaque comptine s'ouvre avec un niveau.</p>""",
    """head('📜 Récitations')+`<p class="note" style="margin-bottom:12px">Écoute, puis récite avec ${esc(G().es)}. Chaque récitation s'ouvre avec une leçon.</p>""")
rep("${ok?'4 lignes à chanter':'Réussis le niveau « '+esc(u?u.es:'')+' »'}", "${ok?'4 lignes à réciter':'Réussis la leçon « '+esc(u?u.es:'')+' »'}")
rep("'À toi ! Chante la ligne en couleur 🎤'", "'À toi ! Récite la ligne en couleur 🎤'")
rep("🎤 À moi de chanter</button>", "🎤 À moi de réciter</button>")

# ================= 3. Exercices dans un ordre aléatoire, jamais deux fois le même =================
rep("/* ---------- Construction d'une leçon ---------- */",
    """/* ---------- Construction d'une leçon ---------- */
/* Les exercices (après la découverte des mots) sont mélangés : ordre différent pour chaque enfant
   et jamais deux fois de suite le même enchaînement (S.seq garde le dernier, par leçon). */
const sigOf=s=>s.t+':'+(s.w?s.w.es:s.g?s.g.s:s.d?s.d.l:s.sent||(s.ws||[]).map(w=>w.es).join(','));
function mix(key,head,rest){
  S.seq=S.seq||{};const old=S.seq[key];let steps,sig;
  for(let n=0;n<8;n++){steps=head.concat(shuffle(rest.slice()));sig=steps.map(sigOf).join('|');if(sig!==old)break}
  S.seq[key]=sig;return steps;
}
const kindFor=(w,conv)=>Math.random()<.5?'pick':(conv?'mean':'listen');""")
rep("""  const u=UNITS[i],words=u.words.map(W),steps=[],phr=!!u.conv;
  if(!S.stars[u.id])words.forEach(w=>steps.push({t:'learn',w,conv:phr}));
  steps.push(matchStep(words));
  shuffle(words.slice()).slice(0,4).forEach((w,k)=>steps.push({t:k%2?'pick':(phr?'mean':'listen'),w,opts:optsFor(w,words)}));""",
    """  const u=UNITS[i],words=shuffle(u.words.map(W)),learn=[],steps=[],phr=!!u.conv;
  if(!S.stars[u.id])words.forEach(w=>learn.push({t:'learn',w,conv:phr}));
  steps.push(matchStep(words));
  shuffle(words.slice()).slice(0,4).forEach(w=>steps.push({t:kindFor(w,phr),w,opts:optsFor(w,words)}));""")
rep("""  u.talk.forEach(d=>steps.push({t:'talk',d,opts:shuffle(d.o.slice())}));
  L={unit:i,kind:'unit',steps,""", """  u.talk.forEach(d=>steps.push({t:'talk',d,opts:shuffle(d.o.slice())}));
  L={unit:i,kind:'unit',steps:mix(u.id,learn,steps),""")
rep("""  pk.slice(4,6).forEach(w=>steps.push({t:'speak',w}));
  L={unit:-1,steps,""", """  pk.slice(4,6).forEach(w=>steps.push({t:'speak',w}));
  L={unit:-1,steps:mix('review',[],steps),""")
rep("""  L={unit:-1,kind:'seance',steps,""", """  L={unit:-1,kind:'seance',steps:mix('seance',[],steps),""")

# ================= 4. Temps d'écran compté en direct, blocage réel =================
rep("function addTime(){if(L&&L.t0){const s=Math.min(1200,(Date.now()-L.t0)/1000),k=dayPlus(0);S.days=S.days||{};S.days[k]=(S.days[k]||0)+Math.round(s);L.t0=0}}",
    "/* Le temps est compté en direct par le minuteur plus bas (timeTick) ; addTime ne fait plus que clore la leçon. */\nfunction addTime(){if(L)L.t0=0}")
rep("addCoins(coins);addPts(coins);const s=Math.min(1200,(Date.now()-g.t0)/1000),k=dayPlus(0);S.days[k]=(S.days[k]||0)+Math.round(s);save();",
    "addCoins(coins);addPts(coins);save();")
rep("const overLimit=()=>S.limit>0&&usedMin()>=S.limit&&S.unlockDay!==dayPlus(0);",
    """const extraMin=s=>s&&s.extra&&s.extra.d===dayPlus(0)?s.extra.m:0;
const overLimit=()=>S.limit>0&&usedMin()>=S.limit+extraMin(S)&&S.unlockDay!==dayPlus(0);
/* Écrans libres (pas comptés, accessibles même quand le temps est fini) */
const FREE=new Set(['stop','pgate','parent','who','welcome','tuto']);
function stopAll(){try{speechSynthesis.cancel()}catch(e){}karaToken++;if(GM&&GM.timer){clearInterval(GM.timer);GM.timer=null}}
let lastTick=Date.now(),tickN=0;
function timeTick(){
  const now=Date.now(),dt=Math.min(30,(now-lastTick)/1000);lastTick=now;
  if(document.visibilityState!=='visible'||!S.name||!S.theme||FREE.has(view)||view==='settings')return;
  const k=dayPlus(0);S.days=S.days||{};S.days[k]=(S.days[k]||0)+dt;if(++tickN%3===0)save();
  if(overLimit()){stopAll();save();view='stop';render()}
}
setInterval(timeTick,10000);document.addEventListener('visibilitychange',()=>{lastTick=Date.now()});""")
rep("""function stop(){
  app.innerHTML=`<div class="center"><div class="lola big" aria-hidden="true">${avatar()}</div><h2 style="font-size:32px">C'est fini pour aujourd'hui !</h2>
  <p class="say">${esc(G().es)} se repose. Tu as joué ${usedMin()} minutes aujourd'hui. Reviens demain 😴</p>
  <div style="width:100%;display:grid;gap:12px"><button class="btn" data-act="home">Retour à la carte</button><button class="btn ghost" data-act="parent">Espace parent</button></div></div>`;
}""", """function stop(){
  app.innerHTML=`<div class="center"><div class="lola big" aria-hidden="true">${avatar()}</div><h2 style="font-size:32px">C'est fini pour aujourd'hui !</h2>
  <p class="say">Tu as joué ${usedMin()} minutes : c'est le temps prévu par tes parents. ${esc(G().es)} se repose aussi 😴</p>
  <div class="set" style="width:100%;text-align:center;align-items:center"><b style="font-size:20px">🙋 Demande à tes parents</b><p class="note" style="margin:0">Seul un parent peut te donner un peu plus de temps. Sinon, on se retrouve demain !</p></div>
  <div style="width:100%;display:grid;gap:12px"><button class="btn" data-act="parent">👨‍👩‍👧 Je suis un parent</button>${P.list.length>1?'<button class="btn ghost" data-act="who">Changer de joueur</button>':''}</div></div>`;
}""")
rep("""function render(){
  if(view!=='game'&&GM&&GM.timer){clearInterval(GM.timer);GM.timer=null}""",
    """let lastView=null,toCur=false;
function render(){
  if(S.name&&S.theme&&!FREE.has(view)&&overLimit()){stopAll();view='stop'}
  if(S.name&&S.theme&&!S.tuto&&!FREE.has(view)){tutoK=0;view='tuto'}
  if(view!=='game'&&GM&&GM.timer){clearInterval(GM.timer);GM.timer=null}
  toCur=view==='home'&&lastView!=='home';lastView=view;""")
rep("""  else if(view==='dico')dico();else if(view==='settings')settings();else home();
}""", """  else if(view==='dico')dico();else if(view==='settings')settings();else if(view==='tuto')tuto();else home();
  /* sur la carte : aller directement à la leçon en cours */
  if(toCur){const c=document.querySelector('.map .node.current');if(c)requestAnimationFrame(()=>c.scrollIntoView({block:'center',behavior:'auto'}));else window.scrollTo(0,0)}
  else if(view!=='home')window.scrollTo(0,0);
  totopSync();
}""")
# espace parent : plus de temps, langue, explication « bien retenu »
rep("""      ${s.limit>0&&Math.round(((s.days||{})[dayPlus(0)]||0)/60)>=s.limit&&s.unlockDay!==dayPlus(0)?`<button class="tool" data-act="punlock" data-id="${p.id}" style="justify-content:center">🔓 Débloquer pour aujourd'hui</button>`:''}""",
    """      ${s.limit>0&&Math.round(((s.days||{})[dayPlus(0)]||0)/60)>=s.limit+extraMin(s)&&s.unlockDay!==dayPlus(0)?`<div class="row" style="gap:8px"><button class="tool" data-act="pextra" data-id="${p.id}" style="flex:1;justify-content:center">➕ 15 min aujourd'hui</button><button class="tool" data-act="punlock" data-id="${p.id}" style="flex:1;justify-content:center">🔓 Sans limite aujourd'hui</button></div>`:''}""")
rep("""`Aujourd'hui : ${Math.round(((s.days||{})[dayPlus(0)]||0)/60)} min sur ${s.limit} min.`""",
    """`Aujourd'hui : ${Math.round(((s.days||{})[dayPlus(0)]||0)/60)} min sur ${s.limit+extraMin(s)} min.${s.unlockDay===dayPlus(0)?' Débloqué pour aujourd\\'hui.':''} Quand le temps est écoulé, l'appli se bloque et demande un parent.`""")
rep("""      <div class="limit"><b>🇫🇷 Bouton « Traduire » sur les questions</b>""",
    """      <div class="limit"><b>🌍 Langue de traduction</b>
        <div class="seg three">${Object.entries(LANGS).map(([k,[n,f]])=>`<button class="${(s.lang||'fr')===k?'on':''}" data-act="plang" data-id="${p.id}" data-l="${k}" aria-pressed="${(s.lang||'fr')===k}">${f}<small>${n}</small></button>`).join('')}</div>
        <p class="note">Langue des traductions des mots et des phrases (après chaque réponse, bouton « Traduire », dico). Les menus restent en français.</p></div>
      <div class="limit"><b>💬 Bouton « Traduire » sur les questions</b>""")
rep("""      <div class="bars" role="img\"""", """      <p class="note"><b>Mot bien retenu</b> : un mot réussi lors de 3 révisions espacées (1 jour, puis 2, puis 4 jours plus tard). Il est en mémoire depuis au moins une semaine. Un mot raté redescend et revient dans la Séance du jour.</p>
      <div class="bars" role="img\"""")
rep("Le temps compté est celui passé dans les leçons, séances, évaluations et jeux.", "Le temps compté est le temps passé à jouer dans l'appli (hors réglages et espace parent).")

# ================= 5. Didacticiel =================
TUTO = r"""
/* ---------- Didacticiel : à la première ouverture d'un profil (S.tuto), revisible depuis les réglages ---------- */
let tutoK=0,tutoFrom='home';
function tutoSlides(){const c=esc(G().es);return [
  {b:avatar(),h:`¡Hola, ${esc(S.name)}!`,t:`Je suis ${c}. Chaque jour, on apprend l'espagnol ensemble, en quelques minutes.`},
  {b:'🗺️',h:'La carte',t:`Suis le chemin des leçons et gagne des étoiles ⭐. À la fin de chaque niveau, une petite évaluation ouvre le niveau suivant.`},
  {b:'🔊 👆 🎤',h:'Dans une leçon',t:`Écoute ${c} 🔊, touche la bonne réponse, puis répète à voix haute 🎤. Après chaque réponse, tu vois la traduction.`},
  {b:'🎯',h:'La Séance du jour',t:`Le petit chiffre, c'est le nombre de mots à revoir aujourd'hui. Les revoir au bon moment, c'est le secret pour ne plus les oublier !`},
  {b:'🪙 🎮 👗',h:'Des pièces et des surprises',t:`Gagne des pièces pour habiller ${c}. Joue aux jeux, lis l'histoire, remplis ton album, récite et défie ta famille !`},
  {b:'👨‍👩‍👧',h:'Pour les parents',t:`Dans ⚙️ Réglages → Espace parent (protégé par une multiplication) : temps d'écran par jour, langue de traduction, bouton « Traduire », progrès de chaque enfant. Sans publicité, aucune donnée envoyée.`}]}
function tuto(){
  const sl=tutoSlides(),k=Math.min(tutoK,sl.length-1),s=sl[k],end=k===sl.length-1;
  app.innerHTML=`<div class="head"><h2 style="flex:1">${k===sl.length-1?'Pour les parents':'Bienvenue !'}</h2><button class="tool" data-act="tutoend">Passer</button></div>
  <div class="panel tuto"><div class="tbig">${s.b}</div><h2 style="margin:0;font-size:28px">${s.h}</h2><p class="say" style="margin:0">${s.t}</p></div>
  <div class="dots">${sl.map((_,i)=>`<i class="${i===k?'on':''}"></i>`).join('')}</div>
  <div class="row">${k>0?'<button class="btn ghost" data-act="tutoprev">← Retour</button>':''}<button class="btn ${end?'sun':''}" data-act="${end?'tutoend':'tutonext'}">${end?'C\'est parti !':'Suivant →'}</button></div>`;
}
/* ---------- Bouton pour remonter en haut ---------- */
const totop=document.createElement('button');totop.id='totop';totop.type='button';totop.setAttribute('aria-label','Remonter en haut');totop.textContent='↑';totop.hidden=true;
document.body.appendChild(totop);
function totopSync(){totop.hidden=window.scrollY<500||view==='game'}
window.addEventListener('scroll',totopSync,{passive:true});
totop.addEventListener('click',()=>window.scrollTo({top:0,behavior:'smooth'}));
"""
rep("/* ---------- Dico, réglages, accueil ---------- */", TUTO + "\n/* ---------- Dico, réglages, accueil ---------- */")
rep("""    <button class="tool" data-act="parent" style="justify-content:center">👨‍👩‍👧 Espace parent</button></div>""",
    """    <button class="tool" data-act="parent" style="justify-content:center">👨‍👩‍👧 Espace parent</button>
    <button class="tool" data-act="tutoagain" style="justify-content:center">📘 Revoir le didacticiel</button></div>""")
# actions
rep("""  else if(a==='trq'){""", """  else if(a==='tutonext'){tutoK++;render()}
  else if(a==='tutoprev'){tutoK=Math.max(0,tutoK-1);render()}
  else if(a==='tutoend'){S.tuto=1;save();view=tutoFrom;tutoFrom='home';render()}
  else if(a==='tutoagain'){readName();tutoK=0;tutoFrom='settings';view='tuto';render()}
  else if(a==='plang'){const l=b.dataset.l;editProfile(b.dataset.id,s=>{s.lang=l});render()}
  else if(a==='pextra'){editProfile(b.dataset.id,s=>{const d=dayPlus(0);s.extra={d,m:(s.extra&&s.extra.d===d?s.extra.m:0)+15}});render()}
  else if(a==='trq'){""")

# styles
rep(""".seg.two{""", """.seg.three{grid-template-columns:repeat(3,1fr)}
.seg.three button{font-size:22px}
.tuto{min-height:300px;justify-content:center}
.tuto .tbig{font-size:76px;line-height:1.1}
.tuto .tbig .ava{font-size:76px}
#totop{position:fixed;right:calc(16px + env(safe-area-inset-right,0px));bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:30;width:52px;height:52px;border-radius:50%;border:0;background:var(--lagoon);color:#fff;font-size:28px;font-weight:800;box-shadow:0 4px 0 var(--lagoon-d),0 6px 16px rgba(0,0,0,.18);cursor:pointer}
#totop[hidden]{display:none}
.seg.two{""")

rep("const APP_VERSION=16,", "const APP_VERSION=17,")
rep("""tu vois le mot en français."};""", """tu vois le mot en français.",
  17:"Nouveau : un petit guide pour bien démarrer, des exercices dans un ordre différent à chaque fois, et la carte t'emmène directement à ta leçon !"};""")
open('index.html', 'w').write(p)
print('ok')
