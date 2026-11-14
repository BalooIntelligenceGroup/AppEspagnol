const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();
for(const [tg,lang] of [['es','fr'],['en','fr'],['it','en']]){const ctx=await b.newContext({viewport:{width:400,height:820},locale:lang});
await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#warn{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st))});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');
await p.evaluate(([tg,l])=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:l,target:tg,stars:{},ver:30,seen:30,mig12:1,mig13:1,mig22:1,mig23:1,mig29:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{},days:{},coins:20,words:{}}))},[tg,lang]);
await p.reload();await p.waitForTimeout(400);
const out=[];
for(const good of [true,false]){
 await p.evaluate(()=>{startUnit(0);L.i=L.steps.findIndex(s=>s.opts&&s.t!=='talk');L.answered=null;render()});
 await p.evaluate(g=>{const s=L.steps[L.i];const k=s.opts.findIndex(o=>(s.t==='gap'?o===s.g.a:o.es===s.w.es)===g);document.querySelector(`[data-act="ans"][data-k="${k}"]`).click()},good);
 await p.waitForTimeout(1100);
 out.push(await p.evaluate(()=>{const c=document.querySelector('.cast-row');return c?((document.querySelector('.cast img')||{}).alt||document.querySelector('.cast').textContent)+' '+c.querySelector('.cbub').innerText.replace(/\n/g,' / '):'NONE'}));
 await p.screenshot({path:S+`v30b-${tg}-${good?'ok':'ko'}.png`});
}
console.log(tg,lang,out,errs);await ctx.close()}
await b.close()})();
