import sys, json, re
sys.path.insert(0, '/home/claude')
from ui_tr import UI, UIP
p = open('index.html').read()
def rep(o, n, cnt=1):
    global p
    c = p.count(o)
    if c != cnt: sys.exit(f'{c}x: {o[:110]}')
    p = p.replace(o, n)

ui_js = json.dumps({k: list(v) for k, v in UI.items()}, ensure_ascii=False, separators=(',', ':'))
uip_js = json.dumps([[k, list(v)] for k, v in UIP.items()], ensure_ascii=False, separators=(',', ':'))

I18N = r"""
/* ---------- Langue de l'interface (v18) ----------
   Toute l'interface est écrite en français ; quand S.lang vaut 'en' ou 'it', chaque texte affiché est traduit
   au moment où il apparaît (même MutationObserver que les images 3D). Clés : texte français où les nombres,
   les prénoms, les noms des compagnons et le texte entre « » deviennent {0}, {1}… (repris tels quels).
   UIP : motifs dont les {n} captent n'importe quel texte, lui-même traduit s'il est connu.
   Nouveau texte français dans l'appli → ajouter sa traduction dans UI (sinon il reste en français). */
const UI=""" + ui_js + r""";
const UIP=""" + uip_js + r""".map(([k,t])=>[new RegExp('^'+k.split(/\{\d+\}/).map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('(.+?)')+'$','u'),t]);
let uiNamesC=null;
function uiNames(){if(uiNamesC)return uiNamesC;const n=new Set(Object.values(THEMES).map(t=>t.es));
  try{P.list.forEach(x=>{const s=x.id===P.cur?S:profileInfo(x.id);if(s&&s.name)n.add(s.name)})}catch(e){}if(S.name)n.add(S.name);
  const ns=[...n].filter(x=>x&&x.length>1).sort((a,b)=>b.length-a.length).map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&'));
  return uiNamesC=new RegExp('«\\s?[^»]*?\\s?»|\\d+'+(ns.length?'|(?<!\\p{L})(?:'+ns.join('|')+')(?!\\p{L})':''),'gu')}
function uiT(t,depth){
  if(!S.lang||S.lang==='fr'||!t)return null;const li=S.lang==='en'?0:1;
  const vals=[];let i=0;const k=t.replace(uiNames(),m=>{if(m[0]==='«'){vals.push(m.replace(/^«\s?|\s?»$/g,''));return '«{'+(i++)+'}»'}vals.push(m);return '{'+(i++)+'}'});
  const e=UI[k];if(e)return e[li].replace(/\{(\d+)\}/g,(m,j)=>{const v=vals[j]??'';return (depth||0)<2&&/\p{L}{3}/u.test(v)&&UI[v]?(uiT(v,(depth||0)+1)??v):v});
  if((depth||0)>2)return null;
  for(const [re,tr] of UIP){const m=t.match(re);if(m)return tr[li].replace(/\{(\d+)\}/g,(x,j)=>{const v=m[+j+1]||'';return uiT(v,(depth||0)+1)??v})}
  return null;
}
const uiDone=new WeakMap();
function i18nText(node){
  if(!S.lang||S.lang==='fr')return;const raw=node.nodeValue;if(!raw||uiDone.get(node)===raw)return;
  const par=node.parentNode;if(!par||/^(TEXTAREA|SCRIPT|STYLE|TITLE)$/.test(par.nodeName))return;
  const t=raw.replace(/\s+/g,' ').trim();if(!t||!/\p{L}/u.test(t))return;
  const r=uiT(t);if(r!=null&&r!==t){const lead=raw.match(/^\s*/)[0],trail=raw.match(/\s*$/)[0];const v=lead+r+trail;uiDone.set(node,v);node.nodeValue=v}else uiDone.set(node,raw);
}
function i18nAttrs(el){
  if(!S.lang||S.lang==='fr'||el.nodeType!==1)return;
  const els=[el,...el.querySelectorAll('[aria-label],[placeholder]')];
  for(const e of els)for(const a of ['aria-label','placeholder']){const v=e.getAttribute&&e.getAttribute(a);if(v){const r=uiT(v.replace(/\s+/g,' ').trim());if(r!=null&&r!==v)e.setAttribute(a,r)}}
}
"""
# brancher la traduction avant les images 3D
rep("/* ---------- Images 3D : Fluent Emoji", I18N + "\n/* ---------- Images 3D : Fluent Emoji")
rep("""function fxText(node){
  const t=node.nodeValue,par=node.parentNode;""", """function fxText(node){
  i18nText(node);
  const t=node.nodeValue,par=node.parentNode;""")
rep("""  if(root.nodeType===3)return fxText(root);if(root.nodeType!==1)return;""",
    """  if(root.nodeType===3)return fxText(root);if(root.nodeType!==1)return;i18nAttrs(root);""")
rep("""  if(S.name&&S.theme&&overLimit()&&!FREE.has(view)){stopAll();view='stop'}""" if False else """  if(S.name&&S.theme&&!FREE.has(view)&&overLimit()){stopAll();view='stop'}""",
    """  uiNamesC=null;document.documentElement.lang=S.lang||'fr';
  if(S.name&&S.theme&&!FREE.has(view)&&overLimit()){stopAll();view='stop'}""")

# jours de la semaine
rep("DN=['D','L','M','M','J','V','S'];", "DN=({en:['S','M','T','W','T','F','S'],it:['D','L','M','M','G','V','S']})[S.lang]||['D','L','M','M','J','V','S'];")
# textes mis à jour
rep("langue de traduction, bouton « Traduire »", "langue de l'appli, bouton « Traduire »")
rep("""<div class="limit"><b>🌍 Langue de traduction</b>""", """<div class="limit"><b>🌍 Langue de l'appli</b>""")
rep("""<p class="note">Langue des traductions des mots et des phrases (après chaque réponse, bouton « Traduire », dico). Les menus restent en français.</p>""",
    """<p class="note">L'appli et les traductions des mots et des phrases s'affichent dans cette langue. L'espagnol reste en espagnol.</p>""")

# choix de la langue au tout début de la création d'un profil
rep("  const st=wStep||(!S.name?'name':!S.gender?'gender':'theme');\n  if(st==='name'){",
    """  const st=wStep||(!S.name?(S.lang?'name':'lang'):!S.gender?'gender':'theme');
  if(st==='lang'){const pre=S.lang||((navigator.language||'fr').slice(0,2));app.innerHTML=`<div class="center">
    <div class="lola big" aria-hidden="true">🌍</div>
    <h1 style="font-size:30px">Langue · Language · Lingua</h1>
    <div style="width:100%;display:grid;gap:12px">${Object.entries(LANGS).map(([k,[n,f]])=>`<button class="btn ${pre===k?'sun':'ghost'} big2" data-act="setlang" data-l="${k}">${f} ${n}</button>`).join('')}</div>
    <p class="note">On apprend l'espagnol · We learn Spanish · Impariamo lo spagnolo</p>
    ${P.list.length>1?'<button class="btn ghost" data-act="who">←</button>':''}</div>`;return}
  if(st==='name'){""")
rep("""    <button class="btn sun" data-act="go">Suivant →</button>
    ${P.list.length>1?'<button class="btn ghost" data-act="who">← Choisir un autre joueur</button>':''}</div>`;return}""",
    """    <button class="btn sun" data-act="go">Suivant →</button>
    <button class="btn ghost" data-act="wback">← Retour</button></div>`;return}""")
rep("""  else if(a==='wback'){const st=wStep||(!S.name?'name':!S.gender?'gender':'theme');
    if(st==='gender')wStep='name';""", """  else if(a==='setlang'){S.lang=b.dataset.l;save();wStep='name';render()}
  else if(a==='wback'){const st=wStep||(!S.name?(S.lang?'name':'lang'):!S.gender?'gender':'theme');
    if(st==='name'){readName();wStep='lang'}
    else if(st==='gender')wStep='name';""")
rep("""  else if(a==='addp'){save();const id='p'+Date.now().toString(36);P.list.push({id});loadProfile(id);wStep='name';""",
    """  else if(a==='addp'){save();const id='p'+Date.now().toString(36);P.list.push({id});loadProfile(id);wStep='lang';""")

rep("const APP_VERSION=17,", "const APP_VERSION=18,")
rep("""directement à ta leçon !"};""", """directement à ta leçon !",
  18:"Nouveau : la langue de l'appli au choix (français, anglais ou italien), à choisir dans l'espace parent."};""")
rep("function totopSync(){totop.hidden=window.scrollY<500||view==='game'}","function totopSync(){totop.hidden=window.scrollY<500||view==='game';totop.setAttribute('aria-label',uiT('Remonter en haut')||'Remonter en haut')}")
open('index.html', 'w').write(p)
print('ok', len(UI), len(UIP))
