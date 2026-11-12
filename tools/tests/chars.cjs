const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();await p.goto('http://localhost:8765/index.html');await p.waitForTimeout(500);
console.log(JSON.stringify(await p.evaluate(()=>{const out={};for(const t of ['es','en','it']){setTarget(t);const set=new Set();
 const units=[...ACTIVE.map(id=>ALL_UNITS.find(u=>u.id===id)),...FAM_UNITS,...EXTRA_UNITS,...Object.values(BONUS_LV[t]||{}).flatMap(l=>l.ids.map(bonUnit)).filter(Boolean)];
 units.forEach(u=>{u.words.forEach(w=>set.add(w[0]));(u.talk||[]).forEach(d=>{set.add(d.l);d.o.forEach(o=>set.add(o[0]))});(u.gaps||[]).forEach(g=>set.add(g[0].replace('_',g[1])))});
 SONGS.forEach(s=>s.l.forEach(l=>set.add(l)));
 out[t]={clips:set.size,chars:[...set].join('').length}}return out})));await b.close()})();
