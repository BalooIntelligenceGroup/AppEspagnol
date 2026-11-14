const {chromium}=require('playwright');const S=''+require('os').tmpdir()+'/';
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:400,height:820},deviceScaleFactor:2,locale:'fr-FR'});
await ctx.addInitScript(()=>{const st=document.createElement('style');st.textContent='#warn{display:none!important}';document.addEventListener('DOMContentLoaded',()=>document.head.appendChild(st))});
await ctx.clock.setFixedTime(new Date('2026-12-03T10:00:00'));
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));const log=(...a)=>console.log(...a);
await p.goto('http://localhost:8765/index.html');
const base={name:'Lola',gender:'f',theme:'jungla',lang:'fr',stars:{saludos:3,colores:3},ver:27,mig12:1,mig13:1,mig22:1,mig23:1,tuto:1,tsetup:1,limit:0,coins:20,days:{},opened:[],evals:{},words:{}};
const setup=(subs,extra)=>p.evaluate(([base,subs,extra])=>{localStorage.clear();localStorage.setItem('hola-lola-v1',JSON.stringify(Object.assign({},base,extra||{})));if(subs)localStorage.setItem('hola-lola-subs',JSON.stringify(subs));setPin('1234');setQ(0,'paris')},[base,subs,extra]);
const grp=()=>p.evaluate(()=>({head:[...document.querySelectorAll('.tier.bon b')].map(x=>x.textContent),nodes:[...document.querySelectorAll('.bonusn')].map(x=>x.dataset.id+':'+x.dataset.act),bon:S.bon}));
// 1. non-abonné
await setup(null);await p.reload();await p.waitForTimeout(500);log('free',await grp());
await p.click('.bonusn');await p.waitForTimeout(300);log('free bubble',await p.evaluate(()=>document.querySelector('.hint-bubble')?.textContent.slice(0,40)));
// 2. abonné Famille espagnol
await setup([{lang:'es',offer:'famille',start:'2026-11-01',period:'month'}]);await p.reload();await p.waitForTimeout(500);log('sub dec 3',await grp());
await p.evaluate(()=>document.querySelector('.tier.bon').scrollIntoView({block:'start'}));await p.screenshot({path:S+'v28-sub.png'});
await p.click('[data-act="bonwait"]');await p.waitForTimeout(300);log('wait bubble',await p.evaluate(()=>document.querySelector('.hint-bubble')?.textContent.slice(0,40)));
// play first bonus lesson (should not count as play day)
await p.click('[data-act="mbonus"]');log('in bonus',await p.evaluate(()=>({view,id:L.u&&L.u.id,steps:L.steps.length})));
await p.evaluate(()=>{L.mistakes=0;finish()});log('after bonus lesson',await p.evaluate(()=>({bonNew:R.bonNew,lv:S.bon.lv})));
// new lesson success = play day
await p.evaluate(()=>{const i=UNITS.findIndex(u=>!S.stars[u.id]);startUnit(i);L.mistakes=0;finish()});await p.waitForTimeout(200);
log('after new lesson',await p.evaluate(()=>({bonNew:R.bonNew,lv:S.bon.lv,btn:document.querySelector('[data-act="home"].btn')?.innerText})));
await p.screenshot({path:S+'v28-result.png'});
// seance same day : no more
await p.evaluate(()=>{startSeance&&startSeance();L.kind='seance';L.mistakes=0;finish()});log('seance same day',await p.evaluate(()=>({bonNew:R.bonNew,lv:S.bon.lv})));
// next day seance
await ctx.clock.setFixedTime(new Date('2026-12-04T10:00:00'));
await p.evaluate(()=>{L={kind:'seance',steps:[],i:0,ok:0,mistakes:0};finish()});log('dec 4 seance',await p.evaluate(()=>({bonNew:R.bonNew,lv:S.bon.lv})));
// january: dec level in Mes niveaux bonus, jan level appears
await ctx.clock.setFixedTime(new Date('2027-01-02T10:00:00'));
await p.evaluate(()=>{view='home';render()});log('jan',await grp());
await p.evaluate(()=>{L={kind:'seance',steps:[],i:0,ok:0,mistakes:0};finish()});log('jan seance -> oldest first',await p.evaluate(()=>S.bon.lv));
// 3. english subscriber
await ctx.clock.setFixedTime(new Date('2026-12-03T10:00:00'));
await setup([{lang:'en',offer:'solo',pid:'p1',start:'2026-12-01',period:'month'}],{target:'en'});await p.reload();await p.waitForTimeout(500);log('en',await grp());
await p.evaluate(()=>document.querySelector('.tier.bon').scrollIntoView({block:'start'}));await p.screenshot({path:S+'v28-en.png'});
await setup([{lang:'it',offer:'famille',start:'2026-12-01',period:'month'}],{target:'it'});await p.reload();await p.waitForTimeout(500);log('it',await grp());
// 4. ultimate (es)
await setup(null);await p.reload();await p.waitForTimeout(300);await p.evaluate(()=>{openGate(null);gateMode='pin';render();$('#pg').value='1234'});await p.click('[data-act="pgok"]');await p.fill('#promo',process.env.BETA_CODE||'');await p.click('[data-act="promo"]');await p.waitForTimeout(400);
await p.evaluate(()=>{view='home';render()});log('ult',await grp());
// 5. audit all bonus units in their language
log('audit',await p.evaluate(()=>{const bad=[];const go=(t)=>{setTarget(t);Object.values(BONUS_LV[t]).forEach(l=>l.ids.forEach(id=>{const u=bonUnit(id);startUnit(-1,u);L.steps.forEach((s,k)=>{L.i=k;L.answered=null;render();if(s.t==='build'&&!document.querySelectorAll('.bank .tile').length)bad.push(id+k);if(s.t==='gap'&&s.g.s.indexOf('_')<0)bad.push('gap'+id)});
   const tr0=u.talk.map(d=>tr(d.l)).filter(x=>!x);if(tr0.length)bad.push('notr '+id);u.gaps.forEach(g=>{if(!tr(g[0].replace('_',g[1])))bad.push('nogapfr '+id)})}))};go('es');go('en');go('it');setTarget(S.target||'es');return bad}));
// play one translate step end-to-end in an EN bonus
log('play en',await p.evaluate(()=>{setTarget('en');startUnit(-1,bonUnit('bx_santa'));L.i=L.steps.findIndex(s=>s.t==='build');render();const s=L.steps[L.i];s.target.forEach(w=>{const k=s.tiles.findIndex((t,x)=>t===w&&!s.used.includes(x));document.querySelector(`.bank [data-k="${k}"]`).click()});const c=document.querySelector('[data-act="check"]');if(c)c.click();return {ok:L.answered&&L.answered.ok}}));
log('ERR',errs);await b.close()})();
