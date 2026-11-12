import sys
p = open('index.html').read()
def rep(o, n):
    global p
    c = p.count(o)
    if c != 1: sys.exit(f'{c}x: {o[:100]}')
    p = p.replace(o, n)

TR = r"""
/* ---------- Traductions en français (affichées après la réponse, ou sur demande si le parent l'autorise) ---------- */
const FR_EXTRA={
 '¡Buenos días! Ya es de día.':'Bonjour ! Il fait déjà jour.',
 'Toma tu regalo. — ¡Muchas gracias!':'Voici ton cadeau. — Merci beaucoup !',
 'El plátano es amarillo.':'La banane est jaune.',
 'El tomate es rojo.':'La tomate est rouge.',
 'Uno, dos, tres.':'Un, deux, trois.',
 'Tengo dos manos.':"J'ai deux mains.",
 'El gato dice «miau».':'Le chat fait « miaou ».',
 'El perro dice «guau».':'Le chien fait « ouaf ».',
 'La mamá de mi mamá es mi abuela.':'La maman de ma maman est ma grand-mère.',
 'Mi hermano se llama Hugo. Es un niño.':"Mon frère s'appelle Hugo. C'est un garçon.",
 'El mono come un plátano.':'Le singe mange une banane.',
 'Quiero una naranja, por favor.':"Je veux une orange, s'il te plaît.",
 'La sandía es verde y roja.':'La pastèque est verte et rouge.',
 'Quiero un helado, por favor.':"Je veux une glace, s'il te plaît.",
 'Como pan con queso.':'Je mange du pain avec du fromage.',
 'Hace frío. Me pongo el abrigo.':'Il fait froid. Je mets mon manteau.',
 'Me pongo los zapatos para correr.':'Je mets mes chaussures pour courir.',
 'Duermo en mi cama.':'Je dors dans mon lit.',
 'Me siento en la silla.':"Je m'assois sur la chaise.",
 'Escribo con el lápiz.':"J'écris avec le crayon.",
 'Leo un libro.':'Je lis un livre.',
 'Me llamo Lola.':"Je m'appelle Lola.",
 'Vivo en Francia.':"J'habite en France.",
 'Estoy bien, gracias.':'Je vais bien, merci.',
 'Tengo sed. Quiero agua.':"J'ai soif. Je veux de l'eau.",
 '¡Me encanta el chocolate!':"J'adore le chocolat !",
 '¿El brócoli? No, no me gusta.':"Le brocoli ? Non, je n'aime pas ça.",
 '¿Dónde está el gato? — En la cama.':'Où est le chat ? — Sur le lit.',
 '¿Quién es? — Es mi abuelo.':"Qui est-ce ? — C'est mon grand-père.",
 'No entiendo. Más despacio, por favor.':"Je ne comprends pas. Plus lentement, s'il te plaît.",
 'Otra vez, por favor.':"Encore une fois, s'il te plaît.",
 '¿Qué fruta te gusta, {name}?':'Quel fruit aimes-tu, {name} ?',
 'Me gusta la fresa.':"J'aime la fraise.",
 'Me gusta el zapato.':"J'aime la chaussure.",
 '¿De qué color es el plátano?':'De quelle couleur est la banane ?',
 'Es amarillo.':'Elle est jaune.',
 'Es azul.':'Elle est bleue.',
 '¿Quieres una naranja?':'Tu veux une orange ?',
 'Sí, por favor.':"Oui, s'il te plaît.",
 'Buenas noches.':'Bonne nuit.'};
let TRM=null;
function trMap(){if(TRM)return TRM;TRM={};
  ALL_UNITS.forEach(u=>(u.talk||[]).forEach(d=>{if(d.f)TRM[d.l]=d.f;d.o.forEach(o=>{if(o.length>2)TRM[o[0]]=o[1]})}));
  return Object.assign(TRM,FR_EXTRA)}
const tr=es=>trMap()[es]||'';
const trOpt=o=>o.length>2?o[1]:tr(o[0]);
/* lignes de traduction pour l'encadré « Continuer » */
function trOf(s){
  let out=[];
  if(s.t==='talk'){const right=s.d.o.find(isOk)||s.opts.find(isOk);out=[[G().es+' a dit',fillG(s.d.f||tr(s.d.l))],['Bonne réponse',right?fill(trOpt(right)):'']]}
  else if(s.t==='gap')out=[['',fill(tr(s.g.s.replace('_',s.g.a)))]];
  else if(s.t==='build')out=[['',fill(tr(s.sent))]];
  else if(s.t==='tf')out=[['',`${s.w.es} = ${s.w.fr}`]];
  else if(s.t==='match')out=[['',s.ws.map(w=>`${w.es} = ${w.fr}`).join(' · ')]];
  return out.filter(x=>x[1]);
}
const trBox=s=>{const ls=trOf(s);return ls.length?`<div class="trad">${ls.map(([l,t])=>`<p>🇫🇷 ${l?`<b>${esc(l)} :</b> `:''}${esc(t)}</p>`).join('')}</div>`:''};
"""
rep("function lesson(){", TR + "function lesson(){")

# drapeaux en tête de lesson()
rep("""  const s=L.steps[L.i],pct=L.i/L.steps.length*100;let body=""",
    """  const s=L.steps[L.i],pct=L.i/L.steps.length*100;
  const canT=!!S.trQ&&L.kind!=='eval'&&!L.answered,showT=canT&&L.trI===L.i,trBtn=canT&&!showT?'<button class="tool" data-act="trq">🇫🇷 Traduire</button>':'';
  const trRow=t=>!canT||!t?'':showT?`<div class="frq big">🇫🇷 ${esc(t)}</div>`:`<div class="tools">${trBtn}</div>`;
  let body=""")
# vrai/faux
rep("""    <div class="card"><div class="pic">${pic(s.shown.e)}</div><div class="es">${esc(s.w.es)}</div></div>
    <div class="tools"><button class="tool" data-act="hear">🔊 Écouter</button></div>""",
    """    <div class="card"><div class="pic">${pic(s.shown.e)}</div><div class="es">${esc(s.w.es)}</div>${showT?`<div class="fr">🇫🇷 ${esc(s.w.fr)}</div>`:''}</div>
    <div class="tools"><button class="tool" data-act="hear">🔊 Écouter</button>${trBtn}</div>""")
# construire la phrase
rep("""<button class="speaker sm" data-act="hear" aria-label="Écouter la phrase">🔊</button></div>""",
    """<button class="speaker sm" data-act="hear" aria-label="Écouter la phrase">🔊</button></div>${trRow(fill(tr(s.sent)))}""")
# phrase à trou
rep("""<div class="gapline">${esc(fill(parts[0]))}${hole}${esc(fill(parts[1]||''))}</div></div>""",
    """<div class="gapline">${esc(fill(parts[0]))}${hole}${esc(fill(parts[1]||''))}</div></div>${trRow(fill(tr(s.g.s.replace('_',s.g.a))))}""")
# dialogue
rep("""<div class="es">${esc(fillG(d.l))}</div></div></div>""",
    """<div class="es">${esc(fillG(d.l))}</div>${showT&&(d.f||tr(d.l))?`<div class="frq">🇫🇷 ${esc(fillG(d.f||tr(d.l)))}</div>`:''}</div></div>""")
rep("""    <div class="tools"><button class="tool" data-act="hear">🔊 Réécouter</button></div>""",
    """    <div class="tools"><button class="tool" data-act="hear">🔊 Réécouter</button>${trBtn}</div>""")
rep("""<span>💬</span><span>${esc(fill(o[0]))}</span></button>""",
    """<span>💬</span><span>${esc(fill(o[0]))}${showT&&trOpt(o)?`<small class="frq">${esc(fill(trOpt(o)))}</small>`:''}</span></button>""")
# encadré « Continuer » : traduction
rep("""      ${L.answered.msg?`<p>${L.answered.msg}</p>`:''}<button class="btn" data-act="next">Continuer</button></div>`;""",
    """      ${L.answered.msg?`<p>${L.answered.msg}</p>`:''}${trBox(s)}<button class="btn" data-act="next">Continuer</button></div>`;""")
# action
rep("""  else if(a==='setg'){""", """  else if(a==='trq'){if(L){L.trI=L.i;render()}}
  else if(a==='ptr'){const v=b.dataset.v==='1';editProfile(b.dataset.id,s=>{s.trQ=v});render()}
  else if(a==='setg'){""")
# espace parent
rep("""      <div class="limit"><b>⏳ Temps d'écran maximum par jour</b>""",
    """      <div class="limit"><b>🇫🇷 Bouton « Traduire » sur les questions</b>
        <div class="seg two">${[[0,'Non'],[1,'Oui']].map(([v,t])=>`<button class="${!!s.trQ===!!v?'on':''}" data-act="ptr" data-id="${p.id}" data-v="${v}" aria-pressed="${!!s.trQ===!!v}">${t}</button>`).join('')}</div>
        <p class="note">Utile si vous ne parlez pas espagnol. La traduction s'affiche toujours après la réponse ; le bouton n'apparaît jamais pendant les évaluations.</p></div>
      <div class="limit"><b>⏳ Temps d'écran maximum par jour</b>""")
# styles
rep(""".limit{""", """.trad{background:var(--card);border-radius:14px;padding:8px 12px;margin:2px 0 10px;text-align:left;color:var(--ink)}
.trad p{margin:2px 0!important;font-size:16px;font-weight:700;line-height:1.35}
.frq{display:block;font-size:15px;font-weight:700;color:var(--muted);margin-top:4px;line-height:1.3}
.frq.big{font-size:18px;text-align:center;background:var(--card);border-radius:14px;padding:8px 12px;margin:10px 0 0;color:var(--ink)}
.seg.two{grid-template-columns:repeat(2,1fr)}
.limit{""")
rep("const APP_VERSION=14,", "const APP_VERSION=15,")
rep("""changer « fille ou garçon » dans les réglages."};""", """changer « fille ou garçon » dans les réglages.",
  15:"Nouveau : après chaque réponse, tu vois la traduction en français. Tes parents peuvent aussi activer un bouton « Traduire » sur les questions."};""")
open('index.html', 'w').write(p)
print('ok')
