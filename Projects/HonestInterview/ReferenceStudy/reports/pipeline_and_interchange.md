# Three-App Workflow and Interchange Findings

## Capability Checks

Adobe Animate MCP:
- `get_documents` works.
- `execute_extend_script` works for JSFL and successfully exported `animate_effect_pass.png`.
- Known risk: bridge timeout is about 20-21s, and timed-out JSFL may continue inside Animate. Keep creation/export calls short and verify state before retrying.

Moho MCP:
- `document_getInfo` works: connected to `Untitled 2.moho`, 1280x720, 24 fps, unsaved.
- `document_screenshot` timed out after 30s. It was not retried.
- Exposed MCP is good for document/layer/bone/vector inspection and some animation transforms, but not full new-rig authoring from scratch.

Moho local scripting:
- Moho 14 is installed at `C:\Program Files\Moho 14`.
- Installed command-line examples show `Moho.exe -attachconsole script.lua`, `FileNew`, `FileSaveAs`, and `FileRender`.
- A disposable script `interchange_test/moho_shape_pass.lua` was attempted. The shell returned before outputs were visible, but the files appeared afterward. This confirms delayed execution is possible.
- Created real Moho outputs: `moho_shape_pass.moho` and `moho_shape_pass.png`.
- The Moho PNG is transparent at empty pixels, but it rendered at 1280x720 and contains Demo Mode watermark lines. It is not production-ready.

Blender MCP:
- Connected and can execute Python in the live scene.
- Saved `interchange_test.blend` and rendered PNG composites.

## Interchange Test Results

Files:
- Real Moho shape pass: `interchange_test/moho_shape_pass.png`
- Real Moho file: `interchange_test/moho_shape_pass.moho`
- Animate effect pass: `interchange_test/animate_effect_pass.png`
- Moho fallback pass, not validated: `interchange_test/moho_pass_fallback_not_validated.png`
- Blender scene: `interchange_test/interchange_test.blend`
- First composite: `interchange_test/blender_interchange_composite.png`
- Corrected composite: `interchange_test/blender_interchange_composite_corrected.png`
- Real-Moho composite: `interchange_test/blender_interchange_real_moho_composite.png`

Validated:
- Animate can export a transparent 1080x1920 PNG. Alpha range verified as 0-255.
- Blender can load transparent PNG passes as planes and align them at 1080x1920.
- Blender material setup must use emission/transparent nodes for 2D passes; standard Principled materials render too dark under scene lighting.
- Moho command-line Lua can create a simple `.moho` and render a PNG, but output detection may lag after the process returns.
- Moho rendered alpha, and Blender could composite the real Moho PNG with the Animate PNG.

Not production-ready:
- Moho output size/default document was 1280x720, not 1080x1920.
- Moho render contained Demo Mode watermark lines.
- Moho MCP `document_screenshot` timed out after 30s and was not retried.
- Blender composite background rendered dark gray rather than intended cream; production template needs explicit 2D/color setup.

## Practical Production Ownership

Moho:
- Owns character rigs, body mechanics, held poses, subtle eye/face controls, and primary performance.
- Assets live as `.moho` files under `D:\Animate\Projects\HonestInterview\moho`.
- Export target should be transparent PNG image sequences per shot/layer group once Moho rendering is validated.

Animate:
- Owns custom replacement drawings, mouth libraries, smear frames, graphic accents, and any one-off hand-drawn effects.
- Assets live as `.fla` plus exported transparent PNG/SVG/sprite sheets under `D:\Animate\Projects\HonestInterview\animate`.
- Do not rely on Animate for long monolithic exports; use short frame ranges and verify output.

Blender:
- Owns background assembly, camera if needed, compositing, final audio, final render.
- Assets live as `.blend` files under `D:\Animate\Projects\HonestInterview\blender`.
- Camera ownership should be Blender only unless a shot explicitly requires a Moho camera render. Avoid applying camera movement both in Moho and Blender.

Shared settings:
- Resolution: 1080x1920.
- FPS: 24 for project delivery, with reference timing converted from source fps where needed.
- Frame origin: production frame 1 equals time 0.000s. Store source reference frame indices separately.
- Audio offset: original audio starts at 0.000s in Blender final assembly.
- Pass format: PNG sequence with straight alpha where possible. Verify alpha with Pillow before compositing.
- Color: use Standard/view-transform or emission materials for 2D passes; verify sampled colors after render.

## Next Pipeline Task

Before new production animation, validate real Moho pass export:
1. Solve Moho document settings for 1080x1920 and 24 fps in Lua or via a saved template.
2. Confirm whether the installed Moho license/demo state can render without watermark.
3. Render a transparent character pass from Moho at exact delivery resolution.
4. Verify alpha, color, and no watermark with Pillow and visual inspection.
5. Build a Blender compositing template with emission materials and an explicit flat background color.
