const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await (await b.newContext({locale:'fr-FR'})).newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');
await p.evaluate(()=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:'fr',stars:{saludos:3},ver:26,mig12:1,mig13:1,mig22:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{},days:{},coins:20,words:{}}))});
await p.reload();await p.waitForTimeout(500);
console.log(JSON.stringify(await p.evaluate(()=>{const r={};const run=(i)=>{startUnit(i);const st=L.steps;return {learn:st.filter(s=>s.t==='learn').map(s=>s.w.es).join(','),seq:st.filter(s=>s.t!=='learn').map(sigOf),pos:st.filter(s=>s.opts).map(s=>s.opts.findIndex(o=>s.t==='talk'?isOk(o):s.t==='gap'?o===s.g.a:o.es===(s.w&&s.w.es)))}};
 const i=UNITS.findIndex(u=>u.id==='colores');const runs=[...Array(10)].map(()=>run(i));
 r.learnDistinct=new Set(runs.map(x=>x.learn)).size;
 let sameStart=0,sameSeq=0;for(let k=1;k<runs.length;k++){if(runs[k].seq.slice(0,3).join()==runs[k-1].seq.slice(0,3).join())sameStart++;if(runs[k].seq.join()==runs[k-1].seq.join())sameSeq++}
 r.sameStartConsecutive=sameStart;r.sameSeqConsecutive=sameSeq;
 const pos=runs.flatMap(x=>x.pos);r.answerPositions=[0,1,2].map(n=>pos.filter(v=>v===n).length);
 return r})));console.log('ERR',errs);await b.close()})();
