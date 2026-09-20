# Cognitive Command Face Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an original, always-active cyber-digital Cognitive Command face for Alfred and make it the verified local default.

**Architecture:** Add one self-contained face that consumes the existing `core.js` signal bus and is discovered automatically by `server.py`. Keep rendering, responsive layout, state reactions, and honest diagnostics in that face; leave the server, shared core, and existing faces unchanged.

**Tech Stack:** HTML5 Canvas 2D, vanilla JavaScript, existing `core.js`, Python standard-library `unittest`.

**Spec:** `docs/superpowers/specs/2026-09-20-cognitive-command-face-design.md`

## Global Constraints

- Use a deep blue-black field, cyan mesh, amber operational accents, and red only for alerts.
- Keep the mesh continuously active without making it visually frantic.
- Display only real values from `AV`, browser measurements, or the local clock; unsupported values render as `—`.
- Preserve `core.js`, `server.py`, Neural Core, and every other existing face unchanged.
- Add no dependency, build step, server endpoint, theme framework, Batman element, humanoid face, or copied franchise graphic.
- Keep `ai-visualizer.json` untracked; change only its local `face` value after verification passes.

## Review Focus

- No published usage data: omit usage rows instead of inventing percentages; verify in the idle shot with the current default config.
- Microphone denied or flat: listening still renders and the MIC meter honestly reads zero; verify with browser microphone permission denied.
- Unsupported memory and bus-health values: display `—`, never `OK`, `READY`, or another inferred status; verify in every fixed-state shot.
- Narrow or resized viewport: command rails do not cover the mesh or bottom waveform; verify at 720×900 and after resizing from 1920×1080.
- Alert override: red styling remains readable and does not hide state, clock, or waveform data; verify with `?shot=idle&alert=1`.

---

### Task 1: Add a discoverable face shell and contract check

**Files:**

- Create: `tests/test_cognitive_command_face.py`
- Create: `faces/cognitive-command/face.json`
- Create: `faces/cognitive-command/index.html`

**Interfaces:**

- Consumes: `server.list_faces()` and the existing browser global `AV` from `../../core.js`.
- Produces: gallery face id `cognitive-command`; an HTML page that initializes `AV` with microphone input, ticks it every frame, supports deterministic shots, and toggles fullscreen with `F`.

- [ ] **Step 1: Write the failing discovery and core-contract test**

Create `tests/test_cognitive_command_face.py`:

```python
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FACE = ROOT / "faces" / "cognitive-command"
sys.path.insert(0, str(ROOT))

import server  # noqa: E402


class CognitiveCommandFaceTest(unittest.TestCase):
    def test_manifest_is_discovered(self):
        manifest = json.loads((FACE / "face.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["title"], "Cognitive Command")
        self.assertIn("mesh", manifest["tagline"].lower())

        faces = {face["id"]: face for face in server.list_faces()}
        self.assertIn("cognitive-command", faces)
        self.assertEqual(faces["cognitive-command"]["title"], "Cognitive Command")

    def test_page_uses_the_shared_face_contract(self):
        html = (FACE / "index.html").read_text(encoding="utf-8")
        required = (
            '<script src="../../core.js"></script>',
            "AV.init({mic:true})",
            "AV.ready(",
            "AV.tick(dt)",
            "AV.shotRun(frame)",
            "document.documentElement.requestFullscreen()",
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, html)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the contract test and confirm it fails**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: `ERROR` because `faces/cognitive-command/face.json` and `index.html` do not exist.

- [ ] **Step 3: Add the manifest and minimal face shell**

Create `faces/cognitive-command/face.json`:

```json
{
  "title": "Cognitive Command",
  "tagline": "An always-active cyan cognitive mesh surrounded by dense, honest command telemetry."
}
```

Create `faces/cognitive-command/index.html` with this complete shell; Task 2 replaces the empty draw body while preserving the contract:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cognitive Command</title>
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:100%;height:100%;overflow:hidden;background:#01060b;cursor:none}
  canvas{position:fixed;inset:0;width:100vw;height:100vh;display:block}
</style>
</head>
<body>
<canvas id="stage" role="img" aria-label="Alfred Cognitive Command interface"></canvas>
<script src="../../core.js"></script>
<script>
"use strict";
const Q=new URLSearchParams(location.search);
const SHOT=Q.get("shot");
AV.init({mic:true});
AV.ready(a=>{document.title=a.name+" Cognitive Command";});
const cv=document.getElementById("stage"),ctx=cv.getContext("2d");
let W=0,H=0,DPR=1;
function resize(){
  DPR=Math.min(2,devicePixelRatio||1);
  W=innerWidth;H=innerHeight;
  cv.width=Math.round(W*DPR);cv.height=Math.round(H*DPR);
  ctx.setTransform(DPR,0,0,DPR,0,0);
}
function frame(dt){
  AV.tick(dt);
  ctx.fillStyle="#01060b";ctx.fillRect(0,0,W,H);
}
addEventListener("resize",resize);resize();
addEventListener("keydown",e=>{
  if(e.key==="f"||e.key==="F"){
    document.fullscreenElement?document.exitFullscreen()
      :document.documentElement.requestFullscreen();
  }
});
if(SHOT){AV.shotRun(frame)}else{
  let last=performance.now();
  (function loop(ts){const dt=Math.min(100,ts-last);last=ts;frame(dt);requestAnimationFrame(loop)})(last);
}
</script>
</body>
</html>
```

- [ ] **Step 4: Run the contract test and confirm it passes**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: 2 tests pass.

- [ ] **Step 5: Commit the independently discoverable shell**

```powershell
git add tests/test_cognitive_command_face.py faces/cognitive-command/face.json faces/cognitive-command/index.html
git commit -m "feat: add Cognitive Command face shell"
```

### Task 2: Build and verify the living command mesh

**Files:**

- Modify: `tests/test_cognitive_command_face.py`
- Modify: `faces/cognitive-command/index.html`
- Modify locally, never stage: `ai-visualizer.json`

**Interfaces:**

- Consumes: `AV.state`, `AV.env`, `AV.samples`, `AV.micLevel`, `AV.alert`, `AV.label`, `AV.badge`, and `AV.util.usageRows()`.
- Produces: `buildMesh()`, `updateSignals(dt,state)`, `drawBackground(t)`, `drawMesh(t)`, `drawChrome(state)`, `drawWaveforms(state)`, `drawAlertFrame()`, `resize()`, and `frame(dt)` inside the self-contained page.

- [ ] **Step 1: Extend the contract test for renderer and telemetry boundaries**

Add this method to `CognitiveCommandFaceTest`:

```python
    def test_page_contains_renderer_and_honest_telemetry(self):
        html = (FACE / "index.html").read_text(encoding="utf-8")
        required = (
            "function mulberry32(",
            "function buildMesh(",
            "function updateSignals(",
            "function drawBackground(",
            "function drawMesh(",
            "function drawChrome(",
            "function drawWaveforms(",
            "function drawAlertFrame(",
            "AV.util.usageRows()",
            '["MEMORY","—"]',
            '["BUS HEALTH","—"]',
            'Q.get("alert")==="1"',
        )
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, html)

        forbidden = ('["MEMORY","OK"]', '["BUS HEALTH","OK"]')
        for token in forbidden:
            with self.subTest(token=token):
                self.assertNotIn(token, html)
```

- [ ] **Step 2: Run the expanded test and confirm it fails**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: the new renderer test fails on `function mulberry32(`.

- [ ] **Step 3: Implement the deterministic mesh and state model**

Replace the shell script body after `AV.ready(a=>...)` with these exact contracts and values:

```javascript
const U=AV.util;
const CYAN=[80,205,255],PALE=[190,238,255],AMBER=[239,182,94],RED=[255,58,68];
const PROFILE={
  idle:{traffic:1.8,drift:.22,scan:.18,energy:.34},
  listening:{traffic:4.0,drift:.16,scan:.32,energy:.52},
  thinking:{traffic:12.0,drift:.58,scan:1.0,energy:.92},
  speaking:{traffic:8.0,drift:.40,scan:.62,energy:.70},
};
const FORCE_ALERT=Q.get("alert")==="1";
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const TAU=Math.PI*2;
let rng=mulberry32(41),mesh={nodes:[],edges:[],pulses:[]},spawnCarry=0;
let listenMix=0,thinkMix=0,speakMix=0,stateAge=0,previousState="idle";
function buildMesh(){
  rng=mulberry32(41);
  const nodes=Array.from({length:96},(_,i)=>{
    const a=rng()*TAU,r=Math.sqrt(rng());
    return{x:Math.cos(a)*r,y:Math.sin(a)*r*.68,z:(rng()-.5)*.9,
      phase:rng()*TAU,size:1+rng()*1.6,band:i%4};
  });
  const edges=[],seen=new Set();
  // ponytail: O(n²) runs only on resize; add a spatial index only if resize profiling needs it.
  nodes.forEach((n,i)=>{
    nodes.map((m,j)=>({j,d:j===i?Infinity:Math.hypot(n.x-m.x,n.y-m.y,n.z-m.z)}))
      .sort((a,b)=>a.d-b.d).slice(0,3).forEach(({j})=>{
        const a=Math.min(i,j),b=Math.max(i,j),key=`${a}:${b}`;
        if(!seen.has(key)){seen.add(key);edges.push({a,b})}
      });
  });
  mesh={nodes,edges,pulses:[]};spawnCarry=0;
}
function pulseDirection(edge,state){
  const a=mesh.nodes[edge.a],b=mesh.nodes[edge.b];
  const ra=Math.hypot(a.x,a.y,a.z),rb=Math.hypot(b.x,b.y,b.z);
  if(state==="listening")return ra>rb?1:-1;
  if(state==="speaking")return ra<rb?1:-1;
  return rng()<.5?1:-1;
}
function updateSignals(dt,state){
  spawnCarry+=PROFILE[state].traffic*dt/1000;
  while(spawnCarry>=1&&mesh.pulses.length<72){
    spawnCarry--;
    const edge=rng()*mesh.edges.length|0;
    mesh.pulses.push({edge,t:0,speed:.30+rng()*.32,
      dir:pulseDirection(mesh.edges[edge],state)});
  }
  for(const pulse of mesh.pulses)pulse.t+=pulse.speed*dt/1000;
  mesh.pulses=mesh.pulses.filter(pulse=>pulse.t<1);
}
function easeMix(value,target,dt){return value+(target-value)*(1-Math.exp(-dt/280))}
```

Call `buildMesh()` from `resize()`. In `frame(dt)`, reset `stateAge` when `AV.state` changes, then update it and the three mixes with `easeMix`. This preserves one stable mesh identity while state changes crossfade rather than cut.

- [ ] **Step 4: Implement the full command-centre rendering pass**

Add these rendering helpers and keep their data sources unchanged:

```javascript
let field=document.createElement("canvas"),fg=field.getContext("2d");
let micHistory=Array(72).fill(0),now=0,fps=0,fpsCount=0,fpsAt=0;
function rgba(c,a){return`rgba(${c[0]},${c[1]},${c[2]},${a})`}
function projectNode(n,t){
  const yaw=Math.sin(t*.18)*.22+thinkMix*.12,cy=Math.cos(yaw),sy=Math.sin(yaw);
  const x=n.x*cy+n.z*sy,z=-n.x*sy+n.z*cy;
  const perspective=2.7/(2.7+z),scale=Math.min(W,H)*.39;
  return{x:W/2+x*scale*perspective,y:H*.49+n.y*scale*perspective,
    z,perspective};
}
function drawBackground(t){
  const alert=FORCE_ALERT||AV.alert,col=alert?RED:CYAN;
  const g=ctx.createRadialGradient(W/2,H*.48,0,W/2,H*.48,Math.max(W,H)*.72);
  g.addColorStop(0,alert?"#21060a":"#071d2b");g.addColorStop(.5,"#020a11");g.addColorStop(1,"#010306");
  ctx.fillStyle=g;ctx.fillRect(0,0,W,H);
  ctx.strokeStyle=rgba(col,.08);ctx.lineWidth=1;
  for(let i=0;i<12;i++){
    const y=H*.58+i*i*H*.0036;ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(W,y);ctx.stroke();
  }
  for(let i=-10;i<=10;i++){
    ctx.beginPath();ctx.moveTo(W/2,H*.56);ctx.lineTo(W/2+i*W*.09,H);ctx.stroke();
  }
  const scan=(t*40*(.2+PROFILE[AV.state].scan))%(W+240)-120;
  ctx.fillStyle=rgba(col,.035);ctx.fillRect(scan,0,80,H);
}
function drawMesh(t){
  fg.clearRect(0,0,W,H);
  const alert=FORCE_ALERT||AV.alert,col=alert?RED:CYAN;
  const projected=mesh.nodes.map(node=>projectNode(node,t));
  fg.globalCompositeOperation="lighter";fg.lineWidth=1;
  for(const edge of mesh.edges){
    const a=projected[edge.a],b=projected[edge.b];
    fg.strokeStyle=rgba(col,.10+.16*thinkMix);
    fg.beginPath();fg.moveTo(a.x,a.y);fg.lineTo(b.x,b.y);fg.stroke();
  }
  for(let i=0;i<projected.length;i++){
    const p=projected[i],node=mesh.nodes[i];
    const r=node.size*p.perspective*(1+AV.env*.7*speakMix);
    fg.fillStyle=rgba(col,.42+.35*Math.sin(t*1.2+node.phase)**2);
    fg.beginPath();fg.arc(p.x,p.y,r,0,TAU);fg.fill();
  }
  for(const pulse of mesh.pulses){
    const edge=mesh.edges[pulse.edge],a=projected[edge.a],b=projected[edge.b];
    const q=pulse.dir>0?pulse.t:1-pulse.t,x=a.x+(b.x-a.x)*q,y=a.y+(b.y-a.y)*q;
    fg.fillStyle=rgba(alert?RED:(AV.state==="listening"?AMBER:PALE),1);
    fg.beginPath();fg.arc(x,y,2.5+2*thinkMix,0,TAU);fg.fill();
  }
  fg.globalCompositeOperation="source-over";
  U.bloomBlit(ctx,field,W,H);
}
function drawPanel(x,y,title,rows,right=false){
  ctx.textAlign=right?"right":"left";ctx.textBaseline="top";
  ctx.font="11px Consolas,monospace";ctx.fillStyle=rgba(PALE,.9);ctx.fillText(title,x,y);
  ctx.strokeStyle=rgba(CYAN,.3);ctx.beginPath();ctx.moveTo(right?x-160:x,y+18);ctx.lineTo(right?x:x+160,y+18);ctx.stroke();
  rows.forEach((row,i)=>{
    const yy=y+28+i*18;ctx.fillStyle=rgba(CYAN,.6);ctx.fillText(`${row[0]}  ${row[1]}`,x,yy);
  });
  ctx.textAlign="left";
}
function drawChrome(state){
  const pct=value=>`${Math.round(Math.max(0,Math.min(1,value))*100)}%`;
  const energy=AV.samples.reduce((sum,value)=>sum+Math.abs(value),0)/AV.samples.length;
  let left=[["STATE",state.toUpperCase()],["STATE AGE",`${(stateAge/1000).toFixed(1)}s`],
    ["MIC LEVEL",pct(AV.micLevel)],["VOICE ENV",pct(AV.env)],["WAVE ENERGY",pct(energy)],["FPS",String(fps)]];
  let right=[["LOCAL TIME",new Date().toLocaleTimeString([], {hour12:false})],
    ["VIEWPORT",`${W}×${H}`],["MEMORY","—"],["BUS HEALTH","—"]];
  for(const row of AV.util.usageRows())right.push([row.label,row.text]);
  if(W<1000){left=left.slice(0,4);right=right.slice(0,4)}
  ctx.font="bold 15px Consolas,monospace";ctx.fillStyle=rgba(PALE,.95);
  ctx.fillText(AV.label,24,22);ctx.textAlign="center";ctx.fillText(state.toUpperCase(),W/2,22);ctx.textAlign="left";
  if(W>=760){drawPanel(24,72,"INPUT / COGNITION",left);drawPanel(W-24,72,"SYSTEM / SESSION",right,true)}
}
function drawWaveforms(state){
  micHistory.push(AV.micLevel);micHistory=micHistory.slice(-72);
  const draw=(values,y,h,col)=>{
    ctx.strokeStyle=rgba(col,.9);ctx.lineWidth=1.5;ctx.beginPath();
    values.forEach((value,i)=>{const x=24+i*(W-48)/(values.length-1),yy=y-value*h;(i?ctx.lineTo(x,yy):ctx.moveTo(x,yy))});ctx.stroke();
  };
  draw(micHistory,H-34,22,state==="listening"?AMBER:CYAN);
  draw(Array.from(AV.samples),H-68,26,state==="speaking"?PALE:CYAN);
}
function drawAlertFrame(){
  const a=.45+.35*Math.sin(now/180)**2;ctx.fillStyle=rgba(RED,a);
  ctx.fillRect(0,0,W,6);ctx.fillRect(0,H-6,W,6);ctx.fillRect(0,0,6,H);ctx.fillRect(W-6,0,6,H);
  ctx.textAlign="center";ctx.font="bold 14px Consolas,monospace";ctx.fillText("ALERT",W/2,48);ctx.textAlign="left";
}
```

Keep the whole page in one canvas. In `resize()`, set `field.width=W` and `field.height=H` after applying `DPR=Math.min(2,devicePixelRatio||1)` to the visible canvas, then call `buildMesh()`. In `frame(dt)`, call functions in this order: `AV.tick`, state-age/mix easing, `updateSignals`, `drawBackground`, `drawMesh`, `drawChrome`, `drawWaveforms`, and `drawAlertFrame` when `FORCE_ALERT||AV.alert` is true. Update `fps` once per second from `fpsCount` and `fpsAt`.

For widths under 1000 px, reduce each side rail to four rows and narrow it to 150 px. For widths under 760 px, keep only the title/state header, central mesh, bottom waveforms, and alert treatment.

- [ ] **Step 5: Run the automated checks**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
git diff --check
```

Expected: 3 tests pass and `git diff --check` prints nothing.

- [ ] **Step 6: Verify the fixed states and review-focus cases in a browser**

Start the local server in a persistent terminal:

```powershell
python server.py --port 8791 --no-open
```

Open each URL, wait until the tab title becomes `ready`, and inspect at 1920×1080:

```text
http://127.0.0.1:8791/faces/cognitive-command/?shot=idle&t=4000
http://127.0.0.1:8791/faces/cognitive-command/?shot=listening&t=4000
http://127.0.0.1:8791/faces/cognitive-command/?shot=thinking&t=4000
http://127.0.0.1:8791/faces/cognitive-command/?shot=speaking&t=4000
http://127.0.0.1:8791/faces/cognitive-command/?shot=idle&t=4000&alert=1
```

Confirm: state reactions are distinct; idle remains active; unsupported MEMORY and BUS HEALTH show `—`; no usage row appears when no usage is published; alert data remains readable.

Repeat the listening shot at 720×900 with microphone permission denied. Confirm the mesh still reacts to state, MIC reads zero, and the rails do not overlap the mesh or waveforms. Resize the live demo from 1920×1080 to 720×900 and back to confirm buffers rebuild without stale pixels:

```text
http://127.0.0.1:8791/faces/cognitive-command/?demo=1
```

Watch one complete demo cycle and confirm all four state transitions. Then verify the real alert signal only when no alert is already present:

```powershell
$alertSignal = 'E:\Alfred\backtalk\.voice_alert'
if (Test-Path -LiteralPath $alertSignal) { throw 'Existing alert is active; do not replace it.' }
try {
  Set-Content -LiteralPath $alertSignal -Value 'visual verification'
  Read-Host 'Open http://127.0.0.1:8791/faces/cognitive-command/ and confirm the red alert treatment, then press Enter'
}
finally {
  Remove-Item -LiteralPath $alertSignal -ErrorAction SilentlyContinue
}
```

Confirm the live page enters and leaves the red alert treatment. The `finally` block removes only the signal this step created.

- [ ] **Step 7: Make Cognitive Command the local default only after verification**

Change exactly this ignored local-config line in `ai-visualizer.json`:

```diff
-  "face": "neural",
+  "face": "cognitive-command",
```

Verify the config and gallery discovery:

```powershell
python -c "import json,urllib.request; c=json.load(open('ai-visualizer.json')); assert c['face']=='cognitive-command'; d=json.load(urllib.request.urlopen('http://127.0.0.1:8791/config')); assert any(f['id']=='cognitive-command' for f in d['faces']); print('config and gallery ok')"
```

Expected: `config and gallery ok`.

Start Alfred through `E:\Alfred\Talk to Alfred.bat`, open the Cognitive Command face without `shot` or `demo` parameters, and complete one short spoken turn. Confirm the real bus drives listening → thinking → speaking, the microphone trace moves during listening, and the output trace follows Alfred's spoken response. If this live check fails, change the local `face` value back to `neural` before stopping and report the observed failure instead of claiming completion.

- [ ] **Step 8: Prove existing faces and shared plumbing were not modified**

Run:

```powershell
git diff --exit-code HEAD -- core.js server.py faces/board faces/radial faces/rain faces/neural
git status --short
```

Expected: the first command prints nothing; status shows only `faces/cognitive-command/` and `tests/test_cognitive_command_face.py`. The ignored `ai-visualizer.json` does not appear.

- [ ] **Step 9: Commit the verified face**

```powershell
git add faces/cognitive-command/index.html tests/test_cognitive_command_face.py
git commit -m "feat: add Alfred cognitive command face"
```
