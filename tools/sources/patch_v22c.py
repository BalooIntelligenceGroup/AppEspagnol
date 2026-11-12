import sys, json
p = open('index.html').read()
def rep(a, b, c=1):
    global p
    if p.count(a) != c: sys.exit(f'{p.count(a)}x: ' + a[:110])
    p = p.replace(a, b)
def addjs(obj_start, entries):
    add = ''.join(json.dumps(k, ensure_ascii=False) + ':' + json.dumps(v, ensure_ascii=False) + ',' for k, v in entries.items())
    rep(obj_start, obj_start + add)

# ---------- 15 minutes par défaut ----------
rep("const def=()=>({limit:10,", "const def=()=>({limit:15,")
rep("if(!S.mig22){if(S.limit===undefined)S.limit=10;", "if(!S.mig22){if(S.limit===undefined)S.limit=15;")
rep("Conseillé : 10 minutes par jour, c'est suffisant pour progresser.", "Conseillé : 15 minutes par jour, c'est suffisant pour progresser.")

# ---------- avertissement au-delà de 15 minutes ----------
rep("""    <p class="note">Choisissez entre 1 et 300 minutes, puis Valider.</p></div>`}""",
    """    <p class="note">Choisissez entre 1 et 300 minutes, puis Valider.</p>
    ${!(s.limit>0&&s.limit<=15)?'<p class="note warnbox">⚠️ Au-delà de 15 minutes par jour : cette appli est conçue pour limiter le temps d\\'écran, de façon préventive. Le choix vous appartient : vous restez seul décideur du temps d\\'écran de votre enfant.</p>':''}</div>`}""")

# ---------- code parent ----------
rep("function parentGate(){\n  if(!gateQ){const a=6+(Math.random()*4|0),b=6+(Math.random()*4|0);gateQ={a,b}}",
"""/* Code parent (4 chiffres), un seul par téléphone (clé hola-lola-pin). Sans code, ou code oublié :
   une multiplication difficile (2 chiffres × 2 chiffres), puis création du code. */
const PINK='hola-lola-pin';
const pinHash=c=>{let h=5381;for(const ch of 'hola-lola:'+c)h=((h*33)^ch.charCodeAt(0))>>>0;return h.toString(36)};
const getPin=()=>{try{return localStorage.getItem(PINK)}catch(e){return null}};
const setPin=c=>{try{localStorage.setItem(PINK,pinHash(c))}catch(e){}};
let gateMode='pin';
function openGate(next){readName();gateNext=next||null;gateMode=getPin()?'pin':'math';gateQ=null;gateMsg='';popen=null;view='pgate';render()}
function gatePass(){const g=gateNext;gateNext=null;gateMode='pin';
  if(g&&g.act==='pick'){loadProfile(g.id);wStep=null;themeFrom='setup';view=S.name&&S.gender&&S.theme?'home':'welcome';render()}
  else if(g&&g.act==='addp'){save();const id='p'+Date.now().toString(36);P.list.push({id});loadProfile(id);wStep='lang';themeFrom='setup';view='welcome';render()}
  else if(g&&g.act==='reset'){confirmReset=true;view='settings';render()}
  else{view='parent';render()}}
function parentGate(){
  if(gateMode==='pin'&&!getPin())gateMode='math';
  const back=gateNext&&gateNext.act!=='reset'?'who':'settings',title=gateNext&&gateNext.act!=='reset'?'Choisir le joueur':'Espace parent';
  const msg=gateMsg?`<p class="note" style="color:var(--bad)">${esc(gateMsg)}</p>`:'';
  let body;
  if(gateMode==='pin')body=`<p style="margin:0;font-weight:800">🔒 Code parent</p>
    <label class="field" for="pg">Code à 4 chiffres<input id="pg" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    <button class="btn" data-act="pgok">Entrer</button>${msg}<button class="tool" data-act="pgforgot" style="justify-content:center">Code oublié ?</button>`;
  else if(gateMode==='math'){if(!gateQ){const a=12+(Math.random()*14|0),b=13+(Math.random()*13|0);gateQ={a,b}}
    body=`<p style="margin:0;font-weight:800">${getPin()?'Code oublié : pour en créer un nouveau, combien font':'Pour les parents : combien font'} ${gateQ.a} × ${gateQ.b} ?</p>
    <label class="field" for="pg">Réponse<input id="pg" inputmode="numeric" autocomplete="off"></label>
    <button class="btn" data-act="pgok">Entrer</button>${msg}`}
  else body=`<p style="margin:0;font-weight:800">🔒 Créez votre code parent</p><p class="note" style="margin:0">4 chiffres, à ne pas donner aux enfants. Il protège l'espace parent et le temps d'écran.</p>
    <label class="field" for="pn1">Code à 4 chiffres<input id="pn1" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    <label class="field" for="pn2">Confirmer le code<input id="pn2" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    <button class="btn" data-act="pgnew">Enregistrer le code</button>${msg}`;
  app.innerHTML=`<div class="head"><button class="icon-btn" data-act="${back}" aria-label="Retour">←</button><h2>${title}</h2></div><div class="set">${body}</div>`;
}
function oldParentGate(){
  if(!gateQ){const a=6+(Math.random()*4|0),b=6+(Math.random()*4|0);gateQ={a,b}}""")
rep("""  else if(a==='pgok'){const v=+(($('#pg')||{}).value||'');if(gateQ&&v===gateQ.a*gateQ.b){const g=gateNext;gateNext=null;
      if(g&&g.act==='pick'){loadProfile(g.id);wStep=null;themeFrom='setup';view=S.name&&S.gender&&S.theme?'home':'welcome';render()}
      else if(g&&g.act==='addp'){save();const id='p'+Date.now().toString(36);P.list.push({id});loadProfile(id);wStep='lang';themeFrom='setup';view='welcome';render()}
      else{view='parent';render()}}else{gateQ=null;gateMsg='Ce n\\'est pas la bonne réponse.';render()}}""",
    """  else if(a==='pgok'){const raw=(($('#pg')||{}).value||'').trim();
    if(gateMode==='pin'){if(getPin()&&pinHash(raw)===getPin())gatePass();else{gateMsg='Ce n\\'est pas le bon code.';render()}}
    else{if(gateQ&&+raw===gateQ.a*gateQ.b){gateMode='new';gateMsg='';render()}else{gateQ=null;gateMsg='Ce n\\'est pas la bonne réponse.';render()}}}
  else if(a==='pgforgot'){gateMode='math';gateQ=null;gateMsg='';render()}
  else if(a==='pgnew'){const c1=(($('#pn1')||{}).value||'').trim(),c2=(($('#pn2')||{}).value||'').trim();
    if(!/^\\d{4}$/.test(c1)){gateMsg='Le code doit faire 4 chiffres.';render()}else if(c1!==c2){gateMsg='Les deux codes ne sont pas pareils.';render()}else{setPin(c1);gateMsg='';gatePass()}}""")
rep("""  else if(a==='parent'){readName();gateNext=null;popen=null;gateQ=null;""", """  else if(a==='parent'){openGate(null);return;readName();gateNext=null;popen=null;gateQ=null;""")
rep("""  else if(a==='pick'&&anyOver()){gateNext={act:'pick',id:b.dataset.id};gateQ=null;gateMsg='';view='pgate';render()}
  else if(a==='addp'&&anyOver()){gateNext={act:'addp'};gateQ=null;gateMsg='';view='pgate';render()}""",
    """  else if(a==='pick'&&anyOver())openGate({act:'pick',id:b.dataset.id});
  else if(a==='addp'&&anyOver())openGate({act:'addp'});""")
rep("""  else if(a==='reset'){readName();confirmReset=true;render()}""", """  else if(a==='reset')openGate({act:'reset'});""")

# ---------- création du code au premier démarrage (écran du temps d'écran) ----------
rep("""  ${limitBox(S,P.cur)}</div>${PROMISE}
  <button class="btn sun" data-act="tsetok">Valider et commencer</button>`;""",
    """  ${limitBox(S,P.cur)}</div>
  ${getPin()?'':`<div class="set"><b>🔒 Code parent</b><p class="note" style="margin:0">4 chiffres, à ne pas donner aux enfants. Il protège l'espace parent et le temps d'écran.</p>
    <label class="field" for="pn1">Code à 4 chiffres<input id="pn1" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    <label class="field" for="pn2">Confirmer le code<input id="pn2" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    ${tsetMsg?`<p class="note" style="color:var(--bad)">${esc(tsetMsg)}</p>`:''}</div>`}
  ${PROMISE}
  <button class="btn sun" data-act="tsetok">Valider et commencer</button>`;""")
rep("function tsetup(){", "let tsetMsg='';\nfunction tsetup(){")
rep("""  else if(a==='tsetok'){const inp=document.getElementById('plim-'+P.cur),m=Math.round(+(inp&&inp.value));""",
    """  else if(a==='tsetok'){if(!getPin()){const c1=(($('#pn1')||{}).value||'').trim(),c2=(($('#pn2')||{}).value||'').trim();
      if(!/^\\d{4}$/.test(c1)){tsetMsg='Le code doit faire 4 chiffres.';render();return}if(c1!==c2){tsetMsg='Les deux codes ne sont pas pareils.';render();return}setPin(c1);tsetMsg=''}
    const inp=document.getElementById('plim-'+P.cur),m=Math.round(+(inp&&inp.value));""")
# didacticiel parents
rep("t:`Dans ⚙️ Réglages → Espace parent (protégé par une multiplication) :", "t:`Dans ⚙️ Réglages → Espace parent (protégé par votre code parent) :")

rep(".promise{", ".warnbox{background:var(--bad-bg);color:var(--ink)!important;border-radius:12px;padding:8px 10px;font-weight:700}\n.promise{")

addjs('const UI={', {
 "⚠️ Au-delà de {0} minutes par jour : cette appli est conçue pour limiter le temps d'écran, de façon préventive. Le choix vous appartient : vous restez seul décideur du temps d'écran de votre enfant.":
   ["⚠️ Beyond {0} minutes a day: this app is designed to limit screen time, as a preventive measure. The choice is yours: you alone decide your child's screen time.", "⚠️ Oltre {0} minuti al giorno: questa app è pensata per limitare il tempo di schermo, in modo preventivo. La scelta è vostra: siete voi a decidere il tempo di schermo di vostro figlio."],
 "🔒 Code parent": ["🔒 Parent code", "🔒 Codice genitore"],
 "Code à {0} chiffres": ["{0}-digit code", "Codice di {0} cifre"],
 "Code oublié ?": ["Forgot the code?", "Codice dimenticato?"],
 "Code oublié : pour en créer un nouveau, combien font {0} × {1} ?": ["Forgot the code: to create a new one, what is {0} × {1}?", "Codice dimenticato: per crearne uno nuovo, quanto fa {0} × {1}?"],
 "🔒 Créez votre code parent": ["🔒 Create your parent code", "🔒 Create il vostro codice genitore"],
 "{0} chiffres, à ne pas donner aux enfants. Il protège l'espace parent et le temps d'écran.": ["{0} digits, not to be shared with children. It protects the parents' area and screen time.", "{0} cifre, da non dare ai bambini. Protegge l'area genitori e il tempo di schermo."],
 "Confirmer le code": ["Confirm the code", "Conferma il codice"],
 "Enregistrer le code": ["Save the code", "Salva il codice"],
 "Ce n'est pas le bon code.": ["That's not the right code.", "Non è il codice giusto."],
 "Le code doit faire {0} chiffres.": ["The code must have {0} digits.", "Il codice deve avere {0} cifre."],
 "Les deux codes ne sont pas pareils.": ["The two codes don't match.", "I due codici non coincidono."],
 "Dans ⚙️ Réglages → Espace parent (protégé par votre code parent) : temps d'écran par jour, langue de l'appli, bouton «{0}», progrès de chaque enfant. Sans publicité, aucune donnée envoyée.":
   ["In ⚙️ Settings → Parents' area (protected by your parent code): daily screen time, app language, “{0}” button, each child's progress. No ads, no data sent.", "In ⚙️ Impostazioni → Area genitori (protetta dal vostro codice genitore): tempo di schermo al giorno, lingua dell'app, pulsante «{0}», progressi di ogni bambino. Niente pubblicità, nessun dato inviato."],
})
open('index.html', 'w').write(p)
print('ok')
