# Frame-addressed motion blueprint

30 fps; 3840×1920; all frame ranges are **zero-based and half-open**. Global frame = section start + local frame. Audio uses exact 48 kHz sample positions; picture cue rounding is at most half a frame.

## Timing

| Recording | Decoded seconds | Start time | Global frames |
|---|---:|---:|---:|
| Immad-01 | 40.340000 | 18.000000 s | [540, 1750) |
| Immad-02 | 19.020000 | 58.340000 s | [1750, 2321) |
| Raj-01 | 50.533500 | 77.360000 s | [2321, 3837) |
| Raj-02 | 44.913500 | 127.893500 s | [3837, 5184) |
| Raj-03 | 30.793500 | 172.807000 s | [5184, 6108) |
| Awais-01 | 54.633500 | 203.600500 s | [6108, 7747) |
| Awais-02 | 39.193500 | 258.234000 s | [7747, 8923) |
| Raja-01 | 45.653500 | 297.427500 s | [8923, 10292) |
| Raja-02 | 48.773500 | 343.081000 s | [10292, 11756) |
| Immad-03 | 60.740000 | 391.854500 s | [11756, 13578) |

Opening: [0,540). References: [13578,13818). Full picture length: **460.600 seconds**.

## Camera poses

| Pose | Camera XYZ | Look-at XYZ |
|---|---|---|
| N | 0,0,2400 | 0,0,0 |
| H | 0,0,2240 | 0,100,80 |
| W | 0,0,2680 | 0,0,0 |
| L | -120,25,2340 | -360,0,100 |
| R | 120,25,2340 | 360,0,100 |
| G | 0,75,2360 | 0,80,120 |
| A | 0,0,2540 | 0,0,0 |

For an A→B camera sweep, use cubic spatial controls P1=A+(B−A)/3+bulge and P2=A+2(B−A)/3+bulge. Bulge X=40×sign(Bx−Ax), Y=−12×sign(Bx−Ax), Z=0. Time ease is cubic Bezier (0.42,0,0.58,1). Target interpolates with the same eased progress. Hold the destination for the rest of the beat; the last 18 section frames return toward N.

## Shared layer and typography rules

- The primary plate is projected through a real 2400-unit pinhole camera and an eight-parameter homography.
- Source viewport: crop x=352,y=0,w=2320,h=1582 from the original 3024×1582 capture. Preserve source pixels, cursor and recorded numbers.
- Video enters over 24 frames: opacity .3→1, Y −180→0, Z −180→120, X tilt 7→0°, Y tilt −9→0°. Ease-out (0.16,1,0.3,1).
- Main glass is a separate frosted/rim material; no blur is applied to the recording. A reading-safe projected containment rectangle prevents camera sweeps from cropping controls.
- Narrative panels use Z=160, 4° X / −6° Y tilt, 24-frame elevation/opacity reveal.
- Headline: Inter 650, 112 design pixels (57 on demo sidebars), tracking −.035em, warm white. Word reveal is 10 frames, 3-frame stagger, Y +24→0. Default delay is 12 frames.
- Eyebrow: Inter 600, 32 px, uppercase, +.12em tracking. Captions: 54 px, 1.27 line height, screen-space bottom-safe area.
- Avatar motion uses per-recording librosa RMS/band data. Hero motion is 2% amplitude scale plus .6% low-band scale, low-band lift, mid-band glow/rotation, gated high-band onset particles. Reading mode uses 35% motion and zero particles.
- At a new beat, cards fade/lift in over 24 frames and the camera follows the specified sweep. Numeric results fade in without inventing intermediate count-up values.
- Hybrid, focus, accessibility and privacy diagrams are labelled as proposed/untested, reported observations, or future conditional flows as appropriate.

## Every narrated beat

### Immad-01 — Muhammad Immad

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,150) | [540,690) | N→H, 75f | question | A conversation can feel successful. / Even when the information is wrong. | Hero: waveform scale/glow; gated particles |
| [150,454) | [690,994) | H→W, 75f | comparison | When does chat help? / Chat-style onboarding / A traditional form | Hero: waveform scale/glow; gated particles |
| [454,704) | [994,1244) | W→A, 75f | team | We are teamGARI. / Raja Suleman / Raj Lakhani / Awais Basheer / Muhammad Immad | Hero: waveform scale/glow; gated particles |
| [704,930) | [1244,1470) | A→N, 75f | task | One study-planner profile. / Courses / Exam dates / Work evenings | Hero: waveform scale/glow; gated particles |
| [930,1210) | [1470,1750) | N→H, 75f | criteria | Three questions. / How long does it take? / What information gets confirmed? / Can users check and correct it? | Hero: waveform scale/glow; gated particles |

### Immad-02 — Muhammad Immad

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,60) | [1750,1810) | N→H, 60f | disclosure | Before the demonstration. /  | Hero: waveform scale/glow; gated particles |
| [60,270) | [1810,2020) | H→G, 75f | disclosure | A scripted simulation. / Not a live language model. | Hero: waveform scale/glow; gated particles |
| [270,440) | [2020,2190) | G→G, 75f | disclosure | Deliberately programmed mistakes. / Illustrating possible failure modes. | Hero: waveform scale/glow; gated particles |
| [440,571) | [2190,2321) | G→N, 75f | disclosure | One team member’s run. / Illustrative, not a validated comparison. | Hero: waveform scale/glow; gated particles |

### Raj-01 — Raj Lakhani

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,210) | [2321,2531) | N→W, 75f | demo | Form on the left. Chat on the right. / Scripted simulation | Reading: 35%, no particles |
| [210,495) | [2531,2816) | W→N, 75f | demo | Two exams next week. / CS3014 + MT1003 / Tuesday + Thursday evenings | Reading: 35%, no particles |
| [495,838) | [2816,3159) | N→R, 75f | demo; line delay 291f | Review. Confirm. / Chat: displayed timer 8.6 s | Reading: 35%, no particles |
| [838,1131) | [3159,3452) | R→L, 75f | demo; line delay 241f | Individual exam dates. / Form: displayed timer 12.5 s | Reading: 35%, no particles |
| [1131,1516) | [3452,3837) | L→W, 75f | demo | The outputs differ in detail. / Chat records the week. / The form records exact dates. | Reading: 35%, no particles |

### Raj-02 — Raj Lakhani

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,194) | [3837,4031) | N→R, 75f | demo | “Exams are after the break…” / “CS 3041” / “I work Mondays.” | Reading: 35%, no particles |
| [194,395) | [4031,4232) | R→R, 75f | demo | No exact exam date. / Mistyped code: CS3041 / Intended code: CS3014 | Reading: 35%, no particles |
| [395,768) | [4232,4605) | R→R, 75f | demo | The message never gave that date. / Summary: 22 Nov 2026 / Incorrect course code carried through. | Reading: 35%, no particles |
| [768,933) | [4605,4770) | R→H, 75f | demo; headline delay 69f; line delay 112f | “Profile saved.” / Both incorrect values accepted. | Reading: 35%, no particles |
| [933,1347) | [4770,5184) | H→W, 75f | demo | A programmed demonstration. / Not an observed language-model prediction. / What if the user misses the correction? | Reading: 35%, no particles |

### Raj-03 — Raj Lakhani

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,223) | [5184,5407) | N→L, 75f | demo | Required entries are missing. / Exam date / Work evenings | Reading: 35%, no particles |
| [223,390) | [5407,5574) | L→L, 75f | demo | An error summary identifies them. / Two missing entries → one → saved | Reading: 35%, no particles |
| [390,514) | [5574,5698) | L→L, 75f | demo | Correct and save. / Displayed timer: 18.7 s | Reading: 35%, no particles |
| [514,720) | [5698,5904) | L→L, 75f | demo | Missing required information caught. / This does not detect every wrong answer. | Reading: 35%, no particles |
| [720,924) | [5904,6108) | L→W, 75f | demo | An explicit value. / The chat substitutes a date and accepts the typo. | Reading: 35%, no particles |

### Awais-01 — Awais Basheer

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,163) | [6108,6271) | N→H, 75f | question | What do the results tell us? /  | Hero: waveform scale/glow; gated particles |
| [163,500) | [6271,6608) | H→W, 75f | metrics | First, time. / Scenario 1 / Chat 8.6 s / Form 12.5 s / Scenario 2 / Chat 13.0 s / Form 18.7 s | Hero: waveform scale/glow; gated particles |
| [500,760) | [6608,6868) | W→G, 75f | timing | Different starting points. / Form: first input. / Chat: message sent. | Hero: waveform scale/glow; gated particles |
| [760,980) | [6868,7088) | G→G, 75f | timing | Message preparation is excluded. / Different levels of date detail. | Hero: waveform scale/glow; gated particles |
| [980,1129) | [7088,7237) | G→H, 75f | question | Not a controlled test. / These timings do not prove chat is faster. | Hero: waveform scale/glow; gated particles |
| [1129,1392) | [7237,7500) | H→L, 75f | errors | Second, errors. / Chat: two incorrect values accepted. / Form: missing entries blocked. | Hero: waveform scale/glow; gated particles |
| [1392,1639) | [7500,7747) | L→N, 75f | control | Third, control. / Showing information does not guarantee / that mistakes will be noticed. | Hero: waveform scale/glow; gated particles |

### Awais-02 — Awais Basheer

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,376) | [7747,8123) | N→W, 75f | research | Published research. / A single-page form was fastest in one comparison. / A chatbot took longer in another. | Hero: waveform scale/glow; gated particles |
| [376,736) | [8123,8483) | W→G, 75f | coverage | Collecting target information. / Leaving information out differs from / counting wrong values. | Hero: waveform scale/glow; gated particles |
| [736,895) | [8483,8642) | G→H, 75f | question | No universal ranking. / Different tasks and systems. | Hero: waveform scale/glow; gated particles |
| [895,1176) | [8642,8923) | H→N, 75f | question | An illustration of a design problem. / Not a measurement of real chatbot failure rates. | Hero: waveform scale/glow; gated particles |

### Raja-01 — Raja Suleman

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,240) | [8923,9163) | N→G, 75f | limits | Important limits. / Built by the team. / Tested with one team member. / Mistakes deliberately scripted. | Hero: waveform scale/glow; gated particles |
| [240,473) | [9163,9396) | G→H, 75f | limits | We cannot generalise. / To all users or real language models. | Hero: waveform scale/glow; gated particles |
| [473,832) | [9396,9755) | H→R, 75f | focus | Reaching Confirm took extra navigation. / Focus did not move to the new summary. | Hero: waveform scale/glow; gated particles |
| [832,1132) | [9755,10055) | R→L, 75f | calendar | Difficulty dismissing the date picker. / Browser and platform may affect this. | Hero: waveform scale/glow; gated particles |
| [1132,1369) | [10055,10292) | L→N, 75f | question | A visually clear interface is not enough. / Accessibility needs its own evaluation. | Hero: waveform scale/glow; gated particles |

### Raja-02 — Raja Suleman

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,240) | [10292,10532) | N→H, 75f | screenreader | We did not test with a screen reader. / A conversation log role alone is not verification. | Hero: waveform scale/glow; gated particles |
| [240,479) | [10532,10771) | H→G, 75f | screenreader | What needs testing? / Announcements / Focus order / Correction controls | Hero: waveform scale/glow; gated particles |
| [479,740) | [10771,11032) | G→W, 75f | marketing | Research evidence and marketing. / Typeform claim: secondhand vendor figure. | Hero: waveform scale/glow; gated particles |
| [740,929) | [11032,11221) | W→H, 75f | marketing | We did not test it. / Conversational forms are not LLM chat. | Hero: waveform scale/glow; gated particles |
| [929,1210) | [11221,11502) | H→R, 75f | privacy | Free text can invite over-disclosure. / An external service would add privacy considerations. | Hero: waveform scale/glow; gated particles |
| [1210,1464) | [11502,11756) | R→N, 75f | privacy | Fake data. Local scripted parser. / The current demonstration. | Hero: waveform scale/glow; gated particles |

### Immad-03 — Muhammad Immad

| Local frames | Global frames | Camera / sweep | Visual layer | Exact editorial copy | Audio reactivity |
|---|---|---|---|---|---|
| [0,280) | [11756,12036) | N→L, 75f | recommendation | Start with the information the task requires. / Known fields. Visible requirements. | Hero: waveform scale/glow; gated particles |
| [280,573) | [12036,12329) | L→R, 75f | recommendation | Messy, narrative information. / Keep uncertainty visible. / Make corrections easy. | Hero: waveform scale/glow; gated particles |
| [573,820) | [12329,12576) | R→W, 75f | hybrid | Free text → review → confirm. / Pre-fill editable form fields. / Let the user inspect and edit. | Hero: waveform scale/glow; gated particles |
| [820,1103) | [12576,12859) | W→H, 75f | hybrid | Ask instead of guessing. / Missing date → ask. / Unrecognised course code → flag. | Hero: waveform scale/glow; gated particles |
| [1103,1330) | [12859,13086) | H→G, 75f | next | D3 / D4 / D5. / Input-flow design. / Accessibility evaluation. | Hero: waveform scale/glow; gated particles |
| [1330,1547) | [13086,13303) | G→W, 75f | next | What we would test next. / Real users and consistent timing. / Screen readers and repeated-run errors. | Hero: waveform scale/glow; gated particles |
| [1547,1750) | [13303,13506) | W→H, 75f | question | Understand and control what the system records. /  | Hero: waveform scale/glow; gated particles |
| [1750,1822) | [13506,13578) | H→A, 72f | team | Thank you for watching. / Raja Suleman / Raj Lakhani / Awais Basheer / Muhammad Immad | Hero: waveform scale/glow; gated particles |

## Exact recorded-source conform

Each moving interval retimes only the recorded source PTS range. Each hold repeats one native recorded frame. The UI content is never AI-generated. Timer values remain their original values; playback retiming is disclosed.

### Raj-01 — scenario-1.mov

| Output local frames | Source operation |
|---|---|
| [0,216) | Hold native source frame 0 |
| [216,496) | Play PTS 0.000000→6.000000 s |
| [496,707) | Play PTS 6.000000→13.400000 s |
| [707,838) | Hold native source frame 373 |
| [838,1079) | Play PTS 14.000000→28.216667 s |
| [1079,1516) | Hold native source frame 1050 |

### Raj-02 — scenario-2.mov

| Output local frames | Source operation |
|---|---|
| [0,194) | Play PTS 0.000000→2.900000 s |
| [194,395) | Hold first decoded frame at/after PTS 2.9 s |
| [395,692) | Play PTS 2.900000→14.900000 s |
| [692,768) | Play PTS 14.900000→16.316667 s |
| [768,1347) | Hold native source frame 687 |

### Raj-03 — scenario-2.mov

| Output local frames | Source operation |
|---|---|
| [0,223) | Play PTS 22.000000→30.945000 s |
| [223,315) | Hold native source frame 1164 |
| [315,360) | Play PTS 40.000000→42.125000 s |
| [360,392) | Play PTS 42.125000→46.491667 s |
| [392,924) | Hold native source frame 1856 |

The Raj-03 conform removes inactive time between the two-error state and the later correction. It preserves the recorded state order. The required date, course-code typo and timer outcomes are not changed.

## Opening and references

Opening [0,90): “A conversation.”; [90,240): “Confirmed.”; [240,420): “But is it correct?”; [420,540): “Chat or form?”. Glass check/lens visual, slow dolly, subtle procedural sound bed, no added synthetic narrator.

References [13578,13698): first four references; [13698,13818): remaining references and production notes. Final 18 frames fade toward obsidian.
