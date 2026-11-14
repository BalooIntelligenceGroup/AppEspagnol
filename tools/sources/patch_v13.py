import re, sys
p = open('index.html').read()
fun = open('/home/claude/fun_v13.js').read()

def rep(old, new, count=1):
    global p
    n = p.count(old)
    if n != count:
        sys.exit(f'expected {count}, found {n}: {old[:110]}')
    p = p.replace(old, new)

def cut(start, end_marker, new):
    """remplace de start (inclus) jusqu'à end_marker (exclu)"""
    global p
    a = p.index(start); b = p.index(end_marker, a)
    p = p[:a] + new + p[b:]

# ---- version
rep("const APP_VERSION=12,NEW_IN={", "const APP_VERSION=13,NEW_IN={")
rep("""Toutes tes étoiles sont gardées."};""",
    """Toutes tes étoiles sont gardées.",
  13:"Nouveau : l'histoire de ton compagnon, l'album d'autocollants, 3 jeux, la garde-robe, les défis en famille et les comptines !"};""")

# ---- révision espacée : un mot n'avance qu'une fois par échéance ; date de première rencontre (rapport parent)
cut("function srs(w,ok){", "function wordMap(){",
"""function srs(w,ok){if(!w||!w.es)return;if(view==='lesson'&&L&&L.kind==='chat')return;S.words=S.words||{};const t=dayPlus(0);
  const r=S.words[w.es]||{b:0,d:t,ok:0,ko:0,f:t};if(!r.f)r.f=t;
  if(ok){r.ok++;if(r.d<=t){r.b=Math.min(r.b+1,6);r.d=dayPlus(IV[r.b])}}else{r.ko++;r.b=1;r.d=t}S.words[w.es]=r}
function seen(w){S.words=S.words||{};if(w&&w.es&&!S.words[w.es])S.words[w.es]={b:1,d:dayPlus(1),ok:0,ko:0,f:dayPlus(0)}}
""")
rep("""  if(!S.mig12){""", """  if(!S.mig13){for(const k in S.words){const r=S.words[k];if(r.b>=2&&r.ok<3)r.ok=3}S.coins=S.coins||0;S.mig13=1;if(S.name)save()}
  if(!S.mig12){""")
# les mots des niveaux déjà réussis comptent comme bien connus (autocollants dès la mise à jour)
rep("""S.words[x.es]={b:2,d:dayPlus(0),ok:1,ko:0}""", """S.words[x.es]={b:2,d:dayPlus(0),ok:3,ko:0}""")

# ---- toutes les activités notent l'album au départ (pour annoncer les nouveaux autocollants)
p = p.replace("t0:Date.now()};view='lesson'", "t0:Date.now(),stk0:stickerCount()};view='lesson'")
assert p.count("stk0:stickerCount()") == 5, p.count("stk0:stickerCount()")

# ---- accueil : compagnon habillé, pièces, temps restant, barre des activités ludiques
rep("""<button class="lola" data-act="who" aria-label="Changer de joueur">${G().e}</button>""",
    """<button class="lola" data-act="who" aria-label="Changer de joueur">${avatar()}</button>""")
rep("""<span class="chip">🏅 Niveau ${level()}</span></div>""",
    """<span class="chip">🪙 ${S.coins||0}</span>${S.limit>0?`<span class="chip">⏳ ${Math.max(0,S.limit-usedMin())} min</span>`:''}</div>""")
rep("""💬 Parler avec ${G().es}</button></div>""", """💬 Parler avec ${G().es}</button></div>
  <div class="funbar">
    <button class="fun" data-act="games"><span>🎮</span>Jeux</button>
    <button class="fun" data-act="story"><span>📖</span>Histoire</button>
    <button class="fun" data-act="album"><span>🏆</span>Album</button>
    <button class="fun" data-act="wardrobe"><span>👗</span>Garde-robe</button>
    <button class="fun" data-act="duel"><span>⚔️</span>Défi famille</button>
    <button class="fun" data-act="songs"><span>🎵</span>Comptines</button></div>""")

# ---- fin de leçon : pièces, points de la semaine, autocollants, épisode
rep("S.todayCount++;S.xp+=gain;", "S.todayCount++;addPts(gain);const coins=L.kind==='chat'?3:L.unit>=0?(5+(L.mistakes===0?3:0)):5;addCoins(coins);")
rep("save();R={stars,gain,newUnit,unit:L.unit,goalHit:S.todayCount===S.goal};",
    "save();R={stars,gain,newUnit,unit:L.unit,goalHit:S.todayCount===S.goal,coins,newStk:Math.max(0,stickerCount()-(L.stk0||0)),episode:newUnit&&L.unit>=0&&STORY[UNITS[L.unit].id]?L.unit:null};")
rep("S.xp+=20}", "addPts(20);addCoins(10)}")
rep("""    <div class="xp">+${R.gain} points</div>""",
    """    <div class="xp">+${R.gain} points · +${R.coins} 🪙</div>
    ${R.newStk?`<p class="say" style="color:var(--ink)">🆕 ${R.newStk} nouvel${R.newStk>1?'s':''} autocollant${R.newStk>1?'s':''} dans ton album !</p>`:''}""")
rep("""      ${R.newUnit&&next?`<button class="btn sun" data-act="unit" data-i="${R.unit+1}">Niveau suivant →</button>`:''}""",
    """      ${R.episode!=null?`<button class="btn coral" data-act="epopen" data-i="${R.episode}">📖 Nouvel épisode de l'histoire !</button>`:''}
      ${R.newUnit&&next&&unlocked(R.unit+1)?`<button class="btn sun" data-act="unit" data-i="${R.unit+1}">Niveau suivant →</button>`:''}""")

# ---- tout le côté ludique
rep("/* ---------- Dico, réglages, accueil ---------- */", fun + "\n/* ---------- Dico, réglages, accueil ---------- */")

# ---- accueil d'un joueur, avec retour à chaque étape
cut("/* Accueil d'un joueur", "/* Qui joue ? */", r"""/* Accueil d'un joueur : prénom → fille ou garçon → univers. Chaque étape a son bouton retour. */
let wStep=null,themeFrom='setup',prevTheme='';
function welcome(){
  const st=wStep||(!S.name?'name':!S.gender?'gender':'theme');
  if(st==='name'){app.innerHTML=`<div class="center">
    <div class="lola big" aria-hidden="true">👋</div>
    <h1 style="font-size:40px">¡Hola!</h1>
    <p class="say" style="font-size:19px">Chaque jour, on apprend l'espagnol en quelques minutes. ¿Cómo te llamas ?</p>
    <label class="field" for="nm" style="width:100%;text-align:left">Ton prénom<input id="nm" maxlength="20" autocomplete="off" placeholder="Écris ton prénom" value="${esc(S.name||'')}"></label>
    <button class="btn sun" data-act="go">Suivant →</button>
    ${P.list.length>1?'<button class="btn ghost" data-act="who">← Choisir un autre joueur</button>':''}</div>`;return}
  if(st==='gender'){app.innerHTML=`<div class="center">
    <h1 style="font-size:34px">¡Hola, ${esc(S.name)}!</h1>
    <p class="say" style="font-size:19px">Tu es…</p>
    <div class="row" style="width:100%"><button class="btn sun big2" data-act="gender" data-g="f">👧 Une fille</button><button class="btn big2" data-act="gender" data-g="m">👦 Un garçon</button></div>
    <p class="note">Pour dire « encantada » ou « encantado » 😉</p>
    <button class="btn ghost" data-act="wback">← Retour</button></div>`;return}
  const keys=allThemes?Object.keys(THEMES):THEME_FOR[S.gender||'f'];
  app.innerHTML=`<div class="center" style="justify-content:flex-start;padding-top:12px">
    <h1 style="font-size:32px">Choisis ton univers</h1>
    <p class="say">Ton compagnon t'accompagne dans toutes tes leçons.</p>
    <div class="themes">${keys.map(k=>{const t=THEMES[k];return `<button class="thcard ${S.theme===k?'on':''}" data-act="theme" data-t="${k}" style="--tb:${t.c.bg};--tl:${t.c.lagoon};--ts:${t.c.sun}">
      <span class="thmas">${t.e}</span><span class="thtxt"><b>${esc(t.name)}</b><small>avec ${esc(t.title)}</small><span class="thdeco">${t.deco}</span></span></button>`}).join('')}</div>
    <button class="btn ghost" data-act="allthemes">${allThemes?'Voir moins d\'univers':'Voir les 6 univers'}</button>
    <button class="btn ghost" data-act="wback">← Retour</button></div>`;
}
""")
rep("""    <h1 style="font-size:36px">¿Quién juega?</h1>""",
    """    ${S.name&&S.gender&&S.theme?'<div class="head" style="width:100%;margin:0"><button class="icon-btn" data-act="home" aria-label="Retour">←</button></div>':''}
    <h1 style="font-size:36px">¿Quién juega?</h1>""")
rep("""    return `<button class="pcard ${p.id===P.cur?'cur':''}" data-act="pick" data-id="${p.id}" style="--pc:${th.c.lagoon};--pb:${th.c.bg}"><span class="pav">${s.theme?th.e:'🙂'}</span><b>${esc(s.name||'Nouveau joueur')}</b><small>${n} niveau${n>1?'x':''} réussi${n>1?'s':''}</small></button>`}).join('');""",
    """    return `<button class="pcard ${p.id===P.cur?'cur':''}" data-act="pick" data-id="${p.id}" style="--pc:${th.c.lagoon};--pb:${th.c.bg}"><span class="pav">${s.theme?th.e:'🙂'}</span><b>${esc(s.name||'Nouveau joueur')}</b><small>${n} niveau${n>1?'x':''} réussi${n>1?'s':''} · ${weekPts(s)} pts</small></button>`}).join('');""")

# ---- espace parent : confidentialité, rapport de la semaine, minuteur
rep("""  <p class="note" style="margin-bottom:12px">Le temps compté est celui passé dans les leçons, séances et évaluations.</p>${cards}""",
    """  <div class="set" style="background:var(--good-bg)"><b>🔒 Sans publicité, sans collecte de données</b><p class="note" style="color:var(--ink)">Tout reste sur ce téléphone : aucun compte, aucune donnée envoyée. Le temps compté est celui passé dans les leçons, séances, évaluations et jeux.</p></div>${cards}""")
rep("""      <p class="note">Évaluations : ${ev.length?""",
    """      <p class="note" style="color:var(--ink)"><b>Cette semaine :</b> ${week} min, ${keys.filter(k=>ws[k].f&&ws[k].f>=dayPlus(-6)).length} mots nouveaux, ${keys.filter(k=>ws[k].ok>=3).length} autocollants au total, ${weekPts(s)} points.</p>
      <div class="toggle"><span>⏳ Limite par jour</span><span class="row" style="flex:none;gap:6px;flex-wrap:wrap;justify-content:flex-end">${[0,10,15,20,30].map(m=>`<button class="tool" style="min-width:44px;justify-content:center;padding:0 10px;${(s.limit||0)===m?'background:var(--sun)':''}" data-act="plim" data-id="${p.id}" data-m="${m}">${m?m+' min':'Aucune'}</button>`).join('')}</span></div>
      ${s.limit>0&&Math.round(((s.days||{})[dayPlus(0)]||0)/60)>=s.limit&&s.unlockDay!==dayPlus(0)?`<button class="tool" data-act="punlock" data-id="${p.id}" style="justify-content:center">🔓 Débloquer pour aujourd'hui</button>`:''}
      <p class="note">Évaluations : ${ev.length?""")

# ---- affichage des nouveaux écrans
rep("""  if(view==='who')who();else if(view==='pgate')parentGate();else if(view==='parent')parent();else""",
    """  if(view!=='game'&&GM&&GM.timer){clearInterval(GM.timer);GM.timer=null}
  if(view==='who')who();else if(view==='pgate')parentGate();else if(view==='parent')parent();else
  if(view==='stop')stop();else if(view==='album')album();else if(view==='wardrobe')wardrobe();else if(view==='story')story();else if(view==='episode')episode();else
  if(view==='songs')songs();else if(view==='song')songView();else if(view==='games')games();else if(view==='game')game();else if(view==='gameover')gameover();else
  if(view==='duel')duel();else if(view==='duel2')duel2();else""")

# ---- actions
rep("""  else if(a==='go'){readName();if(!S.name){$('#nm').focus();return}if(!S.ver)S.ver=APP_VERSION;save();render();say('¡Hola, '+S.name+'!')}
  else if(a==='gender'){S.gender=b.dataset.g;allThemes=false;save();render()}
  else if(a==='theme'){S.theme=b.dataset.t;if(!S.ver)S.ver=APP_VERSION;applyTheme();save();view='home';render();say('¡Hola, '+S.name+'! Soy '+G().es+'. ¡Vamos!')}""",
"""  else if(a==='go'){readName();if(!S.name){$('#nm').focus();return}if(!S.ver)S.ver=APP_VERSION;save();wStep='gender';themeFrom='setup';render();say('¡Hola, '+S.name+'!')}
  else if(a==='gender'){S.gender=b.dataset.g;allThemes=false;save();wStep='theme';render()}
  else if(a==='theme'){S.theme=b.dataset.t;if(!S.ver)S.ver=APP_VERSION;applyTheme();save();wStep=null;view='home';render();say('¡Hola, '+S.name+'! Soy '+G().es+'. ¡Vamos!')}
  else if(a==='wback'){const st=wStep||(!S.name?'name':!S.gender?'gender':'theme');
    if(st==='gender')wStep='name';
    else if(st==='theme'&&themeFrom==='settings'){S.theme=prevTheme;applyTheme();wStep=null;view='settings'}
    else if(st==='theme')wStep='gender';
    render()}""")
rep("""  else if(a==='chtheme'){readName();S.theme='';allThemes=true;view='welcome';render()}""",
    """  else if(a==='chtheme'){readName();prevTheme=S.theme;themeFrom='settings';wStep='theme';allThemes=true;view='welcome';render()}""")
rep("""  else if(a==='pick'){loadProfile(b.dataset.id);view=S.name&&S.gender&&S.theme?'home':'welcome';render()}
  else if(a==='addp'){save();const id='p'+Date.now().toString(36);P.list.push({id});loadProfile(id);view='welcome';render()}""",
"""  else if(a==='pick'){loadProfile(b.dataset.id);wStep=null;themeFrom='setup';view=S.name&&S.gender&&S.theme?'home':'welcome';render()}
  else if(a==='addp'){save();const id='p'+Date.now().toString(36);P.list.push({id});loadProfile(id);wStep='name';themeFrom='setup';view='welcome';render()}""")
rep("""  else if(a==='seance'){if(startSeance())speakStep()}
  else if(a==='seancemiss'){if(startSeance(R&&R.missed&&R.missed.length?R.missed:null))speakStep()}
  else if(a==='eval'){const t=+b.dataset.t;if(!stageDone(t)&&!S.evals[t]){say('¡Todavía no!');return}startEval(t);speakStep()}""",
"""  else if(a==='seance'){if(guard()&&startSeance())speakStep()}
  else if(a==='seancemiss'){if(guard()&&startSeance(R&&R.missed&&R.missed.length?R.missed:null))speakStep()}
  else if(a==='eval'){const t=+b.dataset.t;if(!stageDone(t)&&!S.evals[t]){say('¡Todavía no!');return}if(!guard())return;startEval(t);speakStep()}
  else if(a==='album'){view='album';render()}
  else if(a==='wardrobe'){shopMsg='';view='wardrobe';render()}
  else if(a==='acc'){const sl=b.dataset.slot,e=b.dataset.e,pr=+b.dataset.p;S.acc=S.acc||{};S.owned=S.owned||[];
    if(S.acc[sl]===e){S.acc[sl]='';shopMsg=''}
    else if(S.owned.includes(e)){S.acc[sl]=e;shopMsg=''}
    else if((S.coins||0)>=pr){S.coins-=pr;S.owned.push(e);S.acc[sl]=e;shopMsg='Acheté ! '+e;tone(true)}
    else shopMsg=`Il te manque ${pr-(S.coins||0)} pièces. Joue encore un peu !`;
    save();render()}
  else if(a==='accoff'){S.acc={};save();render()}
  else if(a==='story'){view='story';render()}
  else if(a==='epopen'){const i=+b.dataset.i;if(!S.stars[UNITS[i].id])return;epi={i,k:0};view='episode';render();say(fillG(STORY[UNITS[i].id].p[0][1]))}
  else if(a==='epnext'){const e=STORY[UNITS[epi.i].id];if(epi.k<e.p.length-1){epi.k++;render();say(fillG(e.p[epi.k][1]))}else{view='story';render()}}
  else if(a==='epprev'){if(epi.k>0){epi.k--;render();say(fillG(STORY[UNITS[epi.i].id].p[epi.k][1]))}}
  else if(a==='ephear')say(fillG(STORY[UNITS[epi.i].id].p[epi.k][1]));
  else if(a==='songs'){karaToken++;view='songs';render()}
  else if(a==='songopen'){const i=+b.dataset.i;if(!S.stars[SONGS[i].after])return;song={i,line:-1,mode:null};view='song';render()}
  else if(a==='karaplay')karaRun('play');
  else if(a==='karame')karaRun('repeat');
  else if(a==='games'){if(GM&&GM.timer)clearInterval(GM.timer);view='games';render()}
  else if(a==='game'){if(gamePool().length<4||!guard())return;startGame(b.dataset.g)}
  else if(a==='gsay'){GM&&GM.cur&&say(GM.cur.target.es)}
  else if(a==='gcatch')catchTap(+b.dataset.k);
  else if(a==='gmem')memTap(+b.dataset.k);
  else if(a==='gchr')chronoTap(+b.dataset.k);
  else if(a==='duel'){DU=DU&&DU.phase?{opp:DU.opp}:DU;view='duel';render()}
  else if(a==='dopp'){DU={opp:b.dataset.id};render()}
  else if(a==='dstart'){if(!guard())return;duelStart()}
  else if(a==='dgo'){DU.phase='q';DU.i=0;DU.t0=Date.now();render()}
  else if(a==='dans')duelAnswer(b.dataset.es);
  else if(a==='plim'){const m=+b.dataset.m;editProfile(b.dataset.id,s=>{s.limit=m});render()}
  else if(a==='punlock'){editProfile(b.dataset.id,s=>{s.unlockDay=dayPlus(0)});render()}""")
rep("""  else if(a==='unit'){const i=+b.dataset.i;if(!unlocked(i)){say('¡Todavía no!');return}startUnit(i);speakStep()}""",
    """  else if(a==='unit'){const i=+b.dataset.i;if(!unlocked(i)){say('¡Todavía no!');return}if(!guard())return;startUnit(i);speakStep()}""")
# toute autre action arrête la comptine en cours
rep("""  const b=e.target.closest('[data-act]');if(!b||b.disabled)return;const a=b.dataset.act;""",
    """  const b=e.target.closest('[data-act]');if(!b||b.disabled)return;const a=b.dataset.act;
  if(a!=='karaplay'&&a!=='karame')karaToken++;""")
# bulle ratée : elle touche le sol avant d'être attrapée
rep("""app.addEventListener('keydown',""", """app.addEventListener('animationend',e=>{
  const t=e.target;if(view!=='game'||!GM||GM.g!=='catch'||GM.lock||!t.dataset||t.dataset.act!=='gcatch')return;
  if(GM.cur.opts[+t.dataset.k].w!==GM.cur.target)return;
  GM.lock=true;tone(false);srs(GM.cur.target,false);render();setTimeout(nextCatch,900);
});
app.addEventListener('keydown',""")

# ---- styles
rep("""button.lola{border:0;cursor:pointer;padding:0}""", """button.lola{border:0;cursor:pointer;padding:0}
.ava{position:relative;display:inline-grid;place-items:center;line-height:1}
.ava-h{position:absolute;top:-.46em;left:50%;transform:translateX(-50%);font-size:.58em}
.ava-f{position:absolute;top:.2em;left:50%;transform:translateX(-50%);font-size:.42em}
.ava-x{position:absolute;right:-.42em;bottom:-.12em;font-size:.5em}
.lola.big .ava{font-size:70px}
.funbar{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:12px}
.fun{background:var(--card);border-radius:18px;box-shadow:0 4px 0 var(--line);padding:10px 4px;display:flex;flex-direction:column;align-items:center;gap:2px;font-weight:800;font-size:14px}
.fun span{font-size:30px;line-height:1.1}
.eplist{display:flex;flex-direction:column;gap:10px}
.epi{display:flex;align-items:center;gap:12px;background:var(--card);border-radius:18px;box-shadow:0 4px 0 var(--line);padding:12px 14px;text-align:left;font-size:20px}
.epi.lock{opacity:.55}
.epn{flex:none;width:46px;height:46px;border-radius:14px;background:var(--bg2);display:grid;place-items:center;font-family:var(--f-display);font-weight:800;font-size:22px}
.ept{flex:1;min-width:0;display:flex;flex-direction:column}
.ept b{font-family:var(--f-display);font-size:19px;line-height:1.15}
.ept small{font-size:14px;font-weight:700;color:var(--muted)}
.panel{background:var(--card);border-radius:26px;box-shadow:0 6px 0 var(--line);padding:24px 18px;display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center;margin:8px 0 14px}
.pscene{display:flex;align-items:center;justify-content:center;gap:14px;font-size:64px;line-height:1.1;flex-wrap:wrap}
.pscene .pg{font-size:56px}
.dots{display:flex;justify-content:center;gap:8px;margin-bottom:14px}
.dots i{width:10px;height:10px;border-radius:50%;background:var(--line)}
.dots i.on{background:var(--lagoon)}
.kara{background:var(--card);border-radius:22px;box-shadow:0 5px 0 var(--line);padding:16px 18px;display:flex;flex-direction:column;gap:4px;margin-bottom:8px}
.kl{margin:0;font-family:var(--f-display);font-weight:800;font-size:22px;line-height:1.3;color:var(--muted);transition:color .2s,transform .2s}
.kl.on{color:var(--lagoon-d);transform:scale(1.03);transform-origin:left}
.kl.me{color:var(--coral-d)}
.stk{display:grid;grid-template-columns:repeat(auto-fill,minmax(88px,1fr));gap:10px}
.sticker{aspect-ratio:1;border-radius:20px;background:var(--bg2);border:3px dashed var(--line);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;font-weight:800;color:var(--muted);max-width:100%}
.sticker span{font-size:34px;line-height:1}
.sticker.on{background:var(--card);border:3px solid var(--sun);box-shadow:0 4px 0 var(--sun-d);color:var(--ink);transform:rotate(-2deg)}
.sticker.on:nth-child(2n){transform:rotate(2deg)}
.sticker.on .swatch{width:38px;height:38px;border-radius:10px}
.sticker b{font-size:13px;text-align:center;line-height:1.1;padding:0 4px}
.shop{display:grid;grid-template-columns:repeat(auto-fill,minmax(100px,1fr));gap:10px}
.item{background:var(--card);border-radius:18px;border:3px solid transparent;box-shadow:0 4px 0 var(--line);padding:10px 6px;display:flex;flex-direction:column;align-items:center;gap:2px}
.item span{font-size:34px;line-height:1.1}
.item b{font-size:14px;line-height:1.15;text-align:center}
.item small{font-size:13px;font-weight:800;color:var(--muted)}
.item.on{border-color:var(--good);background:var(--good-bg)}
.item.poor{opacity:.6}
.ghead{display:flex;justify-content:space-between;font-weight:800;font-size:17px}
.sky{position:relative;height:430px;overflow:hidden;border-radius:24px;background:linear-gradient(var(--bg2),var(--card));margin-top:6px}
.bubble-f{position:absolute;top:-96px;width:88px;height:88px;border-radius:50%;background:var(--card);border:3px solid var(--line);box-shadow:0 4px 0 var(--line);display:grid;place-items:center;font-size:48px;animation-name:fall2;animation-timing-function:linear;animation-fill-mode:forwards}
.bubble-f .swatch{width:56px;height:56px;border-radius:50%}
.bubble-f.sel-good{border-color:var(--good);background:var(--good-bg)}
.bubble-f.sel-bad{border-color:var(--bad);background:var(--bad-bg)}
@keyframes fall2{from{top:-96px}to{top:calc(100% + 4px)}}
.mem{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:6px}
.mcard{aspect-ratio:1;border-radius:18px;background:var(--lagoon);box-shadow:0 5px 0 var(--lagoon-d);color:#fff;font-size:34px;display:grid;place-items:center;max-width:100%;padding:4px}
.mcard.up{background:var(--card);color:var(--ink);box-shadow:0 5px 0 var(--line);font-size:44px}
.mcard.up b{font-size:16px;line-height:1.15;overflow-wrap:anywhere}
.mcard.ok{background:var(--good-bg);box-shadow:0 5px 0 var(--good)}
.mcard .swatch{width:60%;height:60%;border-radius:12px}
.rank{display:flex;align-items:center;gap:10px;font-size:17px}
.rank .re{font-size:26px}
.rank b{flex:1;min-width:0}
.rank .rp{font-weight:800;color:var(--muted);font-variant-numeric:tabular-nums}""")
open('index.html', 'w').write(p)
print('ok')
