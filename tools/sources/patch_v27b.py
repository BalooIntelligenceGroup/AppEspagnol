import json,sys,re
sys.path.insert(0,'/home/claude');import content_v27 as C
R='/home/claude/appespagnol/';p=R+'index.html';h=open(p,encoding='utf8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:80],h.count(a));h=h.replace(a,b)
J=lambda x:json.dumps(x,ensure_ascii=False)

# ---------- 1. Nom de l'appli ----------
rep("<title>¡Hola Lola!</title>","<title>Petit Polyglotte</title>")

# ---------- 2. Langue apprise : données, transformation du contenu ----------
rep("function tx(es,fr){if(!S.lang||S.lang==='fr')return fr;const t=TRX[es];return t?t[S.lang==='en'?0:1]:fr}",
"""function tx(es,fr){es=TA[es]||es;if(!S.lang||S.lang==='fr')return fr;const t=TRX[es];return t?t[S.lang==='en'?0:1]:fr}
/* ---------- Langue apprise (v27) : es (par défaut, profils existants), en ou it. Une langue par profil (S.target), choisie à la création.
   Le contenu est écrit en espagnol ; pour en/it, setTarget() remplace à la volée mots, titres, répliques (TRX), phrases à trou (TG_GAPS),
   histoires (TG_STORY) et récitations des Niveaux 1-3 (TG_SONGS). TA[texte affiché] = clé espagnole d'origine : sens et traductions passent par elle.
   Anglais et italien : les 15 leçons gratuites seulement pour l'instant (pas de Famille, de Bonus ni d'Ultimate). ---------- */
const TARGETS={es:['Espagnol','🇪🇸','Español'],en:['Anglais','🇬🇧','English'],it:['Italien','🇮🇹','Italiano']};
const TLC={es:'es-ES',en:'en-GB',it:'it-IT'};
let TGT='es';const TA={};
const TG_GAPS="""+J(C.GAPS)+""";
const TG_STORY="""+J(C.STORY)+""";
const TG_SONGS="""+J(C.SONGS)+""";
const TG_OVR="""+J(C.OVR)+""";
const TG_PH=Object.entries("""+J(C.PH)+""").sort((a,b)=>b[0].length-a[0].length);
/* noms de langue dans l'interface : « espagnol » devient la langue apprise */
const TG_LN={en:{fr:[['espagnole','anglaise'],['Espagnole','Anglaise'],['espagnol','anglais'],['Espagnol','Anglais'],['Espagne','Angleterre']],en:[],it:[['dello spagnolo',"dell'inglese"],['lo spagnolo',"l'inglese"],['spagnola','inglese'],['spagnolo','inglese'],['Spagnolo','Inglese'],['Spagna','Inghilterra']]},
 it:{fr:[['espagnole','italienne'],['Espagnole','Italienne'],['espagnol','italien'],['Espagnol','Italien'],['Espagne','Italie']],en:[['Spanish','Italian'],['Spain','Italy']],it:[]}};
function tgUI(t){if(TGT==='es'||!t)return t;const li=TGT==='en'?0:1;
  for(const [a,b] of TG_PH)if(t.includes(a))t=t.split(a).join(b[li]);
  for(const [a,b] of (TG_LN[TGT][S.lang||'fr']||[]))if(t.includes(a))t=t.split(a).join(b);
  return t}
function setTarget(t){
  t=TARGETS[t]?t:'es';TGT=t;for(const k in TA)delete TA[k];
  const li=t==='en'?0:1,TT=es=>(TG_OVR[t]||{})[es]??(TRX[es]?TRX[es][li]:es),al=(x,es)=>{if(x!==es)TA[x]=es;return x};
  ALL_UNITS.forEach(u=>{if(!u._o)u._o={es:u.es,words:u.words,talk:u.talk,gaps:u.gaps};const o=u._o;
    if(t==='es'||!ACTIVE.includes(u.id)){u.es=o.es;u.words=o.words;u.talk=o.talk;u.gaps=o.gaps;return}
    u.es=al(TT(o.es),o.es);
    u.words=o.words.map(w=>{const n=w.slice();n[0]=al(TT(w[0]),w[0]);return n});
    u.talk=(o.talk||[]).map(d=>Object.assign({},d,{l:al(TT(d.l),d.l),o:d.o.map(x=>{const n=x.slice();n[0]=al(TT(x[0]),x[0]);return n})}));
    const G=(TG_GAPS[t]||{})[u.id];
    u.gaps=(o.gaps||[]).map((g,k)=>{const n=G&&G[k];if(!n)return g;al(n[0].replace('_',n[1]),g[0].replace('_',g[1]));return n})});
  Object.keys(STORY).forEach(id=>{const e=STORY[id];if(!e._p)e._p=e.p;const L=t==='es'?null:(TG_STORY[t]||{})[id];e.p=L?e._p.map((pp,k)=>[pp[0],al(L[k],pp[1])]):e._p});
  SONGS.forEach(s=>{if(!s._o)s._o={t:s.t,l:s.l}});
  SONGS.filter(s=>s.tier<=3).forEach((s,k)=>{const n=t==='es'?null:(TG_SONGS[t]||[])[k];if(!n){s.t=s._o.t;s.l=s._o.l}else{s.t=n[0];s.l=n[1].map((x,j)=>al(x,s._o.l[j]))}});
  TRM=null;esVoice=null;uiNamesC=null}""")
# les sens se cherchent toujours avec la clé espagnole d'origine
rep("ALL_UNITS.forEach(u=>{(u.talk||[]).forEach(d=>{if(d.f)TRM[d.l]=d.f;","ALL_UNITS.forEach(u=>{((u._o&&u._o.talk)||u.talk||[]).forEach(d=>{if(d.f)TRM[d.l]=d.f;")
rep("if(u.phr)u.words.forEach(w=>{if(!TRM[w[0]])TRM[w[0]]=w[1]})});","if(u.phr)((u._o&&u._o.words)||u.words).forEach(w=>{if(!TRM[w[0]])TRM[w[0]]=w[1]})});")
rep("const tr=es=>tx(es,trMap()[es]||'');","const tr=es=>{const k=TA[es]||es;return tx(k,trMap()[k]||'')};")
rep("const trOpt=o=>tx(o[0],o.length>2?o[1]:trMap()[o[0]]||'');","const trOpt=o=>{const k=TA[o[0]]||o[0];return tx(k,o.length>2?o[1]:trMap()[k]||'')};")
rep("e:ABSTRACT.has(w[0])?","e:ABSTRACT.has(TA[w[0]]||w[0])?")

# ---------- 3. Voix et micro dans la langue apprise ----------
rep("esVoice=(want&&v.find(x=>x.voiceURI===want))||v.find(x=>/^es[-_]ES/i.test(x.lang))||v.find(x=>/^es/i.test(x.lang))||null",
    "const c=TGT,pre=new RegExp('^'+c,'i');esVoice=(want&&v.find(x=>x.voiceURI===want&&pre.test(x.lang)))||v.find(x=>new RegExp('^'+TLC[c].replace('-','[-_]'),'i').test(x.lang))||v.find(x=>pre.test(x.lang))||null")
rep("function esVoices(){try{return speechSynthesis.getVoices().filter(v=>/^es/i.test(v.lang))}catch(e){return []}}",
    "function esVoices(){try{return speechSynthesis.getVoices().filter(v=>new RegExp('^'+TGT,'i').test(v.lang))}catch(e){return []}}")
rep("const VREG={ES:['🇪🇸','Espagne'],","const VREG={GB:['🇬🇧','Royaume-Uni'],AU:['🇦🇺','Australie'],IE:['🇮🇪','Irlande'],IN:['🇮🇳','Inde'],IT:['🇮🇹','Italie'],CH:['🇨🇭','Suisse'],ES:['🇪🇸','Espagne'],")
rep("const u=new SpeechSynthesisUtterance(nameFill(t));u.lang=esVoice?esVoice.lang:'es-ES';","const u=new SpeechSynthesisUtterance(nameFill(tgUI(t)));u.lang=esVoice?esVoice.lang:TLC[TGT];")
rep("const r=new SR();r.lang='es-ES';","const r=new SR();r.lang=TLC[TGT];")

# ---------- 4. Profil : langue apprise ----------
rep("function loadProfile(id){P.cur=id;saveP();const k=pkey(id);const s=readSave(k)||readSave(k+'-secours');S=Object.assign(def(),s||{});migrate();applyTheme()}",
    "function loadProfile(id){P.cur=id;saveP();const k=pkey(id);const s=readSave(k)||readSave(k+'-secours');S=Object.assign(def(),s||{});if(!S.target&&S.name)S.target='es';migrate();setTarget(S.target);famSync();applyTheme()}")
rep("""  const st=wStep||(!S.name?(S.lang?'name':'lang'):!S.gender?'gender':'theme');
  if(st==='lang'){""","""  const st=wStep||(!S.target?'target':!S.name?(S.lang?'name':'lang'):!S.gender?'gender':'theme');
  if(st==='target'){app.innerHTML=`<div class="center">
    <div class="lola big" aria-hidden="true">🌍</div>
    <h1 style="font-size:30px">Quelle langue veux-tu apprendre ?</h1>
    <div style="width:100%;display:grid;gap:12px">${['en','es','it'].map(k=>`<button class="btn ${S.target===k?'sun':'ghost'} big2" data-act="settarget" data-t="${k}">${TARGETS[k][1]} ${TARGETS[k][2]}</button>`).join('')}</div>
    <p class="note">Which language? · ¿Qué idioma? · Quale lingua?</p>
    ${P.list.length>1?'<button class="btn ghost" data-act="who">←</button>':''}</div>`;return}
  if(st==='lang'){""")
rep("""${Object.entries(LANGS).map(([k,[n,f]])=>`<button class="btn ${pre===k?'sun':'ghost'} big2" data-act="setlang" data-l="${k}">${f} ${n}</button>`).join('')}</div>
    <p class="note">On apprend l'espagnol · We learn Spanish · Impariamo lo spagnolo</p>
    ${P.list.length>1?'<button class="btn ghost" data-act="who">←</button>':''}</div>`;return}""",
"""${Object.entries(LANGS).filter(([k])=>k!==S.target).map(([k,[n,f]])=>`<button class="btn ${pre===k?'sun':'ghost'} big2" data-act="setlang" data-l="${k}">${f} ${n}</button>`).join('')}</div>
    <p class="note">${TARGETS[S.target||'es'][1]} Langue des traductions · Translations · Traduzioni</p>
    <button class="btn ghost" data-act="wback">←</button></div>`;return}""")
rep("const st=wStep||(!S.name?(S.lang?'name':'lang'):!S.gender?'gender':'theme');\n    if(st==='name'){readName();wStep='lang'}",
    "const st=wStep||(!S.target?'target':!S.name?(S.lang?'name':'lang'):!S.gender?'gender':'theme');\n    if(st==='lang'){wStep='target'}\n    else if(st==='name'){readName();wStep='lang'}")
rep("  else if(a==='setlang'){S.lang=b.dataset.l;save();wStep='name';render()}",
    "  else if(a==='setlang'){S.lang=b.dataset.l;save();wStep='name';render()}\n  else if(a==='settarget'){S.target=b.dataset.t;if(S.lang===S.target)S.lang='fr';setTarget(S.target);famSync();save();wStep='lang';render()}")
rep("loadProfile(id);wStep='lang';themeFrom='setup';view='welcome';render()}",
    "loadProfile(id);wStep='target';themeFrom='setup';view='welcome';render()}",2)
# « Qui joue ? » : drapeau de la langue apprise
rep("""<span class="pav">${s.theme?th.e:'🙂'}</span><b>${esc(s.name||'Nouveau joueur')}</b>""",
    """<span class="pav">${s.theme?th.e:'🙂'}</span><b>${esc(s.name||'Nouveau joueur')} ${s.name?TARGETS[s.target||'es'][1]:''}</b>""")
# espace parent : langue apprise affichée, langue des traductions sans la langue apprise
rep("""<span class="acc-t"><b>${esc(s.name||'Nouveau joueur')}</b><small>${s.limit>0?""","""<span class="acc-t"><b>${esc(s.name||'Nouveau joueur')} ${s.name?TARGETS[s.target||'es'][1]:''}</b><small>${s.limit>0?""")
rep("""      <div class="limit"><b>🌍 Langue de l'appli</b>
        <div class="seg three">${Object.entries(LANGS).map(""","""      <div class="limit"><b>🎓 Langue apprise : ${TARGETS[s.target||'es'][1]} ${TARGETS[s.target||'es'][0]}</b><p class="note">Pour apprendre une autre langue, ajoutez un profil : chaque langue garde sa propre progression.</p></div>
      <div class="limit"><b>🌍 Langue de l'appli</b>
        <div class="seg three">${Object.entries(LANGS).filter(([k])=>k!==(s.target||'es')).map(""")

# ---------- 5. Interface : phrases espagnoles et noms de langue ----------
rep("""function i18nText(node){
  if(!S.lang||S.lang==='fr')return;const raw=node.nodeValue;if(!raw||uiDone.get(node)===raw)return;""",
"""function i18nText(node){
  if((!S.lang||S.lang==='fr')&&TGT==='es')return;const raw=node.nodeValue;if(!raw||uiDone.get(node)===raw)return;""")
rep("""  const r=uiT(t);if(r!=null&&r!==t){const lead=raw.match(/^\\s*/)[0],trail=raw.match(/\\s*$/)[0];const v=lead+r+trail;uiDone.set(node,v);node.nodeValue=v}else uiDone.set(node,raw);""",
"""  const r0=uiT(t),r=tgUI(r0!=null?r0:t);if(r!=null&&r!==t){const lead=raw.match(/^\\s*/)[0],trail=raw.match(/\\s*$/)[0];const v=lead+r+trail;uiDone.set(node,v);node.nodeValue=v}else uiDone.set(node,raw);""")
rep("""function i18nAttrs(el){
  if(!S.lang||S.lang==='fr'||el.nodeType!==1)return;""","""function i18nAttrs(el){
  if((!S.lang||S.lang==='fr')&&TGT==='es'||el.nodeType!==1)return;""")
rep("""const r=uiT(v.replace(/\\s+/g,' ').trim());if(r!=null&&r!==v)e.setAttribute(a,r)""","""const r=tgUI(uiT(v.replace(/\\s+/g,' ').trim())??v);if(r!=null&&r!==v)e.setAttribute(a,r)""")

# ---------- 6. Famille, Bonus et Ultimate : espagnol seulement pour l'instant ----------
rep("  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famUltimate()?FAM_UNITS.length:famOpen(famStart())));\n  if(famUltimate())UNITS.push(...EXTRA_UNITS);",
    "  if(TGT!=='es')return;\n  if(famActive())UNITS.push(...FAM_UNITS.slice(0,famUltimate()?FAM_UNITS.length:famOpen(famStart())));\n  if(famUltimate())UNITS.push(...EXTRA_UNITS);")
rep("function famMap(){\n","function famMap(){\n  if(TGT!=='es')return `<div class=\"tier fam\"><b>Bientôt ⭐</b><span>De nouvelles leçons arrivent bientôt !</span></div>`;\n")
rep("function bonusNode(i){\n","function bonusNode(i){\n  if(TGT!=='es')return '';\n")
rep("const songOk=s=>!!((s.after&&S.stars[s.after])","const songOk=s=>!!((s.after&&S.stars[s.after]&&s.tier<=3)")
open(p,'w',encoding='utf8').write(h)

# ---------- 7. Manifeste ----------
m=json.load(open(R+'manifest.webmanifest',encoding='utf8'))
m['name']='Petit Polyglotte';m['short_name']='Petit Polyglotte'
m['description']="Apprendre l'anglais, l'espagnol ou l'italien en s'amusant, 15 minutes et puis s'en vont ! Peu d'écran, beaucoup de mots."
json.dump(m,open(R+'manifest.webmanifest','w',encoding='utf8'),ensure_ascii=False,indent=1)
print('ok')
