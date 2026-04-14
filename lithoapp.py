<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Photolithography Process Simulator</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{
  --color-background-primary:#ffffff;
  --color-background-secondary:#f5f5f0;
  --color-background-tertiary:#eeede8;
  --color-background-info:#e6f1fb;
  --color-background-success:#eaf3de;
  --color-background-warning:#faeeda;
  --color-text-primary:#1a1a18;
  --color-text-secondary:#6b6b66;
  --color-text-tertiary:#9c9a92;
  --color-text-info:#185fa5;
  --color-text-success:#3b6d11;
  --color-text-warning:#854f0b;
  --color-border-tertiary:rgba(0,0,0,0.12);
  --color-border-secondary:rgba(0,0,0,0.22);
  --color-border-primary:rgba(0,0,0,0.32);
  --color-border-info:#b5d4f4;
  --color-border-success:#c0dd97;
  --color-border-warning:#fac775;
  --border-radius-md:8px;
  --border-radius-lg:12px;
  --font-sans:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
}
@media (prefers-color-scheme:dark){
  :root{
    --color-background-primary:#1e1e1c;
    --color-background-secondary:#262624;
    --color-background-tertiary:#2c2c2a;
    --color-background-info:#0c447c;
    --color-background-success:#27500a;
    --color-background-warning:#633806;
    --color-text-primary:#e8e6de;
    --color-text-secondary:#b4b2a9;
    --color-text-tertiary:#6b6b66;
    --color-text-info:#85b7eb;
    --color-text-success:#97c459;
    --color-text-warning:#ef9f27;
    --color-border-tertiary:rgba(255,255,255,0.12);
    --color-border-secondary:rgba(255,255,255,0.22);
    --color-border-primary:rgba(255,255,255,0.32);
    --color-border-info:#185fa5;
    --color-border-success:#3b6d11;
    --color-border-warning:#854f0b;
  }
}
body{
  font-family:var(--font-sans);
  background:var(--color-background-tertiary);
  color:var(--color-text-primary);
  min-height:100vh;
  display:flex;
  align-items:flex-start;
  justify-content:center;
  padding:20px;
}
#app{
  width:100%;
  max-width:1100px;
  display:grid;
  grid-template-columns:160px 1fr 210px;
  grid-template-rows:auto 1fr auto auto;
  background:var(--color-background-tertiary);
  border-radius:var(--border-radius-lg);
  overflow:hidden;
  border:0.5px solid var(--color-border-tertiary);
  box-shadow:0 2px 12px rgba(0,0,0,0.08);
}
#top-bar{
  grid-column:1/-1;
  display:flex;
  align-items:center;
  gap:10px;
  padding:10px 14px;
  background:var(--color-background-primary);
  border-bottom:0.5px solid var(--color-border-tertiary);
}
#top-bar h1{
  font-size:14px;
  font-weight:500;
  color:var(--color-text-primary);
  flex:1;
}
.run-btn{
  padding:5px 14px;
  font-size:12px;
  font-weight:500;
  border:0.5px solid var(--color-border-secondary);
  border-radius:var(--border-radius-md);
  background:var(--color-background-primary);
  color:var(--color-text-primary);
  cursor:pointer;
  transition:background .15s;
}
.run-btn:hover{background:var(--color-background-secondary)}
.run-btn.primary{
  background:var(--color-background-info);
  color:var(--color-text-info);
  border-color:var(--color-border-info);
}
#left-panel{
  grid-column:1;
  grid-row:2;
  display:flex;
  flex-direction:column;
  gap:2px;
  padding:10px 8px;
  background:var(--color-background-primary);
  border-right:0.5px solid var(--color-border-tertiary);
}
#left-panel>label{
  font-size:11px;
  font-weight:500;
  color:var(--color-text-secondary);
  padding:0 4px;
  margin-bottom:2px;
  text-transform:uppercase;
  letter-spacing:.04em;
}
.step-btn{
  display:flex;
  align-items:center;
  gap:7px;
  padding:7px 8px;
  border-radius:6px;
  border:0.5px solid transparent;
  background:transparent;
  cursor:pointer;
  font-size:12px;
  color:var(--color-text-primary);
  text-align:left;
  transition:all .15s;
  width:100%;
  font-family:var(--font-sans);
}
.step-btn:hover{background:var(--color-background-secondary)}
.step-btn.active{
  background:var(--color-background-info);
  color:var(--color-text-info);
  border-color:var(--color-border-info);
}
.step-btn .num{
  width:18px;height:18px;
  border-radius:50%;
  background:var(--color-border-tertiary);
  font-size:10px;
  display:flex;
  align-items:center;
  justify-content:center;
  flex-shrink:0;
  font-weight:500;
}
.step-btn.active .num{
  background:var(--color-text-info);
  color:var(--color-background-primary);
}
.step-btn.done .num{
  background:var(--color-background-success);
  color:var(--color-text-success);
}
#center{
  grid-column:2;
  grid-row:2;
  display:flex;
  flex-direction:column;
  align-items:center;
  padding:16px;
  gap:12px;
  background:var(--color-background-secondary);
}
#canvas-wrap{
  width:100%;
  max-width:460px;
  background:var(--color-background-primary);
  border:0.5px solid var(--color-border-tertiary);
  border-radius:var(--border-radius-lg);
  overflow:hidden;
}
canvas{display:block;width:100%}
#step-info{
  width:100%;
  max-width:460px;
  padding:10px 14px;
  background:var(--color-background-primary);
  border:0.5px solid var(--color-border-tertiary);
  border-radius:var(--border-radius-lg);
}
#step-info h3{font-size:13px;font-weight:500;margin-bottom:4px;color:var(--color-text-primary)}
#step-info p{font-size:12px;color:var(--color-text-secondary);line-height:1.5}
#preview-bar{
  width:100%;
  max-width:460px;
  display:flex;
  gap:6px;
  flex-wrap:wrap;
}
.prev-btn{
  flex:1;
  min-width:80px;
  padding:5px 8px;
  font-size:11px;
  border:0.5px solid var(--color-border-secondary);
  border-radius:var(--border-radius-md);
  background:var(--color-background-primary);
  color:var(--color-text-secondary);
  cursor:pointer;
  text-align:center;
  transition:all .15s;
  font-family:var(--font-sans);
}
.prev-btn:hover{background:var(--color-background-secondary);color:var(--color-text-primary)}
.prev-btn.active{
  background:var(--color-background-warning);
  color:var(--color-text-warning);
  border-color:var(--color-border-warning);
}
#right-panel{
  grid-column:3;
  grid-row:2;
  display:flex;
  flex-direction:column;
  gap:14px;
  padding:12px 10px;
  background:var(--color-background-primary);
  border-left:0.5px solid var(--color-border-tertiary);
  overflow-y:auto;
}
.panel-section h4{
  font-size:11px;
  font-weight:500;
  color:var(--color-text-secondary);
  text-transform:uppercase;
  letter-spacing:.04em;
  margin-bottom:6px;
}
.toggle-group{display:flex;gap:4px}
.tog{
  flex:1;
  padding:5px 4px;
  font-size:11px;
  border:0.5px solid var(--color-border-secondary);
  border-radius:6px;
  background:transparent;
  color:var(--color-text-secondary);
  cursor:pointer;
  text-align:center;
  transition:all .15s;
  font-family:var(--font-sans);
}
.tog:hover{background:var(--color-background-secondary)}
.tog.active{
  background:var(--color-background-info);
  color:var(--color-text-info);
  border-color:var(--color-border-info);
}
.mask-grid{display:grid;grid-template-columns:1fr 1fr;gap:4px}
.mask-btn{
  padding:5px;
  font-size:11px;
  border:0.5px solid var(--color-border-secondary);
  border-radius:6px;
  background:transparent;
  color:var(--color-text-secondary);
  cursor:pointer;
  text-align:center;
  display:flex;
  flex-direction:column;
  align-items:center;
  gap:3px;
  transition:all .15s;
  font-family:var(--font-sans);
}
.mask-btn:hover{background:var(--color-background-secondary)}
.mask-btn.active{
  background:var(--color-background-success);
  color:var(--color-text-success);
  border-color:var(--color-border-success);
}
.mask-icon{width:32px;height:22px}
.param-row{
  display:flex;
  align-items:center;
  gap:6px;
  margin-bottom:8px;
}
.param-row label{font-size:11px;color:var(--color-text-secondary);flex:1}
.param-row input[type=range]{flex:2}
.param-row span{
  font-size:11px;
  color:var(--color-text-primary);
  min-width:28px;
  text-align:right;
}
#legend{display:flex;flex-wrap:wrap;gap:6px}
.leg{display:flex;align-items:center;gap:4px;font-size:10px;color:var(--color-text-secondary)}
.leg-dot{width:10px;height:10px;border-radius:2px;flex-shrink:0}
#bottom-bar{
  grid-column:1/-1;
  display:flex;
  align-items:center;
  gap:8px;
  padding:8px 14px;
  background:var(--color-background-primary);
  border-top:0.5px solid var(--color-border-tertiary);
  font-size:11px;
  color:var(--color-text-secondary);
}
#log{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
#compare-wrap{
  display:none;
  grid-column:1/-1;
  background:var(--color-background-secondary);
  padding:10px 14px;
  border-top:0.5px solid var(--color-border-tertiary);
}
#compare-wrap.show{display:grid;grid-template-columns:1fr 1fr;gap:10px}
#compare-wrap h5{
  font-size:11px;
  color:var(--color-text-secondary);
  margin-bottom:4px;
  text-align:center;
}
.cmp-canvas-wrap{
  background:var(--color-background-primary);
  border:0.5px solid var(--color-border-tertiary);
  border-radius:var(--border-radius-md);
  overflow:hidden;
}
.cmp-canvas-wrap canvas{display:block;width:100%}
input[type=range]{
  -webkit-appearance:none;
  height:4px;
  border-radius:2px;
  background:var(--color-border-secondary);
  outline:none;
}
input[type=range]::-webkit-slider-thumb{
  -webkit-appearance:none;
  width:14px;height:14px;
  border-radius:50%;
  background:var(--color-text-info);
  cursor:pointer;
}
</style>
</head>
<body>
<div id="app">
  <div id="top-bar">
    <h1>Photolithography process simulator</h1>
    <button class="run-btn" onclick="prevStep()">&#9664; Back</button>
    <button class="run-btn primary" id="auto-btn" onclick="autoRun()">&#9654; Auto-run</button>
    <button class="run-btn" onclick="nextStep()">Next &#9654;</button>
    <button class="run-btn" id="cmp-btn" onclick="toggleCompare()">Compare</button>
  </div>

  <div id="left-panel">
    <label>Steps</label>
  </div>

  <div id="center">
    <div id="canvas-wrap">
      <canvas id="main-canvas" width="460" height="230"></canvas>
    </div>
    <div id="preview-bar">
      <button class="prev-btn" onclick="quickPreview(0)">Before exposure</button>
      <button class="prev-btn" onclick="quickPreview(1)">After exposure</button>
      <button class="prev-btn" onclick="quickPreview(2)">After develop</button>
      <button class="prev-btn" onclick="quickPreview(3)">Final output</button>
    </div>
    <div id="step-info">
      <h3 id="si-title">Wafer preparation</h3>
      <p id="si-desc">Silicon wafer cleaned and prepared for processing.</p>
    </div>
  </div>

  <div id="right-panel">
    <div class="panel-section">
      <h4>Photoresist type</h4>
      <div class="toggle-group">
        <button class="tog active" id="pr-pos" onclick="setPR('positive')">Positive PR</button>
        <button class="tog" id="pr-neg" onclick="setPR('negative')">Negative PR</button>
      </div>
      <p id="pr-desc" style="font-size:10px;color:var(--color-text-secondary);margin-top:6px;line-height:1.4">
        Exposed regions are dissolved during development.
      </p>
    </div>
    <div class="panel-section">
      <h4>Mask pattern</h4>
      <div class="mask-grid" id="mask-grid"></div>
    </div>
    <div class="panel-section">
      <h4>Parameters</h4>
      <div class="param-row">
        <label>Dose (mJ/cm²)</label>
        <input type="range" min="20" max="200" value="100" id="dose" oninput="updateParam('dose',this.value)">
        <span id="dose-val">100</span>
      </div>
      <div class="param-row">
        <label>Soft bake (°C)</label>
        <input type="range" min="80" max="130" value="100" id="sbake" oninput="updateParam('sbake',this.value)">
        <span id="sbake-val">100</span>
      </div>
      <div class="param-row">
        <label>PEB (°C)</label>
        <input type="range" min="90" max="140" value="110" id="peb" oninput="updateParam('peb',this.value)">
        <span id="peb-val">110</span>
      </div>
      <div class="param-row">
        <label>Etch depth (nm)</label>
        <input type="range" min="10" max="60" value="30" id="etch" oninput="updateParam('etch',this.value)">
        <span id="etch-val">30</span>
      </div>
    </div>
    <div class="panel-section">
      <h4>Legend</h4>
      <div id="legend">
        <div class="leg"><div class="leg-dot" style="background:#4A90D9"></div>Resist</div>
        <div class="leg"><div class="leg-dot" style="background:#9B59B6"></div>Exposed</div>
        <div class="leg"><div class="leg-dot" style="background:#B0B5C0"></div>Substrate</div>
        <div class="leg"><div class="leg-dot" style="background:#E8D5A3"></div>Metal</div>
        <div class="leg"><div class="leg-dot" style="background:#F0E6FF"></div>UV</div>
      </div>
    </div>
  </div>

  <div id="compare-wrap">
    <div>
      <h5>Ideal output</h5>
      <div class="cmp-canvas-wrap">
        <canvas id="ideal-canvas" width="460" height="120"></canvas>
      </div>
    </div>
    <div>
      <h5>Your output</h5>
      <div class="cmp-canvas-wrap">
        <canvas id="your-canvas" width="460" height="120"></canvas>
      </div>
    </div>
  </div>

  <div id="bottom-bar">
    <span id="log">Ready — select a step or press Auto-run</span>
    <span id="step-counter" style="color:var(--color-text-tertiary)">Step 1/9</span>
  </div>
</div>

<script>
const W=460,H=230;

const STEPS=[
  {id:'wafer',  label:'Wafer',    desc:'Silicon wafer cleaned with piranha solution and RCA clean. Surface hydroxyl groups activated for adhesion.'},
  {id:'coat',   label:'Coat',     desc:'Photoresist spin-coated at 3000 RPM. Thickness ~1 µm. Adhesion promoter (HMDS) applied first.'},
  {id:'softbake',label:'Soft bake',desc:'Wafer baked at set temperature to evaporate solvent. Improves adhesion and resist uniformity.'},
  {id:'align',  label:'Align',    desc:'Mask aligned to wafer using alignment marks. Critical for overlay accuracy in multi-layer processes.'},
  {id:'exposure',label:'Exposure',desc:'UV light (365 nm i-line or 193 nm ArF) exposes resist through the mask. Dose controls acid generation in the resist.'},
  {id:'peb',    label:'PEB',      desc:'Post-exposure bake amplifies acid-catalyzed deprotection in chemically amplified resists (CAR).'},
  {id:'develop',label:'Develop',  desc:'TMAH developer dissolves exposed (positive) or unexposed (negative) resist regions. Pattern is revealed.'},
  {id:'etch',   label:'Etch',     desc:'RIE or wet etch transfers pattern into substrate. Remaining resist acts as protective etch mask.'},
  {id:'strip',  label:'Strip',    desc:'Photoresist stripped with O₂ plasma ash or solvent. Final pattern revealed in the substrate material.'}
];

const MASKS=[
  {id:'lines', label:'Lines',  draw:drawMaskLines},
  {id:'dots',  label:'Dots',   draw:drawMaskDots},
  {id:'grid',  label:'Grid',   draw:drawMaskGrid},
  {id:'text',  label:'Logo',   draw:drawMaskText}
];

let state={
  step:0,
  prType:'positive',
  mask:'lines',
  params:{dose:100,sbake:100,peb:110,etch:30},
  autoRunTimer:null,
  previewMode:-1
};

// --- Mask pattern generators ---
function drawMaskLines(x,y,w){
  const segs=[];const pitch=w/6;
  for(let i=0;i<6;i++){if(i%2===0)segs.push({x:x+i*pitch,w:pitch});}
  return segs;
}
function drawMaskDots(x,y,w){
  const segs=[];const pitch=w/7;
  for(let i=1;i<7;i+=2){segs.push({x:x+i*pitch-pitch*0.4,w:pitch*0.8});}
  return segs;
}
function drawMaskGrid(x,y,w){
  const segs=[];const pitch=w/8;
  for(let i=0;i<8;i++){if(i%2===0)segs.push({x:x+i*pitch,w:pitch});}
  return segs;
}
function drawMaskText(x,y,w){
  return [
    {x:x+w*0.10,w:w*0.08},{x:x+w*0.22,w:w*0.08},{x:x+w*0.34,w:w*0.08},
    {x:x+w*0.50,w:w*0.12},{x:x+w*0.68,w:w*0.08},{x:x+w*0.80,w:w*0.08}
  ];
}

function getMaskFn(){return MASKS.find(m=>m.id===state.mask).draw;}

function getExposedSegs(x,y,w){
  const raw=getMaskFn()(x,y,w);
  if(state.prType==='positive') return raw;
  // negative PR: gaps become exposed
  const gaps=[];let prev=x;
  for(const s of raw){
    if(s.x>prev) gaps.push({x:prev,w:s.x-prev});
    prev=s.x+s.w;
  }
  if(prev<x+w) gaps.push({x:prev,w:(x+w)-prev});
  return gaps;
}

// --- Main drawing ---
const canvas=document.getElementById('main-canvas');
const ctx=canvas.getContext('2d');

function draw(){
  const s=state.previewMode>=0?state.previewMode:state.step;
  ctx.clearRect(0,0,W,H);
  drawStep(ctx,s,W,H);
  drawIdealAndYours();
}

function drawStep(c,s,w,h){
  const sub_y=Math.round(h*0.62);
  const sub_h=Math.round(h*0.22);
  const res_y=Math.round(h*0.38);
  const res_h=Math.round(h*0.22);
  const rx=20, rw=w-40;
  const etch_h=Math.round(state.params.etch*0.55);

  // background
  c.fillStyle='#e8e0d0';c.fillRect(0,0,w,h);

  // substrate (always visible after step 0)
  if(s>=0){
    c.fillStyle='#B0B5C0';c.fillRect(rx,sub_y,rw,sub_h);
    c.fillStyle='#9A9FA8';c.fillRect(rx,sub_y,rw,3);
    c.fillStyle='rgba(255,255,255,0.08)';c.fillRect(rx,sub_y,rw,sub_h);
    c.fillStyle='#555';
    c.font='10px '+getComputedStyle(document.body).fontFamily;
    c.textAlign='center';
    c.fillText('Silicon substrate',w/2,sub_y+sub_h*0.55);
  }

  // step 1: resist coated
  if(s>=1&&s<=6){
    c.fillStyle='#4A90D9';c.fillRect(rx,res_y,rw,res_h);
    c.fillStyle='#6BA8E0';c.fillRect(rx,res_y,rw,3);
    c.fillStyle='rgba(255,255,255,0.1)';c.fillRect(rx,res_y,rw,res_h);
    if(s===1){
      c.fillStyle='#2C6FAC';
      c.font='10px '+getComputedStyle(document.body).fontFamily;
      c.textAlign='center';
      c.fillText('photoresist ('+state.prType+')',w/2,res_y+res_h/2+4);
    }
  }

  // step 2: soft bake glow
  if(s===2){
    c.fillStyle='rgba(255,149,0,0.18)';c.fillRect(rx,res_y,rw,res_h);
    c.fillStyle='#CC7700';
    c.font='10px '+getComputedStyle(document.body).fontFamily;
    c.textAlign='center';
    c.fillText('soft bake: '+state.params.sbake+' °C',w/2,res_y-9);
    // heat lines
    c.strokeStyle='rgba(255,149,0,0.3)';c.lineWidth=1;
    for(let i=0;i<5;i++){
      c.beginPath();c.moveTo(rx+30+i*80,res_y-20);
      c.quadraticCurveTo(rx+50+i*80,res_y-30,rx+70+i*80,res_y-20);
      c.stroke();
    }
  }

  // step 3: mask + alignment
  if(s===3){
    // draw mask above resist
    c.fillStyle='#2C3E50';c.fillRect(rx,22,rw,22);
    c.fillStyle='rgba(236,240,241,0.95)';
    const rawSegs=getMaskFn()(rx,22,rw);
    for(const sg of rawSegs) c.fillRect(sg.x,22,sg.w,22);
    c.fillStyle='#2C3E50';
    c.font='10px '+getComputedStyle(document.body).fontFamily;
    c.textAlign='center';
    c.fillText('mask: '+state.mask,w/2,16);
    // resist
    c.fillStyle='#4A90D9';c.fillRect(rx,res_y,rw,res_h);
    c.fillStyle='rgba(255,255,255,0.1)';c.fillRect(rx,res_y,rw,res_h);
    // alignment markers
    c.strokeStyle='rgba(255,200,0,0.6)';c.lineWidth=1.5;
    c.beginPath();c.moveTo(rx+10,sub_y-4);c.lineTo(rx+20,sub_y-4);c.stroke();
    c.beginPath();c.moveTo(rx+rw-10,sub_y-4);c.lineTo(rx+rw-20,sub_y-4);c.stroke();
  }

  // step 4: UV exposure
  if(s===4){
    const mx=rx, mw=rw;
    // mask
    c.fillStyle='#2C3E50';c.fillRect(mx,22,mw,18);
    const rawSegs=getMaskFn()(mx,22,mw);
    c.fillStyle='rgba(236,240,241,0.95)';
    for(const sg of rawSegs) c.fillRect(sg.x,22,sg.w,18);
    // UV glow background
    c.fillStyle='rgba(240,230,255,0.55)';c.fillRect(mx,40,mw,res_y-40);
    // UV beams through openings
    for(const sg of rawSegs){
      const grd=c.createLinearGradient(0,40,0,res_y);
      grd.addColorStop(0,'rgba(160,90,220,0.75)');
      grd.addColorStop(1,'rgba(160,90,220,0.05)');
      c.fillStyle=grd;c.fillRect(sg.x,40,sg.w,res_y-40);
    }
    // UV label
    c.fillStyle='#7B2FBE';
    c.font='10px '+getComputedStyle(document.body).fontFamily;
    c.textAlign='center';
    c.fillText('UV exposure — dose: '+state.params.dose+' mJ/cm²',w/2,15);
    // resist base
    c.fillStyle='#4A90D9';c.fillRect(mx,res_y,mw,res_h);
    // exposed segments
    const expSegs=getExposedSegs(mx,res_y,mw);
    c.fillStyle='#9B59B6';
    for(const sg of expSegs) c.fillRect(sg.x,res_y,sg.w,res_h);
  }

  // step 5: PEB
  if(s===5){
    c.fillStyle='#4A90D9';c.fillRect(rx,res_y,rw,res_h);
    const expSegs=getExposedSegs(rx,res_y,rw);
    c.fillStyle='#8E44AD';
    for(const sg of expSegs) c.fillRect(sg.x,res_y,sg.w,res_h);
    c.fillStyle='rgba(255,107,53,0.12)';c.fillRect(rx,res_y,rw,res_h);
    c.fillStyle='#CC4400';
    c.font='10px '+getComputedStyle(document.body).fontFamily;
    c.textAlign='center';
    c.fillText('PEB: '+state.params.peb+' °C — acid-catalyzed amplification',w/2,res_y-9);
  }

  // step 6: develop
  if(s===6){
    const keptSegs=(state.prType==='positive')?
      getMaskFn()(rx,res_y,rw):
      getExposedSegs(rx,res_y,rw);
    for(const sg of keptSegs){c.fillStyle='#4A90D9';c.fillRect(sg.x,res_y,sg.w,res_h);}
    c.fillStyle='#27AE60';
    c.font='10px '+getComputedStyle(document.body).fontFamily;
    c.textAlign='center';
    c.fillText(state.prType+' PR: '+(state.prType==='positive'?'exposed':'unexposed')+' regions dissolved',w/2,res_y-9);
  }

  // step 7: etch
  if(s===7){
    const keptSegs=(state.prType==='positive')?
      getMaskFn()(rx,res_y,rw):
      getExposedSegs(rx,res_y,rw);
    for(const sg of keptSegs){c.fillStyle='#3A7BC8';c.fillRect(sg.x,res_y,sg.w,res_h);}
    const etchedSegs=(state.prType==='positive')?
      getExposedSegs(rx,res_y,rw):
      getMaskFn()(rx,res_y,rw);
    for(const sg of etchedSegs){
      c.fillStyle='#8A9BA8';c.fillRect(sg.x,sub_y,sg.w,etch_h);
      c.fillStyle='#6B7D88';c.fillRect(sg.x,sub_y,sg.w,3);
    }
    c.fillStyle='#E74C3C';
    c.font='10px '+getComputedStyle(document.body).fontFamily;
    c.textAlign='center';
    c.fillText('RIE etch depth: '+state.params.etch+' nm',w/2,res_y-9);
  }

  // step 8: strip (final)
  if(s===8){
    c.fillStyle='#B0B5C0';c.fillRect(rx,sub_y,rw,sub_h);
    const etchedSegs=(state.prType==='positive')?
      getExposedSegs(rx,res_y,rw):
      getMaskFn()(rx,res_y,rw);
    for(const sg of etchedSegs){
      c.fillStyle='#8A9BA8';c.fillRect(sg.x,sub_y,sg.w,etch_h);
      c.fillStyle='#6B7D88';c.fillRect(sg.x,sub_y,sg.w,3);
    }
    const highSegs=(state.prType==='positive')?
      getMaskFn()(rx,res_y,rw):
      getExposedSegs(rx,res_y,rw);
    c.fillStyle='rgba(39,174,96,0.15)';
    for(const sg of highSegs) c.fillRect(sg.x,sub_y-4,sg.w,sub_h+4);
    c.fillStyle='#27AE60';
    c.font='11px '+getComputedStyle(document.body).fontFamily;
    c.textAlign='center';
    c.fillText('Final pattern — '+state.mask+' | '+state.prType+' PR | etch: '+state.params.etch+' nm',w/2,sub_y-14);
  }
}

// --- Compare canvases ---
function drawIdealAndYours(){
  const ic=document.getElementById('ideal-canvas');
  const yc=document.getElementById('your-canvas');
  if(!ic||!yc)return;
  drawMiniPattern(ic.getContext('2d'),460,120,'positive','lines',30);
  drawMiniPattern(yc.getContext('2d'),460,120,state.prType,state.mask,state.params.etch);
}

function drawMiniPattern(c,w,h,pr,maskId,etchVal){
  const sub_y=Math.round(h*0.42);
  const sub_h=Math.round(h*0.48);
  const etch_h=Math.round(etchVal*0.38);
  c.clearRect(0,0,w,h);
  c.fillStyle='#e8e0d0';c.fillRect(0,0,w,h);
  c.fillStyle='#B0B5C0';c.fillRect(20,sub_y,w-40,sub_h);
  const mx=20,mw=w-40;
  const maskFn=MASKS.find(m=>m.id===maskId).draw;
  const rawSegs=maskFn(mx,0,mw);
  const etchedSegs=(pr==='positive')?
    (()=>{const gaps=[];let prev=mx;for(const s of rawSegs){if(s.x>prev)gaps.push({x:prev,w:s.x-prev});prev=s.x+s.w;}if(prev<mx+mw)gaps.push({x:prev,w:(mx+mw)-prev});return gaps;})():
    rawSegs;
  for(const sg of etchedSegs){
    c.fillStyle='#8A9BA8';c.fillRect(sg.x,sub_y,sg.w,etch_h);
    c.fillStyle='#6B7D88';c.fillRect(sg.x,sub_y,sg.w,2);
  }
  const highSegs=(pr==='positive')?rawSegs:etchedSegs;
  c.fillStyle='rgba(39,174,96,0.15)';
  for(const sg of highSegs) c.fillRect(sg.x,sub_y-3,sg.w,sub_h+3);
}

// --- UI Controls ---
function updateStepButtons(){
  document.querySelectorAll('.step-btn').forEach((b,i)=>{
    b.classList.toggle('active',i===state.step);
    b.classList.toggle('done',i<state.step);
  });
  document.getElementById('step-counter').textContent='Step '+(state.step+1)+'/'+STEPS.length;
  const si=STEPS[state.step];
  document.getElementById('si-title').textContent=si.label;
  document.getElementById('si-desc').textContent=si.desc;
}

function goToStep(i){
  state.step=i;
  state.previewMode=-1;
  document.querySelectorAll('.prev-btn').forEach(b=>b.classList.remove('active'));
  updateStepButtons();
  draw();
  document.getElementById('log').textContent=
    'Step '+(i+1)+': '+STEPS[i].label+' — '+STEPS[i].desc.substring(0,70)+'…';
}

function nextStep(){if(state.step<STEPS.length-1)goToStep(state.step+1);}
function prevStep(){if(state.step>0)goToStep(state.step-1);}

function autoRun(){
  if(state.autoRunTimer){
    clearInterval(state.autoRunTimer);
    state.autoRunTimer=null;
    document.getElementById('auto-btn').textContent='▶ Auto-run';
    return;
  }
  document.getElementById('auto-btn').textContent='⏹ Stop';
  goToStep(0);
  state.autoRunTimer=setInterval(()=>{
    if(state.step>=STEPS.length-1){
      clearInterval(state.autoRunTimer);
      state.autoRunTimer=null;
      document.getElementById('auto-btn').textContent='▶ Auto-run';
      return;
    }
    nextStep();
  },1400);
}

function setPR(type){
  state.prType=type;
  document.getElementById('pr-pos').classList.toggle('active',type==='positive');
  document.getElementById('pr-neg').classList.toggle('active',type==='negative');
  document.getElementById('pr-desc').textContent=type==='positive'?
    'Exposed regions are dissolved during development.':
    'Unexposed regions are dissolved — pattern inverted!';
  draw();
  document.getElementById('log').textContent=
    'Switched to '+type+' photoresist — pattern will be '+(type==='negative'?'inverted':'normal')+'.';
}

function updateParam(p,v){
  state.params[p]=+v;
  document.getElementById(p+'-val').textContent=v;
  draw();
}

function quickPreview(mode){
  const map=[4,5,6,8];
  state.previewMode=map[mode];
  document.querySelectorAll('.prev-btn').forEach((b,i)=>b.classList.toggle('active',i===mode));
  draw();
  const labels=['Before exposure','After exposure','After development','Final output'];
  document.getElementById('log').textContent='Quick preview: '+labels[mode];
}

function toggleCompare(){
  const w=document.getElementById('compare-wrap');
  w.classList.toggle('show');
  if(w.classList.contains('show'))drawIdealAndYours();
}

// --- Build step buttons ---
function buildUI(){
  const panel=document.getElementById('left-panel');
  STEPS.forEach((s,i)=>{
    const b=document.createElement('button');
    b.className='step-btn'+(i===0?' active':'');
    b.innerHTML=`<span class="num">${i+1}</span>${s.label}`;
    b.onclick=()=>goToStep(i);
    panel.appendChild(b);
  });

  // Build mask buttons
  const mg=document.getElementById('mask-grid');
  MASKS.forEach(m=>{
    const b=document.createElement('button');
    b.className='mask-btn'+(m.id===state.mask?' active':'');
    b.id='mask-'+m.id;
    const ic=document.createElement('canvas');
    ic.className='mask-icon';ic.width=64;ic.height=40;
    const c2=ic.getContext('2d');
    c2.fillStyle='#2C3E50';c2.fillRect(0,0,64,40);
    const segs=m.draw(0,0,64);
    c2.fillStyle='rgba(236,240,241,0.95)';
    for(const sg of segs) c2.fillRect(sg.x,0,sg.w,40);
    b.appendChild(ic);
    const lbl=document.createElement('span');
    lbl.textContent=m.label;
    b.appendChild(lbl);
    b.onclick=()=>{
      state.mask=m.id;
      document.querySelectorAll('.mask-btn').forEach(x=>x.classList.remove('active'));
      b.classList.add('active');
      draw();
      document.getElementById('log').textContent='Mask changed to: '+m.label;
    };
    mg.appendChild(b);
  });
}

buildUI();
goToStep(0);
</script>
</body>
</html>
