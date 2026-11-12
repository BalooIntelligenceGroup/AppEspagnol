import json,sys
sys.path.insert(0,'/home/claude')
from content_v28f import L,SONG,TR
P='/home/claude/appespagnol/index.html'
s=open(P,encoding='utf8').read()
J=lambda x:json.dumps(x,ensure_ascii=False)
def rep(a,b,n=1):
    global s
    c=s.count(a)
    assert c==n,(c,a[:80])
    s=s.replace(a,b)
# 1. les 5 leçons du Niveau 5 Famille, après f_finde
def unit(u):
    talk=','.join('{l:%s,f:%s,p:%s,o:%s}'%(J(l),J(f),J(p),J([list(x) for x in o])) for l,f,p,o in u['talk'])
    return ' {id:%s,tier:5,conv:true,phr:true,es:%s,fr:%s,e:%s,words:%s,talk:[%s],gaps:%s}'%(J(u['id']),J(u['es']),J(u['fr']),J(u['e']),J(u['words']),talk,J(u['gaps']))
i=s.index(' {id:"f_finde"');j=s.index('\n',i)
line=s[i:j]
assert line.endswith('}];')
add=''.join(',\n'+unit(u) for u in L)
s=s[:j-2]+add+s[j-2:]
# 2. les anciennes leçons (Ultimate) commencent après le dernier niveau Famille
rep(".map((u,k)=>Object.assign(u,{tier:5+Math.floor(k/5)}));   /* 5 leçons par niveau, comme les autres : Niveaux 5 à 11 */",
    ".map((u,k)=>Object.assign(u,{tier:Math.max(...FAM_UNITS.map(f=>f.tier))+1+Math.floor(k/5)}));   /* 5 leçons par niveau, comme les autres : Niveaux 6 à 12 (après les niveaux Famille) */")
# 3. noms des niveaux
rep("5:['Niveau 5',\"Animaux et nombres\"],6:['Niveau 6',\"Jouer et bouger\"],7:['Niveau 7',\"Nature et voyages\"],8:['Niveau 8',\"Ma journée\"],9:['Niveau 9',\"La maison et les vacances\"],10:['Niveau 10',\"Sortir et raconter\"],11:['Niveau 11',\"Se débrouiller\"]};",
    "5:['Niveau 5',\"Les jours et les imprévus\"],6:['Niveau 6',\"Animaux et nombres\"],7:['Niveau 7',\"Jouer et bouger\"],8:['Niveau 8',\"Nature et voyages\"],9:['Niveau 9',\"Ma journée\"],10:['Niveau 10',\"La maison et les vacances\"],11:['Niveau 11',\"Sortir et raconter\"],12:['Niveau 12',\"Se débrouiller\"]};")
rep('"Animaux et nombres":["Animals and numbers", "Animali e numeri"],','"Les jours et les imprévus":["Days and little troubles", "Giorni e piccoli imprevisti"],"Animaux et nombres":["Animals and numbers", "Animali e numeri"],')
# 4. récitations : les niveaux 5 à 11 deviennent 6 à 12, nouvelle récitation pour le Niveau 5
a=s.index('const SONGS=[');b=s.index('];',a)
blk=s[a:b]
for t in range(11,4,-1):
    blk=blk.replace(' {tier:%d,t:'%t,' {tier:%d,t:'%(t+1))
k=blk.index(' {tier:6,t:')
blk=blk[:k]+' {tier:5,t:%s,e:%s,l:%s},\n'%(J(SONG['t']),J(SONG['e']),J(SONG['l']))+blk[k:]
s=s[:a]+blk+s[b:]
# 5. pas d'évaluation après le Niveau 4 : le 1er niveau suivant s'ouvre quand la leçon d'avant est réussie
rep("if(u.tier!==UNITS[i-1].tier)return !!(S.evals&&S.evals[UNITS[i-1].tier]);",
    "if(u.tier!==UNITS[i-1].tier&&UNITS[i-1].tier<=3)return !!(S.evals&&S.evals[UNITS[i-1].tier]);   /* pas d'évaluation après les niveaux Famille */")
# 6. traductions anglais / italien
i=s.index('const TRX={');j=s.index('};\n',i)+3
s=s[:j]+'Object.assign(TRX,'+J(TR)+');   /* Niveau 5 Famille (v28) */\n'+s[j:]
# 7. accords (garçon)
rep("['divertita','divertito'],","['divertita','divertito'],['perdue','perdu'],['tranquila','tranquilo'],['tranquilla','tranquillo'],")
open(P,'w',encoding='utf8').write(s)
print('ok')
