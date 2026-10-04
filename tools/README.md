# Audio generation

Regenerates `audio/{id}.wav` for every phrase in `PHRASES` (`../index.html`),
using a locally running [VOICEVOX Engine](https://github.com/VOICEVOX/voicevox_engine).
Run this again whenever phrases are added or changed.

1. Download the Windows CPU engine build from the
   [VOICEVOX Engine releases](https://github.com/VOICEVOX/voicevox_engine/releases/latest)
   (`voicevox_engine-windows-cpu-<version>.7z.001`) and extract it.
2. Run the extracted engine executable. It serves a local API at
   `http://127.0.0.1:50021` -- leave it running.
3. From this `tools/` directory:
   ```
   python generate_audio.py --list-speakers          # see available character/style ids
   python generate_audio.py --speaker <id>            # generate all 60 clips (speedScale 0.85 by default)
   python generate_audio.py --speaker <id> --speed 0.8  # slower/faster: speedScale, 1.0 = normal
   ```
   Output goes to `../audio/p1.wav` .. `p60.wav`.

## stt-bench.html

Throwaway benchmark for in-browser speech recognition (Whisper via
Transformers.js). Open it at `tools/stt-bench.html` on the deployed site (the
mic needs https), load a model, then record yourself saying a chosen phrase or
run the clean-TTS batch. "Copy results as text" gives a table to paste back.
Library and model files come from public CDNs, for the benchmark only.

The engine itself isn't part of the app or this repo -- only the generated
`.wav` files are committed. Safe to delete the extracted engine folder after
generating.

VOICEVOX requires crediting the character voice used wherever the generated
audio is distributed (see the app's info panel for the current credit line).
