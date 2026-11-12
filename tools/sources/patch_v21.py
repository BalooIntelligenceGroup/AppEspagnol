import sys
p=open('index.html').read()
def rep(a,b):
    global p
    if p.count(a)!=1: sys.exit('miss '+a[:90])
    p=p.replace(a,b)
rep("const overLimit=()=>S.limit>0&&((S.days||{})[dayPlus(0)]||0)>=(S.limit+extraMin(S))*60&&S.unlockDay!==dayPlus(0);",
"""const isOver=s=>!!s&&s.limit>0&&((s.days||{})[dayPlus(0)]||0)>=(s.limit+extraMin(s))*60&&s.unlockDay!==dayPlus(0);
const overLimit=()=>isOver(S);
/* Quand un enfant a fini son temps sur ce téléphone, choisir ou créer un joueur demande la multiplication */
const anyOver=()=>P.list.some(x=>isOver(profileInfo(x.id)));
let gateNext=null;""")
rep("""<h1 style="font-size:36px">¿Quién juega?</h1><p class="say">Qui joue aujourd'hui ? Chacun garde sa progression.</p>""",
    """<h1 style="font-size:36px">¿Quién juega?</h1><p class="say">Qui joue aujourd'hui ? Chacun garde sa progression.</p>${anyOver()?'<p class="note" style="color:var(--ink);font-weight:800">🔒 Le temps d\\'écran est écoulé aujourd\\'hui : un parent doit choisir le joueur.</p>':''}""")
rep("""  else if(a==='pick'){loadProfile(b.dataset.id);""","""  else if(a==='pick'&&anyOver()){gateNext={act:'pick',id:b.dataset.id};gateQ=null;gateMsg='';view='pgate';render()}
  else if(a==='addp'&&anyOver()){gateNext={act:'addp'};gateQ=null;gateMsg='';view='pgate';render()}
  else if(a==='pick'){loadProfile(b.dataset.id);""")
rep("""  else if(a==='parent'){readName();gateQ=null;""","""  else if(a==='parent'){readName();gateNext=null;gateQ=null;""")
rep("""  else if(a==='who'){readName();""","""  else if(a==='who'){readName();gateNext=null;""")
rep("""if(gateQ&&v===gateQ.a*gateQ.b){view='parent';render()}""",
    """if(gateQ&&v===gateQ.a*gateQ.b){const g=gateNext;gateNext=null;
      if(g&&g.act==='pick'){loadProfile(g.id);wStep=null;themeFrom='setup';view=S.name&&S.gender&&S.theme?'home':'welcome';render()}
      else if(g&&g.act==='addp'){save();const id='p'+Date.now().toString(36);P.list.push({id});loadProfile(id);wStep='lang';themeFrom='setup';view='welcome';render()}
      else{view='parent';render()}}""")
rep("""data-act="settings" aria-label="Retour">←</button><h2>Espace parent</h2></div>
  <div class="set"><p style="margin:0;font-weight:800">Pour les parents""",
    """data-act="${gateNext?'who':'settings'}" aria-label="Retour">←</button><h2>${gateNext?'Choisir le joueur':'Espace parent'}</h2></div>
  <div class="set"><p style="margin:0;font-weight:800">Pour les parents""")
rep('],"Nouveau : la langue de l','],"🔒 Le temps d\'écran est écoulé aujourd\'hui : un parent doit choisir le joueur.":["🔒 Screen time is up for today: a parent must choose the player.","🔒 Il tempo di schermo per oggi è finito: un genitore deve scegliere il giocatore."],"Choisir le joueur":["Choose the player","Scegli il giocatore"],"Nouveau : la langue de l')
rep("const APP_VERSION=20,","const APP_VERSION=21,")
rep("""est bien respecté."};""","""est bien respecté.",
  21:"Le temps d'écran choisi par tes parents est bien respecté."};""")
open('index.html','w').write(p)
print('ok')
