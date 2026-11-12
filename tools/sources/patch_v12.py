import re, sys
p = open('index.html').read()

def rep(old, new, count=1):
    global p
    n = p.count(old)
    if n != count:
        sys.exit(f'expected {count}, found {n}: {old[:100]}')
    p = p.replace(old, new)

# ---------------------------------------------------------------- 1. Contenu : étapes plus basiques, 5 mots par niveau
rep("""/* ---------- Version 11 : 15 niveaux affichés, 5 par étape ----------
   Les autres niveaux restent dans le code (et leurs étoiles dans la sauvegarde) : il suffit de les remettre dans ACTIVE. */
const ACTIVE=['saludos','presentarse','mascotas','colores','numeros',
              'tiempo','cuerpo','rutina','ciudad','emociones',
              'tienda','restaurante','ayer','fiesta','nueva'];""",
"""/* ---------- Niveaux affichés (version 12) : 3 étapes de 5 niveaux, des basiques aux premières phrases ----------
   Les autres niveaux restent dans le code (et leurs étoiles dans la sauvegarde) : il suffit de les remettre dans ACTIVE.
   L'étape d'un niveau = sa place dans ACTIVE (5 par étape). */
const ACTIVE=['saludos','colores','numeros','mascotas','familia',
              'frutas','comida','ropa','casa','escuela',
              'presentarse','estas','gustos','preguntas','ayuda'];
/* 5 mots par leçon : le mot retiré de chaque niveau (il reste dans le code) */
const DROP={saludos:'por favor',colores:'negro',numeros:'seis',mascotas:'el pájaro',familia:'el abuelo',
  frutas:'la pera',comida:'la manzana',ropa:'el gorro',casa:'el baño',escuela:'las tijeras',
  presentarse:'¿y tú?',estas:'estoy triste',gustos:'¿te gusta?',preguntas:'¿cuántos hay?',ayuda:'¿puedo jugar?'};""")
rep("""const APP_VERSION=11,NEW_IN={""", """const APP_VERSION=12,NEW_IN={""")
rep("""  11:'Nouvelle carte : 15 niveaux, 5 par étape. Toutes tes étoiles sont gardées.'};""",
    """  11:'Nouvelle carte : 15 niveaux, 5 par étape. Toutes tes étoiles sont gardées.',
  12:"Nouveau : ton univers, un profil par enfant, la séance du jour et une évaluation à la fin de chaque étape. Toutes tes étoiles sont gardées."};""")
rep("""UNITS.forEach(u=>{u.tier=u.tier||1;if(!u.gaps)u.gaps=GAPS[u.id]||[]});
const TIERS={1:['Étape 1','Les premiers mots'],2:['Étape 2','Des phrases plus longues'],3:['Étape 3','De vraies conversations']};""",
"""UNITS.forEach(u=>{u.tier=u.tier||1;if(!u.gaps)u.gaps=GAPS[u.id]||[]});
UNITS.forEach((u,k)=>{u.tier=1+Math.floor(k/5);if(DROP[u.id])u.words=u.words.filter(w=>w[0]!==DROP[u.id])});
const TIERS={1:['Étape 1','Premiers mots'],2:['Étape 2','Mon quotidien'],3:['Étape 3','Premières phrases']};""")

# ---------------------------------------------------------------- 2. Univers, profils, révision espacée (avant la sauvegarde)
rep("""/* ---------- Sauvegarde ---------- */
const KEY='hola-lola-v1';""",
"""/* ---------- Univers : couleurs, compagnon, décor (3 proposés aux filles, 3 aux garçons, les 6 accessibles à tous) ---------- */
const THEMES={
 jungla:{name:'La jungle',g:'f',es:'Lola',title:'Lola la llama',e:'🦙',deco:'🌴 🌺 🐒 🍃 🦜',c:{bg:'#E6F6F0',bg2:'#D3EEE5',line:'#C4E2D8',lagoon:'#169C98','lagoon-d':'#0E7673',sun:'#FFC93C','sun-d':'#E0A510',coral:'#FF6F5E','coral-d':'#D9503F'}},
 hadas:{name:'Les fées',g:'f',es:'Luna',title:'Luna la fée',e:'🧚',deco:'✨ 🌸 🦋 🍄 🌙',c:{bg:'#F5EEFB',bg2:'#E9DAF6',line:'#DCC7EE',lagoon:'#8E4FD8','lagoon-d':'#6D35B3',sun:'#FFC6E5','sun-d':'#E59BC4',coral:'#E3489F','coral-d':'#B92F7D'}},
 oceano:{name:"L'océan",g:'f',es:'Tina',title:'Tina la tortue',e:'🐢',deco:'🐚 🐠 🌊 🐙 🐬',c:{bg:'#E5F3FB',bg2:'#CDE8F6',line:'#BBDCEE',lagoon:'#1C7FC0','lagoon-d':'#14629A',sun:'#FFD166','sun-d':'#E2B03C',coral:'#F27A55','coral-d':'#CF5C38'}},
 espacio:{name:"L'espace",g:'m',es:'Robi',title:'Robi le robot',e:'🤖',deco:'🪐 ⭐ 🚀 🌙 🛰️',c:{bg:'#ECEDFB',bg2:'#DADCF6',line:'#C9CCEE',lagoon:'#4A4FC4','lagoon-d':'#33379C',sun:'#FFD23F','sun-d':'#DDB21E',coral:'#0A8F85','coral-d':'#066E66'}},
 piratas:{name:'Les pirates',g:'m',es:'Paco',title:'Paco le perroquet',e:'🦜',deco:'⚓ 🏴‍☠️ 💰 🗺️ 🌊',c:{bg:'#F7F0E3',bg2:'#EEDFC4',line:'#E2CFAB',lagoon:'#B5442C','lagoon-d':'#8E3220',sun:'#F2B134','sun-d':'#CF8F17',coral:'#2E7FA6','coral-d':'#1F6183'}},
 granja:{name:'La ferme',g:'f',es:'Pipa',title:'Pipa la ponette',e:'🐴',deco:'🌻 🐔 🚜 🌾 🐮',c:{bg:'#F1F7E4',bg2:'#E1EFC8',line:'#D2E4B3',lagoon:'#4E8A28','lagoon-d':'#3A6B1D',sun:'#FFCB47','sun-d':'#E0A928',coral:'#E06A4B','coral-d':'#BD4F33'}}};
const THEME_FOR={f:['jungla','hadas','oceano'],m:['espacio','piratas','granja']};
const G=()=>THEMES[S.theme]||THEMES.jungla;
function applyTheme(){const c=G().c,st=document.documentElement.style;for(const k in c)st.setProperty('--'+k,c[k])}
/* Accords : les phrases de l'élève (et celles du compagnon) au masculin quand il le faut */
const GX=[['encantada','encantado'],['cansada','cansado'],['contenta','contento'],['aburrida','aburrido'],['nerviosa','nervioso'],['enfadada','enfadado'],['campeona','campeón'],['enchantée','enchanté'],['fatiguée','fatigué'],['contente','content'],['fâchée','fâché']];
function gx(t,g){if(g!=='m'||!t)return t;for(const [f,m] of GX)t=t.replace(new RegExp('\\\\b'+f+'\\\\b','gi'),x=>x[0]===x[0].toUpperCase()?m[0].toUpperCase()+m.slice(1):m);return t}

/* ---------- Sauvegarde ---------- */
const KEY='hola-lola-v1';""")
rep("""const def=()=>({name:'',xp:0,stars:{},streak:0,lastDay:'',todayDate:'',todayCount:0,slow:false,goal:1});""",
    """const def=()=>({name:'',xp:0,stars:{},streak:0,lastDay:'',todayDate:'',todayCount:0,slow:false,goal:1,words:{},evals:{},days:{}});""")
rep("""{const s=readSave(KEY)||readSave(BAK);if(s)S=Object.assign(def(),s)}
function save(){try{const j=JSON.stringify(S);localStorage.setItem(KEY,j);localStorage.setItem(BAK,j)}catch(e){}}""",
"""/* ---------- Profils : un par enfant. Le profil 1 garde la sauvegarde d'origine (même clé), rien ne bouge pour lui. ---------- */
const PKEY='hola-lola-profiles';
const pkey=id=>id==='p1'?KEY:KEY+'-'+id;
let P={list:[{id:'p1'}],cur:'p1'};
try{const x=JSON.parse(localStorage.getItem(PKEY)||'null');if(x&&Array.isArray(x.list)&&x.list.length)P=x}catch(e){}
function saveP(){try{localStorage.setItem(PKEY,JSON.stringify(P))}catch(e){}}
function profileInfo(id){if(id===P.cur)return S;const k=pkey(id);return readSave(k)||readSave(k+'-secours')||def()}
function loadProfile(id){P.cur=id;saveP();const k=pkey(id);const s=readSave(k)||readSave(k+'-secours');S=Object.assign(def(),s||{});migrate();applyTheme()}
function save(){try{const j=JSON.stringify(S),k=pkey(P.cur);localStorage.setItem(k,j);localStorage.setItem(k+'-secours',j)}catch(e){}}
/* ---------- Révision espacée : chaque mot revient après 1, 2, 4, 7, 15 puis 30 jours ; un mot raté revient tout de suite ---------- */
const IV=[0,1,2,4,7,15,30];
const iso=d=>d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0')+'-'+String(d.getDate()).padStart(2,'0');
const dayPlus=n=>{const d=new Date();d.setDate(d.getDate()+n);return iso(d)};
function srs(w,ok){if(!w||!w.es||!L||L.kind==='chat')return;S.words=S.words||{};const r=S.words[w.es]||{b:0,d:dayPlus(0),ok:0,ko:0};
  if(ok){r.ok++;r.b=Math.min(r.b+1,6);r.d=dayPlus(IV[r.b])}else{r.ko++;r.b=1;r.d=dayPlus(0)}S.words[w.es]=r}
function seen(w){S.words=S.words||{};if(w&&w.es&&!S.words[w.es])S.words[w.es]={b:1,d:dayPlus(1),ok:0,ko:0}}
function wordMap(){const m={};UNITS.forEach(u=>u.words.forEach(w=>{const x=Object.assign(W(w),{conv:!!u.conv});m[x.es]=x}));return m}
function dueList(){const WM=wordMap(),t=dayPlus(0);return Object.entries(S.words||{}).filter(([k,r])=>WM[k]&&r.d<=t).sort((a,b)=>a[1].b-b[1].b).map(([k])=>WM[k])}
function migrate(){
  S.words=S.words||{};S.evals=S.evals||{};S.days=S.days||{};
  if(!S.mig12){UNITS.forEach(u=>{if(S.stars[u.id])u.words.forEach(w=>{const x=W(w);if(!S.words[x.es])S.words[x.es]={b:2,d:dayPlus(0),ok:1,ko:0}})});S.mig12=1;if(S.name)save()}
}
function addTime(){if(L&&L.t0){const s=Math.min(1200,(Date.now()-L.t0)/1000),k=dayPlus(0);S.days=S.days||{};S.days[k]=(S.days[k]||0)+Math.round(s);L.t0=0}}""")
rep("""  if((x.lastDay||'')&&(+x.streak||0)>S.streak){S.streak=+x.streak;S.lastDay=x.lastDay}
  save();""",
"""  if((x.lastDay||'')&&(+x.streak||0)>S.streak){S.streak=+x.streak;S.lastDay=x.lastDay}
  for(const k in (x.words||{})){const a=S.words[k],b=x.words[k];if(!a||(+b.b||0)>a.b)S.words[k]=b}
  for(const k in (x.evals||{})){if(!S.evals[k]||(+x.evals[k].pct||0)>S.evals[k].pct)S.evals[k]=x.evals[k]}
  for(const k in (x.days||{}))S.days[k]=Math.max(S.days[k]||0,+x.days[k]||0);
  if(!S.gender&&x.gender)S.gender=x.gender;if(!S.theme&&x.theme)S.theme=x.theme;
  save();""")

# ---------------------------------------------------------------- 3. Voix, prénom, compagnon, accords
rep("""const fill=t=>t.replace(/\\{name\\}/g,S.name||'amiga');""",
"""const nameFill=t=>t.replace(/\\{name\\}/g,S.name||'amiga').replace(/\\bLola\\b/g,G().es);
const fill=t=>gx(nameFill(t),S.gender);   /* phrases de l'élève */
const fillG=t=>gx(nameFill(t),G().g);     /* phrases du compagnon */""")
rep("new SpeechSynthesisUtterance(fill(t))", "new SpeechSynthesisUtterance(nameFill(t))")
rep("""const W=w=>({es:w[0],fr:w[1],e:w[2]});""", """const W=w=>({es:gx(w[0],S.gender),fr:gx(w[1],S.gender),e:w[2]});""")
rep("<b>🔇 Lola ne peut pas parler ici.</b>", "<b>🔇 ${G().es} ne peut pas parler ici.</b>")
rep("return 'Écoute Lola en lent 🐢, puis répète syllabe par syllabe.'", "return 'Écoute '+G().es+' en lent 🐢, puis répète syllabe par syllabe.'")
rep("<div class=\"heardtxt\">Lola a compris :", "<div class=\"heardtxt\">${G().es} a compris :")
rep("${micOK?'Écoute Lola, puis appuie sur 🎤 et répète.':'Écoute Lola, puis répète à voix haute.'}", "${micOK?'Écoute '+G().es+', puis appuie sur 🎤 et répète.':'Écoute '+G().es+', puis répète à voix haute.'}")
rep("Vrai ou faux ?<small>Écoute Lola :", "Vrai ou faux ?<small>Écoute ${G().es} :")
rep("Construis la phrase<small>Écoute Lola, puis", "Construis la phrase<small>Écoute ${G().es}, puis")
rep("Écoute : que veut dire Lola ?", "Écoute : que veut dire ${G().es} ?")
rep("Dis-le en espagnol. Lola vérifie ton accent", "Dis-le en espagnol. ${G().es} vérifie ton accent")
rep("'Écoute Lola et répète à voix haute.'", "'Écoute '+G().es+' et répète à voix haute.'")
rep("Discute avec Lola<small>", "Discute avec ${G().es}<small>")
rep("<div class=\"es\">${esc(fill(d.l))}</div>", "<div class=\"es\">${esc(fillG(d.l))}</div>")
rep("'Ici, Lola ne peut pas t\\'entendre. Dans l\\'appli installée, elle écoute et vérifie l\\'accent.'", "'Ici, '+G().es+' ne peut pas t\\'entendre. Dans l\\'appli installée, l\\'accent est vérifié.'")
rep("\"Il faut Internet pour que Lola puisse t'écouter.\"", "\"Il faut Internet pour que \"+G().es+\" puisse t'écouter.\"")
rep("'Belle conversation ! Lola est fière de toi.'", "'Belle conversation ! '+G().es+(G().g==='m'?' est fier de toi.':' est fière de toi.')")
rep("'actif. Lola écoute, note l\\'accent sur 100 et ne valide qu\\'au-dessus de '+PASS+'.'", "'actif. '+G().es+' écoute, note l\\'accent sur 100 et ne valide qu\\'au-dessus de '+PASS+'.'")
rep("'bloqué dans cette page. Pour que Lola vérifie l\\'accent, utilise l\\'appli installée.'", "'bloqué dans cette page. Pour vérifier l\\'accent, utilise l\\'appli installée.'")
rep("""  if(s.t==='talk')return say(s.d.l);
  if(s.t==='build')return say(s.sent);""", """  if(s.t==='talk')return say(fillG(s.d.l));
  if(s.t==='build')return say(fill(s.sent));""")
rep("const ok=s.used.map(i=>nw(s.tiles[i])).join(' ')===s.target.map(nw).join(' ');\n  say(s.sent);", "const ok=s.used.map(i=>nw(s.tiles[i])).join(' ')===s.target.map(nw).join(' ');\n  say(fill(s.sent));")
rep("if(s.t==='talk'){const o=s.opts[k];ok=isOk(o);const right=s.opts.find(isOk);say(right[0]);", "if(s.t==='talk'){const o=s.opts[k];ok=isOk(o);const right=s.opts.find(isOk);say(fill(right[0]));")

# ---------------------------------------------------------------- 4. Déblocage : l'étape suivante s'ouvre après l'évaluation réussie
rep("""const unlocked=i=>{
  if(i===0||S.stars[UNITS[i-1].id]||S.stars[UNITS[i].id])return true;
  if((S.opened||[]).includes(UNITS[i].id))return true;
  const j=LEGACY.indexOf(UNITS[i].id);return j>0&&!!S.stars[LEGACY[j-1]];
};""",
"""const unlocked=i=>{
  const u=UNITS[i];
  if(S.stars[u.id]||(S.opened||[]).includes(u.id))return true;
  if(i===0)return true;
  if(u.tier!==UNITS[i-1].tier)return !!(S.evals&&S.evals[UNITS[i-1].tier]);   /* 1er niveau d'une étape : évaluation de l'étape d'avant réussie */
  if(S.stars[UNITS[i-1].id])return true;
  const j=LEGACY.indexOf(u.id);return j>0&&!!S.stars[LEGACY[j-1]];
};
const stageUnits=t=>UNITS.filter(u=>u.tier===t);
const stageDone=t=>stageUnits(t).every(u=>S.stars[u.id]);""")
rep("let view='home',L=null,R=null,confirmReset=false,showBk=false,bkMsg='';",
    "let view='home',L=null,R=null,confirmReset=false,showBk=false,bkMsg='',allThemes=false,gateQ=null,gateMsg='',pdel=null;")

# ---------------------------------------------------------------- 5. Accueil
rep("""  const cur=UNITS.findIndex((u,i)=>unlocked(i)&&!S.stars[u.id]);""",
"""  let cur=UNITS.findIndex((u,i)=>unlocked(i)&&!S.stars[u.id]);
  const evalCur=[1,2,3].find(t=>stageDone(t)&&!S.evals[t]&&(cur<0||UNITS[cur].tier>t));if(evalCur)cur=-1;
  const due=dueList().length,nWords=Object.keys(S.words||{}).length;""")
rep("""    return `${tierHead}<button class="node""", """    const last=i===UNITS.length-1||UNITS[i+1].tier!==u.tier;
    return `${tierHead}<button class="node""")
rep("""      <b>${esc(u.es)}</b><em>${i+1}. ${esc(u.fr)}</em>${u.conv?'<span class="ctag">💬 Conversation</span>':''}</button>`}).join('');""",
"""      <b>${esc(u.es)}</b><em>${i+1}. ${esc(u.fr)}</em>${u.conv?'<span class="ctag">💬 Conversation</span>':''}</button>${last?evalNode(u.tier,evalCur===u.tier):''}`}).join('');""")
rep("""  <div class="top"><div class="lola" aria-hidden="true">🦙</div>
    <div class="hello"><small>Lola la llama te dit :</small><h1>¡Hola, ${esc(S.name)}!</h1></div>""",
"""  <div class="top"><button class="lola" data-act="who" aria-label="Changer de joueur">${G().e}</button>
    <div class="hello"><small>${esc(G().title)} te dit :</small><h1>¡Hola, ${esc(S.name)}!</h1></div>""")
rep("""  <div class="chips"><span class="chip">🔥""", """  <div class="deco" aria-hidden="true">${G().deco}</div>
  <div class="chips"><span class="chip">🔥""")
rep("""    <button class="btn coral" data-act="review" ${learnedUnits().length?'':'disabled'}>🎯 Défi du jour</button>""",
    """    <button class="btn coral" data-act="seance" ${nWords?'':'disabled'}>🎯 Séance du jour${due?` <span class="badge">${due}</span>`:''}</button>""")
rep("""💬 Parler avec Lola</button></div>""", """💬 Parler avec ${G().es}</button></div>""")
rep("""<div class="node"><span class="disc" style="background:var(--coral);box-shadow:0 7px 0 var(--coral-d)">🏆</span><b>¡Campeona!</b>""",
    """<div class="node"><span class="disc" style="background:var(--coral);box-shadow:0 7px 0 var(--coral-d)">🏆</span><b>${S.gender==='m'?'¡Campeón!':'¡Campeona!'}</b>""")
rep("""/* ---------- Construction d'une leçon ---------- */""",
"""function evalNode(t,isCur){
  const ev=S.evals[t],ready=stageDone(t);
  return `<button class="node ev ${ev?'done':ready?'':'locked'} ${isCur?'current':''}" data-act="eval" data-t="${t}" aria-label="Évaluation de l'étape ${t}">
    ${isCur?'<span class="start-tag">À toi !</span>':''}
    <span class="disc">${ev?'🏅':ready?'📝':'🔒'}</span>
    <b>Évaluation</b><em>${ev?`Étape ${t} réussie : ${ev.pct} %`:`Étape ${t} · 80 % pour passer`}</em></button>`;
}

/* ---------- Construction d'une leçon ---------- */""")

# ---------------------------------------------------------------- 6. Leçons : mots nouveaux enregistrés, séance du jour, évaluation
rep("const u=UNITS[i],words=u.words.map(W),steps=[],phr=u.conv||u.tier>1;", "const u=UNITS[i],words=u.words.map(W),steps=[],phr=!!u.conv;")
rep("answered:null,tries:0};view='lesson';render();", "answered:null,tries:0,t0:Date.now()};view='lesson';render();", 3)
rep("""/* ---------- Écran de leçon ---------- */""",
"""/* Séance du jour : les mots à revoir aujourd'hui (révision espacée), complétés par les mots les moins sûrs */
function startSeance(list){
  const WM=wordMap(),all=Object.values(WM);let pool=(list||dueList()).slice(0,8);
  if(pool.length<8){const have=new Set(pool.map(w=>w.es));pool=pool.concat(Object.keys(S.words||{}).filter(k=>WM[k]&&!have.has(k)).sort((a,b)=>S.words[a].b-S.words[b].b).map(k=>WM[k]).slice(0,8-pool.length))}
  if(!pool.length)return false;
  const steps=[];if(uniqPic(pool).length>=4)steps.push(matchStep(pool));
  shuffle(pool.slice()).forEach((w,k)=>steps.push(k%3===2?{t:'speak',w}:{t:k%2?'pick':(w.conv?'mean':'listen'),w,opts:optsFor(w,all)}));
  tfSteps(pool.filter(w=>!w.conv),2).forEach(s=>steps.push(s));
  L={unit:-1,kind:'seance',steps,i:0,mistakes:0,ok:0,answered:null,tries:0,t0:Date.now()};view='lesson';render();return true;
}
/* Évaluation de fin d'étape : 12 questions sur les 5 niveaux, 80 % pour ouvrir l'étape suivante */
function startEval(t){
  const us=stageUnits(t),words=uniqPic(shuffle(us.flatMap(u=>u.words.map(w=>Object.assign(W(w),{conv:!!u.conv})))));
  const steps=[];
  words.slice(0,8).forEach((w,k)=>steps.push({t:k%2?'pick':(w.conv?'mean':'listen'),w,opts:optsFor(w,words)}));
  const rest=words.slice(8).filter(w=>!w.conv);tfSteps(rest.length>=2?rest:words.filter(w=>!w.conv),2).forEach(s=>steps.push(s));
  shuffle(us.flatMap(u=>u.gaps)).slice(0,12-steps.length).forEach(g=>steps.push(gapStep(g)));
  L={unit:-1,kind:'eval',tier:t,steps:shuffle(steps),i:0,mistakes:0,ok:0,answered:null,tries:0,missed:[],t0:Date.now()};view='lesson';render();
}

/* ---------- Écran de leçon ---------- */""")
rep("""  const pct=L.i/L.steps.length*100;let body='';""" if "  const pct=L.i/L.steps.length*100;let body='';" in p else "const s=L.steps[L.i],pct=L.i/L.steps.length*100;let body='';",
    "const s=L.steps[L.i],pct=L.i/L.steps.length*100;let body=L.kind==='eval'&&L.i===0&&!L.answered?`<div class=\"evalhead\">📝 Évaluation de l'étape ${L.tier} · ${L.steps.length} questions · 80 % pour réussir</div>`:'';")
rep("<div class=\"chat\"><div class=\"lola\" aria-hidden=\"true\">🦙</div>", "<div class=\"chat\"><div class=\"lola\" aria-hidden=\"true\">${G().e}</div>")
# pas d'exercice reproposé pendant l'évaluation
rep("if(ok)L.ok++;else{L.mistakes++;if(!s.retry&&again)L.steps.push(Object.assign(again(),{retry:1}))}",
    "if(ok)L.ok++;else{L.mistakes++;if(!s.retry&&again&&L.kind!=='eval')L.steps.push(Object.assign(again(),{retry:1}))}")
rep("""  else{const o=s.opts[k];ok=o.es===s.w.es;say(s.w.es);msg=`${esc(s.w.es)} = ${esc(s.w.fr)}`;}
  tone(ok);
  if(ok)L.ok++;else{L.mistakes++;if(!s.retry)L.steps.push(Object.assign({},s,{retry:1,opts:shuffle(s.opts.slice())}));}""",
"""  else{const o=s.opts[k];ok=o.es===s.w.es;say(s.w.es);msg=`${esc(s.w.es)} = ${esc(s.w.fr)}`;srs(s.w,ok);if(!ok&&L.missed)L.missed.push(s.w);}
  tone(ok);
  if(ok)L.ok++;else{L.mistakes++;if(!s.retry&&L.kind!=='eval')L.steps.push(Object.assign({},s,{retry:1,opts:shuffle(s.opts.slice())}));}""")
rep("""  const ok=(v===1)===s.truth;
  settle(""", """  const ok=(v===1)===s.truth;srs(s.w,ok);if(!ok&&L.missed)L.missed.push(s.w);
  settle(""")
rep("""  if(w.es===s.sel){s.done.push(w.es);s.sel=null;tone(true);""",
    """  if(w.es===s.sel){s.done.push(w.es);srs(w,!(s.wr||[]).includes(w.es));s.sel=null;tone(true);""")
rep("""  }else{s.err++;s.sel=null;s.bad=k;tone(false);render()}""", """  }else{s.err++;(s.wr=s.wr||[]).push(s.sel);s.sel=null;s.bad=k;tone(false);render()}""")
rep("""  if(r.pass){L.ok++;L.answered={ok:true,msg:''};render();return}
  if(L.tries>=3){
    L.mistakes++;""", """  if(r.pass){L.ok++;srs(s.w,true);L.answered={ok:true,msg:''};render();return}
  if(L.tries>=3){
    L.mistakes++;srs(s.w,false);""")

# ---------------------------------------------------------------- 7. Fin de leçon et résultat de l'évaluation
rep("""function finish(){
  const stars=""", """function finish(){
  addTime();
  if(L.kind==='eval')return finishEval();
  const stars=""")
rep("""function result(){""", """function finishEval(){
  const t=today(),pct=Math.round(L.ok/L.steps.length*100),pass=pct>=80;
  if(S.lastDay!==t){S.streak=S.lastDay===yesterday()?S.streak+1:1;S.lastDay=t}
  if(S.todayDate!==t){S.todayDate=t;S.todayCount=0}
  S.todayCount++;
  if(pass){S.evals[L.tier]={pct:Math.max(pct,(S.evals[L.tier]||{}).pct||0),d:dayPlus(0)};S.xp+=20}
  const missed=uniqPic(L.missed||[]);
  save();R={eval:true,tier:L.tier,pct,pass,missed};view='result';render();if(pass)confetti();
  say(pass?'¡Muy bien, '+S.name+'!':'¡Casi, '+S.name+'!');
}
function resultEval(){
  const next=UNITS.findIndex(u=>u.tier===R.tier+1);
  app.innerHTML=`<div class="center">
    <div class="lola big" aria-hidden="true">${G().e}</div>
    <h2 style="font-size:36px">${R.pass?`Étape ${R.tier} réussie !`:'¡Casi! Presque…'}</h2>
    <div class="xp">${R.pct} % de bonnes réponses</div>
    <p class="say">${R.pass?(next>=0?`L'étape ${R.tier+1} est ouverte : ${esc(TIERS[R.tier+1][1])}. +20 points !`:'Tu as réussi toutes les étapes. Bravo !'):`Il faut 80 % pour passer. Révise ces mots avec la séance, puis réessaie :`}</p>
    ${!R.pass&&R.missed.length?`<div class="misslist">${R.missed.map(w=>`<button class="dw" data-act="sayw" data-w="${esc(w.es)}">${w.e[0]==='#'?pic(w.e):`<span>${esc(w.e)}</span>`}<b>${esc(w.es)}</b><small>${esc(w.fr)}</small></button>`).join('')}</div>`:''}
    <div style="width:100%;display:grid;gap:14px;margin-top:8px">
      ${R.pass&&next>=0?`<button class="btn sun" data-act="unit" data-i="${next}">Commencer l'étape ${R.tier+1} →</button>`:''}
      ${!R.pass?`<button class="btn sun" data-act="seancemiss">🎯 Réviser ces mots</button><button class="btn ghost" data-act="eval" data-t="${R.tier}">Réessayer l'évaluation</button>`:''}
      <button class="btn" data-act="home">Retour à la carte</button></div></div>`;
}
function result(){
  if(R.eval)return resultEval();""")
rep("""    <div class="lola big" aria-hidden="true">🦙</div>
    <h2 style="font-size:38px">""", """    <div class="lola big" aria-hidden="true">${G().e}</div>
    <h2 style="font-size:38px">""")
rep("'Défi terminé, tes mots sont bien rangés dans ta tête !'", "'Séance terminée : tes mots sont bien rangés dans ta tête !'")

# ---------------------------------------------------------------- 8. Dico, réglages, accueil des nouveaux joueurs, profils, espace parent
rep("<b>${esc(w[0])}</b><small>${esc(w[1])}</small></button>`).join('')}</div>`).join('')",
    "<b>${esc(gx(w[0],S.gender))}</b><small>${esc(gx(w[1],S.gender))}</small></button>`).join('')}</div>`).join('')")
rep("'<div class=\"empty\" style=\"margin-top:14px\">Termine le premier niveau pour remplir ton dico ! 🦙</div>'",
    "`<div class=\"empty\" style=\"margin-top:14px\">Termine le premier niveau pour remplir ton dico ! ${G().e}</div>`")
rep("""  <div class="set"><label class="field" for="nm">Prénom<input id="nm" value="${esc(S.name)}" maxlength="20" autocomplete="off"></label></div>""",
"""  <div class="set"><label class="field" for="nm">Prénom<input id="nm" value="${esc(S.name)}" maxlength="20" autocomplete="off"></label>
    <button class="tool" data-act="chtheme" style="justify-content:center">🎨 Changer d'univers (${esc(G().name)})</button>
    <button class="tool" data-act="who" style="justify-content:center">👧👦 Changer de joueur</button>
    <button class="tool" data-act="parent" style="justify-content:center">👨‍👩‍👧 Espace parent</button></div>""")
rep("${S.goal===n?'background:var(--sun)':''}", "${S.goal===n?'background:var(--sun)':''}")
rep("""function welcome(){
  app.innerHTML=`<div class="center">
    <div class="lola big" aria-hidden="true">🦙</div>
    <h1 style="font-size:40px">¡Hola!</h1>
    <p class="say" style="font-size:19px">Je suis <b>Lola la llama</b>. Chaque jour, on apprend l'espagnol ensemble en quelques minutes. ¿Cómo te llamas ?</p>
    <label class="field" for="nm" style="width:100%;text-align:left">Ton prénom<input id="nm" maxlength="20" autocomplete="off" placeholder="Écris ton prénom"></label>
    <button class="btn sun" data-act="go">¡Vamos! C'est parti</button></div>`;
}""",
"""/* Accueil d'un joueur : prénom, puis fille ou garçon, puis son univers */
function welcome(){
  if(!S.name){app.innerHTML=`<div class="center">
    <div class="lola big" aria-hidden="true">👋</div>
    <h1 style="font-size:40px">¡Hola!</h1>
    <p class="say" style="font-size:19px">Chaque jour, on apprend l'espagnol en quelques minutes. ¿Cómo te llamas ?</p>
    <label class="field" for="nm" style="width:100%;text-align:left">Ton prénom<input id="nm" maxlength="20" autocomplete="off" placeholder="Écris ton prénom"></label>
    <button class="btn sun" data-act="go">Suivant</button>
    ${P.list.length>1?'<button class="btn ghost" data-act="who">← Choisir un autre joueur</button>':''}</div>`;return}
  if(!S.gender){app.innerHTML=`<div class="center">
    <h1 style="font-size:34px">¡Hola, ${esc(S.name)}!</h1>
    <p class="say" style="font-size:19px">Tu es…</p>
    <div class="row" style="width:100%"><button class="btn sun big2" data-act="gender" data-g="f">👧 Une fille</button><button class="btn big2" data-act="gender" data-g="m">👦 Un garçon</button></div>
    <p class="note">Pour dire « encantada » ou « encantado » 😉</p></div>`;return}
  const keys=allThemes?Object.keys(THEMES):THEME_FOR[S.gender];
  app.innerHTML=`<div class="center" style="justify-content:flex-start;padding-top:12px">
    <h1 style="font-size:32px">Choisis ton univers</h1>
    <p class="say">Ton compagnon t'accompagne dans toutes tes leçons.</p>
    <div class="themes">${keys.map(k=>{const t=THEMES[k];return `<button class="thcard ${S.theme===k?'on':''}" data-act="theme" data-t="${k}" style="--tb:${t.c.bg};--tl:${t.c.lagoon};--ts:${t.c.sun}">
      <span class="thmas">${t.e}</span><span class="thtxt"><b>${esc(t.name)}</b><small>avec ${esc(t.title)}</small><span class="thdeco">${t.deco}</span></span></button>`}).join('')}</div>
    <button class="btn ghost" data-act="allthemes">${allThemes?'Voir moins d\\'univers':'Voir les 6 univers'}</button></div>`;
}
/* Qui joue ? */
function who(){
  const cards=P.list.map(p=>{const s=profileInfo(p.id),th=THEMES[s.theme]||THEMES.jungla,n=Object.keys(s.stars||{}).length;
    return `<button class="pcard ${p.id===P.cur?'cur':''}" data-act="pick" data-id="${p.id}" style="--pc:${th.c.lagoon};--pb:${th.c.bg}"><span class="pav">${s.theme?th.e:'🙂'}</span><b>${esc(s.name||'Nouveau joueur')}</b><small>${n} niveau${n>1?'x':''} réussi${n>1?'s':''}</small></button>`}).join('');
  app.innerHTML=`<div class="center" style="justify-content:flex-start;padding-top:20px">
    <h1 style="font-size:36px">¿Quién juega?</h1><p class="say">Qui joue aujourd'hui ? Chacun garde sa progression.</p>
    <div class="who">${cards}${P.list.length<6?'<button class="pcard add" data-act="addp"><span class="pav">➕</span><b>Ajouter un enfant</b><small>Nouveau profil</small></button>':''}</div></div>`;
}
/* Espace parent : protégé par une petite multiplication */
function parentGate(){
  if(!gateQ){const a=6+(Math.random()*4|0),b=6+(Math.random()*4|0);gateQ={a,b}}
  app.innerHTML=`<div class="head"><button class="icon-btn" data-act="settings" aria-label="Retour">←</button><h2>Espace parent</h2></div>
  <div class="set"><p style="margin:0;font-weight:800">Pour les parents : combien font ${gateQ.a} × ${gateQ.b} ?</p>
    <label class="field" for="pg">Réponse<input id="pg" inputmode="numeric" autocomplete="off"></label>
    <button class="btn" data-act="pgok">Entrer</button>${gateMsg?`<p class="note" style="color:var(--bad)">${esc(gateMsg)}</p>`:''}</div>`;
}
function parent(){
  const WM=wordMap(),days=[6,5,4,3,2,1,0].map(n=>dayPlus(-n)),DN=['D','L','M','M','J','V','S'];
  const cards=P.list.map(p=>{const s=profileInfo(p.id),th=THEMES[s.theme]||THEMES.jungla,ws=s.words||{},keys=Object.keys(ws);
    const mins=days.map(d=>Math.round(((s.days||{})[d]||0)/60)),maxm=Math.max(10,...mins),week=mins.reduce((a,b)=>a+b,0);
    const hard=keys.filter(k=>ws[k].ko>0).sort((a,b)=>(ws[b].ko-ws[b].ok)-(ws[a].ko-ws[a].ok)).slice(0,6);
    const ev=[1,2,3].map(t=>(s.evals||{})[t]?`Étape ${t} : ${(s.evals||{})[t].pct} %`:null).filter(Boolean);
    return `<div class="set pcard2"><div class="row" style="align-items:center"><span class="pav" style="flex:none;background:${th.c.bg}">${s.theme?th.e:'🙂'}</span><b style="font-size:20px">${esc(s.name||'Nouveau joueur')}</b></div>
      <div class="stats"><div><b>${keys.length}</b><small>mots vus</small></div><div><b>${keys.filter(k=>ws[k].b>=4).length}</b><small>mots bien retenus</small></div><div><b>${Object.keys(s.stars||{}).filter(id=>UNITS.some(u=>u.id===id)).length}/${UNITS.length}</b><small>niveaux réussis</small></div><div><b>${week} min</b><small>cette semaine</small></div></div>
      <div class="bars" role="img" aria-label="Minutes par jour sur 7 jours">${mins.map((m,i)=>`<div class="barc"><span class="bv">${m||''}</span><i style="height:${Math.round(m/maxm*70)}px"></i><small>${DN[new Date(days[i]+'T12:00').getDay()]}</small></div>`).join('')}</div>
      <p class="note">Évaluations : ${ev.length?ev.join(' · '):'aucune réussie pour l\\'instant'} · Série : ${s.streak||0} jour(s)</p>
      <p class="note">Mots difficiles : ${hard.length?hard.map(k=>`<b>${esc(k)}</b>${WM[k]?' ('+esc(WM[k].fr)+')':''}`).join(', '):'aucun pour l\\'instant'}</p>
      ${pdel===p.id?`<p style="margin:0;font-weight:800">Supprimer le profil de ${esc(s.name||'ce joueur')} et toute sa progression ?</p><div class="row"><button class="btn coral" data-act="pdelyes" data-id="${p.id}">Oui, supprimer</button><button class="btn ghost" data-act="pdelno">Non</button></div>`
        :`<button class="tool" data-act="pdel" data-id="${p.id}" style="justify-content:center">Supprimer ce profil</button>`}</div>`}).join('');
  app.innerHTML=`<div class="head"><button class="icon-btn" data-act="settings" aria-label="Retour">←</button><h2>Espace parent</h2></div>
  <p class="note" style="margin-bottom:12px">Le temps compté est celui passé dans les leçons, séances et évaluations.</p>${cards}
  ${P.list.length<6?'<button class="btn ghost" data-act="addp">➕ Ajouter un enfant</button>':''}`;
}""")
rep("""function render(){
  if(view==='welcome')welcome();""", """function render(){
  if(view==='who')who();else if(view==='pgate')parentGate();else if(view==='parent')parent();else
  if(view==='welcome')welcome();""")

# ---------------------------------------------------------------- 9. Actions
rep("""  else if(a==='go'){readName();if(!S.name){$('#nm').focus();return}S.ver=APP_VERSION;save();view='home';render();say('¡Hola, '+S.name+'! ¡Vamos!')}""",
"""  else if(a==='go'){readName();if(!S.name){$('#nm').focus();return}if(!S.ver)S.ver=APP_VERSION;save();render();say('¡Hola, '+S.name+'!')}
  else if(a==='gender'){S.gender=b.dataset.g;allThemes=false;save();render()}
  else if(a==='theme'){S.theme=b.dataset.t;if(!S.ver)S.ver=APP_VERSION;applyTheme();save();view='home';render();say('¡Hola, '+S.name+'! Soy '+G().es+'. ¡Vamos!')}
  else if(a==='allthemes'){allThemes=!allThemes;render()}
  else if(a==='chtheme'){readName();S.theme='';allThemes=true;view='welcome';render()}
  else if(a==='who'){readName();addTime();save();view='who';render()}
  else if(a==='pick'){loadProfile(b.dataset.id);view=S.name&&S.gender&&S.theme?'home':'welcome';render()}
  else if(a==='addp'){save();const id='p'+Date.now().toString(36);P.list.push({id});loadProfile(id);view='welcome';render()}
  else if(a==='parent'){readName();gateQ=null;gateMsg='';pdel=null;view='pgate';render()}
  else if(a==='pgok'){const v=+(($('#pg')||{}).value||'');if(gateQ&&v===gateQ.a*gateQ.b){view='parent';render()}else{gateQ=null;gateMsg='Ce n\\'est pas la bonne réponse.';render()}}
  else if(a==='pdel'){pdel=b.dataset.id;render()}
  else if(a==='pdelno'){pdel=null;render()}
  else if(a==='pdelyes'){const id=b.dataset.id,k=pkey(id);try{localStorage.removeItem(k);localStorage.removeItem(k+'-secours')}catch(e){}
    P.list=P.list.filter(x=>x.id!==id);pdel=null;if(!P.list.length)P.list=[{id:'p'+Date.now().toString(36)}];
    if(P.cur===id||!P.list.some(x=>x.id===P.cur))loadProfile(P.list[0].id);else saveP();
    view=S.name?'parent':'welcome';render()}
  else if(a==='seance'){if(startSeance())speakStep()}
  else if(a==='seancemiss'){if(startSeance(R&&R.missed&&R.missed.length?R.missed:null))speakStep()}
  else if(a==='eval'){const t=+b.dataset.t;if(!stageDone(t)&&!S.evals[t]){say('¡Todavía no!');return}startEval(t);speakStep()}""")
rep("""  else if(a==='next'){L.i++;""", """  else if(a==='next'){if(L.steps[L.i]&&L.steps[L.i].t==='learn')seen(L.steps[L.i].w);L.i++;""")
rep("""  else if(a==='quit'){speechSynthesis&&speechSynthesis.cancel();view='home';render()}""",
    """  else if(a==='quit'){speechSynthesis&&speechSynthesis.cancel();addTime();save();view='home';render()}""")
rep("""  else if(a==='resetyes'){try{localStorage.removeItem(KEY);localStorage.removeItem(BAK)}catch(e){}S=def();confirmReset=false;view='welcome';render()}""",
    """  else if(a==='resetyes'){const k=pkey(P.cur);try{localStorage.removeItem(k);localStorage.removeItem(k+'-secours')}catch(e){}S=def();migrate();applyTheme();confirmReset=false;view='welcome';render()}""")
rep("""view=S.name?'home':'welcome';render();""",
    """loadProfile(P.list.some(x=>x.id===P.cur)?P.cur:P.list[0].id);
view=P.list.length>1?'who':(S.name&&S.gender&&S.theme?'home':'welcome');render();""")

# ---------------------------------------------------------------- 10. Styles
rep("""html,body{height:100%}""", """html,body{height:100%}
button.lola{border:0;cursor:pointer;padding:0}
.deco{text-align:center;font-size:20px;letter-spacing:6px;margin-top:10px;opacity:.85}
.badge{display:inline-grid;place-items:center;min-width:26px;height:26px;padding:0 6px;border-radius:999px;background:#fff;color:var(--coral-d);font-size:15px;font-family:var(--f-body)}
.node.ev .disc{background:var(--sun);box-shadow:0 7px 0 var(--sun-d);font-size:36px}
.node.ev.done .disc{background:var(--good);box-shadow:0 7px 0 #17803F}
.node.ev.locked .disc{background:var(--lock);box-shadow:0 7px 0 #8FAAA3}
.evalhead{background:var(--sun);border-radius:14px;padding:8px 12px;font-weight:800;text-align:center}
.misslist{display:grid;grid-template-columns:repeat(auto-fill,minmax(96px,1fr));gap:10px;width:100%}
.big2{min-height:84px;font-size:22px}
.themes{display:grid;gap:12px;width:100%}
.thcard{display:flex;align-items:center;gap:14px;background:var(--tb);border:4px solid transparent;border-radius:22px;padding:12px 14px;text-align:left;box-shadow:0 5px 0 var(--tl)}
.thcard.on{border-color:var(--tl)}
.thmas{flex:none;width:72px;height:72px;border-radius:50%;background:var(--ts);display:grid;place-items:center;font-size:44px}
.thtxt{display:flex;flex-direction:column;gap:2px;min-width:0}
.thtxt b{font-family:var(--f-display);font-size:22px;line-height:1.1}
.thtxt small{font-weight:700;color:var(--muted)}
.thdeco{font-size:18px;letter-spacing:3px}
.who{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px;width:100%}
.pcard{background:var(--pb,var(--card));border:4px solid transparent;border-radius:22px;padding:16px 10px;display:flex;flex-direction:column;align-items:center;gap:4px;box-shadow:0 5px 0 var(--pc,var(--line))}
.pcard.cur{border-color:var(--pc)}
.pcard.add{background:var(--card);box-shadow:0 5px 0 var(--line)}
.pcard b{font-family:var(--f-display);font-size:20px}
.pcard small{font-weight:700;color:var(--muted);font-size:13px}
.pav{width:64px;height:64px;border-radius:50%;background:var(--card);display:grid;place-items:center;font-size:38px}
.stats{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}
.stats div{background:var(--bg);border-radius:14px;padding:8px 10px;display:flex;flex-direction:column}
.stats b{font-family:var(--f-display);font-size:24px;line-height:1.1;font-variant-numeric:tabular-nums}
.stats small{font-weight:700;color:var(--muted);font-size:13px}
.bars{display:flex;align-items:flex-end;gap:6px;height:110px;padding-top:4px}
.barc{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:3px;min-width:0}
.barc i{display:block;width:100%;max-width:28px;min-height:3px;border-radius:6px 6px 2px 2px;background:var(--lagoon)}
.barc .bv{font-size:12px;font-weight:800;font-variant-numeric:tabular-nums}
.barc small{font-size:12px;font-weight:800;color:var(--muted)}""")
open('index.html', 'w').write(p)

# Reste-t-il « Lola » ou le lama en dehors des données ?
code = p[p.index('/* ---------- Univers'):]
left = [m.start() for m in re.finditer(r'Lola|🦙', code)]
for i in left:
    print('LEFT:', code[max(0, i-60):i+40].replace('\n', ' '))
print('ok')
