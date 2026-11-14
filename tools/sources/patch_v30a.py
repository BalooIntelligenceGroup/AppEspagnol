# v30 (2e demande) : expliquer comment sont comptés les mots (règles inchangées) + 🧠 mots retenus côté enfant
import json
P='/home/claude/appespagnol/index.html'
s=open(P,encoding='utf8').read()
J=lambda x:json.dumps(x,ensure_ascii=False)
def rep(a,b,n=1):
    global s
    assert s.count(a)>=1 and (n==0 or s.count(a)==n),(s.count(a),a[:90]);s=s.replace(a,b,1)
UIADD={}
def ui(fr,en,it):UIADD[fr]=[en,it]
# 1. aides : état d'un mot (0 jamais vu, 1 en révision, 2 retenu) — mêmes règles que l'espace parent (b>=4)
rep("function stickerCount(){","""/* v30 : un seul mot pour tout l'appli : « retenu » = réussi lors de 3 révisions espacées (boîte 4 ou plus, au moins une semaine) */
const wState=k=>{const r=(S.words||{})[k];return !r?0:r.b>=4?2:1};
const retainedN=()=>Object.values(S.words||{}).filter(r=>r.b>=4).length;
const RET_HELP="🧠 Mot retenu : réussi lors de 3 révisions espacées (1 jour, puis 2, puis 4 jours plus tard), donc en mémoire depuis au moins une semaine. 🌱 En révision : déjà vu, il revient dans la Séance du jour. Un mot raté redescend et revient plus vite.";
function stickerCount(){""")
ui("🧠 Mot retenu : réussi lors de 3 révisions espacées (1 jour, puis 2, puis 4 jours plus tard), donc en mémoire depuis au moins une semaine. 🌱 En révision : déjà vu, il revient dans la Séance du jour. Un mot raté redescend et revient plus vite.",
   "🧠 Remembered word: answered correctly in 3 spaced reviews (1 day, then 2, then 4 days later), so it has stayed in memory for at least a week. 🌱 Being reviewed: already seen, it comes back in the Daily session. A missed word goes back down and comes back sooner.",
   "🧠 Parola ricordata: indovinata in 3 ripassi distanziati (1 giorno, poi 2, poi 4 giorni dopo), quindi in memoria da almeno una settimana. 🌱 In ripasso: già vista, torna nella Sessione del giorno. Una parola sbagliata scende e torna prima.")
# 2. Dico : compteurs + explication + badge par mot
rep("""  <p class="note">Touche un mot pour l'entendre. ${us.reduce((n,u)=>n+u.words.length,0)} mots appris !</p>""",
"""  <div class="stats" style="margin:4px 0 8px"><div><b>🧠 ${retainedN()}</b><small>mots retenus</small></div><div><b>🌱 ${Object.values(S.words||{}).filter(r=>r.b<4).length}</b><small>en révision</small></div><div><b>${us.reduce((n,u)=>n+u.words.length,0)}</b><small>mots dans tes leçons</small></div></div>
  <p class="note">${RET_HELP}</p><p class="note">Touche un mot pour l'entendre.</p>""")
rep("""<button class="dw" data-act="sayw" data-w="${esc(w[0])}">${w[2][0]==='#'?pic(w[2]):`<span>${esc(w[2])}</span>`}""",
    """<button class="dw" data-act="sayw" data-w="${esc(w[0])}">${(st=>st?`<i class="wst" title="${st===2?'retenu':'en révision'}">${st===2?'🧠':'🌱'}</i>`:'')(wState(W(w).es))}${w[2][0]==='#'?pic(w[2]):`<span>${esc(w[2])}</span>`}""")
for a,b,c in [("mots retenus","words remembered","parole ricordate"),("en révision","being reviewed","in ripasso"),("mots dans tes leçons","words in your lessons","parole nelle tue lezioni"),("Touche un mot pour l'entendre.","Tap a word to hear it.","Tocca una parola per ascoltarla."),("retenu","remembered","ricordata")]:ui(a,b,c)
# 3. Accueil : compteur 🧠 (touche = ouvre le Dico)
rep("""<span class="chip">⭐ ${S.xp} points</span>""","""<span class="chip">⭐ ${S.xp} points</span><button class="chip" data-act="dico" title="Mots retenus">🧠 ${retainedN()} mot${retainedN()>1?'s':''} retenu${retainedN()>1?'s':''}</button>""")
ui("🧠 {0} mots retenus","🧠 {0} words remembered","🧠 {0} parole ricordate");ui("🧠 {0} mot retenu","🧠 {0} word remembered","🧠 {0} parola ricordata");ui("Mots retenus","Words remembered","Parole ricordate")
# 4. Fin de Séance du jour : nouveaux mots retenus
rep("L={unit:-1,kind:'seance',steps:mix('seance',[],steps),i:0,mistakes:0,ok:0,answered:null,tries:0,t0:Date.now(),stk0:stickerCount()};",
    "L={unit:-1,kind:'seance',steps:mix('seance',[],steps),i:0,mistakes:0,ok:0,answered:null,tries:0,t0:Date.now(),stk0:stickerCount(),ret0:retainedN()};")
rep("newStk:Math.max(0,stickerCount()-(L.stk0||0)),","newStk:Math.max(0,stickerCount()-(L.stk0||0)),seance:L.kind==='seance',newRet:L.kind==='seance'?Math.max(0,retainedN()-(L.ret0||0)):0,")
rep("""    ${R.newStk?`<p class="say" style="color:var(--ink)">🆕""","""    ${R.seance?`<p class="say" style="color:var(--ink)">${R.newRet?`🧠 Aujourd'hui : ${R.newRet} nouveau${R.newRet>1?'x':''} mot${R.newRet>1?'s':''} retenu${R.newRet>1?'s':''} ! En tout : ${retainedN()}.`:`🌱 Tes mots avancent : encore quelques séances et ils seront retenus. En tout : ${retainedN()} mot${retainedN()>1?'s':''} retenu${retainedN()>1?'s':''}.`}</p>`:''}
    ${R.newStk?`<p class="say" style="color:var(--ink)">🆕""")
ui("🧠 Aujourd'hui : {0} nouveaux mots retenus ! En tout : {1}.","🧠 Today: {0} new words remembered! In total: {1}.","🧠 Oggi: {0} nuove parole ricordate! In tutto: {1}.")
ui("🧠 Aujourd'hui : {0} nouveau mot retenu ! En tout : {1}.","🧠 Today: {0} new word remembered! In total: {1}.","🧠 Oggi: {0} nuova parola ricordata! In tutto: {1}.")
ui("🌱 Tes mots avancent : encore quelques séances et ils seront retenus. En tout : {0} mots retenus.","🌱 Your words are moving up: a few more sessions and they will be remembered. In total: {0} words remembered.","🌱 Le tue parole avanzano: ancora qualche sessione e saranno ricordate. In tutto: {0} parole ricordate.")
ui("🌱 Tes mots avancent : encore quelques séances et ils seront retenus. En tout : {0} mot retenu.","🌱 Your words are moving up: a few more sessions and they will be remembered. In total: {0} word remembered.","🌱 Le tue parole avanzano: ancora qualche sessione e saranno ricordate. In tutto: {0} parola ricordata.")
# 5. Jeux : dire ce qui est compté
rep("On joue avec tes ${n} mots appris. Chaque partie rapporte des pièces 🪙.","On joue avec les ${n} mots déjà vus dans tes leçons. Chaque partie rapporte des pièces 🪙.")
ui("On joue avec les {0} mots déjà vus dans tes leçons. Chaque partie rapporte des pièces 🪙.","Let's play with the {0} words you have already seen in your lessons. Each game earns coins 🪙.","Giochiamo con le {0} parole già viste nelle tue lezioni. Ogni partita fa guadagnare monete 🪙.")
# 6. Album : rappeler la différence avec « retenu »
rep("<span>1 mot réussi 3 fois = 1 autocollant</span>","<span>1 mot réussi 3 fois = 1 autocollant · 🧠 retenu : voir le Dico</span>")
ui("1 mot réussi 3 fois = 1 autocollant · 🧠 retenu : voir le Dico","1 word right 3 times = 1 sticker · 🧠 remembered: see the Dictionary","1 parola giusta 3 volte = 1 adesivo · 🧠 ricordata: vedi il Dizionario")
# 7. Espace parent : chaque chiffre expliqué
rep("""<p class="note"><b>Mot bien retenu</b> : un mot réussi lors de 3 révisions espacées (1 jour, puis 2, puis 4 jours plus tard). Il est en mémoire depuis au moins une semaine. Un mot raté redescend et revient dans la Séance du jour.</p>""",
"""<details class="acc lacc" style="margin:8px 0"><summary><span class="acc-t"><b>ℹ️ Comment les mots sont-ils comptés ?</b></span><span class="chev">⌄</span></summary><div style="padding:0 12px 12px">
      <p class="note"><b>Mots vus</b> : mots rencontrés au moins une fois dans une leçon.</p>
      <p class="note"><b>Mots bien retenus 🧠</b> : mots réussis lors de 3 révisions espacées (1 jour, puis 2, puis 4 jours plus tard) : ils sont en mémoire depuis au moins une semaine. Un mot raté redescend et revient dans la Séance du jour. C'est le même chiffre que l'enfant voit sur l'accueil et dans son Dico.</p>
      <p class="note"><b>Autocollants</b> : un mot réussi 3 fois, même au cours d'une seule leçon. Ils récompensent l'effort ; la mémoire à long terme, c'est « bien retenus ».</p>
      <p class="note"><b>Leçons réussies</b> : leçons terminées avec au moins une étoile.</p></div></details>""")
ui("ℹ️ Comment les mots sont-ils comptés ?","ℹ️ How are words counted?","ℹ️ Come vengono contate le parole?")
ui("<b>Mots vus</b> : mots rencontrés au moins une fois dans une leçon.","<b>Words seen</b>: words met at least once in a lesson.","<b>Parole viste</b>: parole incontrate almeno una volta in una lezione.")
ui("<b>Mots bien retenus 🧠</b> : mots réussis lors de 3 révisions espacées (1 jour, puis 2, puis 4 jours plus tard) : ils sont en mémoire depuis au moins une semaine. Un mot raté redescend et revient dans la Séance du jour. C'est le même chiffre que l'enfant voit sur l'accueil et dans son Dico.",
   "<b>Words well remembered 🧠</b>: words answered correctly in 3 spaced reviews (1 day, then 2, then 4 days later): they have stayed in memory for at least a week. A missed word goes back down and returns in the Daily session. It is the same number the child sees on the home screen and in the Dictionary.",
   "<b>Parole ben ricordate 🧠</b>: parole indovinate in 3 ripassi distanziati (1 giorno, poi 2, poi 4 giorni dopo): sono in memoria da almeno una settimana. Una parola sbagliata scende e torna nella Sessione del giorno. È lo stesso numero che il bambino vede nella home e nel Dizionario.")
ui("<b>Autocollants</b> : un mot réussi 3 fois, même au cours d'une seule leçon. Ils récompensent l'effort ; la mémoire à long terme, c'est « bien retenus ».",
   "<b>Stickers</b>: a word answered correctly 3 times, even within a single lesson. They reward effort; long-term memory is “well remembered”.",
   "<b>Adesivi</b>: una parola indovinata 3 volte, anche in una sola lezione. Premiano l'impegno; la memoria a lungo termine è «ben ricordate».")
ui("<b>Leçons réussies</b> : leçons terminées avec au moins une étoile.","<b>Lessons passed</b>: lessons finished with at least one star.","<b>Lezioni superate</b>: lezioni finite con almeno una stella.")
# style du badge
rep(".chip{",".dw{position:relative}.wst{position:absolute;top:4px;right:6px;font-style:normal;font-size:15px;line-height:1}\nbutton.chip{border:0;font-family:inherit;color:inherit;cursor:pointer}\n.chip{")
# entrées UI
i=s.index('const UI={')+len('const UI={')
s=s[:i]+J(UIADD)[1:-1]+','+s[i:]
open(P,'w',encoding='utf8').write(s);print('ok',len(UIADD))
