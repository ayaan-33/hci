# Editorial birthday-cake opening

The approved visual study has been expanded into a complete **35-second birthday-cake opening**, replacing the previous 18-second opening. The final film runs **7:57.6**. All 13,278 presentation video frames after the old opening are copied without re-encoding.

- [Full revised film](../../C-10-TeamGARI_Final.mp4)
- [Standalone 35-second birthday opening](../../C-10-TeamGARI_Birthday-Opening.mp4)
- [Final opening review frames](final-review/)
- [Full-film verification](../../C-10-TeamGARI_Final-verification.json)

The cake is packed for Maya at 14 Maple Street. The system records and confirms 14 Beacon Point. A van follows that incorrect destination, delivering to a lighthouse while the birthday table has an empty cake stand. The analogy transitions into the existing study-planner presentation.

New assets include the cake and candles, a physically open box, an isolated closing lid, the coastal miniature town, an isolated delivery van, and the birthday table. The lid and van move independently of the environment; camera motion uses each shot’s actual depth pass. The approved dark glass, metal and porcelain material system is retained. The introductory narration is synthetic; the team’s presentation voices remain original.

The earlier eight-second study and style frames are retained below as the art-direction reference.

## Review files

- [Style board](review/style-board.jpg)
- [Motion test — 8 seconds, 1920 × 960, 30 fps](review/C-10-TeamGARI_Editorial-Motion-Test.mp4)
- [01 — Dispatch](review/dispatch.png)
- [02 — Confirmation](review/confirmation.png)
- [03 — Wrong destination](review/reveal.png)
- [Verification](review/verification.json)

## Authored visual system

Obsidian and graphite surfaces; warm porcelain parcel; champagne metal; smoked, rough transmission glass; restrained mint and amber emission. Real custom Blender geometry, physically based Cycles lighting and reflections. The parcel label reads `14 MAPLE STREET`; the system records `14 Beacon Point`. A sculptural lighthouse represents the incorrect destination. No generated people or external stock imagery.

The motion study uses the actual rendered camera-depth pass for screen-space 2.5D parallax and a restrained dolly simulation. It is **not a fully re-rendered 3D camera sequence**. Inter typography and blurred-backdrop interface cards are composited after rendering so the essential comparison remains crisp. For the final opening, larger viewpoint changes or object interactions should be rendered as new Blender shots.

## Reproduce

Requirements: Blender 4.3, Python 3.12, NumPy, Pillow, OpenCV, FFmpeg, and Intel Open Image Denoise 2.5 (CPU). Inter and its license are supplied. The included WAV clips are synthetic opening narration, not the team's voices.

```bash
export EDITORIAL_WORK="$PWD/build"
export OIDN="/absolute/path/to/oidnDenoise"
mkdir -p "$EDITORIAL_WORK"
for scene in dispatch confirmation reveal; do
  blender -b -t 3 --python scene.py -- \
    --scene "$scene" --out "$EDITORIAL_WORK/$scene.png" \
    --size 1920 --samples 32 --engine CYCLES
done
python finish.py
```

`scene.py` exports both the beauty render and a 16-bit camera-depth PNG. `finish.py` applies OIDN to the beauty assets, adds the editorial graphics, generates a quiet original ambient sound bed and confirmation sounds, and assembles the 240-frame motion study. It checks stream metadata and fully decodes the output. The Cycles render itself has built-in denoising disabled to support Blender builds without OpenImageDenoise.

The full film's original voices, prototype recordings, team portraits, and all project claims remain unchanged. Only opening-direction assets are included in this folder.


## Render the completed opening

After rendering the original three scenes as above, run:

```bash
python render-full-assets.py
python full-sound.py
python full-composite.py
export EDITORIAL_FULL_WORK="$EDITORIAL_WORK/full"
python assemble-full.py --original original-approved.mp4 \
  --narration ../../remotion/public/generated/narration.wav \
  --output "$EDITORIAL_FULL_WORK/C-10-TeamGARI_Final.mp4"
```

`original-approved.mp4` must be the 460.6-second approved film before this opening replacement. The immutable source is available at `https://raw.githubusercontent.com/ayaan-33/hci/a0c0ecb/C-10-TeamGARI_Final.mp4`. `assemble-full.py` deliberately validates that source’s frame count and the original cut at exactly 18 seconds. The new opening contains 1,050 frames; the completed film contains 14,328 frames at 30 fps.

The compositor works at 1920 × 960 and upscales the new intro to the existing 3840 × 1920 output. The existing 4K presentation is copied at its original resolution and encoded picture data. Assembly checks the copied H.264 picture-data hashes, final duration and frame count, and fully decodes the final film. The original continuous narration WAV is trimmed at exactly 864,000 samples (18 seconds), then follows the 35-second opening on one continuous AAC track. SRT cue times after the old opening shift forward by 17 seconds.
