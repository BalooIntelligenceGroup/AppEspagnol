import json
p='/home/claude/appespagnol/index.html';h=open(p,encoding='utf8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:80],h.count(a));h=h.replace(a,b)
J=lambda x:json.dumps(x,ensure_ascii=False)

# ---------- 1. Récitations : une ou plusieurs par Niveau, ouvertes quand le Niveau est terminé ----------
for a in ["{after:'saludos',t:","{after:'colores',t:","{after:'numeros',t:","{after:'familia',t:"]:
    rep(a,a.replace("{after:","{tier:1,after:"))
NEW=[
 (2,'Frutas y más','🍓',['Una manzana, una pera,','un plátano en la nevera.','Pan y queso, leche y miel,','¡qué rica está la merienda!']),
 (3,'¿Cómo te llamas?','🙋',['¿Cómo te llamas? Me llamo Sol.','¿Cómo estás? ¡Mejor que mejor!','¿Qué te gusta? Me gusta jugar,','¡cantar, bailar y saltar!']),
 (4,'En el café','☕',['Un café para papá,','un té con leche para mamá.','Y para mí, un chocolate,','¡con churros, por favor!']),
 (5,'En la granja','🐄',['La vaca dice mu, mu, mu,','el pato dice cua, cua, cua.','El gallo canta por la mañana:','¡quiquiriquí, a desayunar!']),
 (6,'Me muevo','🤸',['Salto, salto, como un canguro,','corro, corro, por el parque.','Nado, nado, en la playa,','¡y por la noche, a dormir!']),
 (7,'Bajo el mar','🐠',['Bajo el mar hay un pez,','un pulpo, una ballena y un cangrejo.','Nadan, nadan todo el día,','¡qué bonito es el mar!']),
 (8,'Mi día','⏰',['Me levanto a las siete,','me lavo la cara y los dientes.','Voy al cole con mi mochila,','¡y por la tarde, a jugar!']),
 (9,'Las estaciones','🍂',['En primavera, flores,','en verano, sol y mar.','En otoño caen las hojas,','¡en invierno, a esquiar!']),
 (10,'¡La fiesta!','🎉',['Hoy es mi cumpleaños,','vienen todos mis amigos.','Una tarta con velas,','¡cumpleaños feliz!']),
 (11,'De viaje','🚆',['Mi maleta, mi billete,','el tren sale a las diez.','Voy a Madrid con mi abuela,','¡buen viaje, hasta la vista!']),
]
rep("""l:['Mamá, papá, os quiero.','Mi hermano y mi abuela también.','Toda mi familia junta,','¡qué bien, qué bien, qué bien!']}];""",
"""l:['Mamá, papá, os quiero.','Mi hermano y mi abuela también.','Toda mi familia junta,','¡qué bien, qué bien, qué bien!']},
"""+',\n'.join(' {tier:%d,t:%s,e:%s,l:%s}'%(t,J(ti),J(e),J(l)) for t,ti,e,l in NEW)+"""];
/* Une récitation s'ouvre quand tout son Niveau est terminé (v25). Une récitation déjà ouverte par l'ancienne règle (leçon « after » réussie) le reste. */
const songOk=s=>!!((s.after&&S.stars[s.after])||(stageUnits(s.tier).length&&stageDone(s.tier)));""")
rep("""Chaque récitation s'ouvre avec une leçon.</p>
  <div class="eplist">${SONGS.map((s,i)=>{const ok=!!S.stars[s.after],u=ALL_UNITS.find(x=>x.id===s.after);return""",
"""Les récitations s'ouvrent quand tu termines un niveau.</p>
  <div class="eplist">${SONGS.map((s,i)=>{if(!stageUnits(s.tier).length&&!songOk(s))return '';const ok=songOk(s);return""")
rep("""<small>${ok?'4 lignes à réciter':'Réussis la leçon « '+esc(u?u.es:'')+' »'}</small>""","""<small>${ok?'4 lignes à réciter':'Termine le Niveau '+s.tier+' pour l\\'ouvrir'}</small>""")
rep("else if(a==='songopen'){const i=+b.dataset.i;if(!S.stars[SONGS[i].after])return;","else if(a==='songopen'){const i=+b.dataset.i;if(!songOk(SONGS[i]))return;")
# annonce sur l'écran de fin de leçon
rep("  if(L.unit>=0){const id=UNITS[L.unit].id;newUnit=","  const tierT=L.unit>=0?UNITS[L.unit].tier:0,songs0=SONGS.filter(songOk).length;\n  if(L.unit>=0){const id=UNITS[L.unit].id;newUnit=")
rep("episode:newUnit&&L.unit>=0&&STORY[UNITS[L.unit].id]?L.unit:null};","episode:newUnit&&L.unit>=0&&STORY[UNITS[L.unit].id]?L.unit:null,song:SONGS.filter(songOk).length>songs0?tierT:0};")
rep("""      ${R.episode!=null?`<button class="btn coral" data-act="epopen" data-i="${R.episode}">📖 Nouvel épisode de l'histoire !</button>`:''}""",
"""      ${R.episode!=null?`<button class="btn coral" data-act="epopen" data-i="${R.episode}">📖 Nouvel épisode de l'histoire !</button>`:''}
      ${R.song?`<button class="btn" data-act="songs">📜 Niveau ${R.song} terminé : nouvelle récitation !</button>`:''}""")

# ---------- 2. Le message « Séance du jour » mène à la séance ----------
rep("""${gate?`<p class="hint-bubble">${gate==='seance'?'🎯 Fais d\\'abord ta Séance du jour, puis cette leçon s\\'ouvre !':""",
"""${gate?`<p class="hint-bubble">${gate==='seance'?'<button class="linkbtn" data-act="seance">🎯 Fais d\\'abord ta Séance du jour, puis cette leçon s\\'ouvre ! <u>C\\'est parti →</u></button>':""")
rep("""{const g=newGate(i);if(g){say(g==='seance'?'¡Primero, tu sesión del día!':'¡Mañana!');""",
"""{const g=newGate(i);if(g==='seance'){say('¡Primero, tu sesión del día!');if(guard()&&startSeance())speakStep();return}if(g){say('¡Mañana!');""")

# ---------- 3. Album et 4. Dico : un accordéon par Niveau / par thème ----------
rep("""  ${[1,2,3].map(t=>`<div class="dunit">${TIERS[t][0]} · ${esc(TIERS[t][1])}</div><div class="stk">${stageUnits(t).flatMap(u=>u.words.map(W)).map(w=>stickerOk(w.es)?`<button class="sticker on" data-act="sayw" data-w="${esc(w.es)}"><span>${pic(w.e)}</span><b>${esc(w.es)}</b></button>`:`<div class="sticker"><span>?</span></div>`).join('')}</div>`).join('')}`;""",
"""  <div class="accs">${Object.keys(TIERS).map(Number).filter(t=>stageUnits(t).length).map(t=>{const ws=stageUnits(t).flatMap(u=>u.words.map(W)),n=ws.filter(w=>stickerOk(w.es)).length,k='al'+t;
    if(!aopen.has(k)&&!aopen.has('al-init')&&!stageDone(t)){aopen.add(k);aopen.add('al-init')}
    return `<details class="acc lacc" data-k="${k}" ${aopen.has(k)?'open':''}><summary><span class="acc-t"><b>${TIERS[t][0]} · ${esc(TIERS[t][1])}</b><small>${n} / ${ws.length} autocollants</small></span><span class="acc-n ${n===ws.length?'full':''}">${n}/${ws.length}</span><span class="chev">⌄</span></summary>
    <div class="stk" style="padding:0 12px 14px">${ws.map(w=>stickerOk(w.es)?`<button class="sticker on" data-act="sayw" data-w="${esc(w.es)}"><span>${pic(w.e)}</span><b>${esc(w.es)}</b></button>`:`<div class="sticker"><span>?</span></div>`).join('')}</div></details>`}).join('')}</div>`;""")
rep("""  ${us.length?us.map(u=>`<div class="dunit">${u.e} ${esc(u.es)}</div><div class="dico">${u.words.map(w=>""",
"""  ${us.length?'<div class="accs">'+us.map(u=>`<details class="acc lacc" data-k="dc${u.id}" ${aopen.has('dc'+u.id)?'open':''}><summary><span class="disc-s">${u.e}</span><span class="acc-t"><b>${esc(u.es)}</b><small>${esc(tx(u.es,u.fr))}</small></span><span class="acc-n">${u.words.length}</span><span class="chev">⌄</span></summary><div class="dico" style="padding:0 12px 14px">${u.words.map(w=>""")
rep("""<small>${esc(gx(tx(w[0],w[1]),S.gender))}</small></button>`).join('')}</div>`).join('')""",
"""<small>${esc(gx(tx(w[0],w[1]),S.gender))}</small></button>`).join('')}</div></details>`).join('')+'</div>'""")
rep("let popen=null;","let popen=null;\nconst aopen=new Set();   /* accordéons ouverts de l'album et du dico (le temps de la visite) */")
rep("app.addEventListener('toggle',e=>{const d=e.target;","app.addEventListener('toggle',e=>{const d=e.target;if(d&&d.matches&&d.matches('details.lacc')){d.open?aopen.add(d.dataset.k):aopen.delete(d.dataset.k);return}")
rep("details.acc[open] .chev{transform:rotate(180deg)}","""details.acc[open] .chev{transform:rotate(180deg)}
.accs{display:grid;gap:12px;margin-top:12px}
.acc-n{flex:none;font-weight:800;font-size:15px;background:var(--bg);color:var(--ink);border-radius:999px;padding:4px 10px}.acc-n.full{background:var(--sun)}
.disc-s{flex:none;font-size:30px;line-height:1}
.linkbtn{all:unset;cursor:pointer;display:block;text-align:inherit}.linkbtn u{font-weight:800;color:var(--coral-d)}""")

ui={"Les récitations s'ouvrent quand tu termines un niveau.":["Recitations open when you finish a level.","Le recite si aprono quando finisci un livello."],
 "Termine le Niveau {0} pour l'ouvrir":["Finish Level {0} to open it","Finisci il Livello {0} per aprirla"],
 "📜 Niveau {0} terminé : nouvelle récitation !":["📜 Level {0} finished: new recitation!","📜 Livello {0} finito: nuova recita!"],
 "🎯 Fais d'abord ta Séance du jour, puis cette leçon s'ouvre ! C'est parti →":["🎯 Do your Daily session first, then this lesson opens! Let's go →","🎯 Prima fai la Sessione del giorno, poi questa lezione si apre! Andiamo →"],
 "C'est parti →":["Let's go →","Andiamo →"],
 "{0} / {1} autocollants":["{0} / {1} stickers","{0} / {1} adesivi"]}
rep("const UI={","const UI={"+','.join(J(k)+':'+J(v) for k,v in ui.items())+",")
open(p,'w',encoding='utf8').write(h);print('ok')
