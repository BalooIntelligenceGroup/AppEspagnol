# v31 (1re demande) : traduction orale et écrite avec des mots découpés (dans les leçons de phrases + atelier « Traduction »)
import json
P='/home/claude/appespagnol/index.html'
s=open(P,encoding='utf8').read()
J=lambda x:json.dumps(x,ensure_ascii=False)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]);s=s.replace(a,b,1)
UIADD={}
def ui(fr,en,it):UIADD[fr]=[en,it]
# 1. création des exercices : mode 'oral' (écoute → traduction) et 'read' (lis → traduction) avec les mots du sens découpés
rep("""function startUnit(i,uo){""","""/* v31 : traduire VERS la langue de l'enfant avec des mots découpés : 'oral' = on entend la phrase sans la voir, 'read' = on la lit */
function trBuild(x,mode,pool){const m=fill(tr(x.s)||'');const ws=tilesOf(m);if(ws.length<2||ws.length>9)return null;const wn=ws.map(nw);
  const extra=shuffle((pool||[]).flatMap(y=>y===x.s?[]:tilesOf(tr(y)||'')).filter(y=>!wn.includes(nw(y)))).filter((y,k,a)=>a.findIndex(z=>nw(z)===nw(y))===k).slice(0,2);
  return {t:'build',mode,sent:x.s,p:x.p,target:ws,tiles:shuffle([...ws,...extra]),used:[],fr:false}}
function sentPool(us){return us.flatMap(u=>[...(u.talk||[]).map(d=>({s:d.o.find(isOk)[0],p:d.p||''})),...(u.gaps||[]).map(g=>({s:g[0].replace('_',g[1]),p:g[3]})),...(u.phr?u.words.map(w=>({s:w[0],p:w[2]})):[])])
  .filter(x=>{const k=tilesOf(x.s).length;return k>=3&&k<=8&&tr(x.s)})}
function trSteps(us,modes){const pool=sentPool(us),all=pool.map(x=>x.s),seen=new Set();const out=[];
  for(const x of shuffle(pool)){if(out.length>=modes.length)break;if(seen.has(x.s))continue;seen.add(x.s);const md=modes[out.length];
    if(md==='dict'||md==='fr'){const ws=tilesOf(x.s),wn=ws.map(nw),ex=shuffle(all.flatMap(y=>y===x.s?[]:tilesOf(y)).filter(y=>!wn.includes(nw(y)))).slice(0,2);out.push({t:'build',sent:x.s,p:x.p,target:ws,tiles:shuffle([...ws,...ex]),used:[],fr:md==='fr'});continue}
    const st=trBuild(x,md,all);if(st)out.push(st)}
  return out}
function startUnit(i,uo){""")
rep("""  if(u.phr){const bs=buildSteps(u,5);bs.forEach((s,k)=>{if(k<2)s.fr=true;steps.push(s)})}   /* phrases : 3 à écouter, 2 à traduire */
  else buildSteps(u,2).forEach(s=>steps.push(s));""",
"""  if(u.phr){const bs=buildSteps(u,4);bs.forEach((s,k)=>{if(k<2)s.fr=true;steps.push(s)});trSteps([u],['oral','read']).forEach(s=>steps.push(s))}   /* phrases : 2 à écouter, 2 à traduire vers la langue apprise, 1 traduction orale, 1 traduction écrite (v31) */
  else{buildSteps(u,2).forEach(s=>steps.push(s));if(u.tier>1||u.conv)trSteps([u],['oral']).forEach(s=>steps.push(s))}""")
# 2. réponse : garder le mode quand l'exercice raté revient, message avec la phrase et son sens
rep("""  say(fill(s.sent));
  settle(s,ok,`« ${esc(fill(s.sent))} »`,()=>({t:'build',sent:s.sent,p:s.p,target:s.target,tiles:shuffle(s.tiles.slice()),used:[],fr:s.fr}));""",
"""  say(fill(s.sent));
  settle(s,ok,`« ${esc(fill(s.sent))} »`,()=>({t:'build',mode:s.mode,sent:s.sent,p:s.p,target:s.target,tiles:shuffle(s.tiles.slice()),used:[],fr:s.fr}));""")
# 3. affichage des deux nouveaux modes (sans bouton Traduire : ce serait la réponse)
rep("""    body=`${s.fr?`<div class="ask">Traduis la phrase""","""    body=`${s.mode==='oral'?`<div class="ask">Écoute et traduis<small>Écoute ${G().es}, puis traduis en français : touche les mots dans le bon ordre.</small></div>
    <div class="buildtop">${s.p?`<div class="prop">${pic(s.p)}</div>`:''}<button class="speaker" data-act="hear" aria-label="Écouter la phrase">🔊</button><button class="speaker sm" data-act="slow" aria-label="Écouter lentement">🐢</button>${a?`<div class="frsent">${esc(fill(s.sent))}</div>`:''}</div>`
    :s.mode==='read'?`<div class="ask">Lis et traduis<small>Traduis en français : touche les mots dans le bon ordre.</small></div>
    <div class="buildtop">${s.p?`<div class="prop">${pic(s.p)}</div>`:''}<div class="frsent tgt">${esc(fill(s.sent))}</div><button class="speaker sm" data-act="hear" aria-label="Écouter la phrase">🔊</button></div>`
    :s.fr?`<div class="ask">Traduis la phrase""")
ui("Écoute et traduis","Listen and translate","Ascolta e traduci")
ui("Écoute {0}, puis traduis en français : touche les mots dans le bon ordre.","Listen to {0}, then translate into English: tap the words in the right order.","Ascolta {0}, poi traduci in italiano: tocca le parole nell'ordine giusto.")
ui("Lis et traduis","Read and translate","Leggi e traduci")
ui("Traduis en français : touche les mots dans le bon ordre.","Translate into English: tap the words in the right order.","Traduci in italiano: tocca le parole nell'ordine giusto.")
ui("Écouter lentement","Listen slowly","Ascolta lentamente")
# lentement pour la phrase
rep("  if(s.t==='build')return say(fill(s.sent));","  if(s.t==='build')return say(fill(s.sent));   /* v31 : aussi pour Écoute et traduis */")
# 4. atelier « Traduction » sur l'accueil
rep("""    <button class="fun" data-act="songs"><span>📜</span>Récitations</button></div>""","""    <button class="fun" data-act="songs"><span>📜</span>Récitations</button>
    <button class="fun" data-act="trad"><span>🔁</span>Traduction</button></div>""")
ui("Traduction","Translation","Traduzione")
rep("""function startChat(){""","""/* v31 : atelier de traduction sur les phrases des leçons déjà réussies (8 phrases à reconstruire avec des mots découpés) */
const TRAD_MODES={oral:['oral','oral','oral','dict','oral','oral','dict','oral'],ecrit:['read','fr','read','fr','read','fr','read','fr']};
function tradView(){const n=sentPool(learnedUnits()).length;
  app.innerHTML=head('🔁 Traduction')+`<p class="note" style="margin-bottom:12px">${n>=4?`8 phrases de tes leçons à reconstruire avec des mots découpés. ${n} phrases disponibles.`:'Termine encore quelques leçons pour débloquer la traduction !'}</p>
  <div class="set"><button class="btn" data-act="tradgo" data-k="oral" ${n>=4?'':'disabled'}>🎧 Traduction orale</button><p class="note">Tu entends la phrase sans la voir, puis tu la traduis en français.</p>
  <button class="btn sun" data-act="tradgo" data-k="ecrit" ${n>=4?'':'disabled'}>✍️ Traduction écrite</button><p class="note">Tu lis la phrase et tu la traduis en français, puis le contraire : du français vers l'espagnol.</p></div>`}
function startTrad(k){const steps=trSteps(learnedUnits(),TRAD_MODES[k]||TRAD_MODES.oral);if(steps.length<3)return false;
  L={unit:-1,kind:'trad',steps,i:0,mistakes:0,ok:0,answered:null,tries:0,t0:Date.now(),stk0:stickerCount()};view='lesson';render();return true}
function startChat(){""")
ui("🔁 Traduction","🔁 Translation","🔁 Traduzione")
ui("8 phrases de tes leçons à reconstruire avec des mots découpés. {0} phrases disponibles.","8 sentences from your lessons to rebuild with word tiles. {0} sentences available.","8 frasi delle tue lezioni da ricostruire con le parole. {0} frasi disponibili.")
ui("Termine encore quelques leçons pour débloquer la traduction !","Finish a few more lessons to unlock translation!","Finisci ancora qualche lezione per sbloccare la traduzione!")
ui("🎧 Traduction orale","🎧 Spoken translation","🎧 Traduzione orale")
ui("Tu entends la phrase sans la voir, puis tu la traduis en français.","You hear the sentence without seeing it, then you translate it into English.","Senti la frase senza vederla, poi la traduci in italiano.")
ui("✍️ Traduction écrite","✍️ Written translation","✍️ Traduzione scritta")
ui("Tu lis la phrase et tu la traduis en français, puis le contraire : du français vers l'espagnol.","You read the sentence and translate it into English, then the other way round: from English into Spanish.","Leggi la frase e la traduci in italiano, poi il contrario: dall'italiano allo spagnolo.")
# actions + vue (guard comme le chat)
rep("  else if(a==='chat'){startChat();speakStep()}","  else if(a==='chat'){startChat();speakStep()}\n  else if(a==='trad'){view='trad';render()}\n  else if(a==='tradgo'){if(startTrad(b.dataset.k))speakStep()}")
open(P,'w',encoding='utf8').write(s)
open('/tmp/claude-0/-home-claude/aa41b3f1-6410-5635-8215-dcdb8c4f13a8/scratchpad/ui31.json','w').write(J(UIADD))
print('ok')
