
fetch('league_data.json').then(r=>r.json()).then(data=>{
document.getElementById('league-name').textContent=data.league.name;
document.getElementById('tagline').textContent=data.league.tagline;
document.getElementById('live-label').textContent=data.live.label;
const s=document.getElementById('standings');
data.standings.forEach(x=>{const e=document.createElement('div');e.className='row';e.innerHTML=`<div class="rank">#${x.rank}</div><div><div class="name">${x.manager}</div><div class="team">${x.team}</div><div class="note">${x.note}</div></div><div class="record">${x.record}</div>`;s.appendChild(e)});
const m=document.getElementById('matchups');
data.live.matchups.forEach(x=>{const e=document.createElement('div');e.className='matchup';e.innerHTML=`<div><strong>${x.a}</strong></div><div class="score">${x.a_score.toFixed(2)} — ${x.b_score.toFixed(2)}</div><div class="right"><strong>${x.b}</strong></div>`;m.appendChild(e)});
const a=document.getElementById('awards');
data.awards.forEach(x=>{const e=document.createElement('div');e.className='award';e.innerHTML=`<strong>${x.title}: ${x.winner}</strong><small>${x.detail}</small>`;a.appendChild(e)});
document.getElementById('roast-headline').textContent=data.latest_roast.headline;
document.getElementById('roast-body').textContent=data.latest_roast.body;
document.getElementById('roast-signature').textContent=data.latest_roast.signature;
const h=document.getElementById('shame');
data.hall_of_shame.forEach(x=>{const e=document.createElement('div');e.className='shame';e.innerHTML=`<strong>${x.label}</strong><div>${x.value}</div><small>${x.extra}</small>`;h.appendChild(e)});
}).catch(err=>document.body.insertAdjacentHTML('beforeend',`<pre style="padding:20px">Could not load league_data.json: ${err}</pre>`));
