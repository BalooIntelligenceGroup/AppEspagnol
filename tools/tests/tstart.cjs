const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();
for(const loc of ['fr-FR','en-GB','it-IT','de-DE']){const ctx=await b.newContext({viewport:{width:400,height:820},locale:loc});const p=await ctx.newPage();
await p.goto('http://localhost:8765/index.html');await p.evaluate(()=>localStorage.clear());await p.reload();await p.waitForTimeout(700);
const t1=await p.evaluate(()=>({view,wStep:typeof wStep!=='undefined'?wStep:null,txt:document.body.innerText.slice(0,300)}));
await p.screenshot({path:S+'start-'+loc+'.png'});
console.log(loc,JSON.stringify(t1));await ctx.close()}
await b.close()})();
