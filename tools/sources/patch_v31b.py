# v31 : déverrouiller l'espace parent avec l'empreinte ou le visage (WebAuthn, appareil seulement), le code reste
import json
P='/home/claude/appespagnol/index.html'
s=open(P,encoding='utf8').read()
J=lambda x:json.dumps(x,ensure_ascii=False)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90]);s=s.replace(a,b,1)
UIADD={}
def ui(fr,en,it):UIADD[fr]=[en,it]
rep("function openGate(next){","""/* v31 : empreinte ou visage (WebAuthn, authentificateur du téléphone, vérification de l'utilisateur obligatoire). Rien n'est envoyé : seule
   l'identité de la clé est gardée (hola-lola-bio). Le code parent reste toujours possible. Liée à l'adresse du site : à réactiver après un changement d'adresse. */
const BIOK='hola-lola-bio';let bioAvail=false,bioMsg='';
const getBio=()=>{try{return JSON.parse(localStorage.getItem(BIOK)||'null')}catch(e){return null}};
const b64=b=>btoa(String.fromCharCode(...new Uint8Array(b))),unb64=t=>Uint8Array.from(atob(t),c=>c.charCodeAt(0));
const rnd=n=>crypto.getRandomValues(new Uint8Array(n));
try{if(window.PublicKeyCredential&&window.isSecureContext&&PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable)PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable().then(v=>{bioAvail=!!v;if(v&&(view==='pgate'||view==='parent'))render()}).catch(()=>{})}catch(e){}
async function bioOn(){bioMsg='';try{const c=await navigator.credentials.create({publicKey:{challenge:rnd(32),rp:{name:'Petit Polyglotte'},user:{id:rnd(16),name:'parent',displayName:'Parent'},
  pubKeyCredParams:[{type:'public-key',alg:-7},{type:'public-key',alg:-257}],authenticatorSelection:{authenticatorAttachment:'platform',userVerification:'required',residentKey:'discouraged'},timeout:60000,attestation:'none'}});
  localStorage.setItem(BIOK,JSON.stringify({id:b64(c.rawId),d:dayPlus(0)}));bioMsg='✅ Activé : la prochaine fois, touchez « Empreinte ou visage ».'}catch(e){bioMsg='Activation annulée ou impossible sur cet appareil.'}render()}
async function bioCheck(){const b=getBio();if(!b)return;gateMsg='';try{const c=await navigator.credentials.get({publicKey:{challenge:rnd(32),allowCredentials:[{type:'public-key',id:unb64(b.id)}],userVerification:'required',timeout:60000}});
  const fl=new Uint8Array(c.response.authenticatorData)[32];if(fl&4){gatePass();return}gateMsg='Vérification non confirmée : utilisez le code.'}catch(e){gateMsg='Empreinte ou visage non reconnu : utilisez le code.'}render()}
function openGate(next){""")
# bouton sur l'écran du code
rep("""    <button class="btn" data-act="pgok" ${wait?'disabled':''}>Entrer</button>${msg}<button class="tool" data-act="pgforgot" style="justify-content:center">Code oublié ?</button>`;""",
    """    <button class="btn" data-act="pgok" ${wait?'disabled':''}>Entrer</button>${bioAvail&&getBio()?'<button class="btn sun" data-act="biogo">👆 Empreinte ou visage</button>':''}${msg}<button class="tool" data-act="pgforgot" style="justify-content:center">Code oublié ?</button>`;""")
# réglage dans l'espace parent
rep("""  <div class="accs">${cards}</div>
  ${P.list.length<6?""","""  ${bioAvail?`<div class="set"><b>👆 Empreinte ou visage</b><p class="note" style="margin:0">Ouvrez l'espace parent avec l'empreinte ou le visage enregistrés sur ce téléphone, au lieu du code. Le code parent reste toujours possible.</p>
    <p class="note" style="margin:0;color:var(--coral-d)">À activer seulement si vous êtes le seul à déverrouiller ce téléphone : il accepte toute empreinte ou tout visage enregistré dessus.</p>
    ${getBio()?'<button class="tool" data-act="biooff" style="justify-content:center">Désactiver l\\'empreinte ou le visage</button>':'<button class="btn sun" data-act="bioon">👆 Activer l\\'empreinte ou le visage</button>'}${bioMsg?`<p class="note" role="status" style="margin:0">${esc(bioMsg)}</p>`:''}</div>`:''}
  <div class="accs">${cards}</div>
  ${P.list.length<6?""")
rep("  else if(a==='pgok'){","  else if(a==='biogo')bioCheck();\n  else if(a==='bioon')bioOn();\n  else if(a==='biooff'){try{localStorage.removeItem(BIOK)}catch(e){}bioMsg='Désactivé : seul le code parent ouvre l\\'espace parent.';render()}\n  else if(a==='pgok'){")
ui("👆 Empreinte ou visage","👆 Fingerprint or face","👆 Impronta o volto")
ui("Ouvrez l'espace parent avec l'empreinte ou le visage enregistrés sur ce téléphone, au lieu du code. Le code parent reste toujours possible.","Open the parent area with the fingerprint or face registered on this phone instead of the code. The parent code still works.","Aprite l'area genitori con l'impronta o il volto registrati su questo telefono, invece del codice. Il codice genitore resta sempre valido.")
ui("À activer seulement si vous êtes le seul à déverrouiller ce téléphone : il accepte toute empreinte ou tout visage enregistré dessus.","Only turn this on if you are the only one who unlocks this phone: it accepts any fingerprint or face registered on it.","Attivatelo solo se siete gli unici a sbloccare questo telefono: accetta qualsiasi impronta o volto registrato.")
ui("Désactiver l'empreinte ou le visage","Turn off fingerprint or face","Disattiva impronta o volto")
ui("👆 Activer l'empreinte ou le visage","👆 Turn on fingerprint or face","👆 Attiva impronta o volto")
ui("✅ Activé : la prochaine fois, touchez « Empreinte ou visage ».","✅ Turned on: next time, tap “Fingerprint or face”.","✅ Attivato: la prossima volta toccate «Impronta o volto».")
ui("Activation annulée ou impossible sur cet appareil.","Set-up cancelled or not possible on this device.","Attivazione annullata o impossibile su questo dispositivo.")
ui("Vérification non confirmée : utilisez le code.","Check not confirmed: use the code.","Verifica non confermata: usate il codice.")
ui("Empreinte ou visage non reconnu : utilisez le code.","Fingerprint or face not recognised: use the code.","Impronta o volto non riconosciuti: usate il codice.")
ui("Désactivé : seul le code parent ouvre l'espace parent.","Turned off: only the parent code opens the parent area.","Disattivato: solo il codice genitore apre l'area genitori.")
i=s.index('const UI={')+len('const UI={');s=s[:i]+J(UIADD)[1:-1]+','+s[i:]
open(P,'w',encoding='utf8').write(s);print('ok')
