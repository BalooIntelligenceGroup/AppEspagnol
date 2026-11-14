import sys, json, re
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
    """ajoute des entrées au début d'un littéral objet JSON (UI, TRX)"""
    add = ''.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False) + ',' for k, v in entries.items())
    rep(obj_start, obj_start + add)

# ======================= 1. 10 mots par leçon =======================
# es, fr, emoji (💬 = mot abstrait, affiché en texte), en, it
MORE = {
 'saludos': [['buenas tardes','bon après-midi','🌇','good afternoon','buon pomeriggio'],['hasta luego','à plus tard','💬','see you later','a più tardi'],['de nada','de rien','💬',"you're welcome",'prego'],['perdón','pardon','💬','sorry','scusa']],
 'colores': [['blanco','blanc','#FAFAFA','white','bianco'],['naranja','orange','#FB8C00','orange','arancione'],['morado','violet','#8E24AA','purple','viola'],['marrón','marron','#6D4C41','brown','marrone']],
 'numeros': [['siete','sept','7️⃣','seven','sette'],['ocho','huit','8️⃣','eight','otto'],['nueve','neuf','9️⃣','nine','nove'],['diez','dix','🔟','ten','dieci']],
 'mascotas': [['el hámster','le hamster','🐹','the hamster','il criceto'],['el caballo','le cheval','🐴','the horse','il cavallo'],['el ratón','la souris','🐭','the mouse','il topo'],['el loro','le perroquet','🦜','the parrot','il pappagallo']],
 'familia': [['el bebé','le bébé','👶','the baby','il bebè'],['el tío',"l'oncle",'🧔','the uncle','lo zio'],['la tía','la tante','👱‍♀️','the aunt','la zia'],['el primo','le cousin','🧒','the cousin','il cugino']],
 'frutas': [['la piña',"l'ananas",'🍍','the pineapple',"l'ananas"],['el limón','le citron','🍋','the lemon','il limone'],['la cereza','la cerise','🍒','the cherry','la ciliegia'],['el melocotón','la pêche','🍑','the peach','la pesca']],
 'comida': [['el huevo',"l'œuf",'🥚','the egg',"l'uovo"],['el arroz','le riz','🍚','the rice','il riso'],['la pizza','la pizza','🍕','the pizza','la pizza'],['la sopa','la soupe','🍲','the soup','la zuppa']],
 'ropa': [['la bufanda',"l'écharpe",'🧣','the scarf','la sciarpa'],['los calcetines','les chaussettes','🧦','the socks','i calzini'],['los guantes','les gants','🧤','the gloves','i guanti'],['el sombrero','le chapeau','👒','the hat','il cappello']],
 'casa': [['la cocina','la cuisine','🍳','the kitchen','la cucina'],['el sofá','le canapé','🛋️','the sofa','il divano'],['la lámpara','la lampe','💡','the lamp','la lampada'],['el jardín','le jardin','🌳','the garden','il giardino']],
 'escuela': [['el cuaderno','le cahier','📓','the exercise book','il quaderno'],['el ordenador',"l'ordinateur",'💻','the computer','il computer'],['los lápices de colores','les crayons de couleur','🖍️','the colouring pencils','le matite colorate'],['la clase','la classe','🏫','the classroom','la classe']],
 'presentarse': [['hablo francés','je parle français','🗣️','I speak French','parlo francese'],['hablo un poco de español',"je parle un peu espagnol",'🤏','I speak a little Spanish',"parlo un po' di spagnolo"],['mi cumpleaños','mon anniversaire','🎁','my birthday','il mio compleanno'],['tengo un perro',"j'ai un chien",'🐕','I have a dog','ho un cane']],
 'estas': [['estoy contenta','je suis contente','😄',"I'm happy",'sono contenta'],['estoy enfadada','je suis fâchée','😠',"I'm angry",'sono arrabbiata'],['tengo frío',"j'ai froid",'🥶',"I'm cold",'ho freddo'],['tengo calor',"j'ai chaud",'🥵',"I'm hot",'ho caldo']],
 'gustos': [['me gusta jugar',"j'aime jouer",'⚽','I like playing','mi piace giocare'],['me gusta leer',"j'aime lire",'📚','I like reading','mi piace leggere'],['me gusta bailar',"j'aime danser",'💃','I like dancing','mi piace ballare'],['¡qué asco!','beurk !','🤢','yuck!','che schifo!']],
 'preguntas': [['¿por qué?','pourquoi ?','💬','why?','perché?'],['¿cuándo?','quand ?','📅','when?','quando?'],['¿cómo?','comment ?','💬','how?','come?'],['¿qué hora es?','quelle heure est-il ?','🕒','what time is it?','che ore sono?']],
 'ayuda': [['no sé','je ne sais pas','🤷',"I don't know",'non lo so'],['¿me ayudas?',"tu m'aides ?",'💬','can you help me?','mi aiuti?'],['¿cómo se dice?','comment on dit ?','💬','how do you say it?','come si dice?'],['tengo una pregunta',"j'ai une question",'✋','I have a question','ho una domanda']],
}
# les mots retirés en version 12 reviennent (traductions anglais / italien)
BACK = {'por favor':['please','per favore'],'negro':['black','nero'],'seis':['six','sei'],'el pájaro':['the bird',"l'uccello"],'el abuelo':['the grandfather','il nonno'],
 'la pera':['the pear','la pera'],'la manzana':['the apple','la mela'],'el gorro':['the woolly hat','il berretto di lana'],'el baño':['the bathroom','il bagno'],'las tijeras':['the scissors','le forbici'],
 '¿y tú?':['and you?','e tu?'],'estoy triste':["I'm sad",'sono triste'],'¿te gusta?':['do you like it?','ti piace?'],'¿cuántos hay?':['how many are there?','quanti ce ne sono?'],'¿puedo jugar?':['can I play?','posso giocare?']}
more_js = json.dumps({k: [w[:3] for w in v] for k, v in MORE.items()}, ensure_ascii=False, separators=(',', ':'))
rep("UNITS.forEach((u,k)=>{u.tier=1+Math.floor(k/5);if(DROP[u.id])u.words=u.words.filter(w=>w[0]!==DROP[u.id])});",
    """/* Version 22 : 10 mots par leçon. Les mots retirés en version 12 (DROP) reviennent, et 4 nouveaux mots par leçon (MORE). */
const MORE=""" + more_js + """;
UNITS.forEach((u,k)=>{u.tier=1+Math.floor(k/5);(MORE[u.id]||[]).forEach(w=>{if(!u.words.some(x=>x[0]===w[0]))u.words.push(w)})});""")
rep("fr:'Compter de 1 à 6'", "fr:'Compter de 1 à 10'")
rep('"Los números":["Counting from 1 to 6","Contare da 1 a 6"]', '"Los números":["Counting from 1 to 10","Contare da 1 a 10"]')
trx = {w[0]: [w[3], w[4]] for v in MORE.values() for w in v}
trx.update(BACK)
addjs('const TRX={', trx)
rep("const ABSTRACT=new Set(['hola',", "const ABSTRACT=new Set(['hasta luego','de nada','perdón','¿y tú?','¿te gusta?','¿por qué?','¿cómo?','¿me ayudas?','¿cómo se dice?','hola',")
rep("['stanca','stanco']];", "['stanca','stanco'],['arrabbiata','arrabbiato']];")
# leçon : découverte des mots jamais vus (même dans une leçon déjà réussie), 2 exercices d'association
rep("""  if(!S.stars[u.id])words.forEach(w=>learn.push({t:'learn',w,conv:phr}));
  steps.push(matchStep(words));
  shuffle(words.slice()).slice(0,4).forEach(w=>steps.push({t:kindFor(w,phr),w,opts:optsFor(w,words)}));
  if(!u.conv)tfSteps(words,2).forEach(s=>steps.push(s));""",
"""  words.filter(w=>!S.stars[u.id]||!(S.words||{})[w.es]).forEach(w=>learn.push({t:'learn',w,conv:phr}));
  steps.push(matchStep(words.slice(0,5)));if(words.length>6)steps.push(matchStep(words.slice(5)));
  shuffle(words.slice()).slice(0,5).forEach(w=>steps.push({t:kindFor(w,phr),w,opts:optsFor(w,words)}));
  if(!u.conv)tfSteps(words,3).forEach(s=>steps.push(s));""")

# ======================= 2. Choix du temps d'écran après le didacticiel =======================
rep("const FREE=new Set(['stop','pgate','parent','who','welcome','tuto']);", "const FREE=new Set(['stop','pgate','parent','who','welcome','tuto','tsetup']);")
rep("""  else if(a==='tutoend'){S.tuto=1;save();view=tutoFrom;tutoFrom='home';render()}""",
    """  else if(a==='tutoend'){const first=!S.tuto;S.tuto=1;save();view=first&&tutoFrom==='home'?'tsetup':tutoFrom;tutoFrom='home';render()}
  else if(a==='tsetok'){const inp=document.getElementById('plim-'+P.cur),m=Math.round(+(inp&&inp.value));if(inp&&inp.value&&m>=1&&m<=300){S.limit=m;delete S.unlockDay;delete S.extra}
    S.tsetup=1;save();view='home';render()}""")
rep("else if(view==='tuto')tuto();else home();", "else if(view==='tuto')tuto();else if(view==='tsetup')tsetup();else home();")

# ======================= 3. « ¿Quién juega? » quand le temps est écoulé =======================
rep("""${anyOver()?'<p class="note" style="color:var(--ink);font-weight:800">🔒 Le temps d\\'écran est écoulé aujourd\\'hui : un parent doit choisir le joueur.</p>':''}""",
    """${anyOver()?'<div class="set" style="width:100%;text-align:center;align-items:center;border:3px solid var(--sun)"><b style="font-size:20px">⏰ Temps de jeu terminé pour aujourd\\'hui !</b><p class="note" style="margin:0;color:var(--ink)">Demande à tes parents un peu plus de temps, ou reviens demain. Pour changer de joueur, un parent doit répondre à la question.</p></div>':''}""")
rep("""· ${weekPts(s)} pts</small></button>`""", """· ${weekPts(s)} pts</small>${isOver(s)?'<small class="over">⏰ Terminé pour aujourd\\'hui</small>':''}</button>`""")

# ======================= 4. Espace parent en accordéon =======================
PARENT = r"""/* Espace parent : un accordéon par enfant (Progrès / Réglages), l'enfant en cours ouvert */
let popen=null;
function limitBox(s,id){const cu=s.limit>0&&![10,15,20,30].includes(s.limit);
  return `<div class="limit"><b>⏳ Temps d'écran maximum par jour</b>
    <div class="seg">${[0,10,15,20,30].map(m=>`<button class="${(s.limit||0)===m?'on':''}" data-act="plim" data-id="${id}" data-m="${m}" aria-pressed="${(s.limit||0)===m}">${m?`${m}<small>min</small>`:'Sans<small>limite</small>'}</button>`).join('')}</div>
    <div class="custom ${cu?'on':''}"><label for="plim-${id}">Personnalisé</label><input id="plim-${id}" type="number" inputmode="numeric" min="1" max="300" step="1" placeholder="45" value="${cu?s.limit:''}"><span>min</span><button class="tool" data-act="plimc" data-id="${id}">Valider</button></div>
    <p class="note">Choisissez entre 1 et 300 minutes, puis Valider.</p></div>`}
const PROMISE=`<div class="set promise"><b>🌱 Notre engagement</b><p class="note" style="color:var(--ink);margin:0">Cette appli aide votre enfant à découvrir l'espagnol et à progresser un peu chaque jour, en s'amusant. Elle ne promet pas de le rendre bilingue : elle l'accompagne, à son rythme, quelques minutes par jour.</p></div>`;
function parent(){
  if(!popen)popen=new Set([P.cur]);
  const WM=wordMap(),days=[6,5,4,3,2,1,0].map(n=>dayPlus(-n)),DN=({en:['S','M','T','W','T','F','S'],it:['D','L','M','M','G','V','S']})[S.lang]||['D','L','M','M','J','V','S'];
  const cards=P.list.map(p=>{const s=profileInfo(p.id),th=THEMES[s.theme]||THEMES.jungla,ws=s.words||{},keys=Object.keys(ws);
    const mins=days.map(d=>Math.round(((s.days||{})[d]||0)/60)),maxm=Math.max(10,...mins),week=mins.reduce((a,b)=>a+b,0);
    const hard=keys.filter(k=>ws[k].ko>0).sort((a,b)=>(ws[b].ko-ws[b].ok)-(ws[a].ko-ws[a].ok)).slice(0,6);
    const ev=[1,2,3].map(t=>(s.evals||{})[t]?`Niveau ${t} : ${(s.evals||{})[t].pct} %`:null).filter(Boolean);
    const nl=Object.keys(s.stars||{}).filter(id=>UNITS.some(u=>u.id===id)).length,todayMin=Math.floor(((s.days||{})[dayPlus(0)]||0)/60);
    return `<details class="acc" data-id="${p.id}" ${popen.has(p.id)?'open':''}><summary>
      <span class="pav" style="flex:none;background:${th.c.bg}">${s.theme?th.e:'🙂'}</span>
      <span class="acc-t"><b>${esc(s.name||'Nouveau joueur')}</b><small>${s.limit>0?`${todayMin} min aujourd'hui / ${s.limit+extraMin(s)} min`:`${todayMin} min aujourd'hui`}</small><small>Leçons : ${nl}/${UNITS.length}</small></span>${isOver(s)?'<span class="over">⏰</span>':''}<span class="chev" aria-hidden="true">▾</span></summary>
      <div class="acc-b">
      <h3 class="acc-h">📈 Progrès</h3>
      <div class="stats"><div><b>${keys.length}</b><small>mots vus</small></div><div><b>${keys.filter(k=>ws[k].b>=4).length}</b><small>mots bien retenus</small></div><div><b>${nl}/${UNITS.length}</b><small>leçons réussies</small></div><div><b>${week} min</b><small>cette semaine</small></div></div>
      <div class="bars" role="img" aria-label="Minutes par jour sur 7 jours">${mins.map((m,i)=>`<div class="barc"><span class="bv">${m||''}</span><i style="height:${Math.round(m/maxm*70)}px"></i><small>${DN[new Date(days[i]+'T12:00').getDay()]}</small></div>`).join('')}</div>
      <p class="note" style="color:var(--ink)"><b>Cette semaine :</b> ${week} min, ${keys.filter(k=>ws[k].f&&ws[k].f>=dayPlus(-6)).length} mots nouveaux, ${keys.filter(k=>ws[k].ok>=3).length} autocollants au total, ${weekPts(s)} points.</p>
      <p class="note">Évaluations : ${ev.length?ev.join(' · '):'aucune réussie pour l\'instant'} · Série : ${s.streak||0} jour(s)</p>
      <p class="note">Mots difficiles : ${hard.length?hard.map(k=>`<b>${esc(k)}</b>${WM[k]?' ('+esc(WM[k].fr)+')':''}`).join(', '):'aucun pour l\'instant'}</p>
      <p class="note"><b>Mot bien retenu</b> : un mot réussi lors de 3 révisions espacées (1 jour, puis 2, puis 4 jours plus tard). Il est en mémoire depuis au moins une semaine. Un mot raté redescend et revient dans la Séance du jour.</p>
      <h3 class="acc-h">⚙️ Réglages</h3>
      ${limitBox(s,p.id)}
      <p class="note">${s.limit>0?`Aujourd'hui : ${todayMin} min sur ${s.limit+extraMin(s)} min.${s.unlockDay===dayPlus(0)?' Débloqué pour aujourd\'hui.':''} Quand le temps est écoulé, l'appli se bloque et demande un parent.`:'Aucune limite : l\'enfant peut jouer autant qu\'il veut.'}</p>
      ${isOver(s)?`<div class="row" style="gap:8px"><button class="tool" data-act="pextra" data-id="${p.id}" style="flex:1;justify-content:center">➕ 15 min aujourd'hui</button><button class="tool" data-act="punlock" data-id="${p.id}" style="flex:1;justify-content:center">🔓 Sans limite aujourd'hui</button></div>`:''}
      <div class="limit"><b>🌍 Langue de l'appli</b>
        <div class="seg three">${Object.entries(LANGS).map(([k,[n,f]])=>`<button class="${(s.lang||'fr')===k?'on':''}" data-act="plang" data-id="${p.id}" data-l="${k}" aria-pressed="${(s.lang||'fr')===k}">${f}<small>${n}</small></button>`).join('')}</div>
        <p class="note">L'appli et les traductions des mots et des phrases s'affichent dans cette langue. L'espagnol reste en espagnol.</p></div>
      <div class="limit"><b>💬 Bouton « Traduire » sur les questions</b>
        <div class="seg two">${[[0,'Non'],[1,'Oui']].map(([v,t])=>`<button class="${!!s.trQ===!!v?'on':''}" data-act="ptr" data-id="${p.id}" data-v="${v}" aria-pressed="${!!s.trQ===!!v}">${t}</button>`).join('')}</div>
        <p class="note">Utile si vous ne parlez pas espagnol. La traduction s'affiche toujours après la réponse ; le bouton n'apparaît jamais pendant les évaluations.</p></div>
      ${pdel===p.id?`<p style="margin:0;font-weight:800">Supprimer le profil de ${esc(s.name||'ce joueur')} et toute sa progression ?</p><div class="row"><button class="btn coral" data-act="pdelyes" data-id="${p.id}">Oui, supprimer</button><button class="btn ghost" data-act="pdelno">Non</button></div>`
        :`<button class="tool" data-act="pdel" data-id="${p.id}" style="justify-content:center">Supprimer ce profil</button>`}
      </div></details>`}).join('');
  app.innerHTML=`<div class="head"><button class="icon-btn" data-act="settings" aria-label="Retour">←</button><h2>Espace parent</h2></div>
  ${PROMISE}
  <div class="set" style="background:var(--good-bg)"><b>🔒 Sans publicité, sans collecte de données</b><p class="note" style="color:var(--ink)">Tout reste sur ce téléphone : aucun compte, aucune donnée envoyée. Le temps compté est le temps passé à jouer dans l'appli (hors réglages et espace parent).</p></div>
  <div class="accs">${cards}</div>
  ${P.list.length<6?'<button class="btn ghost" data-act="addp">➕ Ajouter un enfant</button>':''}`;
}
/* Choix du temps d'écran, juste après le didacticiel d'un nouveau profil */
function tsetup(){
  app.innerHTML=`<div class="head"><h2 style="flex:1">Pour les parents</h2></div>
  <div class="panel" style="align-items:stretch;text-align:left"><div style="text-align:center;font-size:64px;line-height:1.1">⏳</div><h2 style="margin:0;text-align:center">Combien de temps par jour ?</h2>
  <p class="say" style="margin:0">Choisissez le temps d'écran de ${esc(S.name)}. Conseillé : 10 minutes par jour, c'est suffisant pour progresser. Vous pourrez le changer dans l'espace parent.</p>
  ${limitBox(S,P.cur)}</div>${PROMISE}
  <button class="btn sun" data-act="tsetok">Valider et commencer</button>`;
}
app.addEventListener('toggle',e=>{const d=e.target;if(d&&d.matches&&d.matches('details.acc')&&popen){d.open?popen.add(d.dataset.id):popen.delete(d.dataset.id)}},true);

"""
cut("function parent(){", "\nlet lastView=null", PARENT)
rep("""  else if(a==='parent'){readName();gateNext=null;gateQ=null;""", """  else if(a==='parent'){readName();gateNext=null;popen=null;gateQ=null;""")

# ======================= 5. Choix de la voix espagnole =======================
rep("function pickVoice(){try{const v=speechSynthesis.getVoices();esVoice=v.find(x=>/^es[-_]ES/i.test(x.lang))||v.find(x=>/^es/i.test(x.lang))||null}catch(e){}}",
    """function pickVoice(){let want=null;try{want=S.voice}catch(e){}
  try{const v=speechSynthesis.getVoices();esVoice=(want&&v.find(x=>x.voiceURI===want))||v.find(x=>/^es[-_]ES/i.test(x.lang))||v.find(x=>/^es/i.test(x.lang))||null}catch(e){}}
/* Voix espagnoles installées sur le téléphone (Espagne, Mexique, États-Unis…) ; le ton donne encore plus de choix */
const VREG={ES:['🇪🇸','Espagne'],MX:['🇲🇽','Mexique'],US:['🇺🇸','États-Unis'],AR:['🇦🇷','Argentine'],CO:['🇨🇴','Colombie'],CL:['🇨🇱','Chili'],PE:['🇵🇪','Pérou'],'419':['🌎','Amérique latine']};
function esVoices(){try{return speechSynthesis.getVoices().filter(v=>/^es/i.test(v.lang))}catch(e){return []}}
const PITCH={n:1.1,h:1.45,l:.78};""")
rep("if('speechSynthesis' in window){pickVoice();speechSynthesis.onvoiceschanged=pickVoice}",
    "if('speechSynthesis' in window){pickVoice();speechSynthesis.onvoiceschanged=()=>{pickVoice();try{if(view==='settings')render()}catch(e){}}}")
rep("u.rate=slow?0.55:(S.slow?0.7:0.88);u.pitch=1.1;", "u.rate=slow?0.55:(S.slow?0.7:0.88);u.pitch=PITCH[S.pitch]||1.1;")
rep("""    <button class="tool" data-act="test" style="justify-content:center">🔊 Tester la voix espagnole</button>
    <p class="note">${esVoice?`Voix utilisée : ${esc(esVoice.name)}`:'Si la voix a un accent français, installe une voix espagnole dans les réglages Android (Synthèse vocale Google → Espagnol).'}</p>""",
    """    <div class="limit"><b>🗣️ Voix espagnole</b>
      ${(()=>{const vs=esVoices(),cnt={};if(!vs.length)return '<p class="note">Aucune voix espagnole trouvée sur ce téléphone. Installe-la dans les réglages Android (Synthèse vocale Google → Espagnol).</p>';
        return '<div class="voices">'+vs.map(v=>{const r=(v.lang.split(/[-_]/)[1]||'').toUpperCase(),g=VREG[r]||['🌎','Espagnol'];cnt[g[1]]=(cnt[g[1]]||0)+1;
          return `<button class="vbtn ${esVoice&&esVoice.voiceURI===v.voiceURI?'on':''}" data-act="voice" data-v="${esc(v.voiceURI)}"><span class="vf">${g[0]}</span><span class="vt"><b>${g[1]} · ${cnt[g[1]]}</b><small>${esc(v.name)}</small></span></button>`}).join('')+'</div>'})()}
      <b>Ton de la voix</b>
      <div class="seg three">${[['n','Normal'],['h','Aigu'],['l','Grave']].map(([k,t])=>`<button class="${(S.pitch||'n')===k?'on':''}" data-act="vpitch" data-p="${k}" aria-pressed="${(S.pitch||'n')===k}">${t}</button>`).join('')}</div>
      <button class="tool" data-act="test" style="justify-content:center">🔊 Tester la voix espagnole</button>
      <p class="note">Les voix disponibles dépendent du téléphone. Pour en ajouter : réglages Android → Synthèse vocale Google → Espagnol → installer d'autres voix.</p></div>""")
rep("""  else if(a==='plang'){""", """  else if(a==='voice'){S.voice=b.dataset.v;pickVoice();save();render();say('¡Hola! Soy '+G().es+'.')}
  else if(a==='vpitch'){S.pitch=b.dataset.p;save();render();say('¡Hola! Soy '+G().es+'.')}
  else if(a==='plang'){""")

# ======================= 6. Didacticiel : notre engagement =======================
rep("""  {b:'⚙️',h:'Pour les parents'""", """  {b:'🌱',h:'Notre engagement',t:`Cette appli aide votre enfant à découvrir l'espagnol et à progresser un peu chaque jour, en s'amusant. Elle ne promet pas de le rendre bilingue : elle l'accompagne, à son rythme, quelques minutes par jour.`},
  {b:'⚙️',h:'Pour les parents'""")
rep("""<h2 style="flex:1">${k===sl.length-1?'Pour les parents':'Bienvenue !'}</h2>""", """<h2 style="flex:1">${k>=sl.length-2?'Pour les parents':'Bienvenue !'}</h2>""")

# ======================= styles =======================
rep(".hint-bubble{", """.accs{display:flex;flex-direction:column;gap:12px;margin-bottom:12px}
details.acc{background:var(--card);border-radius:22px;box-shadow:0 5px 0 var(--line);overflow:hidden}
details.acc summary{list-style:none;display:flex;align-items:center;gap:12px;padding:12px 14px;cursor:pointer;min-height:64px}
details.acc summary::-webkit-details-marker{display:none}
.acc-t{flex:1;min-width:0;display:flex;flex-direction:column}
.acc-t b{font-size:20px;font-family:var(--f-display)}
.acc-t small{font-size:14px;font-weight:700;color:var(--muted)}
.chev{font-size:22px;color:var(--muted);transition:transform .2s}
details.acc[open] .chev{transform:rotate(180deg)}
.acc .over,.pcard .over{font-size:13px;font-weight:800;color:var(--coral-d)}
.acc-b{padding:0 14px 16px;display:flex;flex-direction:column;gap:10px;border-top:2px solid var(--line)}
.acc-h{margin:12px 0 0;font-family:var(--f-display);font-size:18px}
.promise{border:3px solid var(--good)}
.voices{display:grid;gap:8px}
.vbtn{display:flex;align-items:center;gap:10px;background:var(--bg2);border-radius:14px;padding:8px 12px;text-align:left;box-shadow:0 3px 0 var(--line);min-height:52px}
.vbtn.on{background:var(--sun);box-shadow:0 3px 0 var(--sun-d)}
.vf{font-size:26px}
.vt{display:flex;flex-direction:column;min-width:0}
.vt small{font-size:12px;color:var(--muted);overflow-wrap:anywhere}
.hint-bubble{""")

# ======================= traductions de l'interface =======================
NEW22 = "Nouveau : 10 mots par leçon, ta Séance du jour puis une nouvelle leçon chaque jour, et de nouvelles voix à choisir !"
rep('''  22:"Nouveau : chaque jour, ta Séance du jour, puis une nouvelle leçon. Dix minutes par jour, c'est parfait !"};''',
    '  22:' + json.dumps(NEW22, ensure_ascii=False) + '};')
UIADD = {
 NEW22 + " Ta progression est gardée.": ["New: 10 words per lesson, your Today's practice then a new lesson every day, and new voices to choose from! Your progress is saved.", "Novità: 10 parole per lezione, il Ripasso del giorno poi una nuova lezione ogni giorno, e nuove voci da scegliere! I tuoi progressi sono salvati."],
 "⏰ Temps de jeu terminé pour aujourd'hui !": ["⏰ Playtime is over for today!", "⏰ Il tempo di gioco per oggi è finito!"],
 "Demande à tes parents un peu plus de temps, ou reviens demain. Pour changer de joueur, un parent doit répondre à la question.": ["Ask your parents for a little more time, or come back tomorrow. To switch player, a parent must answer the question.", "Chiedi ai tuoi genitori un po' più di tempo, o torna domani. Per cambiare giocatore, un genitore deve rispondere alla domanda."],
 "⏰ Terminé pour aujourd'hui": ["⏰ Done for today", "⏰ Finito per oggi"],
 "{0} min aujourd'hui / {1} min": ["{0} min today / {1} min", "{0} min oggi / {1} min"],
 "{0} min aujourd'hui": ["{0} min today", "{0} min oggi"],
 "Leçons : {0}/{1}": ["Lessons: {0}/{1}", "Lezioni: {0}/{1}"],
 "📈 Progrès": ["📈 Progress", "📈 Progressi"],
 "⚙️ Réglages": ["⚙️ Settings", "⚙️ Impostazioni"],
 "🌱 Notre engagement": ["🌱 Our commitment", "🌱 Il nostro impegno"],
 "Notre engagement": ["Our commitment", "Il nostro impegno"],
 "Cette appli aide votre enfant à découvrir l'espagnol et à progresser un peu chaque jour, en s'amusant. Elle ne promet pas de le rendre bilingue : elle l'accompagne, à son rythme, quelques minutes par jour.": ["This app helps your child discover Spanish and make a little progress every day, while having fun. It doesn't promise to make them bilingual: it supports them, at their own pace, a few minutes a day.", "Questa app aiuta vostro figlio a scoprire lo spagnolo e a progredire un po' ogni giorno, divertendosi. Non promette di renderlo bilingue: lo accompagna, al suo ritmo, pochi minuti al giorno."],
 "Combien de temps par jour ?": ["How much time per day?", "Quanto tempo al giorno?"],
 "Choisissez le temps d'écran de {0}. Conseillé : {1} minutes par jour, c'est suffisant pour progresser. Vous pourrez le changer dans l'espace parent.": ["Choose {0}'s screen time. Recommended: {1} minutes a day, enough to make progress. You can change it in the parents' area.", "Scegliete il tempo di schermo di {0}. Consigliato: {1} minuti al giorno, bastano per progredire. Potrete cambiarlo nell'area genitori."],
 "Valider et commencer": ["Confirm and start", "Conferma e inizia"],
 "🗣️ Voix espagnole": ["🗣️ Spanish voice", "🗣️ Voce spagnola"],
 "Ton de la voix": ["Voice pitch", "Tono della voce"],
 "Normal": ["Normal", "Normale"], "Aigu": ["High", "Acuto"], "Grave": ["Low", "Grave"],
 "Espagne · {0}": ["Spain · {0}", "Spagna · {0}"], "Mexique · {0}": ["Mexico · {0}", "Messico · {0}"], "États-Unis · {0}": ["United States · {0}", "Stati Uniti · {0}"],
 "Argentine · {0}": ["Argentina · {0}", "Argentina · {0}"], "Colombie · {0}": ["Colombia · {0}", "Colombia · {0}"], "Chili · {0}": ["Chile · {0}", "Cile · {0}"],
 "Pérou · {0}": ["Peru · {0}", "Perù · {0}"], "Amérique latine · {0}": ["Latin America · {0}", "America Latina · {0}"], "Espagnol · {0}": ["Spanish · {0}", "Spagnolo · {0}"],
 "Aucune voix espagnole trouvée sur ce téléphone. Installe-la dans les réglages Android (Synthèse vocale Google → Espagnol).": ["No Spanish voice found on this phone. Install one in the Android settings (Google text-to-speech → Spanish).", "Nessuna voce spagnola trovata su questo telefono. Installala nelle impostazioni Android (Sintesi vocale Google → Spagnolo)."],
 "Les voix disponibles dépendent du téléphone. Pour en ajouter : réglages Android → Synthèse vocale Google → Espagnol → installer d'autres voix.": ["Available voices depend on the phone. To add more: Android settings → Google text-to-speech → Spanish → install other voices.", "Le voci disponibili dipendono dal telefono. Per aggiungerne: impostazioni Android → Sintesi vocale Google → Spagnolo → installa altre voci."],
}
addjs('const UI={', UIADD)
open('index.html', 'w').write(p)
print('ok')
