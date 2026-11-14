import json,hashlib
p='/home/claude/appespagnol/index.html';h=open(p,encoding='utf8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:70],h.count(a));h=h.replace(a,b)
J=lambda x:json.dumps(x,ensure_ascii=False)
codes=open('/home/claude/codes_beta_v24.txt').read().split()
hs=[hashlib.sha256(('hola-lola-promo:'+c).encode()).hexdigest() for c in codes]

# codes promo (empreintes SHA-256 seulement, jamais les codes en clair)
rep("const famStart=()=>{const f=famInfo();return f&&f.start||null};",
"""const famStart=()=>{const f=famInfo();return f&&f.start||null};
/* Offre Ultimate (v24) : code promo de 6 caractères pour les bêta-testeurs, saisi dans l'espace parent.
   Tout est visible (toutes les leçons Famille, tous les Bonus) ; le fonctionnement ne change pas (rythme quotidien, temps d'écran).
   PROMO = empreintes SHA-256 de 'hola-lola-promo:'+CODE ; retirer une empreinte désactive le code à la prochaine mise à jour. */
const PROMO=new Set(%s);
const famUltimate=()=>{const f=famInfo();return !!(f&&f.plan==='ultimate'&&PROMO.has(f.code))};
async function promoCheck(c){
  c=String(c||'').toUpperCase().replace(/[^A-Z0-9]/g,'');if(c.length!==6||!crypto.subtle)return null;
  const b=await crypto.subtle.digest('SHA-256',new TextEncoder().encode('hola-lola-promo:'+c));
  const x=[...new Uint8Array(b)].map(v=>v.toString(16).padStart(2,'0')).join('');return PROMO.has(x)?x:null}
let promoTries=0,promoWait=0;"""%J(hs))
rep("  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famOpen(famStart())));",
    "  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famUltimate()?FAM_UNITS.length:famOpen(famStart())));")
# un code retiré de PROMO ne vaut plus rien
rep("const famActive=()=>!!famStart();","const famActive=()=>{const f=famInfo();return !!(f&&f.start&&(f.plan!=='ultimate'||famUltimate()))};")

# carte : avec Ultimate, tous les Bonus à la fin
rep("""function famMap(){
  const on=famActive(),""","""function famMap(){
  if(famUltimate()){const cb=monthBonus(),us=MONTHLY.filter(b=>b!==cb).map(b=>b.u);
    return us.length?`<div class="tier fam"><b>Tous les bonus 🎁</b><span>Offre Ultimate</span></div>`+us.map((u,i)=>{const st=S.stars[u.id]||0;
      return `<button class="node bonusn ${st?'done':''}" style="transform:translateX(${Math.round(Math.sin((UNITS.length+i)*1.1)*70)}px)" data-act="mbonus" data-id="${u.id}" aria-label="Bonus : ${esc(tx(u.es,u.fr))}">
      <span class="disc">${u.e}</span><span class="stars">${st?'⭐'.repeat(st)+'<span style="opacity:.25">'+'⭐'.repeat(3-st)+'</span>':''}</span>
      <b>${esc(u.es)}</b><em>${esc(tx(u.es,u.fr))}</em><small class="where">${esc(u.where)}</small></button>`}).join(''):''}
  const on=famActive(),""")
rep("else if(a==='mbonus'){const b=monthBonus();if(!b||!famActive())return;if(!guard())return;startUnit(-1,b.u);speakStep()}",
    "else if(a==='mbonus'){const b=b.dataset.id?MONTHLY.find(x=>x.u.id===b.dataset.id):monthBonus();if(!b||!famActive())return;if(!guard())return;startUnit(-1,b.u);speakStep()}")
rep("""  else if(a==='famoff'){""","""  else if(a==='promo'){const el=document.getElementById('promo'),v=el?el.value:'';
    if(Date.now()<promoWait){inlineMsg('promomsg',`Trop d'essais. Réessayez dans ${Math.ceil((promoWait-Date.now())/1000)} s.`);return}
    promoCheck(v).then(x=>{if(!x){promoTries++;if(promoTries>=5){promoTries=0;promoWait=Date.now()+60000}inlineMsg('promomsg','Ce code ne marche pas. Vérifiez les 6 caractères.');return}
      try{localStorage.setItem(FAM_KEY,JSON.stringify({start:dayPlus(0),plan:'ultimate',code:x}))}catch(e){}promoTries=0;famSync();render();confetti()})}
  else if(a==='famoff'){""")
# l'élément mbonus utilise "b" comme bouton : renommer la variable locale
rep("else if(a==='mbonus'){const b=b.dataset.id?MONTHLY.find(x=>x.u.id===b.dataset.id):monthBonus();if(!b||!famActive())return;if(!guard())return;startUnit(-1,b.u);speakStep()}",
    "else if(a==='mbonus'){const mb=b.dataset.id?MONTHLY.find(x=>x.u.id===b.dataset.id):monthBonus();if(!mb||!famActive())return;if(!guard())return;startUnit(-1,mb.u);speakStep()}")

# espace parent : saisie du code / offre active
rep("""${famInfo()&&famInfo().preview?`<p class="note" style="color:var(--coral-d);margin:0">Aperçu""","""${famUltimate()?`<div class="promo on"><b>🎟️ Offre Ultimate activée</b><p class="note" style="color:var(--ink);margin:0">Code bêta-testeur : toutes les leçons et tous les bonus sont ouverts sur ce téléphone. Le fonctionnement reste le même (une nouvelle leçon par jour, temps d'écran).</p><button class="tool" data-act="famoff" style="justify-content:center">Retirer le code</button></div>`
  :`<div class="promo"><b>🎟️ Code promo</b><div class="row"><input id="promo" maxlength="6" autocomplete="off" autocapitalize="characters" spellcheck="false" placeholder="ABC123" aria-label="Code promo"><button class="btn sun" data-act="promo">Valider</button></div><p class="note" id="promomsg" role="status" style="color:var(--coral-d);margin:0"></p></div>`}
  ${famInfo()&&famInfo().preview?`<p class="note" style="color:var(--coral-d);margin:0">Aperçu""")
rep(".famset{",""".promo{display:grid;gap:8px;border-top:2px dashed var(--line);padding-top:10px}.promo .row{display:flex;gap:8px}.promo.on b{color:var(--lagoon-d)}
#promo{flex:1;min-width:0;font:inherit;font-weight:800;font-size:20px;letter-spacing:.2em;text-transform:uppercase;padding:10px 12px;border-radius:14px;border:3px solid var(--line);background:var(--card);color:var(--ink)}
.famset{""")

ui={"Tous les bonus 🎁":["All bonuses 🎁","Tutti i bonus 🎁"],"Offre Ultimate":["Ultimate plan","Offerta Ultimate"],"Bonus : {0}":["Bonus: {0}","Bonus: {0}"],
 "🎟️ Offre Ultimate activée":["🎟️ Ultimate plan activated","🎟️ Offerta Ultimate attiva"],
 "Code bêta-testeur : toutes les leçons et tous les bonus sont ouverts sur ce téléphone. Le fonctionnement reste le même (une nouvelle leçon par jour, temps d'écran).":
  ["Beta-tester code: all lessons and all bonuses are open on this phone. Everything works the same (one new lesson a day, screen time).","Codice beta-tester: tutte le lezioni e tutti i bonus sono aperti su questo telefono. Il funzionamento resta lo stesso (una nuova lezione al giorno, tempo davanti allo schermo)."],
 "Retirer le code":["Remove the code","Rimuovi il codice"],"🎟️ Code promo":["🎟️ Promo code","🎟️ Codice promo"],"Valider":["Confirm","Conferma"],
 "Ce code ne marche pas. Vérifiez les {0} caractères.":["This code doesn't work. Check the {0} characters.","Questo codice non funziona. Controllate i {0} caratteri."],
 "Trop d'essais. Réessayez dans {0} s.":["Too many tries. Try again in {0} s.","Troppi tentativi. Riprovate tra {0} s."]}
rep("const UI={","const UI={"+','.join(J(k)+':'+J(v) for k,v in ui.items())+",")
open(p,'w',encoding='utf8').write(h);print('ok')
