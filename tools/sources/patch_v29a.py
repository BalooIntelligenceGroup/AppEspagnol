import json,sys
sys.path.insert(0,'/home/claude')
from content_v29a import S as ST
P='/home/claude/appespagnol/index.html'
s=open(P,encoding='utf8').read()
J=lambda x:json.dumps(x,ensure_ascii=False)
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80]);s=s.replace(a,b)
i=s.index('const SONGS=[');j=s.index('];',i)+2
s=s[:j]+"\n/* Sens des récitations (v29) : SONG_TR[texte affiché] = [français, anglais, italien], pour les récitations espagnoles et leurs versions anglaise/italienne (Niveaux 1 à 3) */\nconst SONG_TR="+J(ST)+";\nconst songTr=x=>{const v=SONG_TR[x];return v?v[{en:1,it:2}[S.lang]||0]:''};"+s[j:]
rep("""${s.l.map((l,k)=>`<p class="kl ${song.line===k?'on':''} ${song.mode==='me'&&song.line===k?'me':''}">${esc(l)}</p>`).join('')}</div>""",
    """${song.tr?`<p class="klh">${esc(songTr(s.t))}</p>`:''}${s.l.map((l,k)=>`<p class="kl ${song.line===k?'on':''} ${song.mode==='me'&&song.line===k?'me':''}">${esc(l)}${song.tr?`<small class="klt">${esc(songTr(l))}</small>`:''}</p>`).join('')}</div>""")
rep("""<button class="btn sun" data-act="karame">🎤 À moi de réciter</button></div>`;""",
    """<button class="btn sun" data-act="karame">🎤 À moi de réciter</button></div>
  <div class="row" style="justify-content:center;margin-top:8px"><button class="tool" data-act="songtr">${song.tr?'Cacher la traduction':LF()+' Traduire'}</button></div>`;""")
rep("if(a!=='karaplay'&&a!=='karame')karaToken++;","if(a!=='karaplay'&&a!=='karame'&&a!=='songtr')karaToken++;")
rep("  else if(a==='karaplay')karaRun('play');","  else if(a==='karaplay')karaRun('play');\n  else if(a==='songtr'){song.tr=!song.tr;render()}")
rep("<span class=\"ept\"><b>${esc(s.t)}</b><small>","<span class=\"ept\"><b>${esc(s.t)}</b><i class=\"klt\">${esc(songTr(s.t))}</i><small>")
rep(".kl.on{",".klt{display:block;font-family:var(--f-body,inherit);font-size:14px;font-weight:700;font-style:normal;color:var(--muted);line-height:1.3}\n.klh{margin:0 0 4px;font-size:14px;font-weight:800;color:var(--muted)}\n.kl.on{")
rep('"Les jours et les imprévus":[','"Cacher la traduction":["Hide the translation", "Nascondi la traduzione"],"Les jours et les imprévus":[')
open(P,'w',encoding='utf8').write(s);print('ok')
