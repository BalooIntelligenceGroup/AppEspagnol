import sys, json, os
S = '/tmp/claude-0/-home-claude/aa41b3f1-6410-5635-8215-dcdb8c4f13a8/scratchpad/'
keys = sorted(os.path.splitext(f)[0] for f in os.listdir(S + 'fx') if f.endswith('.webp'))
p = open('index.html').read()
def rep(o, n):
    global p
    c = p.count(o)
    if c != 1: sys.exit(f'{c}x: {o[:100]}')
    p = p.replace(o, n)

# mots abstraits : le français à la place d'une image qui ne veut rien dire
rep("const W=w=>({es:gx(w[0],S.gender),fr:gx(w[1],S.gender),e:w[2]});",
    """/* Mots abstraits : aucune image ne les montre bien, on affiche le mot en français à la place */
const ABSTRACT=new Set(['hola','gracias','¿cómo te llamas?','me llamo','¿cómo estás?','yo también','¿qué es?','¿dónde está?','¿quién es?','aquí','allí','no entiendo','otra vez, por favor']);
const W=w=>({es:gx(w[0],S.gender),fr:gx(w[1],S.gender),e:ABSTRACT.has(w[0])?'txt:'+gx(w[1],S.gender):w[2]});
const isTxt=e=>typeof e==='string'&&e.startsWith('txt:');""")
rep("const pic=(e,cls='')=>e[0]==='#'?`<div class=\"swatch ${cls}\" style=\"background:${e}\"></div>`:esc(e);",
    "const pic=(e,cls='')=>isTxt(e)?`<span class=\"pictxt ${cls}\">${esc(e.slice(4))}</span>`:e[0]==='#'?`<div class=\"swatch ${cls}\" style=\"background:${e}\"></div>`:esc(e);")
# pas de doublon « merci / merci »
rep("""<div class="card"><div class="pic">${pic(s.w.e)}</div><div class="es">${esc(s.w.es)}</div><div class="fr">${esc(s.w.fr)}</div></div>
    <div class="tools"><button class="tool" data-act="hear">🔊 Écouter</button><button class="tool" data-act="slow">🐢 Lentement</button>
    ${micOK&&!L.learnDone""",
    """<div class="card"><div class="pic">${pic(s.w.e)}</div><div class="es">${esc(s.w.es)}</div>${isTxt(s.w.e)?'':`<div class="fr">${esc(s.w.fr)}</div>`}</div>
    <div class="tools"><button class="tool" data-act="hear">🔊 Écouter</button><button class="tool" data-act="slow">🐢 Lentement</button>
    ${micOK&&!L.learnDone""")
rep("""<div class="card"><div class="pic">${pic(s.w.e)}</div><div class="es">${esc(s.w.es)}</div><div class="fr">${esc(s.w.fr)}</div></div>
    <div class="tools"><button class="tool" data-act="hear">🔊 Écouter</button><button class="tool" data-act="slow">🐢 Lentement</button>
    ${micOK&&!L.answered""",
    """<div class="card"><div class="pic">${pic(s.w.e)}</div><div class="es">${esc(s.w.es)}</div>${isTxt(s.w.e)?'':`<div class="fr">${esc(s.w.fr)}</div>`}</div>
    <div class="tools"><button class="tool" data-act="hear">🔊 Écouter</button><button class="tool" data-act="slow">🐢 Lentement</button>
    ${micOK&&!L.answered""")
rep("""<button class="opt" data-act="ans" data-k="${k}"><span>${pic(o.e)}</span><span>${esc(o.fr)}</span></button>""",
    """<button class="opt" data-act="ans" data-k="${k}">${isTxt(o.e)?'':`<span>${pic(o.e)}</span>`}<span>${esc(o.fr)}</span></button>""")

FXJS = """
/* ---------- Images 3D : Fluent Emoji © Microsoft Corporation, licence MIT (fichier fx/LICENSE) ----------
   Chaque émoji affiché dans l'appli est remplacé par son image 3D (dossier fx/). Sans image, l'émoji du téléphone reste. */
const FX=new Set('""" + ' '.join(keys) + """'.split(' '));
const FXRE=/\\p{Extended_Pictographic}|\\u20E3/u;
const fxSeg=window.Intl&&Intl.Segmenter?new Intl.Segmenter('fr',{granularity:'grapheme'}):null;
const fxKey=g=>[...g].filter(c=>c!=='\\uFE0F').map(c=>c.codePointAt(0).toString(16)).join('-');
function fxText(node){
  const t=node.nodeValue,par=node.parentNode;
  if(!fxSeg||!t||!FXRE.test(t)||!par||/^(TEXTAREA|SCRIPT|STYLE|TITLE|OPTION)$/.test(par.nodeName))return;
  const frag=document.createDocumentFragment();let buf='',hit=false;
  for(const {segment:g} of fxSeg.segment(t)){
    const k=FXRE.test(g)?fxKey(g):'';
    if(k&&FX.has(k)){if(buf){frag.appendChild(document.createTextNode(buf));buf=''}
      const im=document.createElement('img');im.className='fx';im.src='fx/'+k+'.webp';im.alt=g;im.draggable=false;im.decoding='async';
      im.onerror=()=>im.replaceWith(document.createTextNode(g));frag.appendChild(im);hit=true}
    else buf+=g}
  if(!hit)return;if(buf)frag.appendChild(document.createTextNode(buf));par.replaceChild(frag,node);
}
function fxify(root){
  if(root.nodeType===3)return fxText(root);if(root.nodeType!==1)return;
  const w=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),ns=[];while(w.nextNode())ns.push(w.currentNode);ns.forEach(fxText);
}
try{new MutationObserver(ms=>{for(const m of ms){if(m.type==='characterData')fxText(m.target);else m.addedNodes.forEach(fxify)}})
  .observe(document.body,{childList:true,subtree:true,characterData:true});fxify(document.body)}catch(e){}
"""
rep("loadProfile(P.list.some(x=>x.id===P.cur)?P.cur:P.list[0].id);\nview=", FXJS + "\nloadProfile(P.list.some(x=>x.id===P.cur)?P.cur:P.list[0].id);\nview=")

# crédit dans les réglages
rep("""<div class="set"><p class="note">Version ${APP_VERSION} · ${UNITS.length} niveaux</p>""",
    """<div class="set"><p class="note">Version ${APP_VERSION} · ${UNITS.length} niveaux<br>Images 3D : Fluent Emoji © Microsoft Corporation, licence MIT.</p>""")

rep(""".trad{""", """img.fx{width:1.18em;height:1.18em;object-fit:contain;vertical-align:-.22em;display:inline-block;pointer-events:none;user-select:none;-webkit-user-drag:none}
.pictxt{display:inline-block;max-width:100%;font-family:var(--f-display);font-weight:800;font-size:30px;line-height:1.12;color:var(--lagoon-d);text-align:center;overflow-wrap:anywhere;padding:4px 6px}
.opts.pics .pictxt,.mpic .pictxt,.mcard .pictxt,.sticker .pictxt{font-size:15px;padding:2px}
.bubble-f .pictxt{font-size:11px;line-height:1.05;padding:2px}
.trad{""")
rep("const APP_VERSION=15,", "const APP_VERSION=16,")
rep("""bouton « Traduire » sur les questions."};""", """bouton « Traduire » sur les questions.",
  16:"Nouveau : de belles images en 3D partout dans l'appli ! Pour les mots comme « gracias », tu vois le mot en français."};""")
open('index.html', 'w').write(p)

sw = open('sw.js').read()
sw = sw.replace("hola-lola-v15", "hola-lola-v16").replace("version 13", "version 16")
old = "self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE.map(u=>new Request(u,{cache:'reload'})))));self.skipWaiting()});"
assert old in sw
sw = sw.replace(old, "const FXL='" + ' '.join(keys) + "'.split(' ').map(k=>'fx/'+k+'.webp');\n"
  "/* les images 3D sont mises en cache dès l'installation pour fonctionner hors ligne */\n"
  "self.addEventListener('install',e=>{e.waitUntil(caches.open(C).then(c=>c.addAll(CORE.map(u=>new Request(u,{cache:'reload'}))).then(()=>c.addAll(FXL).catch(()=>{}))));self.skipWaiting()});")
open('sw.js', 'w').write(sw)
print('ok', len(keys))
