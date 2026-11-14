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

# ---------- question secrète, essais limités ----------
rep("let gateMode='pin';", r"""let gateMode='pin';
/* Question secrète (v23) : choisie avec le code, elle remplace la multiplication en cas d'oubli.
   Clé hola-lola-pinq = {q: n° de question, h: empreinte de la réponse}. 5 erreurs → 1 minute d'attente. */
const PINQ='hola-lola-pinq',PINLOCK='hola-lola-pinlock';
const SECRET_Q=["Ville de naissance d'un parent ?","Prénom de votre premier animal ?","Rue de votre enfance ?","Plat préféré d'un parent ?","Prénom d'un grand-parent ?"];
const normAns=t=>(t||'').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'').replace(/[^a-z0-9]/g,'');
const getQ=()=>{try{return JSON.parse(localStorage.getItem(PINQ)||'null')}catch(e){return null}};
const setQ=(q,a)=>{try{localStorage.setItem(PINQ,JSON.stringify({q,h:pinHash('q:'+normAns(a))}))}catch(e){}};
let gateFails=0;
const lockLeft=()=>{let u=0;try{u=+localStorage.getItem(PINLOCK)||0}catch(e){}return Math.max(0,Math.ceil((u-Date.now())/1000))};
function gateFail(msg){gateFails++;if(gateFails>=5){gateFails=0;try{localStorage.setItem(PINLOCK,String(Date.now()+60000))}catch(e){}}gateMsg=msg}
const qFields=()=>`<label class="field" for="pq">Question secrète (si vous oubliez le code)<select id="pq">${SECRET_Q.map((q,i)=>`<option value="${i}">${q}</option>`).join('')}</select></label>
    <label class="field" for="pa">Réponse<input id="pa" autocomplete="off"></label>`;
/* lit et vérifie code + question ; renvoie un message d'erreur ou '' */
function readNewPin(withQ){const c1=(($('#pn1')||{}).value||'').trim(),c2=(($('#pn2')||{}).value||'').trim();
  if(!/^\d{4}$/.test(c1))return 'Le code doit faire 4 chiffres.';if(c1!==c2)return 'Les deux codes ne sont pas pareils.';
  if(withQ){const a=(($('#pa')||{}).value||'');if(normAns(a).length<2)return 'Écrivez une réponse à la question secrète.';setQ(+(($('#pq')||{}).value||0),a)}
  setPin(c1);return ''}""")
rep("function openGate(next){readName();gateNext=next||null;gateMode=getPin()?'pin':'math';",
    "function openGate(next){readName();gateNext=next||null;gateMode=getPin()?'pin':'new';")
rep("""function gatePass(){const g=gateNext;gateNext=null;gateMode='pin';""",
    """function gatePass(){if(getPin()&&!getQ()){gateMode='setq';gateMsg='';render();return}
  gateFails=0;const g=gateNext;gateNext=null;gateMode='pin';""")
cut("function parentGate(){", "function oldParentGate(){", r"""function parentGate(){
  if(gateMode==='pin'&&!getPin())gateMode='new';
  const back=gateNext&&gateNext.act!=='reset'?'who':'settings',title=gateNext&&gateNext.act!=='reset'?'Choisir le joueur':'Espace parent';
  const wait=lockLeft(),msg=wait?`<p class="note" style="color:var(--bad)">Trop d'essais. Réessayez dans ${wait} secondes.</p>`:gateMsg?`<p class="note" style="color:var(--bad)">${esc(gateMsg)}</p>`:'';
  const q=getQ();let body;
  if(gateMode==='pin')body=`<p style="margin:0;font-weight:800">🔒 Code parent</p>
    <label class="field" for="pg">Code à 4 chiffres<input id="pg" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    <button class="btn" data-act="pgok" ${wait?'disabled':''}>Entrer</button>${msg}<button class="tool" data-act="pgforgot" style="justify-content:center">Code oublié ?</button>`;
  else if(gateMode==='ask')body=`<p style="margin:0;font-weight:800">🔑 Code oublié</p><p class="note" style="margin:0">Répondez à votre question secrète pour créer un nouveau code.</p>
    <p style="margin:0;font-weight:800">${esc(SECRET_Q[q.q]||SECRET_Q[0])}</p>
    <label class="field" for="pa">Réponse<input id="pa" autocomplete="off"></label>
    <button class="btn" data-act="pgans" ${wait?'disabled':''}>Valider</button>${msg}`;
  else if(gateMode==='math'){if(!gateQ){const a=12+(Math.random()*14|0),b=13+(Math.random()*13|0);gateQ={a,b}}
    body=`<p class="note" style="margin:0">Aucune question secrète n'a encore été enregistrée sur ce téléphone.</p><p style="margin:0;font-weight:800">Code oublié : pour en créer un nouveau, combien font ${gateQ.a} × ${gateQ.b} ?</p>
    <label class="field" for="pg">Réponse<input id="pg" inputmode="numeric" autocomplete="off"></label>
    <button class="btn" data-act="pgok" ${wait?'disabled':''}>Entrer</button>${msg}`}
  else if(gateMode==='setq')body=`<p style="margin:0;font-weight:800">🔑 Ajoutez une question secrète</p><p class="note" style="margin:0">Elle servira si vous oubliez votre code. Les enfants ne doivent pas connaître la réponse.</p>
    ${qFields()}<button class="btn" data-act="pgsetq">Enregistrer</button>${msg}`;
  else body=`<p style="margin:0;font-weight:800">🔒 Créez votre code parent</p><p class="note" style="margin:0">4 chiffres, à ne pas donner aux enfants. Il protège l'espace parent et le temps d'écran.</p>
    <label class="field" for="pn1">Code à 4 chiffres<input id="pn1" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    <label class="field" for="pn2">Confirmer le code<input id="pn2" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    ${q?'':qFields()}<button class="btn" data-act="pgnew">Enregistrer le code</button>${msg}`;
  app.innerHTML=`<div class="head"><button class="icon-btn" data-act="${back}" aria-label="Retour">←</button><h2>${title}</h2></div><div class="set">${body}</div>`;
}
""")
# actions
rep("""  else if(a==='pgok'){const raw=(($('#pg')||{}).value||'').trim();
    if(gateMode==='pin'){if(getPin()&&pinHash(raw)===getPin())gatePass();else{gateMsg='Ce n\\'est pas le bon code.';render()}}
    else{if(gateQ&&+raw===gateQ.a*gateQ.b){gateMode='new';gateMsg='';render()}else{gateQ=null;gateMsg='Ce n\\'est pas la bonne réponse.';render()}}}
  else if(a==='pgforgot'){gateMode='math';gateQ=null;gateMsg='';render()}
  else if(a==='pgnew'){const c1=(($('#pn1')||{}).value||'').trim(),c2=(($('#pn2')||{}).value||'').trim();
    if(!/^\\d{4}$/.test(c1)){gateMsg='Le code doit faire 4 chiffres.';render()}else if(c1!==c2){gateMsg='Les deux codes ne sont pas pareils.';render()}else{setPin(c1);gateMsg='';gatePass()}}""",
"""  else if(a==='pgok'){if(lockLeft()){render();return}const raw=(($('#pg')||{}).value||'').trim();
    if(gateMode==='pin'){if(getPin()&&pinHash(raw)===getPin())gatePass();else{gateFail('Ce n\\'est pas le bon code.');render()}}
    else{if(gateQ&&+raw===gateQ.a*gateQ.b){gateMode='new';gateMsg='';render()}else{gateQ=null;gateFail('Ce n\\'est pas la bonne réponse.');render()}}}
  else if(a==='pgforgot'){gateMode=getQ()?'ask':'math';gateQ=null;gateMsg='';render()}
  else if(a==='pgans'){if(lockLeft()){render();return}const q=getQ(),ans=(($('#pa')||{}).value||'');
    if(q&&pinHash('q:'+normAns(ans))===q.h){gateMode='new';gateMsg='';render()}else{gateFail('Ce n\\'est pas la bonne réponse.');render()}}
  else if(a==='pgsetq'){const ans=(($('#pa')||{}).value||'');if(normAns(ans).length<2){gateMsg='Écrivez une réponse à la question secrète.';render();return}
    setQ(+(($('#pq')||{}).value||0),ans);gateMsg='';gatePass()}
  else if(a==='pgnew'){const m=readNewPin(!getQ());if(m){gateMsg=m;render()}else{gateMsg='';gatePass()}}""")
# écran du temps d'écran (nouveau téléphone) : code + question
rep("""    <label class="field" for="pn2">Confirmer le code<input id="pn2" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    ${tsetMsg?""", """    <label class="field" for="pn2">Confirmer le code<input id="pn2" type="password" inputmode="numeric" maxlength="4" autocomplete="off"></label>
    ${getQ()?'':qFields()}
    ${tsetMsg?""")
rep("""  else if(a==='tsetok'){if(!getPin()){const c1=(($('#pn1')||{}).value||'').trim(),c2=(($('#pn2')||{}).value||'').trim();
      if(!/^\\d{4}$/.test(c1)){tsetMsg='Le code doit faire 4 chiffres.';render();return}if(c1!==c2){tsetMsg='Les deux codes ne sont pas pareils.';render();return}setPin(c1);tsetMsg=''}""",
    """  else if(a==='tsetok'){if(!getPin()){const m=readNewPin(!getQ());if(m){tsetMsg=m;render();return}tsetMsg=''}""")
rep(".slogan{", "select{min-height:48px;border-radius:12px;border:2px solid var(--line);background:var(--card);color:var(--ink);font:inherit;font-weight:700;padding:0 10px;width:100%}\n.slogan{")
addjs('const UI={', {
 "Question secrète (si vous oubliez le code)": ["Secret question (if you forget the code)", "Domanda segreta (se dimenticate il codice)"],
 "Ville de naissance d'un parent ?": ["A parent's town of birth?", "Città di nascita di un genitore?"],
 "Prénom de votre premier animal ?": ["Name of your first pet?", "Nome del vostro primo animale?"],
 "Rue de votre enfance ?": ["Street where you grew up?", "Via della vostra infanzia?"],
 "Plat préféré d'un parent ?": ["A parent's favourite dish?", "Piatto preferito di un genitore?"],
 "Prénom d'un grand-parent ?": ["A grandparent's first name?", "Nome di un nonno o una nonna?"],
 "🔑 Code oublié": ["🔑 Forgot the code", "🔑 Codice dimenticato"],
 "Répondez à votre question secrète pour créer un nouveau code.": ["Answer your secret question to create a new code.", "Rispondete alla vostra domanda segreta per creare un nuovo codice."],
 "Aucune question secrète n'a encore été enregistrée sur ce téléphone.": ["No secret question has been saved on this phone yet.", "Nessuna domanda segreta è ancora stata salvata su questo telefono."],
 "🔑 Ajoutez une question secrète": ["🔑 Add a secret question", "🔑 Aggiungete una domanda segreta"],
 "Elle servira si vous oubliez votre code. Les enfants ne doivent pas connaître la réponse.": ["It will be used if you forget your code. Children must not know the answer.", "Servirà se dimenticate il codice. I bambini non devono conoscere la risposta."],
 "Enregistrer": ["Save", "Salva"],
 "Écrivez une réponse à la question secrète.": ["Write an answer to the secret question.", "Scrivete una risposta alla domanda segreta."],
 "Trop d'essais. Réessayez dans {0} secondes.": ["Too many attempts. Try again in {0} seconds.", "Troppi tentativi. Riprovate tra {0} secondi."],
})
open('index.html', 'w').write(p)
print('ok')
