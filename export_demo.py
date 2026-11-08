"""Build a self-contained HTML scenario viewer from actual Python simulation results.

The HTML shows precomputed outputs; 'Run simulation' is via Python CLI or app.py.
"""
import json
from pathlib import Path
from aquagrid import SCENARIOS, run_scenario

ROOT = Path(__file__).parent
SNAPSHOTS = {k: run_scenario(k) for k in SCENARIOS}
OUTPUT = ROOT / 'outputs'
OUTPUT.mkdir(exist_ok=True)
for key, result in SNAPSHOTS.items():
    (OUTPUT / f'{key}.json').write_text(json.dumps(result, indent=2), encoding='utf-8')

TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="AquaGrid AI CS3081 milestone prototype demonstration">
  <title>AquaGrid AI | Crisis Simulation Prototype</title>
  <style>
    :root{color-scheme:dark;--bg:#071323;--card:#0c2031;--card2:#0f2939;--border:#1e3d4d;--text:#ecf7fa;--muted:#91a9ba;--mint:#54e0cb;--blue:#6ab9ed;--yellow:#f5be70;--red:#ff6e83}
    *{box-sizing:border-box}html,body{margin:0;background:var(--bg);color:var(--text);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
    body{background-image:radial-gradient(ellipse 65% 45% at 96% 0%,rgba(20,169,190,.13),transparent 68%),radial-gradient(ellipse 50% 34% at 0% 90%,rgba(55,126,218,.09),transparent 85%);min-height:100vh}
    .wrap{max-width:1470px;margin:0 auto;padding:28px 34px 50px}.top{display:flex;justify-content:space-between;align-items:center;padding-bottom:28px;border-bottom:1px solid var(--border)}
    .brand{font-size:25px;letter-spacing:-.9px;font-weight:850;display:flex;align-items:center;gap:13px}.brand-mark{display:grid;place-items:center;width:37px;height:37px;background:linear-gradient(135deg,#22d8bd,#2b83be);border-radius:12px;color:#032132;font-size:26px;font-weight:900}.brand span{color:var(--mint)}
    .topright{display:flex;gap:12px;align-items:center}.badge{border:1px solid #2e5263;border-radius:22px;padding:7px 11px;color:#a9c2cf;font-size:11px;font-weight:700;letter-spacing:1px;text-transform:uppercase}.dot{display:inline-block;background:#62d8bf;border-radius:50%;height:8px;width:8px;margin-right:6px}
    .hero{display:flex;justify-content:space-between;gap:35px;align-items:flex-end;margin:35px 0 27px}.eyebrow{color:var(--mint);font-size:12px;letter-spacing:2.6px;font-weight:800}.hero h1{font-size:clamp(31px,3vw,48px);letter-spacing:-1.7px;margin:12px 0 10px;line-height:1.09}.hero p{color:var(--muted);margin:0;max-width:700px;line-height:1.7;font-size:15px}.scenario-area{min-width:330px;text-align:right}.scenario-area label{display:block;color:var(--muted);font-size:12px;margin-bottom:9px;text-transform:uppercase;letter-spacing:1.4px;font-weight:750}
    select{background:#133244;color:#f0fafb;border:1px solid #347386;border-radius:10px;padding:13px 16px;width:100%;max-width:365px;font-size:14px;font-weight:650;outline:none;cursor:pointer}
    .notice{font-size:11px;color:#91afbb;margin:11px 0 0;font-style:italic}.grid{display:grid;grid-template-columns:minmax(0,1fr) 350px;gap:18px}.metrics{grid-column:1/-1;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
    .metric{border:1px solid var(--border);background:linear-gradient(150deg,#103045,#0a2133);border-radius:16px;padding:17px 20px;position:relative;overflow:hidden}.metric:after{content:'';position:absolute;width:80px;height:80px;right:-37px;top:-38px;border-radius:100%;background:rgba(79,224,201,.08)}.metric-label{color:#a4bbc7;font-size:11px;font-weight:750;text-transform:uppercase;letter-spacing:1px}.metric-value{font-size:32px;font-weight:850;letter-spacing:-.9px;margin:9px 0 2px}.metric-note{font-size:12px;color:#92a8b5}.metric:nth-child(2) .metric-value{color:var(--mint)}.metric:nth-child(3) .metric-value{color:var(--blue)}.metric:nth-child(4) .metric-value{color:var(--yellow)}
    .panel{border:1px solid var(--border);background:rgba(12,32,49,.94);border-radius:16px;min-width:0;overflow:hidden}.panel-header{display:flex;justify-content:space-between;gap:12px;align-items:center;padding:18px 22px;border-bottom:1px solid var(--border)}.panel-title{font-size:16px;font-weight:800;letter-spacing:-.3px}.mini{font-size:11px;color:var(--muted)}.network{height:452px;padding:12px 16px 0}.network svg{width:100%;height:100%;overflow:visible}.legend{display:flex;gap:22px;flex-wrap:wrap;align-items:center;margin:0 22px 19px;color:#a9c1cc;font-size:12px}.key{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:7px}.pipe-key{height:3px;width:16px;display:inline-block;vertical-align:middle;margin-right:7px;background:#66b7d2}.red-key{background:var(--red)}
    .statblock{display:flex;justify-content:space-between;padding:14px 20px;border-bottom:1px solid var(--border);gap:15px;font-size:12px}.statblock:last-child{border-bottom:0}.stat-label{color:#a3bdc7}.stat-value{font-weight:750}.critical{color:var(--yellow)}.panel-sub{font-size:11px;font-weight:800;letter-spacing:1.3px;color:var(--mint);text-transform:uppercase;margin-bottom:14px}
    .districts{padding:17px 20px 18px}.district{margin:0 0 16px}.district:last-child{margin-bottom:0}.district-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:7px;font-size:13px}.district-val{color:#bed7e0;font-variant-numeric:tabular-nums;font-size:11px}.track{height:6px;border-radius:6px;background:#183c4d;overflow:hidden}.fill{height:100%;background:linear-gradient(90deg,#2c9ea7,#53e0ca);border-radius:6px}.fill.warn{background:linear-gradient(90deg,#dd984d,#ffc874)}.fill.low{background:linear-gradient(90deg,#bf5067,#f87a8c)}.smallflag{font-size:9px;padding:2px 5px;border:1px solid #8c7442;color:var(--yellow);border-radius:4px;margin-left:6px}
    .secondary{grid-column:1/-1;display:grid;grid-template-columns:1fr 1fr;gap:18px}.foot-panel{padding:20px 22px}.trace{color:#bfd3de;font-size:12px;line-height:1.65;margin:0;padding:0;list-style:none}.trace li{padding:8px 0;border-bottom:1px solid #1c3a4b}.trace li:last-child{border:0}.trace b{color:#7fe1d7}.resource{display:flex;gap:10px;justify-content:space-between;padding:12px 0;border-bottom:1px solid #1c3a4b;font-size:12px}.resource:last-child{border:0}.resource span{color:#96b4c1}.resource strong{color:#e2f5f9}.footer{display:flex;justify-content:space-between;gap:20px;color:#7897a8;font-size:11px;padding-top:26px;line-height:1.55}
    @media(max-width:1000px){.grid{grid-template-columns:1fr}.metrics{grid-template-columns:repeat(2,1fr)}.secondary{grid-template-columns:1fr 1fr}.hero{align-items:stretch}.scenario-area{min-width:240px}}@media(max-width:680px){.wrap{padding:19px 15px 34px}.hero{display:block}.scenario-area{text-align:left;margin:24px 0}.metrics{grid-template-columns:1fr 1fr;gap:8px}.metric{padding:13px}.metric-value{font-size:25px}.grid{gap:11px}.network{height:320px}.secondary{grid-template-columns:1fr}.topright .badge:last-child{display:none}.footer{display:block}.hero h1{letter-spacing:-.7px}}
  </style>
</head>
<body><div class="wrap">
  <header class="top"><div class="brand"><div class="brand-mark">≈</div>AquaGrid<span>AI</span></div><div class="topright"><div class="badge"><span class="dot"></span>ENGINE TESTED</div><div class="badge">CS3081 · MILESTONE 01</div></div></header>
  <div class="hero"><div><div class="eyebrow">MULTI-AGENT SYSTEM · CONCEPT PROTOTYPE</div><h1>Water distribution,<br>under pressure.</h1><p>See how autonomous district, reservoir, network and coordination agents allocate limited supply as conditions change.</p></div><div class="scenario-area"><label for="scenario">Select crisis scenario</label><select id="scenario" aria-label="Choose crisis scenario"></select><div class="notice">Interactive playback of verified Python simulation outputs</div></div></div>
  <main class="grid">
    <section class="metrics" aria-label="Water allocation metrics">
      <div class="metric"><div class="metric-label">Total demand satisfied</div><div class="metric-value" id="m-coverage">–</div><div class="metric-note">Requested volume delivered</div></div>
      <div class="metric"><div class="metric-label">Water delivered</div><div class="metric-value" id="m-delivered">–</div><div class="metric-note">Simulation units / cycle</div></div>
      <div class="metric"><div class="metric-label">Hospital coverage</div><div class="metric-value" id="m-hospital">–</div><div class="metric-note">Critical district priority</div></div>
      <div class="metric"><div class="metric-label">Pipeline failures</div><div class="metric-value" id="m-failures">–</div><div class="metric-note">Simulated network disruptions</div></div>
    </section>
    <section class="panel"><div class="panel-header"><div class="panel-title">Simulated city network</div><div class="mini">2 reservoirs · 6 districts · 16 pipelines</div></div><div class="network"><svg viewBox="0 0 900 520" role="img" aria-label="Water distribution network diagram" id="net"></svg></div><div class="legend"><span><i class="key" style="background:#6bbaf1"></i>Reservoir</span><span><i class="key" style="background:#54e0cb"></i>District</span><span><i class="key" style="background:#f4be73"></i>Hospital</span><span><i class="pipe-key"></i>Flow / pipeline</span><span><i class="pipe-key red-key"></i>Failed pipe</span></div></section>
    <section class="panel"><div class="panel-header"><div class="panel-title">District water service</div><div class="mini" id="district-sub">Demand vs. allocation</div></div><div class="districts" id="districts"></div><div class="statblock"><span class="stat-label">Unmet demand</span><strong class="stat-value" id="m-unmet"></strong></div><div class="statblock"><span class="stat-label">Dispatch transfers</span><strong class="stat-value" id="m-transfers"></strong></div><div class="statblock"><span class="stat-label">Lowest district coverage</span><strong class="stat-value critical" id="m-min"></strong></div></section>
    <section class="secondary"><article class="panel foot-panel"><div class="panel-sub">Agent decision activity</div><div class="mini" id="description" style="margin:-5px 0 8px"></div><ul class="trace" id="trace"></ul></article><article class="panel foot-panel"><div class="panel-sub">Agent roles & constraints</div><div class="resource"><strong>District agents</strong><span>Publish requests and priorities</span></div><div class="resource"><strong>Reservoir agents</strong><span>Offer limited supply</span></div><div class="resource"><strong>Network agent</strong><span>A* feasible route proposals</span></div><div class="resource"><strong>Crisis coordinator</strong><span>Critical-first + round robin</span></div><div class="resource"><strong>Experiment model</strong><span>Single simulated allocation cycle</span></div></article></section>
  </main><div class="footer"><span>Proof-of-concept only. Synthetic numbers; no hydraulic physics or real-city data. Algorithm runs in Python; this offline viewer displays exported scenario results.</span><span>CS3081 · AquaGrid AI · Milestone 01</span></div>
</div><script>
const snapshots = __DATA__;
const selector = document.getElementById('scenario');
const ids = Object.keys(snapshots);
for(const id of ids){const option=document.createElement('option');option.value=id;option.textContent=snapshots[id].scenario;selector.append(option)}
function safe(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function pct(n){return Number(n).toFixed(1).replace(/\.0$/,'')+'%';}
function drawNetwork(s){
  const map=Object.fromEntries(s.nodes.map(n=>[n.id,n]));
  const sx=x=>50 + x*8;const sy=y=>490 - y*4.6;
  const pipes=s.pipes.map(p=>{
    const a=map[p.a],b=map[p.b];const used=p.used/p.capacity;
    const color=p.active ? (p.used ? '#39b8c9':'#25475c') : '#f77688';
    const width=p.active?(p.used?2.5 + used*6.5:2):4;
    return `<line x1="${sx(a.x)}" y1="${sy(a.y)}" x2="${sx(b.x)}" y2="${sy(b.y)}" stroke="${color}" stroke-width="${width}" stroke-linecap="round" ${p.active?'':'stroke-dasharray="9 7"'}><title>${safe(a.label)} ↔ ${safe(b.label)} | ${p.active ? 'Used '+p.used+'/'+p.capacity+' units':'FAILED'}</title></line>`;
  }).join('');
  const nodes=s.nodes.map(n=>{
    const district=s.districts.find(d=>d.id===n.id);
    const isReservoir=n.kind==='reservoir', isCritical=!!district?.critical;
    const col=isReservoir?'#71bcf3':isCritical?'#f2c47a':n.kind==='district'?'#59dfc7':'#668a9f';
    const r=isReservoir?13:n.kind==='district'?12:7;
    const px=sx(n.x),py=sy(n.y);
    const labelY=py + (n.kind==='junction'?24:-21);
    const name=n.label;
    const sub=district?`<text x="${px}" y="${py+31}" font-size="12" text-anchor="middle" fill="#91abb8">${district.delivered}/${district.demand}</text>`:'';
    return `<g><circle cx="${px}" cy="${py}" r="${r+6}" fill="${col}" opacity=".13"/><circle cx="${px}" cy="${py}" r="${r}" fill="#0d2635" stroke="${col}" stroke-width="3"/><circle cx="${px}" cy="${py}" r="${isReservoir?5:3}" fill="${col}"/><text x="${px}" y="${labelY}" text-anchor="middle" font-size="14" font-weight="650" fill="#e0f2f5">${safe(name)}</text>${sub}<title>${safe(name)} ${district?district.satisfaction_pct+'% covered':''}</title></g>`;
  }).join('');
  document.getElementById('net').innerHTML=`<defs><pattern id="gridpat" width="45" height="45" patternUnits="userSpaceOnUse"><path d="M 45 0 L 0 0 0 45" fill="none" stroke="#173347" stroke-width=".65"/></pattern></defs><rect width="900" height="520" fill="url(#gridpat)" opacity=".7"/>${pipes}${nodes}`;
}
function render(id){
  const s=snapshots[id],m=s.metrics;
  document.getElementById('m-coverage').textContent=pct(m.satisfaction_pct);
  document.getElementById('m-delivered').textContent=m.delivered.toLocaleString();
  document.getElementById('m-hospital').textContent=pct(m.hospital_satisfaction_pct);
  document.getElementById('m-failures').textContent=m.failed_pipes;
  document.getElementById('m-unmet').textContent=m.unmet+' units';
  document.getElementById('m-transfers').textContent=m.transfers;
  document.getElementById('m-min').textContent=pct(m.min_district_satisfaction_pct);
  document.getElementById('description').textContent=s.description;
  document.getElementById('districts').innerHTML=s.districts.map(d=>`<div class="district"><div class="district-head"><span>${safe(d.label)}${d.critical?'<span class="smallflag">CRITICAL</span>':''}</span><span class="district-val">${d.delivered}/${d.demand} · ${pct(d.satisfaction_pct)}</span></div><div class="track"><div class="fill ${d.satisfaction_pct<60?'low':d.satisfaction_pct<90?'warn':''}" style="width:${d.satisfaction_pct}%"></div></div></div>`).join('');
  // Aggregate actual transfers so the trace does not repeat every 20-unit dispatch.
  const routeGroups=new Map();
  for(const t of s.transfers){const key=t.destination+'|'+t.path.join('>');const item=routeGroups.get(key)||{...t,units:0};item.units+=t.units;routeGroups.set(key,item)}
  let summary=[`<li><b>REQUESTS:</b> Six district agents requested ${m.total_demand} units; two reservoirs offered ${m.total_supply} units.</li>`];
  if(m.failed_pipes) summary.push('<li><b>ALERT:</b> Hospital main pipeline is blocked. The network agent excludes the failed pipe.</li>');
  const shown=[...routeGroups.values()].filter(t=>t.destination==='D_H').concat([...routeGroups.values()].filter(t=>t.destination!=='D_H')).slice(0,5);
  summary=summary.concat(shown.map(t=>`<li><b>ROUTE:</b> ${safe(t.destination)} received ${t.units} units via ${safe(t.path.join(' → '))}.</li>`));
  summary.push(`<li><b>OUTCOME:</b> ${m.delivered} of ${m.total_demand} requested units delivered.</li>`);
  document.getElementById('trace').innerHTML=summary.join('');
  drawNetwork(s);
}
selector.onchange=()=>render(selector.value);
render('normal');
</script></body></html>'''
(ROOT / 'AquaGrid_Demo.html').write_text(TEMPLATE.replace('__DATA__', json.dumps(SNAPSHOTS, separators=(',', ':'))), encoding='utf-8')
print('Exported offline viewer and 5 JSON scenario results')
