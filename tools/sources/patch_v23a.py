import sys, json
p = open('index.html').read()
def rep(a, b, c=1):
    global p
    if p.count(a) != c: sys.exit(f'{p.count(a)}x: ' + a[:110])
    p = p.replace(a, b)
def cut(start, end, new):
    global p
    a = p.index(start); b = p.index(end, a)
    p = p[:a] + new + p[b:]
def addjs(obj_start, entries):
    add = ''.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False) + ',' for k, v in entries.items())
    rep(obj_start, obj_start + add)

# ===================== A. Temps d'écran : bouton + pour une durée personnalisée =====================
rep("""function limitBox(s,id){const cu=s.limit>0&&![10,15,20,30].includes(s.limit);
  return `<div class="limit"><b>⏳ Temps d'écran maximum par jour</b>
    <div class="seg">${[0,10,15,20,30].map(m=>`<button class="${(s.limit||0)===m?'on':''}" data-act="plim" data-id="${id}" data-m="${m}" aria-pressed="${(s.limit||0)===m}">${m?`${m}<small>min</small>`:'Sans<small>limite</small>'}</button>`).join('')}</div>
    <div class="custom ${cu?'on':''}"><label for="plim-${id}">Personnalisé</label><input id="plim-${id}" type="number" inputmode="numeric" min="1" max="300" step="1" placeholder="45" value="${cu?s.limit:''}"><span>min</span><button class="tool" data-act="plimc" data-id="${id}">Valider</button></div>
    <p class="note">Choisissez entre 1 et 300 minutes, puis Valider.</p>""",
"""const limOpen=new Set();
function limitBox(s,id){const cu=s.limit>0&&![10,15,20,30].includes(s.limit),op=limOpen.has(id);
  return `<div class="limit"><b>⏳ Temps d'écran maximum par jour</b>
    <div class="seg six">${[0,10,15,20,30].map(m=>`<button class="${(s.limit||0)===m?'on':''}" data-act="plim" data-id="${id}" data-m="${m}" aria-pressed="${(s.limit||0)===m}">${m?`${m}<small>min</small>`:'Sans<small>limite</small>'}</button>`).join('')}<button class="${cu?'on':''}" data-act="plimplus" data-id="${id}" aria-expanded="${op}" aria-label="Autre durée">${cu?`${s.limit}<small>min</small>`:'+<small>Autre</small>'}</button></div>
    ${op?`<div class="custom ${cu?'on':''}"><label for="plim-${id}">Personnalisé</label><input id="plim-${id}" type="number" inputmode="numeric" min="1" max="300" step="1" placeholder="45" value="${cu?s.limit:''}"><span>min</span><button class="tool" data-act="plimc" data-id="${id}">Valider</button></div>
    <p class="note">Choisissez entre 1 et 300 minutes, puis Valider.</p>`:''}""")
rep("""  else if(a==='plimc'){""", """  else if(a==='plimplus'){const id=b.dataset.id;limOpen.has(id)?limOpen.delete(id):limOpen.add(id);render();const i=document.getElementById('plim-'+id);if(i)i.focus()}
  else if(a==='plimc'){""")
rep("""  else if(a==='plim'){const m=+b.dataset.m;""", """  else if(a==='plim'){const m=+b.dataset.m;limOpen.delete(b.dataset.id);""")
rep("editProfile(id,s=>{s.limit=m;delete s.unlockDay;delete s.extra});render()}", "editProfile(id,s=>{s.limit=m;delete s.unlockDay;delete s.extra});limOpen.delete(id);render()}")

# ===================== B. Boutique : accessoires, skins, univers =====================
SHOP = r"""/* ---------- Garde-robe et boutique : tout se gagne avec les pièces ----------
   Accessoires (5 emplacements), skins du compagnon (filtres de couleur), univers à débloquer. */
const ACC={head:[['🎀','Nœud',15],['🧢','Casquette',15],['🎩','Chapeau',20],['🌸','Fleur dans les cheveux',20],['🎓','Toque',30],['👒','Capeline',30],['⛑️','Casque',35],['👑','Couronne',60],['🪖','Casque de soldat',40]],
  face:[['👓','Lunettes',15],['🕶️','Lunettes de soleil',25],['🥽','Lunettes de ski',35],['🤿','Masque de plongée',45]],
  neck:[['🧣','Écharpe',20],['📿','Collier',30],['🏅','Médaille',40],['👔','Cravate',25],['🦋','Papillon',35]],
  hand:[['🎈','Ballon',10],['🍦','Glace',10],['🌻','Fleur',10],['⚽','Ballon de foot',15],['🍭','Sucette',15],['🧸','Nounours',25],['🪄','Baguette magique',30],['🪁','Cerf-volant',35],['🎸','Guitare',45],['🌂','Parapluie',30],['🏆','Coupe',80]],
  fx:[['✨','Paillettes',60],['💖','Cœurs',70],['🫧','Bulles',70],['❄️','Flocons',80],['🌈','Arc-en-ciel',100],['🎉','Confettis',90],['⭐','Étoiles',100]]};
const SLOT={head:'Sur la tête',face:'Sur les yeux',neck:'Autour du cou',hand:'Dans la main',fx:'Effet magique'};
const SKINS=[['base','Classique',0],['candy','Bonbon',120],['ice','Glacier',150],['sun','Soleil',150],['night','Nuit étoilée',200],['ghost','Fantôme',200],['gold','Doré',300],['rainbow','Arc-en-ciel',400]];
const THEME_PRICE=300;
const freeThemes=()=>THEME_FOR[S.gender||'f'].slice(0,2);
const hasTheme=k=>freeThemes().includes(k)||(S.ownT||[]).includes(k)||S.theme===k;
let shopMsg='',shopTab='acc';
function avatar(cls=''){const a=S.acc||{};return `<span class="ava ${cls} ${S.skin&&S.skin!=='base'?'sk-'+S.skin:''}"><span class="ava-b">${G().e}</span>${a.fx?`<span class="ava-e" aria-hidden="true">${a.fx}</span>`:''}${a.head?`<span class="ava-h">${a.head}</span>`:''}${a.face?`<span class="ava-f">${a.face}</span>`:''}${a.neck?`<span class="ava-n">${a.neck}</span>`:''}${a.hand?`<span class="ava-x">${a.hand}</span>`:''}</span>`}
/* achat : true si payé ; sinon message « il te manque… » */
function spend(price){if((S.coins||0)>=price){S.coins-=price;tone(true);return true}shopMsg=`Il te manque ${price-(S.coins||0)} pièces. Joue encore un peu !`;return false}
function wardrobe(){
  const a=S.acc||{},own=S.owned||[],tabs=[['acc','👕 Accessoires'],['skin','🎨 Skins'],['univ','🌍 Univers']];
  let body='';
  if(shopTab==='acc')body=Object.entries(ACC).map(([slot,items])=>`<div class="dunit">${SLOT[slot]}</div><div class="shop">${items.map(([e,n,price])=>{const has=own.includes(e),on=a[slot]===e;
    return `<button class="item ${on?'on':''} ${!has&&(S.coins||0)<price?'poor':''}" data-act="acc" data-slot="${slot}" data-e="${e}" data-p="${price}"><span>${e}</span><b>${n}</b><small>${on?'Porté ✓':has?'Mettre':`🪙 ${price}`}</small></button>`}).join('')}</div>`).join('')
    +`<button class="btn ghost" data-act="accoff" style="margin-top:14px">Tout enlever</button>`;
  else if(shopTab==='skin')body=`<p class="note">Change la couleur de ${esc(G().es)} !</p><div class="shop">${SKINS.map(([k,n,price])=>{const has=!price||(S.skins||[]).includes(k),on=(S.skin||'base')===k;
    return `<button class="item ${on?'on':''} ${!has&&(S.coins||0)<price?'poor':''}" data-act="skin" data-k="${k}" data-p="${price}"><span class="ava ${k!=='base'?'sk-'+k:''}"><span class="ava-b">${G().e}</span></span><b>${n}</b><small>${on?'Porté ✓':has?'Mettre':`🪙 ${price}`}</small></button>`}).join('')}</div>`;
  else body=`<p class="note">Chaque univers change les couleurs et le compagnon. Ta progression reste la même.</p><div class="themes">${Object.keys(THEMES).map(k=>{const t=THEMES[k],has=hasTheme(k),on=S.theme===k;
    return `<button class="thcard ${on?'on':''} ${!has&&(S.coins||0)<THEME_PRICE?'poor':''}" data-act="univ" data-t="${k}" style="--tb:${t.c.bg};--tl:${t.c.lagoon};--ts:${t.c.sun}">
      <span class="thmas">${t.e}</span><span class="thtxt"><b>${esc(t.name)}</b><small>avec ${esc(t.title)}</small><span class="thdeco">${on?'Ton univers ✓':has?'Choisir':`🔒 🪙 ${THEME_PRICE}`}</span></span></button>`}).join('')}</div>`;
  app.innerHTML=head('👗 Garde-robe')+`<div class="center" style="flex:none;padding:16px 0 6px;gap:8px"><div class="lola big" aria-hidden="true">${avatar()}</div>
    <p class="note">Tu as <b>🪙 ${S.coins||0}</b> pièces. Gagne-en avec les leçons, la séance du jour, les jeux et les défis.</p>${shopMsg?`<p class="note" role="status" style="color:var(--coral-d)">${esc(shopMsg)}</p>`:''}</div>
  <div class="tabs" role="tablist">${tabs.map(([k,t])=>`<button role="tab" aria-selected="${shopTab===k}" class="${shopTab===k?'on':''}" data-act="shoptab" data-k="${k}">${t}</button>`).join('')}</div>${body}`;
}

"""
cut("/* ---------- Compagnon à habiller", "/* ---------- Mini-jeux", SHOP)

# ===================== C. Jeux : 2 nouveaux jeux, décors, bonus =====================
GAMES = r"""/* ---------- Mini-jeux : 3 offerts + 2 à débloquer, décors et bonus achetés avec les pièces ---------- */
let GM=null;
const GAMES=[['catch','🫧','Attrape les mots',"Touche la bonne bulle avant qu'elle tombe",0],['memory','🃏','Memory','Retrouve chaque mot et son image',0],
  ['chrono','⏱️','Course contre la montre','Le plus de bonnes réponses en 45 secondes',0],['letters','🔤','Les lettres','Écris le mot espagnol, lettre par lettre',120],['tfx','✅','Vrai ou faux express','Oui ou non ? Réponds vite, 30 secondes !',100]];
const DECORS=[['classic','Classique',0],['ocean','Océan',60],['space','Espace',80],['candy','Bonbons',60],['forest','Forêt',60]];
const BONUS={time:['⏱️','+10 secondes','Course et Vrai ou faux',15],shield:['🛡️','Deuxième chance','Attrape les mots',15],hint:['💡','Indice','Memory et Les lettres',15]};
const gameOwned=g=>{const x=GAMES.find(y=>y[0]===g);return !x||!x[4]||(S.gOwned||[]).includes(g)};
const bonusN=k=>(S.bonus||{})[k]||0;
function gamePool(){const WM=wordMap();return uniqPic(shuffle(Object.keys(S.words||{}).filter(k=>WM[k]).map(k=>WM[k])))}
function games(){
  const n=gamePool().length,ok=n>=4;
  app.innerHTML=head('🎮 Jeux')+`<p class="note" style="margin-bottom:12px">${ok?`On joue avec tes ${n} mots appris. Chaque partie rapporte des pièces 🪙.`:'Termine ta première leçon pour débloquer les jeux !'} <b>🪙 ${S.coins||0}</b></p>
  ${shopMsg?`<p class="note" role="status" style="color:var(--coral-d)">${esc(shopMsg)}</p>`:''}
  <div class="eplist">${GAMES.map(([g,e,t,d,price])=>gameOwned(g)
    ?`<button class="epi ${ok?'':'lock'}" data-act="game" data-g="${g}"><span class="epn">${e}</span><span class="ept"><b>${t}</b><small>${d}</small></span><span>▶</span></button>`
    :`<button class="epi ${(S.coins||0)<price?'lock':''}" data-act="gbuy" data-g="${g}" data-p="${price}"><span class="epn">${e}</span><span class="ept"><b>${t}</b><small>${d}</small></span><span class="price">🔒 🪙 ${price}</span></button>`).join('')}</div>
  <div class="dunit">🎨 Décors des jeux</div><div class="shop">${DECORS.map(([k,n2,price])=>{const has=!price||(S.decors||[]).includes(k),on=(S.decor||'classic')===k;
    return `<button class="item deco-${k} ${on?'on':''} ${!has&&(S.coins||0)<price?'poor':''}" data-act="decor" data-k="${k}" data-p="${price}"><span class="dprev"></span><b>${n2}</b><small>${on?'Choisi ✓':has?'Choisir':`🪙 ${price}`}</small></button>`}).join('')}</div>
  <div class="dunit">🎁 Bonus</div><div class="shop">${Object.entries(BONUS).map(([k,[e,n2,where,price]])=>`<button class="item ${(S.coins||0)<price?'poor':''}" data-act="bonus" data-k="${k}" data-p="${price}"><span>${e}</span><b>${n2}</b><small>${where}</small><small>🪙 ${price} · ${bonusN(k)}</small></button>`).join('')}</div>
  <p class="note">Les bonus aident pendant une partie. Ils n'ajoutent jamais de temps d'écran.</p>`;
}
function gTimer(ms){GM.end=Date.now()+ms;GM.span=ms;GM.timer=setInterval(()=>{if(!GM||!GM.end||view!=='game'){clearInterval(GM&&GM.timer);return}
  if(Date.now()>=GM.end){clearInterval(GM.timer);endGame()}else{const b=$('#tbar');if(b)b.style.width=Math.max(0,(GM.end-Date.now())/GM.span*100)+'%'}},200)}
const strip=es=>es.replace(/^(el|la|los|las) /i,'');
function startGame(g){
  const pool=gamePool();if(pool.length<4)return;
  if(GM&&GM.timer)clearInterval(GM.timer);
  if(g==='catch'){GM={g,round:0,n:8,score:0,pool,t0:Date.now()};nextCatch()}
  else if(g==='memory'){const ws=pool.slice(0,6);GM={g,cards:shuffle(ws.flatMap(w=>[{w,k:'t'},{w,k:'p'}])),open:[],done:[],moves:0,pairs:ws.length,t0:Date.now()};view='game';render()}
  else if(g==='letters'){const ws=shuffle(pool.filter(w=>{const s=strip(w.es);return s.length>=3&&s.length<=9&&!/[\s¿?¡!,]/.test(s)}));if(!ws.length)return;
    GM={g,round:0,n:Math.min(6,ws.length),score:0,pool,ws,t0:Date.now()};nextLetters()}
  else if(g==='tfx'){GM={g,score:0,pool,t0:Date.now()};nextTfx();gTimer(30000)}
  else{GM={g:'chrono',score:0,pool,t0:Date.now()};nextChrono();gTimer(45000)}
}
function nextCatch(){
  if(!GM||GM.g!=='catch')return;if(GM.round>=GM.n)return endGame();
  const target=pick(GM.pool);GM.cur={target,opts:optsFor(target,GM.pool).map((w,i)=>({w,x:4+i*32+Math.random()*8,dur:(4.4+Math.random()*1.2).toFixed(2),delay:(Math.random()*.6).toFixed(2)}))};
  GM.round++;GM.lock=false;GM.miss=null;view='game';render();say(target.es);
}
function nextChrono(){const w=pick(GM.pool);GM.cur={w,opts:optsFor(w,GM.pool)};GM.lock=false;GM.bad=null;view='game';render()}
function nextLetters(){
  if(GM.round>=GM.n)return endGame();
  const w=GM.ws[GM.round],t=strip(w.es);GM.cur={w,t,tiles:shuffle([...t]),used:[],typed:'',res:null};GM.round++;GM.lock=false;view='game';render();say(w.es);
}
function nextTfx(){const w=pick(GM.pool),other=pick(GM.pool.filter(x=>x!==w)),truth=Math.random()<.5;GM.cur={w,show:truth?w:other,truth};GM.lock=false;GM.bad=null;view='game';render()}
function game(){
  const g=GM;let body='';
  if(g.g==='catch'){const c=g.cur;body=`<div class="ghead"><span>Manche ${g.round} / ${g.n}</span><span>⭐ ${g.score}</span></div>
    <div class="ask" style="text-align:center">Attrape : <span class="es">${esc(c.target.es)}</span> <button class="tool" data-act="gsay" aria-label="Réécouter">🔊</button></div>
    <div class="sky">${c.opts.map((o,i)=>`<button class="bubble-f ${g.miss===i?'sel-bad':''} ${g.lock&&o.w===c.target?'sel-good':''}" data-act="gcatch" data-k="${i}" style="left:${o.x}%;animation-duration:${o.dur}s;animation-delay:${o.delay}s" aria-label="${esc(o.w.fr)}">${pic(o.w.e)}</button>`).join('')}</div>
    ${bonusN('shield')?`<p class="note" style="text-align:center">🛡️ Deuxième chance : ${bonusN('shield')}</p>`:''}${g.msg?`<p class="note" style="text-align:center;color:var(--good)">${esc(g.msg)}</p>`:''}`}
  else if(g.g==='memory'){body=`<div class="ghead"><span>${g.done.length} / ${g.pairs} paires</span><span>${g.moves} coups</span></div>
    <div class="mem">${g.cards.map((c,i)=>{const up=g.open.includes(i)||g.done.includes(c.w.es)||g.peek;return `<button class="mcard ${up?'up':''} ${g.done.includes(c.w.es)?'ok':''}" data-act="gmem" data-k="${i}" aria-label="${up?esc(c.k==='t'?c.w.es:c.w.fr):'Carte cachée'}">${up?(c.k==='t'?`<b>${esc(c.w.es)}</b>`:pic(c.w.e)):'❓'}</button>`}).join('')}</div>
    ${bonusN('hint')&&!g.peek?`<button class="tool" data-act="gbonus" data-k="hint" style="margin:12px auto 0">💡 Indice (${bonusN('hint')})</button>`:''}`}
  else if(g.g==='letters'){const c=g.cur;body=`<div class="ghead"><span>Mot ${g.round} / ${g.n}</span><span>⭐ ${g.score}</span></div>
    <div class="card"><div class="pic">${pic(c.w.e)}</div><button class="tool" data-act="gsay" aria-label="Réécouter">🔊</button></div>
    <div class="spell" aria-live="polite">${[...c.t].map((ch,i)=>`<span class="sl ${c.res==='ok'?'ok':c.res==='bad'?'bad':''}">${c.res==='bad'?esc(ch):esc(c.typed[i]||'')}</span>`).join('')}</div>
    ${c.res?'':`<div class="tiles">${c.tiles.map((ch,i)=>`<button class="tile" data-act="ltr" data-k="${i}" ${c.used.includes(i)?'disabled':''}>${esc(ch)}</button>`).join('')}</div>
    <div class="row" style="justify-content:center;gap:8px;margin-top:10px"><button class="tool" data-act="ldel">⌫ Effacer</button>${bonusN('hint')?`<button class="tool" data-act="gbonus" data-k="hint">💡 Indice (${bonusN('hint')})</button>`:''}</div>`}`}
  else if(g.g==='tfx'){const c=g.cur;body=`<div class="ghead"><span>✅ Vrai ou faux</span><span>⭐ ${g.score}</span></div><div class="bar"><i id="tbar" style="width:${Math.max(0,(g.end-Date.now())/g.span*100)}%;background:var(--coral)"></i></div>
    <div class="card" style="margin-top:14px"><div class="pic">${pic(c.w.e)}</div><div class="es">${esc(c.show.es)}</div></div>
    <div class="opts tf" style="margin-top:14px"><button class="opt ${g.bad===1?'sel-bad':''}" data-act="gtf" data-k="1">✅ Sí</button><button class="opt ${g.bad===0?'sel-bad':''}" data-act="gtf" data-k="0">❌ No</button></div>
    ${bonusN('time')?`<button class="tool" data-act="gbonus" data-k="time" style="margin:12px auto 0">⏱️ +10 s (${bonusN('time')})</button>`:''}`}
  else{const c=g.cur;body=`<div class="ghead"><span>⏱️ Course</span><span>⭐ ${g.score}</span></div><div class="bar"><i id="tbar" style="width:${Math.max(0,(g.end-Date.now())/g.span*100)}%;background:var(--coral)"></i></div>
    <div class="card" style="margin-top:14px"><div class="pic">${pic(c.w.e)}</div></div>
    <div class="opts" style="margin-top:14px">${c.opts.map((o,i)=>`<button class="opt ${g.bad===i?'sel-bad':''}" data-act="gchr" data-k="${i}">${esc(o.es)}</button>`).join('')}</div>
    ${bonusN('time')?`<button class="tool" data-act="gbonus" data-k="time" style="margin:12px auto 0">⏱️ +10 s (${bonusN('time')})</button>`:''}`}
  const title=(GAMES.find(x=>x[0]===g.g)||['','','Jeu'])[2];
  app.innerHTML=`<div class="lbar"><button class="icon-btn" data-act="games" aria-label="Quitter le jeu">✕</button><b style="flex:1;font-family:var(--f-display);font-size:20px">${title}</b></div><div class="stage deco-${S.decor||'classic'}">${body}</div>`;
}
function catchTap(k){
  const g=GM,c=g.cur;if(!g||g.lock)return;g.lock=true;const o=c.opts[k],ok=o.w===c.target;g.msg='';
  srs(c.target,ok);tone(ok);if(ok)g.score++;else{g.miss=k;if(bonusN('shield')){S.bonus.shield--;save();g.round--;g.msg='🛡️ Deuxième chance !'}}render();setTimeout(nextCatch,ok?500:1100);
}
function memTap(k){
  const g=GM;if(!g||g.lock||g.peek||g.open.includes(k)||g.done.includes(g.cards[k].w.es))return;
  g.open.push(k);if(g.cards[k].k==='t')say(g.cards[k].w.es);
  if(g.open.length<2){render();return}
  g.moves++;const [a,b]=g.open.map(i=>g.cards[i]);
  if(a.w.es===b.w.es&&a.k!==b.k){g.done.push(a.w.es);g.open=[];tone(true);srs(a.w,true);render();if(g.done.length===g.pairs)setTimeout(endGame,600);return}
  g.lock=true;render();setTimeout(()=>{if(GM!==g)return;g.open=[];g.lock=false;render()},950);
}
function chronoTap(k){
  const g=GM;if(!g||g.lock)return;const ok=g.cur.opts[k].es===g.cur.w.es;srs(g.cur.w,ok);tone(ok);
  if(ok){g.score++;nextChrono()}else{g.lock=true;g.bad=k;render();setTimeout(()=>{if(GM===g&&view==='game')nextChrono()},450)}
}
function tfxTap(k){
  const g=GM;if(!g||g.lock)return;const ok=(k===1)===g.cur.truth;srs(g.cur.w,ok);tone(ok);
  if(ok){g.score++;nextTfx()}else{g.lock=true;g.bad=k;render();setTimeout(()=>{if(GM===g&&view==='game')nextTfx()},450)}
}
function letterTap(k){
  const g=GM,c=g&&g.cur;if(!c||c.res||c.used.includes(k))return;c.used.push(k);c.typed+=c.tiles[k];
  if(c.typed.length===c.t.length){const ok=c.typed.toLowerCase()===c.t.toLowerCase();c.res=ok?'ok':'bad';srs(c.w,ok);tone(ok);if(ok)g.score++;render();say(c.w.es);setTimeout(()=>{if(GM===g)nextLetters()},ok?900:1700)}
  else render();
}
function useBonus(k){
  const g=GM;if(!g||!bonusN(k))return;
  if(k==='time'&&g.end){g.end+=10000;g.span+=10000}
  else if(k==='hint'&&g.g==='memory'){g.peek=true;setTimeout(()=>{if(GM===g){g.peek=false;render()}},1500)}
  else if(k==='hint'&&g.g==='letters'){const c=g.cur,need=c.t[c.typed.length];if(c.res||need==null)return;const i=c.tiles.findIndex((ch,j)=>ch===need&&!c.used.includes(j));
    if(c.typed!==c.t.slice(0,c.typed.length)){c.typed='';c.used=[]}const j=c.tiles.findIndex((ch,x)=>ch===c.t[c.typed.length]&&!c.used.includes(x));if(j<0)return;S.bonus.hint--;save();letterTap(j);return}
  else return;
  S.bonus[k]--;save();render();
}
function endGame(){
  const g=GM;if(!g||g.over)return;g.over=true;if(g.timer)clearInterval(g.timer);
  const coins=g.g==='memory'?Math.max(3,12-(g.moves-g.pairs)):g.g==='letters'?g.score*2:g.score,score=g.g==='memory'?g.done.length:g.score;
  addCoins(coins);addPts(coins);save();
  g.coins=coins;g.final=score;view='gameover';render();if(coins>=5)confetti();
}
function gameover(){
  const g=GM,txt=g.g==='memory'?`Toutes les paires en ${g.moves} coups !`:g.g==='catch'?`${g.final} mots attrapés sur ${g.n}`:g.g==='letters'?`${g.final} mots écrits sur ${g.n}`:g.g==='tfx'?`${g.final} bonnes réponses en 30 secondes`:`${g.final} bonnes réponses en 45 secondes`;
  app.innerHTML=`<div class="center"><div class="lola big" aria-hidden="true">${avatar()}</div><h2 style="font-size:36px">${g.final?'¡Muy bien!':'¡Casi!'}</h2>
  <div class="xp">${txt}</div><div class="xp" style="font-size:24px">+${g.coins} 🪙</div>
  <div style="width:100%;display:grid;gap:12px"><button class="btn sun" data-act="game" data-g="${g.g}">Rejouer</button><button class="btn ghost" data-act="games">Autres jeux</button><button class="btn" data-act="home">Retour à la carte</button></div></div>`;
}

"""
cut("/* ---------- Mini-jeux", "/* ---------- Défi en famille", GAMES)

# actions boutique et jeux
rep("""  else if(a==='accoff'){S.acc={};save();render()}""", """  else if(a==='accoff'){S.acc={};save();render()}
  else if(a==='shoptab'){shopTab=b.dataset.k;shopMsg='';render()}
  else if(a==='skin'){const k=b.dataset.k,pr=+b.dataset.p;S.skins=S.skins||[];shopMsg='';
    if(pr&&!S.skins.includes(k)){if(!spend(pr)){save();render();return}S.skins.push(k);shopMsg='Acheté !'}S.skin=k;save();render()}
  else if(a==='univ'){const k=b.dataset.t;shopMsg='';if(S.theme===k)return;
    if(!hasTheme(k)){if(!spend(THEME_PRICE)){render();return}S.ownT=S.ownT||[];S.ownT.push(k);shopMsg='Acheté !'}
    S.theme=k;applyTheme();save();render();say('¡Hola! Soy '+G().es+'.')}
  else if(a==='gbuy'){const g=b.dataset.g,pr=+b.dataset.p;shopMsg='';if(spend(pr)){S.gOwned=S.gOwned||[];S.gOwned.push(g);shopMsg='Nouveau jeu débloqué !'}save();render()}
  else if(a==='decor'){const k=b.dataset.k,pr=+b.dataset.p;S.decors=S.decors||[];shopMsg='';
    if(pr&&!S.decors.includes(k)){if(!spend(pr)){render();return}S.decors.push(k);shopMsg='Acheté !'}S.decor=k;save();render()}
  else if(a==='bonus'){const k=b.dataset.k,pr=+b.dataset.p;shopMsg='';if(spend(pr)){S.bonus=S.bonus||{};S.bonus[k]=(S.bonus[k]||0)+1;shopMsg='Acheté !'}save();render()}
  else if(a==='gbonus')useBonus(b.dataset.k);
  else if(a==='ltr')letterTap(+b.dataset.k);
  else if(a==='ldel'){const c=GM&&GM.cur;if(c&&!c.res&&c.used.length){c.used.pop();c.typed=c.typed.slice(0,-1);render()}}
  else if(a==='gtf')tfxTap(+b.dataset.k);""")
rep("""  else if(a==='acc'){const sl=b.dataset.slot,e=b.dataset.e,pr=+b.dataset.p;S.acc=S.acc||{};S.owned=S.owned||[];""",
    """  else if(a==='acc'){const sl=b.dataset.slot,e=b.dataset.e,pr=+b.dataset.p;S.acc=S.acc||{};S.owned=S.owned||[];shopMsg='';""")
rep("""  else if(a==='game'){if(gamePool().length<4||!guard())return;startGame(b.dataset.g)}""",
    """  else if(a==='game'){if(gamePool().length<4||!gameOwned(b.dataset.g)||!guard())return;shopMsg='';startGame(b.dataset.g)}""")
rep("""  else if(a==='games'){""", """  else if(a==='games'){shopMsg='';""")
# changer d'univers depuis les réglages = onglet Univers de la garde-robe
rep("""  else if(a==='chtheme'){readName();prevTheme=S.theme;themeFrom='settings';wStep='theme';allThemes=true;view='welcome';render()}""",
    """  else if(a==='chtheme'){readName();shopTab='univ';shopMsg='';view='wardrobe';render()}""")
# choix de l'univers à la création : 2 univers offerts, les autres se débloquent avec les pièces
rep("""  const keys=allThemes?Object.keys(THEMES):THEME_FOR[S.gender||'f'];""", """  const keys=allThemes?Object.keys(THEMES):freeThemes();""")
rep("""    <div class="themes">${keys.map(k=>{const t=THEMES[k];return `<button class="thcard ${S.theme===k?'on':''}" data-act="theme" data-t="${k}" style="--tb:${t.c.bg};--tl:${t.c.lagoon};--ts:${t.c.sun}">
      <span class="thmas">${t.e}</span><span class="thtxt"><b>${esc(t.name)}</b><small>avec ${esc(t.title)}</small><span class="thdeco">${t.deco}</span></span></button>`}).join('')}</div>
    <button class="btn ghost" data-act="allthemes">${allThemes?'Voir moins d\\'univers':'Voir les 6 univers'}</button>""",
    """    <div class="themes">${keys.map(k=>{const t=THEMES[k],has=hasTheme(k);return `<button class="thcard ${S.theme===k?'on':''} ${has?'':'poor'}" data-act="${has?'theme':'themelock'}" data-t="${k}" style="--tb:${t.c.bg};--tl:${t.c.lagoon};--ts:${t.c.sun}">
      <span class="thmas">${t.e}</span><span class="thtxt"><b>${esc(t.name)}</b><small>avec ${esc(t.title)}</small><span class="thdeco">${has?t.deco:`🔒 🪙 ${THEME_PRICE}`}</span></span></button>`}).join('')}</div>
    ${allThemes?'<p class="note">Les autres univers se débloquent plus tard avec les pièces gagnées, dans la garde-robe.</p>':''}
    <button class="btn ghost" data-act="allthemes">${allThemes?'Voir moins d\\'univers':'Voir les autres univers'}</button>""")
rep("""  else if(a==='allthemes'){allThemes=!allThemes;render()}""", """  else if(a==='allthemes'){allThemes=!allThemes;render()}
  else if(a==='themelock'){say('¡Todavía no!');const n=document.querySelector('.themes + .note');if(n){n.classList.remove('shake');void n.offsetWidth;n.classList.add('shake')}}""")

# ===================== D. Voix : femme, fille, 2 voix d'homme =====================
rep("const PITCH={n:1.1,h:1.45,l:.78};", "const PITCH={n:1.1,h:1.45,l:.78,m:.72,g:.5},RATEK={n:1,h:1,l:1,m:.94,g:.9};")
rep("u.pitch=PITCH[S.pitch]||1.1;", "u.pitch=PITCH[S.pitch]||1.1;u.rate*=RATEK[S.pitch]||1;")
rep("""      <b>Ton de la voix</b>
      <div class="seg three">${[['n','Normal'],['h','Aigu'],['l','Grave']].map(([k,t])=>""",
    """      <b>Qui parle ?</b>
      <div class="seg four">${[['n','👩 Femme'],['h','👧 Fille'],['m','👨 Homme'],['g','🧔 Homme grave']].map(([k,t])=>""")
rep("""      <p class="note">Les voix disponibles dépendent du téléphone. Pour en ajouter : réglages Android → Synthèse vocale Google → Espagnol → installer d'autres voix.</p></div>""",
    """      <p class="note">Les voix disponibles dépendent du téléphone. Pour en ajouter : réglages Android → Synthèse vocale Google → Espagnol → installer d'autres voix.</p>
      <p class="note">Les voix d'homme sont créées à partir de la voix choisie au-dessus, en plus grave. Si le téléphone propose une vraie voix d'homme (Android : Synthèse vocale Google → Espagnol → voix), elle apparaît dans la liste.</p></div>""")

# ===================== E. Langue du système par défaut =====================
rep("""  if(st==='lang'){const pre=S.lang||((navigator.language||'fr').slice(0,2));""", """  if(st==='lang'){const pre=S.lang||sysLang();""")
rep("const LF=()=>", """const sysLang=()=>{const l=((navigator.languages&&navigator.languages[0])||navigator.language||'fr').slice(0,2).toLowerCase();return LANGS[l]?l:'fr'};
const LF=()=>""")
rep("  if(!S.mig22){", "  if(!S.mig23){if(!S.lang&&S.name)S.lang=sysLang();S.ownT=S.ownT||[];if(S.theme&&!S.ownT.includes(S.theme))S.ownT.push(S.theme);S.mig23=1;if(S.name)save()}\n  if(!S.mig22){")

# ===================== styles =====================
rep(".accs{", """.seg.six{grid-template-columns:repeat(6,1fr);gap:5px}
.seg.six button{font-size:16px}
.seg.four{grid-template-columns:repeat(2,1fr)}
.seg.four button{font-size:16px;min-height:46px}
.tabs{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:6px 0 10px;background:var(--bg2);padding:5px;border-radius:16px}
.tabs button{min-height:44px;border-radius:12px;font-weight:800;font-size:15px;background:transparent}
.tabs button.on{background:var(--card);box-shadow:0 2px 0 var(--line)}
.thcard.poor{opacity:.6}
.ava-n{position:absolute;bottom:.02em;left:50%;transform:translateX(-50%);font-size:.38em}
.ava-e{position:absolute;inset:-.25em;font-size:.36em;display:flex;justify-content:space-between;align-items:flex-start;pointer-events:none;animation:floaty 3s ease-in-out infinite}
@keyframes floaty{0%,100%{transform:translateY(0)}50%{transform:translateY(-.25em)}}
.sk-candy .ava-b{filter:hue-rotate(290deg) saturate(1.6)}
.sk-ice .ava-b{filter:hue-rotate(170deg) saturate(.8) brightness(1.15)}
.sk-sun .ava-b{filter:hue-rotate(25deg) saturate(2) brightness(1.08)}
.sk-night .ava-b{filter:hue-rotate(210deg) saturate(1.3) brightness(.75) drop-shadow(0 0 .08em #7aa2ff)}
.sk-ghost .ava-b{filter:grayscale(1) brightness(1.35) opacity(.75)}
.sk-gold .ava-b{filter:sepia(1) saturate(4) hue-rotate(-12deg) brightness(1.05) drop-shadow(0 0 .08em #ffd54f)}
.sk-rainbow .ava-b{animation:rainbow 4s linear infinite}
@keyframes rainbow{from{filter:hue-rotate(0deg) saturate(1.6)}to{filter:hue-rotate(360deg) saturate(1.6)}}
.item .ava{font-size:34px}
.epi .price{font-weight:800;font-size:15px;white-space:nowrap}
.dprev{display:block;width:44px;height:34px;border-radius:10px;background:linear-gradient(var(--bg2),var(--card));border:2px solid var(--line)}
.deco-ocean .dprev,.deco-ocean .sky{background:linear-gradient(#b3e5fc,#4fc3f7)}
.deco-space .dprev,.deco-space .sky{background:linear-gradient(#1a237e,#5c6bc0)}
.deco-candy .dprev,.deco-candy .sky{background:linear-gradient(#fce4ec,#f8bbd0)}
.deco-forest .dprev,.deco-forest .sky{background:linear-gradient(#dcedc8,#81c784)}
.deco-ocean .mcard:not(.up){background:#0288d1;box-shadow:0 5px 0 #01579b}
.deco-space .mcard:not(.up){background:#283593;box-shadow:0 5px 0 #1a237e}
.deco-candy .mcard:not(.up){background:#ec407a;box-shadow:0 5px 0 #ad1457}
.deco-forest .mcard:not(.up){background:#43a047;box-shadow:0 5px 0 #1b5e20}
.spell{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin:14px 0}
.sl{width:36px;height:46px;border-bottom:4px solid var(--line);display:grid;place-items:center;font-family:var(--f-display);font-weight:800;font-size:26px}
.sl.ok{color:var(--good);border-color:var(--good)}
.sl.bad{color:var(--bad);border-color:var(--bad)}
@media (prefers-reduced-motion:reduce){.ava-e,.sk-rainbow .ava-b{animation:none}}
.accs{""")

# ===================== traductions =====================
UIADD = {
 "Autre": ["Other", "Altro"], "Autre durée": ["Other duration", "Altra durata"],
 "👕 Accessoires": ["👕 Accessories", "👕 Accessori"], "🎨 Skins": ["🎨 Skins", "🎨 Skin"], "🌍 Univers": ["🌍 Worlds", "🌍 Mondi"],
 "Change la couleur de {0} !": ["Change {0}'s colour!", "Cambia il colore di {0}!"],
 "Classique": ["Classic", "Classico"], "Bonbon": ["Candy", "Caramella"], "Glacier": ["Glacier", "Ghiacciaio"], "Soleil": ["Sun", "Sole"],
 "Nuit étoilée": ["Starry night", "Notte stellata"], "Fantôme": ["Ghost", "Fantasma"], "Doré": ["Golden", "Dorato"], "Arc-en-ciel": ["Rainbow", "Arcobaleno"],
 "Chaque univers change les couleurs et le compagnon. Ta progression reste la même.": ["Each world changes the colours and the companion. Your progress stays the same.", "Ogni mondo cambia i colori e il compagno. I tuoi progressi restano gli stessi."],
 "Ton univers ✓": ["Your world ✓", "Il tuo mondo ✓"], "Choisir": ["Choose", "Scegli"], "Choisi ✓": ["Chosen ✓", "Scelto ✓"], "Mettre": ["Wear", "Indossa"],
 "🔒 🪙 {0}": ["🔒 🪙 {0}", "🔒 🪙 {0}"], "Acheté !": ["Bought!", "Comprato!"], "Nouveau jeu débloqué !": ["New game unlocked!", "Nuovo gioco sbloccato!"],
 "Autour du cou": ["Around the neck", "Al collo"], "Effet magique": ["Magic effect", "Effetto magico"],
 "Fleur dans les cheveux": ["Flower in the hair", "Fiore nei capelli"], "Capeline": ["Sun hat", "Cappellino"], "Casque": ["Helmet", "Casco"], "Casque de soldat": ["Army helmet", "Elmetto"],
 "Lunettes de ski": ["Ski goggles", "Occhiali da sci"], "Masque de plongée": ["Diving mask", "Maschera da sub"],
 "Écharpe": ["Scarf", "Sciarpa"], "Collier": ["Necklace", "Collana"], "Médaille": ["Medal", "Medaglia"], "Cravate": ["Tie", "Cravatta"], "Papillon": ["Butterfly", "Farfalla"],
 "Sucette": ["Lollipop", "Lecca-lecca"], "Nounours": ["Teddy bear", "Orsacchiotto"], "Cerf-volant": ["Kite", "Aquilone"], "Guitare": ["Guitar", "Chitarra"], "Parapluie": ["Umbrella", "Ombrello"], "Coupe": ["Trophy", "Coppa"],
 "Paillettes": ["Sparkles", "Brillantini"], "Cœurs": ["Hearts", "Cuori"], "Bulles": ["Bubbles", "Bolle"], "Flocons": ["Snowflakes", "Fiocchi di neve"], "Confettis": ["Confetti", "Coriandoli"], "Étoiles": ["Stars", "Stelle"],
 "Les lettres": ["Letters", "Le lettere"], "Écris le mot espagnol, lettre par lettre": ["Spell the Spanish word, letter by letter", "Scrivi la parola spagnola, lettera per lettera"],
 "Vrai ou faux express": ["Quick true or false", "Vero o falso lampo"], "Oui ou non ? Réponds vite, {0} secondes !": ["Yes or no? Answer fast, {0} seconds!", "Sì o no? Rispondi veloce, {0} secondi!"],
 "🔒 🪙 {0} ": ["🔒 🪙 {0}", "🔒 🪙 {0}"],
 "🎨 Décors des jeux": ["🎨 Game backgrounds", "🎨 Sfondi dei giochi"], "Océan": ["Ocean", "Oceano"], "Espace": ["Space", "Spazio"], "Bonbons": ["Sweets", "Caramelle"], "Forêt": ["Forest", "Foresta"],
 "🎁 Bonus": ["🎁 Bonuses", "🎁 Bonus"], "+{0} secondes": ["+{0} seconds", "+{0} secondi"], "Deuxième chance": ["Second chance", "Seconda possibilità"], "Indice": ["Hint", "Indizio"],
 "Course et Vrai ou faux": ["Race and True or false", "Corsa e Vero o falso"], "Memory et Les lettres": ["Memory and Letters", "Memory e Le lettere"],
 "🪙 {0} · {1}": ["🪙 {0} · {1}", "🪙 {0} · {1}"],
 "Les bonus aident pendant une partie. Ils n'ajoutent jamais de temps d'écran.": ["Bonuses help during a game. They never add screen time.", "I bonus aiutano durante una partita. Non aggiungono mai tempo di schermo."],
 "🛡️ Deuxième chance : {0}": ["🛡️ Second chance: {0}", "🛡️ Seconda possibilità: {0}"], "🛡️ Deuxième chance !": ["🛡️ Second chance!", "🛡️ Seconda possibilità!"],
 "💡 Indice ({0})": ["💡 Hint ({0})", "💡 Indizio ({0})"], "⏱️ +{0} s ({1})": ["⏱️ +{0} s ({1})", "⏱️ +{0} s ({1})"],
 "Mot {0} / {1}": ["Word {0} / {1}", "Parola {0} / {1}"], "⌫ Effacer": ["⌫ Delete", "⌫ Cancella"], "✅ Vrai ou faux": ["✅ True or false", "✅ Vero o falso"],
 "{0} mots écrits sur {1}": ["{0} words spelled out of {1}", "{0} parole scritte su {1}"], "{0} bonnes réponses en {1} secondes": ["{0} right answers in {1} seconds", "{0} risposte giuste in {1} secondi"],
 "Les autres univers se débloquent plus tard avec les pièces gagnées, dans la garde-robe.": ["The other worlds unlock later with the coins you earn, in the wardrobe.", "Gli altri mondi si sbloccano più tardi con le monete guadagnate, nel guardaroba."],
 "Voir les autres univers": ["See the other worlds", "Vedi gli altri mondi"],
 "Qui parle ?": ["Who is speaking?", "Chi parla?"], "👩 Femme": ["👩 Woman", "👩 Donna"], "👧 Fille": ["👧 Girl", "👧 Bambina"], "👨 Homme": ["👨 Man", "👨 Uomo"], "🧔 Homme grave": ["🧔 Deep male voice", "🧔 Uomo, voce grave"],
 "Les voix d'homme sont créées à partir de la voix choisie au-dessus, en plus grave. Si le téléphone propose une vraie voix d'homme (Android : Synthèse vocale Google → Espagnol → voix), elle apparaît dans la liste.": ["Male voices are made from the voice chosen above, made deeper. If the phone offers a real male voice (Android: Google text-to-speech → Spanish → voice), it appears in the list.", "Le voci maschili sono create dalla voce scelta sopra, resa più grave. Se il telefono offre una vera voce maschile (Android: Sintesi vocale Google → Spagnolo → voce), compare nell'elenco."],
}
UIADD.pop("🔒 🪙 {0} ")
addjs('const UI={', UIADD)
rep("const APP_VERSION=22,", "const APP_VERSION=23,")
rep("""  22:""", """  23:"Nouveau : une boutique avec plein d'accessoires, des skins, des univers, 2 nouveaux jeux, des décors et des bonus à gagner avec tes pièces !",
  22:""")
addjs('const UI={', {"Nouveau : une boutique avec plein d'accessoires, des skins, des univers, {0} nouveaux jeux, des décors et des bonus à gagner avec tes pièces ! Ta progression est gardée.":
  ["New: a shop full of accessories, skins, worlds, {0} new games, backgrounds and bonuses to win with your coins! Your progress is saved.", "Novità: un negozio pieno di accessori, skin, mondi, {0} nuovi giochi, sfondi e bonus da vincere con le tue monete! I tuoi progressi sono salvati."]})
open('index.html', 'w').write(p)
print('ok')
