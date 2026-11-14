import json,sys
sys.path.insert(0,'/home/claude');import content_v28 as C, content_v28x as X, content_v27 as C7
def strs(us):
    out=[]
    for u in us:
        s=[u['t']]+[w[0] for w in u['words']]
        for d in u['talk']: s+= [d['l']]+[o[0] for o in d['o']]
        s+=[g[0].replace('_',g[1]) for g in u['gaps']]
        for x in s:
            if x not in out: out.append(x)
    return out
e=strs(C.EN);i=strs(C.IT)
assert len(e)==len(X.EN_IT),(len(e),len(X.EN_IT));assert len(i)==len(X.IT_EN),(len(i),len(X.IT_EN))
T={}
for s,t in zip(e,X.EN_IT):T[s]=[s,t]
for s,t in zip(i,X.IT_EN):T[s]=[t,s]
T.update(X.ES_WRONG)
# histoires : sens anglais/italien des lignes espagnoles = versions déjà écrites
p='/home/claude/appespagnol/index.html';h=open(p,encoding='utf8').read()
import re
m=re.search(r"const STORY=\{(.*?)\}\};",h,re.S)
for uid,lines in C7.STORY['en'].items():
    es=re.search(uid+r":\{t:'[^']*',p:\[(.*?)\]\]\}",h)
    esl=re.findall(r"\['[^']*','((?:[^'\\]|\\.)*)'\]",es.group(1)+"]") if es else []
    for k,l in enumerate(esl[:3]):T.setdefault(l.replace("\\'","'"),[lines[k],C7.STORY['it'][uid][k]])
J=lambda x:json.dumps(x,ensure_ascii=False)
assert h.count("const TRX={")==1
h=h.replace("const TRX={","const TRX={"+','.join(J(k)+':'+J(v) for k,v in T.items())+",")
open(p,'w',encoding='utf8').write(h);print('entries',len(T))
