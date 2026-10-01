# DesignV3 Pipeline Repair Report

## Moho State

Moho output from the prior interchange test is preserved at:

- `ReferenceStudy/interchange_test/moho_shape_pass.moho`
- `ReferenceStudy/interchange_test/moho_shape_pass.png`

The rendered PNG is 1280 x 720 with alpha range 0-255 and a transparent corner pixel `(0, 0, 0, 0)`.

The render contains visible red Demo Mode watermark lines. That is an actual license/export restriction observed in output. It was not removed, cropped, painted out, or hidden. A valid production license is required before Moho output can be used as final character art.

This turn's Moho MCP read attempt timed out once after about 10 seconds, and I did not repeatedly retry mutations. A brief command-line help probe launched a Moho process that kept running; the process was stopped after inspection. No project files were modified by that probe.

Unresolved Moho item: the supported API/path for setting a portrait 1080 x 1920 project template through automation is still not verified. The working render path currently proves delayed render output and transparency, but not production dimensions or licensed output.

## Blender Color Diagnosis

A known RGBA patch pass was created:

- `DesignV3/pipeline_test/known_rgba_patch_pass.png`

Tested colors included red, green, blue, yellow, skin, and half-alpha cream blocks.

Observed:
- Blender `Raw` view transform preserved a flat material background more directly, but damaged image-pass colors, especially yellow and skin.
- Blender `Standard` view transform preserved image-pass colors much better, but a Blender material flat-color background did not match the intended cream exactly.
- The best current route is to use `Standard`, transparent/emission image planes for 2D passes, and an image-textured background pass instead of a Blender material color for the final flat background.

Current measured file:

- `DesignV3/pipeline_test/blender_color_patch_composite_imagebg.png`
- Dimensions: 1080 x 1920.
- Alpha range: 255-255.
- Corner sample: `(248, 237, 218, 255)`.

The corner is close to the intended cream but not byte-exact in the saved render. Use patch-sample verification on future renders rather than trusting the viewport appearance.

## Interchange Retest

Inputs:

- Moho pass: `ReferenceStudy/interchange_test/moho_shape_pass.png`, 1280 x 720, alpha 0-255, transparent corner.
- Animate effect pass: `ReferenceStudy/interchange_test/animate_effect_pass.png`, 1080 x 1920, alpha 0-255, transparent corner.
- Blender background/image composition test: `DesignV3/pipeline_test/interchange_retest_moho_animate_blender.blend`.

Output:

- `DesignV3/pipeline_test/interchange_retest_moho_animate_blender.png`
- Dimensions: 1080 x 1920.
- Alpha range: 255-255.
- Corner sample: `(248, 237, 218, 255)`.

Result:
- Alignment and transparency mechanically work for combining a Moho character/shape pass, an Animate effect pass, and a Blender composite.
- The visible Moho Demo Mode watermark remains, so the Moho pass is an integration test only.
- The Moho source resolution mismatch remains a blocker for production-ready interchange.

## Practical Pipeline Status

- Moho remains the preferred character performance target once license and template dimensions are solved.
- Animate remains suitable for custom replacement drawings, smears, and effects as transparent PNG passes.
- Blender can assemble transparent passes at 1080 x 1920, but final color must be verified by sampled pixels and visual inspection.
- The final composite should own the opaque background. Character/effect passes should remain transparent.

