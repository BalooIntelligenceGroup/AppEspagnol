const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const lang of ['fr','en','it']){const ctx=await b.newContext({viewport:{width:400,height:820},locale:lang});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://localhost:8765/index.html');
await p.evaluate(l=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:l,stars:{saludos:3},ver:28,mig12:1,mig13:1,mig22:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{},days:{},coins:20,words:{}}))},lang);
await p.reload();await p.waitForTimeout(700);
console.log(lang,await p.evaluate(()=>{const e=document.querySelector('.newver');return e?e.innerText:'(aucun)'}),errs)}
await b.close()})();
