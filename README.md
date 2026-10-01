# Animate / HonestInterview

Full animation workspace: editable production documents, generators, original audio, reference media, rendered frames, exports, experiments, review records, and bundled tools.

The current production is [`Projects/HonestInterview/ProductionFull_v5`](Projects/HonestInterview/ProductionFull_v5). Its existing status records identify **v5f** as the delivered revision. The picture is rendered by Adobe Animate from the same document supplied as editable FLA/XFL.

## Start here

- [Final MP4](Projects/HonestInterview/ProductionFull_v5/exports/HonestInterview_v5_final.mp4)
- [Editable FLA](Projects/HonestInterview/ProductionFull_v5/editable/HonestInterview_v5_final.fla)
- [Uncompressed XFL](Projects/HonestInterview/ProductionFull_v5/xfl/honest_v5f)
- [Production status](Projects/HonestInterview/ProductionFull_v5/STATUS.md), [issue log](Projects/HonestInterview/ProductionFull_v5/ISSUE_LOG.md), and [existing final report](Projects/HonestInterview/ProductionFull_v5/FINAL_REPORT.md)
- [Requirements and rebuild instructions](docs/WORKFLOW.md)

## Download

Install Git and Python 3.11, then clone and restore the five oversized bundled files:

```powershell
git clone https://github.com/Roy-Mutwiri/Animate.git D:\Animate
cd D:\Animate
python scripts/large_assets.py restore
```

The original workspace occupies approximately 2.48 GB before Git metadata. Allow additional space for repository storage and new renders. Some historical scripts and JSFL files contain absolute `D:/Animate` paths, so this location is the simplest way to reproduce the original setup.

## Contents

| Directory | Purpose |
| --- | --- |
| `Projects/HonestInterview/ProductionFull_v5` | Current Animate production, code, cues, sources, frames, exports and reviews |
| `Projects/HonestInterview/ProductionFull_v1` through `ProductionFull_v4` | Preserved earlier production revisions |
| Other `Projects/HonestInterview` directories | Reference study, design/construction experiments, Blender work, tools and evidence |
| `Goal` | Original reference material and existing bundled utilities |
| `Sounds` | Original dialogue audio |
| `Moho Pro` | Existing Moho project/tutorial material |
| `Tests` | Existing animation experiments |
| `.agents/skills` and `AGENTS.md` | Project operating instructions |

Original media and previous revisions are preserved. Temporary Python caches and credential/session files are excluded by `.gitignore`; nested third-party ignore rules may also exclude runtime data. GitHub rejected the initial LFS upload because the account's LFS budget was exhausted, so five files larger than 50 MiB are archived in ordinary Git as 45 MiB parts under `.repo-assets`. The restore command reconstructs their original paths and verifies their SHA-256 hashes without overwriting differing local files. Git LFS is not required. Run `python scripts/large_assets.py verify` to check the archived parts alone. Bundled third-party software retains its own license terms; this repository does not grant new rights to reference media, commercial applications, or third-party assets.

## Production constraints and known limitations

Use versioned output names and keep a single controller responsible for changes in animation applications. v5 must continue to render through Animate, rather than the earlier raster-generator route. Hand edits to an FLA do not flow back into the Python generators.

The existing final report records technical and frame-level checks, but **no listening or normal-speed playback with sound**. It also records residual mouth holds, framing and movement limitations. This repository upload does not constitute a new artistic or lip-sync review.

`D:\Animate\HONEST_INTERVIEW_PRODUCTION_DIRECTIVE.md` is missing. Project instructions say directive text was supplied inline in the original production session; no replacement text has been invented here.
