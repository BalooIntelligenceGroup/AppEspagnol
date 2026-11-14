import json,sys,os
sys.path.insert(0,'/home/claude');import content_v28 as C
R='/home/claude/appespagnol/';p=R+'index.html';h=open(p,encoding='utf8').read()
def rep(a,b,n=1):
    global h
    assert h.count(a)==n,(a[:90],h.count(a));h=h.replace(a,b)
J=lambda x:json.dumps(x,ensure_ascii=False)

# images
keys=sorted(f[:-5] for f in os.listdir(R+'fx') if f.endswith('.webp'))
import re
h=re.sub(r"const FX=new Set\('[^']*'",lambda m:"const FX=new Set('"+' '.join(keys)+"'",h,count=1)
sw=open(R+'sw.js',encoding='utf8').read();sw=re.sub(r"const FXL='[^']*'",lambda m:"const FXL='"+' '.join(keys)+"'",sw,count=1);open(R+'sw.js','w',encoding='utf8').write(sw)

def unit_js(u):
    talk=','.join('{l:%s,f:%s,p:%s,o:%s}'%(J(d['l']),J(d['f']),J(d['p']),J(d['o'])) for d in u['talk'])
    gaps=[g[:4] for g in u['gaps']]
    return '{id:%s,tier:4,conv:true,phr:true,bonus:true,es:%s,fr:%s,e:%s,words:%s,talk:[%s],gaps:%s}'%(J(u['id']),J(u['t']),J(u['fr']),J(u['e']),J(u['words']),talk,J(gaps))
allnew=C.ES[1:]+C.EN+C.IT
lv={'es':{'11':{'t':'¡Vamos de tapas!','fr':"Les tapas d'Espagne",'e':'🫒','ids':['b_tapas']},
          '12':{'t':C.LEVELS['es']['12'][0],'fr':C.LEVELS['es']['12'][1],'e':'🎄','ids':['b_navidad']+[u['id'] for u in C.ES[1:]]},
          '01':{'t':'Los Reyes Magos','fr':'Les Rois mages','e':'👑','ids':['b_reyes']}},
    'en':{'12':{'t':C.LEVELS['en']['12'][0],'fr':C.LEVELS['en']['12'][1],'e':'🎄','ids':[u['id'] for u in C.EN]}},
    'it':{'12':{'t':C.LEVELS['it']['12'][0],'fr':C.LEVELS['it']['12'][1],'e':'🎄','ids':[u['id'] for u in C.IT]}}}

# ---------- données ----------
rep("ALL_UNITS.push(...FAM_UNITS,...MONTHLY.map(b=>b.u));","""ALL_UNITS.push(...FAM_UNITS,...MONTHLY.map(b=>b.u));
/* ---------- Niveaux Bonus du calendrier (v28) : un niveau de 5 leçons par fête, par langue et par mois (clé = numéro du mois).
   Abonnés de la langue : le 1er du mois le niveau apparaît avec sa 1re leçon ouverte (S.bon.lv['AAAA-MM']=1), puis
   1 jour de jeu (Séance du jour ou nouvelle leçon réussie, au plus 1 par jour) = 1 leçon de plus, en servant d'abord le niveau le plus ancien
   pas encore complet. Rien ne disparaît : les niveaux passés vont dans « Mes niveaux bonus » en fin de carte. Ultimate : tout ouvert. ---------- */
const BON_UNITS=[
 """+',\n '.join(unit_js(u) for u in allnew)+"""];
ALL_UNITS.push(...BON_UNITS);
const BONUS_LV="""+J(lv)+""";""")
rep("const PL=['stars','words','evals','opened','seq','newDay','seanceDay','xp'];","const PL=['stars','words','evals','opened','seq','newDay','seanceDay','xp','bon'];")
rep("function famMap(){","""const bonUnit=id=>ALL_UNITS.find(u=>u.id===id);
const bonLv=k=>(BONUS_LV[TGT]||{})[String(k).slice(-2)]||null;
function bonState(){S.bon=S.bon||{lv:{},day:''};S.bon.lv=S.bon.lv||{};return S.bon}
function bonCurKey(){const d=new Date(),mm=String(d.getMonth()+1).padStart(2,'0');return Object.keys(bonState().lv).find(k=>k.slice(-2)===mm)||d.getFullYear()+'-'+mm}
function bonusSync(){if(!famActive()||famUltimate())return;const k=bonCurKey(),b=bonState();if(bonLv(k)&&!b.lv[k]){b.lv[k]=1;save()}}
function bonusDay(){if(!famActive()||famUltimate())return false;bonusSync();const b=bonState(),t=dayPlus(0);if(b.day===t)return false;b.day=t;
  const k=Object.keys(b.lv).sort().find(k=>{const l=bonLv(k);return l&&b.lv[k]<l.ids.length});if(!k)return false;b.lv[k]++;return true}
const BON_BUBBLE=`<p class="hint-bubble">🎁 Chaque jour où tu joues (Séance du jour ou nouvelle leçon), une leçon bonus s'ouvre !</p>`;
function bonusGroup(k,i,cur){const l=bonLv(k);if(!l)return '';const on=famActive(),ult=famUltimate(),n=ult?l.ids.length:(bonState().lv[k]||0);
  const ids=on||ult?l.ids:l.ids.slice(0,1);
  return `<div class="tier bon"><b>🎁 ${cur?'Bonus du mois':'Niveau bonus'} · ${esc(l.t)}</b><span>${esc(l.fr)}${on&&!ult?` · ${Math.min(n,l.ids.length)}/${l.ids.length} ouvertes`:''}</span></div>`+
  ids.map((id,j)=>{const u=bonUnit(id);if(!u)return '';const open=ult||(on&&j<n),st=S.stars[id]||0;
    return `<button class="node bonusn ${open?(st?'done':''):'locked'}" style="transform:translateX(${Math.round(Math.sin((i+j*.9+.5)*1.1)*70)}px)" data-act="${open?'mbonus':on?'bonwait':'fam'}" data-id="${id}" data-k="${k}" data-w="b${k}" aria-label="Leçon bonus : ${esc(tx(u.es,u.fr))}">
      <span class="disc">${open?u.e:'🔒'}</span><span class="stars">${st?'⭐'.repeat(st)+'<span style="opacity:.25">'+'⭐'.repeat(3-st)+'</span>':''}</span>
      <b>${esc(u.es)}</b><em>${esc(tx(u.es,u.fr))}</em>${open?'':`<span class="ctag fam">${on?'🎁 Un jour de jeu':'🔒 Famille'}</span>`}</button>`}).join('')+(famMsg==='b'+k?(on?BON_BUBBLE:FAM_BUBBLE):'')}
/* niveaux bonus passés (abonné) ou tous les autres mois (Ultimate), en fin de carte */
function bonusPast(){const cur=bonCurKey(),ks=famUltimate()?Object.keys(BONUS_LV[TGT]||{}).map(m=>'U-'+m).filter(k=>k.slice(-2)!==cur.slice(-2)):famActive()?Object.keys(bonState().lv).filter(k=>k!==cur).sort():[];
  return ks.length?`<div class="tier fam"><b>🎁 Mes niveaux bonus</b><span>${famUltimate()?'Offre Ultimate':'Gardés pour toujours'}</span></div>`+ks.map((k,j)=>bonusGroup(k,UNITS.length+j*5,false)).join(''):''}
function famMap(){""")
# l'ancienne liste Ultimate des bonus (une leçon par mois) disparaît
rep("""  if(famUltimate()){const cb=monthBonus(),us=MONTHLY.filter(b=>b!==cb).map(b=>b.u);
    return us.length?`<div class="tier fam"><b>Tous les bonus 🎁</b><span>Offre Ultimate</span></div>`+us.map((u,i)=>{const st=S.stars[u.id]||0;
      return `<button class="node bonusn ${st?'done':''}" style="transform:translateX(${Math.round(Math.sin((UNITS.length+i)*1.1)*70)}px)" data-act="mbonus" data-id="${u.id}" aria-label="Bonus : ${esc(tx(u.es,u.fr))}">
      <span class="disc">${u.e}</span><span class="stars">${st?'⭐'.repeat(st)+'<span style="opacity:.25">'+'⭐'.repeat(3-st)+'</span>':''}</span>
      <b>${esc(u.es)}</b><em>${esc(tx(u.es,u.fr))}</em><small class="where">${esc(u.where)}</small></button>`}).join(''):''}
""","  if(famUltimate())return '';\n")
i=h.index("function bonusNode(i){");j=h.index("\nfunction evalNode")
h=h[:i]+"function bonusNode(i){return bonusGroup(bonCurKey(),i,true)}\n"+h[j:]
rep("<em>Termine les ${UNITS.length} leçons</em></div>${famMap()}</div>`;","<em>Termine les ${UNITS.length} leçons</em></div>${famMap()}${bonusPast()}</div>`;")
rep("function home(){\n","function home(){\n  bonusSync();\n")
rep("""  else if(a==='mbonus'){const mb=b.dataset.id?MONTHLY.find(x=>x.u.id===b.dataset.id):monthBonus();if(!mb||!famActive())return;if(!guard())return;startUnit(-1,mb.u);speakStep()}""",
"""  else if(a==='mbonus'){const u=bonUnit(b.dataset.id),l=bonLv(b.dataset.k);if(!u||!l)return;const j=l.ids.indexOf(u.id);
    if(!(famUltimate()||(famActive()&&j>=0&&j<(bonState().lv[b.dataset.k]||0))))return;if(!guard())return;startUnit(-1,u);speakStep()}
  else if(a==='bonwait'){famMsg=b.dataset.w;render();const hb=document.querySelector('.hint-bubble');if(hb)hb.scrollIntoView({block:'center',behavior:'smooth'})}""")
rep("function wordMap(){const m={};UNITS.concat(MONTHLY.map(b=>b.u).filter(u=>S.stars[u.id])).forEach(u=>",
    "function wordMap(){const m={};UNITS.concat(BON_UNITS.concat(MONTHLY.map(b=>b.u)).filter(u=>S.stars[u.id])).forEach(u=>")
# jour de jeu
rep("  if(L.kind==='seance')S.seanceDay=dayPlus(0);\n  save();R={stars,","  if(L.kind==='seance')S.seanceDay=dayPlus(0);\n  const bonNew=(newUnit||L.kind==='seance')?bonusDay():false;\n  save();R={bonNew,stars,")
rep("""      ${R.song?`<button class="btn" data-act="songs">📜 Niveau ${R.song} terminé : nouvelle récitation !</button>`:''}""",
"""      ${R.song?`<button class="btn" data-act="songs">📜 Niveau ${R.song} terminé : nouvelle récitation !</button>`:''}
      ${R.bonNew?`<button class="btn" data-act="home">🎁 Une nouvelle leçon bonus s'est ouverte !</button>`:''}""")
rep(".famset{",".tier.bon{background:var(--coral)}.tier.bon b,.tier.bon span{color:#fff}\n.famset{")

# traductions : sens anglais/italien des leçons espagnoles ; français des phrases à trou
rep("const TRX={","const TRX={"+','.join(J(k)+':'+J(v) for k,v in C.ES_X.items())+",")
fx={}
for u in allnew:
    for g in u['gaps']:fx[g[0].replace('_',g[1])]=g[4]
rep("const FR_EXTRA={","const FR_EXTRA={\n "+',\n '.join(J(k)+':'+J(v) for k,v in fx.items())+",")
ui={"Bonus du mois":["Bonus of the month","Bonus del mese"],"Niveau bonus":["Bonus level","Livello bonus"],"🎁 Mes niveaux bonus":["🎁 My bonus levels","🎁 I miei livelli bonus"],
 "Gardés pour toujours":["Kept forever","Tuoi per sempre"],"· {0}/{1} ouvertes":["· {0}/{1} open","· {0}/{1} aperte"],"Leçon bonus : {0}":["Bonus lesson: {0}","Lezione bonus: {0}"],
 "🎁 Un jour de jeu":["🎁 One day of play","🎁 Un giorno di gioco"],"🎁 Une nouvelle leçon bonus s'est ouverte !":["🎁 A new bonus lesson has opened!","🎁 Si è aperta una nuova lezione bonus!"],
 "🎁 Chaque jour où tu joues (Séance du jour ou nouvelle leçon), une leçon bonus s'ouvre !":["🎁 Every day you play (Daily session or a new lesson), a bonus lesson opens!","🎁 Ogni giorno che giochi (Sessione del giorno o nuova lezione), si apre una lezione bonus!"],
 "Noël et Nouvel An":["Christmas and New Year","Natale e Capodanno"],"Noël":["Christmas","Natale"],"Les tapas d'Espagne":["Tapas from Spain","Le tapas della Spagna"],"Les Rois mages":["The Three Kings","I Re Magi"]}
rep("const UI={","const UI={"+','.join(J(k)+':'+J(v) for k,v in ui.items())+",")
open(p,'w',encoding='utf8').write(h);print('ok',len(allnew))
