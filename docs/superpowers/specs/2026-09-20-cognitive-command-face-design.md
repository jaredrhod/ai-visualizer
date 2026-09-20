# Cognitive Command Face Design

## Objective

Give Alfred an original cyber-digital command-centre face built around a living cognitive mesh. The face must feel continuously active, expose dense real diagnostics, and react clearly to Alfred's voice states without copying the visual identity of JARVIS, Batman, or another franchise.

## User experience

The full-screen view uses a deep blue-black field, a central cyan cognitive mesh, restrained amber operational highlights, and red only for alerts. Motion continues at idle through low-amplitude node drift, signal traffic, and scanning planes. The interface remains readable rather than becoming visually frantic.

The layout has four zones:

- A large central three-dimensional mesh with traveling signals and depth haze.
- A left command rail for input, cognition, memory, and local-runtime telemetry.
- A right command rail for subsystem status, plan usage, bus health, clock, and state timing.
- A bottom rail for microphone and voice waveforms plus the current session state.

## State behaviour

| State | Visual response |
|---|---|
| Idle | Continuous low-rate traffic, slow scans, and stable diagnostics. |
| Listening | Microphone energy pulls signals inward; the input rail turns amber. |
| Thinking | Routing traffic accelerates; active nodes and cognition or memory panels brighten. |
| Speaking | Energy propagates outward; the bottom waveform follows the real audio envelope. |
| Alert | The palette shifts to red and the perimeter pulse strengthens without hiding diagnostics. |

Transitions are eased rather than cut. Missing or disconnected values display `—` or `OFFLINE`; the face never invents telemetry.

## Technical design

Add a standalone face at `faces/cognitive-command/` containing:

- `index.html` for the canvas renderer, layout, animation, and state reactions.
- `face.json` for gallery discovery, title, and description.

The face uses the existing `core.js` contract: `AV.state`, `AV.env`, `AV.samples`, `AV.micLevel`, `AV.alert`, identity labels, rate-limit rows, and shared utilities. No dependency, build step, new server endpoint, or change to `core.js` is required.

The existing Neural Core and other upstream faces remain unchanged. After verification, the untracked local `ai-visualizer.json` default changes from `neural` to `cognitive-command`. Reverting that one value restores the previous default.

## Rendering approach

Use one full-window canvas and deterministic seeded geometry so the mesh has a stable identity between launches. Build the mesh once on startup, then update only positions, signal progress, eased state weights, and telemetry each frame. Draw luminous elements to an off-screen field and apply the existing bloom utility before compositing crisp labels and panels.

Use native Canvas 2D, browser APIs, and existing utilities only. The design should degrade cleanly in smaller windows by reducing secondary labels before shrinking the central mesh.

## Boundaries

- No Batman, bat emblem, yellow oval, cave styling, or copied franchise graphics.
- No humanoid face.
- No fabricated CPU, memory, security, or connectivity values.
- No change to voice, approval, memory-vault, server, or signal-bus behaviour.
- No new dependencies or reusable theme framework.

## Verification

Verify:

1. `?shot=idle`, `listening`, `thinking`, and `speaking` rendering.
2. The complete `?demo=1` transition cycle.
3. Live microphone and voice-waveform reactions through the existing bus.
4. Alert rendering through the existing `.voice_alert` signal.
5. Missing-bus behaviour and honest offline indicators.
6. Fullscreen keyboard behaviour.
7. Layout at 1920×1080 and a smaller window.
8. Gallery discovery through `face.json`.
9. The previous Neural Core remains selectable and unchanged.

## Acceptance criteria

- Alfred defaults to the new Cognitive Command face locally.
- The central mesh is visibly alive at idle and clearly differentiates all live states.
- Dense diagnostics remain legible and show only available data.
- No new dependency, server change, or modification to an existing face is introduced.
- Relevant static, demo, and live checks pass, and the final diff contains no private configuration or generated mockups.
