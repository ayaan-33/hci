# Team C-10 / teamGARI — Confirmed ≠ Correct

Revised HCI Tool Talk: chat-style onboarding versus a traditional form.

**Status: review cut.** The 3D opening, original recorded narration, prototype demonstrations, captions, analysis, conclusion and references are assembled. The original four portrait files are still needed for background-only cutouts; no generated substitutes are used.

## Watch

- [MP4 video](C-10-TeamGARI.mp4)
- [English captions (SRT)](C-10-TeamGARI.srt)
- [English captions (WebVTT)](C-10-TeamGARI.vtt)
- [Viewing page](index.html)
- [Original interactive prototype](prototype.html)

The viewing page includes chapter navigation and a direct MP4 download.

## Sequence

1. A newly rendered 3D parcel sorter routes a wrongly labelled package to the wrong destination. Synthetic AI narration is used only here.
2. Muhammad Immad: introduction and simulation disclosure.
3. Raj Lakhani: clear input, messy input and form recovery, using the original scenario recordings, retimed to the commentary.
4. Awais Basheer: measurements and research context.
5. Raja Suleman: limitations, accessibility, evidence and privacy.
6. Muhammad Immad: proposed hybrid, future evaluation and conclusion.
7. References and production notes.

Team order: **Raja Suleman · Raj Lakhani · Awais Basheer · Muhammad Immad**.

## Evidence boundaries

The chat is a scripted simulation, not a live LLM. Its two errors were deliberately programmed. The demonstration comes from one team member’s run and does not establish a general performance ranking. Form and chat timers start at different points and capture different date detail. The hybrid is a proposal and was not tested. Screen-reader behaviour was not tested.

Source documents supplied background material; editorial TODOs inside them were not treated as user instructions. The supplied narration is the source of truth for the spoken claims and the full member names in this revision.

## Production

- Blender 4.3.2: actual 3D parcel-sorter geometry and camera animation. Scene: `production/parcel-sorter.blend`.
- FFmpeg: footage editing, perspective effects, caption compositing, encoding and dialogue loudness normalization.
- Opening synthetic narration: Microsoft Edge TTS, `en-GB-RyanNeural`.
- Main voices: supplied original OGG recordings, without synthetic replacement.
- Captions: supplied script aligned to word timestamps from Whisper tiny.en.
- Editing, programming and animation assisted by OpenAI Codex.

`production/` contains the editing scripts and timeline from the rendering workspace. They reference the original media under `/workspace/attachments/`, which are not duplicated here. To reproduce, restore the supplied assets to those paths or update the media paths, install Pillow, numpy, edge-tts and faster-whisper, then render the Blender scene, run the transcription/alignment and execute the edit and assembly scripts from the workspace root. Scripts use `work/` for intermediates and `output/` for results. `finish.py` waits for `edit.py` and the last Blender frame before assembling.

## References supplied in the project

- Soni et al. (2022), Frontiers in Digital Health: https://doi.org/10.3389/fdgth.2022.954069
- JMIR Human Factors (2021): https://doi.org/10.2196/25787
- Xiao et al. (2020), ACM TOCHI: https://doi.org/10.1145/3381804
- Wei et al., arXiv preprint: https://arxiv.org/abs/2301.05843
- Amershi et al. (2019), Guidelines for Human–AI Interaction, CHI.
- W3C, WCAG 2.2 SC 4.1.3: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
- W3C, ARIA23: https://w3c.github.io/wcag/techniques/aria/ARIA23
- Typeform completion-rate claim via tinycommand.com (2025): secondhand vendor claim, not tested by this team.
