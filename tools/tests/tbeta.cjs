const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();
for(const tg of ['es','en','it']){for(const code of [false,true]){const ctx=await b.newContext({viewport:{width:400,height:820},locale:'fr-FR'});const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await ctx.addInitScript(()=>{Date.now=(n=>()=>n)(new Date('2026-12-03T10:00:00').getTime())});
await p.goto('http://localhost:8765/index.html');
await p.evaluate(tg=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify({name:'Lola',gender:'f',theme:'jungla',lang:'fr',target:tg,stars:{},ver:28,seen:28,mig12:1,mig13:1,mig22:1,tuto:1,tsetup:1,limit:0,opened:[],evals:{},days:{},coins:20,words:{}}))},tg);
await p.reload();await p.waitForTimeout(500);
if(code){await p.evaluate(()=>{setPin('1234');setQ(0,'paris');view='parent';render()});await p.fill('#promo',process.env.BETA_CODE||'');await p.click('[data-act="promo"]');await p.waitForTimeout(400);await p.evaluate(()=>{view='home';render()})}
await p.waitForTimeout(300);
const r=await p.evaluate(()=>{famSync();return {lessons:UNITS.length,bonusNodes:document.querySelectorAll('.bonusn').length,bonusOpen:document.querySelectorAll('.bonusn:not(.locked)').length,songs:SONGS.filter(s=>stageUnits(s.tier).length).length,voiceLang:TLC[TGT]}});
console.log(tg,code?'code bêta':'gratuit',JSON.stringify(r),errs);await ctx.close()}}
await b.close()})();
