const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();
for(const [tg,lang] of [['es','fr'],['it','en'],['en','it']]){const ctx=await b.newContext({viewport:{width:400,height:820},locale:lang});
await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#warn{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st))});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');
await p.evaluate(([tg,l])=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:l,target:tg,stars:{saludos:3},ver:28,seen:28,mig12:1,mig13:1,mig22:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{},days:{},coins:20,words:{}}))},[tg,lang]);
await p.reload();await p.waitForTimeout(600);
await p.evaluate(()=>{view='songs';render()});await p.waitForTimeout(200);
const list=await p.evaluate(()=>[...document.querySelectorAll('.epi')].slice(0,2).map(e=>e.innerText.replace(/\n/g,' / ')));
await p.click('.epi');await p.waitForTimeout(200);
const before=await p.evaluate(()=>document.querySelector('[data-act="songtr"]').innerText);
await p.click('[data-act="songtr"]');await p.waitForTimeout(200);
const after=await p.evaluate(()=>({btn:document.querySelector('[data-act="songtr"]').innerText,kara:document.querySelector('.kara').innerText}));
await p.screenshot({path:S+`v29-song-${tg}-${lang}.png`});
console.log(tg,lang,JSON.stringify({list,before,after}),errs);await ctx.close()}
await b.close()})();
