# Editorial opening — visual study

Three style frames and an eight-second motion study establish the darker editorial direction for the courier analogy. This is a review deliverable; it does **not** replace `C-10-TeamGARI_Final.mp4`.

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
