import sys, json
p = open('index.html').read()
def rep(a, b, c=1):
    global p
    if p.count(a) != c: sys.exit(f'{p.count(a)}x: ' + a[:100])
    p = p.replace(a, b)

# 10 minutes par jour par défaut (nouveaux profils et profils existants sans réglage)
rep("const def=()=>({name:'',xp:0,", "const def=()=>({limit:10,name:'',xp:0,")
rep("  if(!S.mig13){", "  if(!S.mig22){if(S.limit===undefined)S.limit=10;S.mig22=1;if(S.name)save()}\n  if(!S.mig13){")

# une nouvelle leçon par jour, après la Séance du jour
rep("/* ---------- Accueil ---------- */", """/* Rythme : au plus une NOUVELLE leçon par jour (S.newDay), et seulement après la Séance du jour
   quand des mots sont à revoir (S.seanceDay). Les leçons déjà réussies restent libres. */
function newGate(i){
  if(i<0||i>=UNITS.length||!unlocked(i)||S.stars[UNITS[i].id])return null;
  const t=dayPlus(0);if(S.newDay===t)return 'tomorrow';
  if(S.seanceDay!==t&&dueList().length)return 'seance';return null;
}
/* ---------- Accueil ---------- */""")
rep("""      ${i===cur?'<span class="start-tag">À toi !</span>':''}""",
    """      ${i===cur?`<span class="start-tag">${gate==='tomorrow'?'🌙 Demain !':gate==='seance'?'🎯 Séance d\\'abord':'À toi !'}</span>`:''}""")
rep("""    const last=i===UNITS.length-1||UNITS[i+1].tier!==u.tier,li=UNITS.slice(0,i+1).filter(x=>x.tier===u.tier).length;
    return `${tierHead}<button class="node ${lk?'locked':dn?'done':''} ${i===cur?'current':''}\"""",
    """    const last=i===UNITS.length-1||UNITS[i+1].tier!==u.tier,li=UNITS.slice(0,i+1).filter(x=>x.tier===u.tier).length,gate=i===cur?newGate(i):null;
    return `${tierHead}<button class="node ${lk?'locked':dn?'done':''} ${i===cur?'current':''} ${gate?'wait':''}\"""")
rep("""<span class="ctag">💬 Conversation</span>':''}</button>${last?evalNode""",
    """<span class="ctag">💬 Conversation</span>':''}</button>${gate?`<p class="hint-bubble">${gate==='seance'?'🎯 Fais d\\'abord ta Séance du jour, puis cette leçon s\\'ouvre !':'🌙 Une nouvelle leçon par jour : celle-ci s\\'ouvre demain. En attendant, révise ou joue !'}</p>`:''}${last?evalNode""")
rep("""<button class="btn coral" data-act="seance" ${nWords?'':'disabled'}>""",
    """<button class="btn coral ${cur>=0&&newGate(cur)==='seance'?'pulse':''}" data-act="seance" ${nWords?'':'disabled'}>""")
rep("""  else if(a==='unit'){const i=+b.dataset.i;if(!unlocked(i)){say('¡Todavía no!');return}""",
    """  else if(a==='unit'){const i=+b.dataset.i;if(!unlocked(i)){say('¡Todavía no!');return}
    {const g=newGate(i);if(g){say(g==='seance'?'¡Primero, tu sesión del día!':'¡Mañana!');const h=document.querySelector('.hint-bubble');if(h){h.classList.remove('shake');void h.offsetWidth;h.classList.add('shake')}return}}""")
rep("""  if(L.unit>=0){const id=UNITS[L.unit].id;newUnit=!S.stars[id];S.stars[id]=Math.max(S.stars[id]||0,stars)}""",
    """  if(L.unit>=0){const id=UNITS[L.unit].id;newUnit=!S.stars[id];S.stars[id]=Math.max(S.stars[id]||0,stars);if(newUnit)S.newDay=dayPlus(0)}
  if(L.kind==='seance')S.seanceDay=dayPlus(0);""")
rep("""      ${R.newUnit&&next&&unlocked(R.unit+1)?""",
    """      ${R.newUnit&&next&&newGate(R.unit+1)==='tomorrow'?'<p class="hint-bubble">🌙 Une nouvelle leçon par jour : la prochaine s\\'ouvre demain. En attendant, révise ou joue !</p>':''}
      ${R.newUnit&&next&&unlocked(R.unit+1)&&!newGate(R.unit+1)?""")
# didacticiel
rep("t:`Le petit chiffre, c'est le nombre de mots à revoir aujourd'hui. Les revoir au bon moment, c'est le secret pour ne plus les oublier !",
    "t:`Le petit chiffre, c'est le nombre de mots à revoir aujourd'hui. Fais ta séance chaque jour : ensuite, une nouvelle leçon s'ouvre. Une par jour, c'est le secret pour ne rien oublier !")
# styles
rep(".start-tag{", """.node.wait .start-tag{background:var(--lagoon)}
.hint-bubble{position:relative;max-width:300px;margin:4px auto 10px;background:var(--card);border:3px solid var(--sun);border-radius:18px;padding:10px 14px;font-weight:800;font-size:16px;line-height:1.3;text-align:center;color:var(--ink);box-shadow:0 4px 0 var(--sun-d)}
.hint-bubble.shake{animation:shake .45s}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-8px)}75%{transform:translateX(8px)}}
.btn.pulse{animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.04)}}
@media (prefers-reduced-motion:reduce){.btn.pulse,.hint-bubble.shake{animation:none}}
.start-tag{""")

# version de la prochaine mise en ligne
rep("const APP_VERSION=21,", "const APP_VERSION=22,")
NEW22 = "Nouveau : chaque jour, ta Séance du jour, puis une nouvelle leçon. Dix minutes par jour, c'est parfait !"
rep("""  21:"Le temps d'écran choisi par tes parents est bien respecté."};""",
    """  21:"Le temps d'écran choisi par tes parents est bien respecté.",
  22:""" + json.dumps(NEW22, ensure_ascii=False) + "};")
UIADD = {
 "🌙 Demain !": ["🌙 Tomorrow!", "🌙 Domani!"],
 "🎯 Séance d'abord": ["🎯 Practice first", "🎯 Prima il ripasso"],
 "🎯 Fais d'abord ta Séance du jour, puis cette leçon s'ouvre !": ["🎯 Do Today's practice first, then this lesson opens!", "🎯 Prima fai il Ripasso del giorno, poi questa lezione si apre!"],
 "🌙 Une nouvelle leçon par jour : celle-ci s'ouvre demain. En attendant, révise ou joue !": ["🌙 One new lesson a day: this one opens tomorrow. Meanwhile, review or play!", "🌙 Una nuova lezione al giorno: questa si apre domani. Intanto ripassa o gioca!"],
 "🌙 Une nouvelle leçon par jour : la prochaine s'ouvre demain. En attendant, révise ou joue !": ["🌙 One new lesson a day: the next one opens tomorrow. Meanwhile, review or play!", "🌙 Una nuova lezione al giorno: la prossima si apre domani. Intanto ripassa o gioca!"],
 "Le petit chiffre, c'est le nombre de mots à revoir aujourd'hui. Fais ta séance chaque jour : ensuite, une nouvelle leçon s'ouvre. Une par jour, c'est le secret pour ne rien oublier !": ["The little number is how many words to review today. Do your practice every day: then a new lesson opens. One a day is the secret to never forgetting!", "Il numerino indica quante parole ripassare oggi. Fai il ripasso ogni giorno: poi si apre una nuova lezione. Una al giorno è il segreto per non dimenticare niente!"],
 NEW22 + " Ta progression est gardée.": ["New: every day, your Today's practice, then a new lesson. Ten minutes a day is perfect! Your progress is saved.", "Novità: ogni giorno il Ripasso del giorno, poi una nuova lezione. Dieci minuti al giorno sono perfetti! I tuoi progressi sono salvati."],
}
add = ''.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False) + ',' for k, v in UIADD.items())
rep('const UI={', 'const UI={' + add)
open('index.html', 'w').write(p)
print('ok')
