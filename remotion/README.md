# teamGARI — Editorial HCI Film

A complete **Remotion + React + TypeScript** project with **Python/librosa media preparation**. It renders the supplied HCI talk as an **18:9, 3840×1920, 30 fps** film with obsidian environments, frosted glass, abstract geometric speaker avatars, kinetic typography and recorded prototype evidence.

**Full composition:** `Film` — 13,818 frames / **7:40.600**.  
**Technical proof:** `Proof` — six seconds, sampling the introduction, team lineup and both Raj demonstrations.  
**Original narration:** ten supplied recordings, 434.5945 decoded seconds. The film adds an 18-second visual opening and eight seconds of references. Audio is placed using 48 kHz sample counts, not rounded section durations.

The downloadable complete package includes the supplied media, concept backgrounds, transparent geometric avatars, Inter font, and **already prepared** audio, waveform data and aligned demo plates. You can render immediately after installing Node dependencies and FFmpeg. Python is needed only to regenerate prepared media or change the editorial/audio configuration.

## 1. Requirements

- **Node.js 22 or 24** (tested with 24.22.1), npm, and **FFmpeg 6+**, including `ffprobe`, on PATH.
- A desktop Chrome/Chromium installation, or let Remotion obtain its compatible browser with `npx remotion browser ensure`.
- For preprocessing: **Python 3.11/3.12**. Tested with Python 3.12.
- A 64-bit desktop with approximately 8 GB RAM for previews; 16 GB is preferable for full-resolution work. Rendering is CPU/software-compatible; a GPU is optional.
- Disk space for the project, generated media, and resumable video chunks. Render time depends strongly on CPU/GPU and compositor performance; the project does not promise real-time 4K rendering.

All Remotion packages are pinned to **4.0.543** in `package-lock.json`. Do not upgrade one `@remotion/*` package independently.

## 2. Quick start — complete package

Unzip the package and open a terminal in the folder containing `package.json`.

```sh
npm ci
ffmpeg -version
ffprobe -version
npm run validate
npm run typecheck
npm test
npm run studio
```

Studio opens an editable timeline. Select `Film` for the complete talk or `Proof` for the short montage. Rendering and previewing use local files; no API token, cloud account, Vercel connection, external font service, AI service or Web Audio permission is required.

Render the technical proof:

```sh
node scripts/render.mjs --composition Proof --quality preview --scale .25 --chunk 90 --concurrency 2 --output out/proof.mp4
```

Render the full film at **1920×960**:

```sh
npm run render:preview
```

Render the final film at **3840×1920**:

```sh
npm run render:final
```

Outputs default to:

```text
out/film-preview-1920x960.mp4
out/film-final-3840x1920.mp4
```

The aspect ratio is native 18:9. These are not 16:9 files with letterbox bars.

## 3. Memory limits, long renders and resuming

The renderer exports **video-only chunks of 900 frames / 30 seconds**, then joins them and encodes **one continuous AAC audio track**. This avoids accumulating AAC encoder priming/delay at each chunk boundary. It never builds an eight-minute array of rendered frames in RAM.

For a slower machine:

```sh
node scripts/render.mjs --quality final --chunk 300 --concurrency 1
```

If interrupted, rerun the **same command**. Completed chunks are reused after frame-count and size validation. A changed source, art asset, prepared manifest, composition, quality, scale or chunk size gets a different cache directory. Incomplete chunks are rendered again.

Choose another Chrome executable when needed:

```sh
node scripts/render.mjs --quality preview --browser "/path/to/chrome"
```

Or set `REMOTION_BROWSER_EXECUTABLE`. On Windows the executable is typically under `C:\Program Files\Google\Chrome\Application\chrome.exe`; macOS uses the app bundle's `Contents/MacOS/Google Chrome`. Existing common installations are detected automatically.

Render an **inclusive** frame range, with the corresponding audio excerpt:

```sh
node scripts/render.mjs --quality preview --frames 3050-3149 --output out/chat-save-check.mp4
```

Remove `.cache/render/` to reclaim rendered chunks. Remove `.cache/prepare/` to discard preprocessing intermediates. `public/generated/` contains required render assets, so do not remove it unless you will run preprocessing again.

## 4. Folder structure and every required asset

```text
teamgari-editorial-film/
  package.json, package-lock.json, tsconfig.json, remotion.config.ts
  requirements.txt
  src/
    index.ts                 Remotion registration
    Root.tsx                 Film and Proof compositions
    Film.tsx                 Local asset/font loading; master audio; frame routing
    geometry.ts              Camera projection and projective corner pin
    motion.ts                Bezier curves, camera poses, voice feature sampling
    types.ts
    components/
      Plane.tsx              Projected layers and glass materials
      Background.tsx         Background parallax and lighting treatment
      Avatar.tsx             Voice-driven scale, glow, bob and onset particles
      Typography.tsx         Deterministic per-word typography
      DemoScreen.tsx         Source-aligned, perspective-warped footage
      EditorialPanels.tsx   Charts, focus diagrams, privacy and proposed hybrid
      Scene.tsx              Scene assembly, captions, opening and credits
    data/
      script.json            Full supplied script, exact sample counts, caption cues
      storyboard.json        54 continuous narrated motion beats
      demo-map.json          Native-source-to-narration edit map
      proof-clips.json       Frame ranges used for the proof montage
      source-integrity.json  SHA-256 checks for original recordings
      config.ts              Format, names, accents, references
  public/
    assets/
      audio/
        Immad-01.ogg, Immad-02.ogg, Immad-03.ogg
        Raj-01.ogg, Raj-02.ogg, Raj-03.ogg
        Awais-01.ogg, Awais-02.ogg
        Raja-01.ogg, Raja-02.ogg
      demos/
        scenario-1.mov
        scenario-2.mov
      backgrounds/
        hero.png             Generated obsidian/frosted-glass environment
        demo.png             Generated display-theatre reference/environment
        avatar-reference.png Generated geometric-avatar art-direction board
      avatars/
        immad.png            Ivory discs and amber orb
        raj.png              Cobalt interlocking bridge
        awais.png            Violet prism and measurement rings
        raja.png             Emerald arch and frosted sphere
      portraits/             Team-approved cutouts for introduction/closing
        raja.png, raj.png, awais.png, immad.png
      fonts/
        InterVariable.woff2
        LICENSE-Inter.txt
      reference/             Original HTML prototype, slides and PDFs
    generated/
      manifest.json          Exact timing, normalized voice features and caption cues
      narration.wav          One 48 kHz PCM master, including opening/references
      proof.wav              Sample-aligned proof montage audio
      captions.srt           Full-film script captions
      demos/
        Raj-01.mp4           1,516 CFR frames, no source audio
        Raj-02.mp4           1,347 CFR frames, no source audio
        Raj-03.mp4           924 CFR frames, no source audio
  scripts/
    import-assets.py, prepare.py, author-storyboard.py
    validate-assets.mjs, render.mjs, export-blueprint.py
  tests/                     Geometry, determinism, timing and native event anchors
  docs/                      Storyboard, camera/audio blueprint and source audit
  out/                       Rendered MP4s
```

The `reference/` documents are retained project material. Their editorial TODOs are not treated as instructions to change the script, evidence or the supplied media.

## 5. Import the original uploaded files — source-only checkout

The complete ZIP already contains everything. If using a source-only checkout, copy your original downloads into one folder and run:

```sh
python scripts/import-assets.py --from "/path/to/teamgari-downloads"
```

The importer searches recursively for the ten `Immad-01…`, `Raj-01…`, etc. OGG files and the two specifically named `C-10-TeamGARI-ToolTalk-Scenario-1.mov` and `…Scenario-2.mov` recordings. It copies these to the canonical paths above. The original Unicode audio filenames are supported. It imports only matching `C-10-TeamGARI` PDF/PPTX/HTML reference documents.

Manually supply `hero.png`, `demo.png`, the four transparent avatar PNGs, and Inter using the paths above when those are not already included. Avatar sprites have transparent outer margins cropped; no human photographs are used in this design.

## 6. Run or regenerate Python/librosa preprocessing

macOS/Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/prepare.py
```

Windows PowerShell, without changing shell execution policies:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts\prepare.py
```

Preprocessing performs these operations:

1. Verify the original source hashes. A different take/capture requires deliberate re-authoring; silently retaining the old source-frame map would be incorrect.
2. Decode each recording to 48 kHz mono PCM. Discard codec skip/padding normally via FFmpeg and check its exact expected sample count.
3. Apply two-pass dialogue normalization targeting **−16 LUFS / −1.5 dBTP**, while preserving the decoded sample length. Original voices are retained.
4. Analyze the **original voice**, independently of background sound, using librosa: 4,096-sample Hann FFT, 1,600-sample hop (30 Hz), RMS and three frequency bands.
5. Conform the two VFR demo captures into three 30 fps plates matched to Raj's narration. Holds reference verified native frames; source footage is never regenerated as AI UI.
6. Stream the master PCM to disk rather than holding the complete narration in RAM. Create sample-aligned captions, proof audio and an atomic final manifest.

Useful options:

```sh
python scripts/prepare.py --skip-demos
python scripts/prepare.py --no-normalize
python scripts/prepare.py --no-intro-sound
```

`--skip-demos` requires valid already conformed plates. `--no-normalize` preserves original recording levels. `--no-intro-sound` replaces the small original procedural opening sound bed with silence. There is no additional synthetic narrator.

## 7. Voice-reactive animation — exact definitions

Features are in `public/generated/manifest.json`, per recording, not calculated from browser playback volume or music.

- Low band: **80–250 Hz** → gentle avatar lift / base pulse.
- Mid band: **250–2,000 Hz** → rim glow and restrained rotation.
- High band: **2,000–8,000 Hz** → small sparkle/glow detail.
- Normalize log-band power between that recording's voiced-frame **P10/P95**. Gate RMS below **−45 dBFS**.
- Smooth with **40 ms attack / 180 ms release**. Clamp features to 0…1.
- Hero scale: `1 + .020 × amplitude + .006 × low`. Reading mode multiplies motion intensity by **0.35** and disables particles.
- Onset particles require high-band rise >0.18, high level >0.65, at least 12 frames since the previous onset; two particles, 18-frame lifetime.
- All positions are derived from current frame and prepared data. There is no `Math.random()`, CSS time animation, wall-clock animation or playback-dependent state.

Different microphone levels therefore do not make one speaker's avatar arbitrarily stronger. The screen recording and captions themselves do not pulse or blur to the audio.

## 8. 2.5D compositing and camera control

`src/geometry.ts` is a real pinhole projection, not a static skew preset. It rotates each layer's four corners in 3D, projects them through the animated camera, solves an eight-parameter homography and creates CSS `matrix3d(...)` for the live HTML/video plane.

World units are design pixels. **+X right / +Y up / +Z toward the viewer.** Default camera is `(0,0,2400)`, looking at `(0,0,0)`, with a 2,400-unit focal length. Layer depths:

| Layer | Depth / behaviour |
|---|---|
| Background environment | Separate parallax movement, approximately distant/background space |
| Secondary glass / evidence surfaces | Around Z=90–160 |
| Recorded prototype | Z=120; true four-corner perspective mapping |
| Editorial labels / captions | Screen-space HUD; remain readable |
| Avatar identity | Screen-space foreground, voice-reactive sprite + local light |

`motion.ts` defines named camera poses `N/H/W/L/R/G/A`. Each beat in `storyboard.json` names its start/end poses and sweep duration. Camera translation follows a cubic Bezier path with a small directional bulge; time uses the exact CSS/AE ease-in-out curve `(0.42,0,0.58,1)`. The last 18 frames of each narrated section return toward neutral for a consistent cut.

`DemoScreen` clamps the projected screen to a reading-safe rectangle. Decorative depth continues around it while the evidence stays large and unblurred. Bezel frosting never changes the actual recorded form/chat pixels.

## 9. Synchronisation — source audit and spoken anchors

The source MOVs are **variable frame rate**. Their reported `r_frame_rate=120/1` is not a valid source-frame indexing assumption. The edit map uses actual native frame numbers and presentation timestamps.

| Event | Native frame (zero-based) | Source PTS | Authored output cue |
|---|---:|---:|---|
| Scenario 1: chat saved | 373 | 13.400000 s | Raj-01 local f707 (23.5667 s), spoken “confirms” |
| Scenario 1: form saved | 1050 | 28.216667 s | Raj-01 f1079 (35.9667 s), spoken “12.5” |
| Scenario 2: chat saved | 687 | 16.316667 s | Raj-02 f768 (25.6000 s), spoken “Confirm” |
| Scenario 2: error summary | 1164 | 30.945000 s | Raj-03 f223 (7.4333 s), “error summary” |
| Scenario 2: one remaining error | 1652 | 42.125000 s | Raj-03 f360 (12.0000 s), “Monday” |
| Scenario 2: form saved | 1856 | 46.491667 s | Raj-03 f392 (13.0667 s), “successfully” |

Raj-02's editorial **“Profile saved.”** headline is delayed until local f837 / 27.900 s, matching that spoken phrase, while the real recorded click/save state appears at the earlier spoken “Confirm.” Raj-01's 8.6 s and 12.5 s callouts are also delayed to the corresponding spoken numbers.

The mapping uses frame holds, clearly retimed playback and one removal of inactive time in form recovery. It does not alter the recorded numbers, controls, course codes, dates or outcomes. On-screen disclosure says playback is retimed and displayed timer values are original. The sequence is not presented as a controlled speed test.

Full frame ranges and source provenance are in `docs/MOTION-BLUEPRINT.md`, `src/data/demo-map.json` and `docs/source-native-events.json`.

## 10. Edit text, layout and timing

- Script/captions: `src/data/script.json`.
- Exact frame choreography: `src/data/storyboard.json`.
- Rebuild the authored defaults: `python scripts/author-storyboard.py` (this intentionally overwrites manual edits to the storyboard/demo map).
- UI playback: `src/data/demo-map.json`.
- Camera poses and curves: `src/motion.ts`.
- Glass styling: `src/components/Plane.tsx`.
- Type: Inter Variable, locally loaded; headline, label and caption settings live in `Typography.tsx` and `Scene.tsx`.
- Names, palette and references: `src/data/config.ts`.

Caption text uses the provided clean script with aligned word-time estimates, rather than retaining ASR transcription mistakes. If changing a recording, re-align the script/captions and update native event anchors as needed. Update expected hashes/sample counts deliberately; the integrity check is designed to catch accidentally using another take with the old timing.

## 11. Verification and supported limitations

```sh
npm run typecheck
npm test
npm run validate
```

Tests cover timeline continuity, every demo-map interval, source save anchors, deterministic camera evaluation, feature interpolation, near-plane handling and true perspective corner pinning. Asset validation checks sample counts, silent demo streams, frame counts, source-plate dimensions and content hashes.

This delivery includes a **short rendered technical proof**, not a completed full-film 4K render. The complete film is authored and executable using the same code. Review the full 1920×960 export before making the longer 4K export, especially typography wrapping and screen-reading duration at your presentation size. The supplied original scenario footage remains the evidence; accessibility illustrations and the hybrid are explicitly labelled as reported observations or proposed/untested designs.

## 12. Provenance

The ten supplied team recordings are the voices. The actual two supplied prototype recordings drive all demos. Original slides/PDF/HTML sources are retained. Individual speaking sections use abstract geometric avatars. At the team’s later request, the introduction and closing use the previously approved portrait cutouts, ordered Raja Suleman, Raj Lakhani, Awais Basheer, Muhammad Immad.

The three art-direction concepts and the transparent geometric-avatar sheet were generated with the available OpenAI image tool. Its interface did not expose a DALL·E 3 model selector. Reusable prompts and art specifications are in `docs/ART-DIRECTION.md`. The Inter font is redistributed with its included license. Code, editing and concept preparation were assisted by OpenAI Codex.
