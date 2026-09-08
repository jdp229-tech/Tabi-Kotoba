"""Generate audio/{id}-{tier}.wav for every phrase, via a locally running VOICEVOX Engine.

Requires VOICEVOX Engine running on http://127.0.0.1:50021 (see tools/README.md).
Not part of the shipped app -- run this once, or again whenever phrases are added.

Three speed tiers match the app's Beginner/Amateur/Expert difficulty levels, so
slower audio is used automatically for less-practiced phrases:
  beginner: speedScale 0.75   amateur: 0.875   expert: 1.0
"""
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from extract_phrases import phrases

ENGINE = "http://127.0.0.1:50021"
SPEAKER = 3  # overridden by --speaker; run with --list-speakers to see options
AUDIO_DIR = Path(__file__).parent.parent / "audio"
TIER_SPEEDS = {"beginner": 0.75, "amateur": 0.875, "expert": 1.0}


def api_post(path, params=None, body=None):
    qs = ""
    if params:
        qs = "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode("utf-8") if body is not None else b""
    req = urllib.request.Request(ENGINE + path + qs, data=data, method="POST",
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def list_speakers():
    with urllib.request.urlopen(ENGINE + "/speakers", timeout=10) as resp:
        speakers = json.loads(resp.read())
    for s in speakers:
        for style in s["styles"]:
            print(f'  id={style["id"]:>4}  {s["name"]} / {style["name"]}')


def generate_tier(speaker_id, tier, speed_scale):
    AUDIO_DIR.mkdir(exist_ok=True)
    pairs = phrases()
    print(f"[{tier}] Generating {len(pairs)} clips with speaker {speaker_id}, speedScale={speed_scale}...")
    for pid, jp in pairs:
        query = json.loads(api_post("/audio_query", params={"text": jp, "speaker": speaker_id}))
        query["speedScale"] = speed_scale
        wav = api_post("/synthesis", params={"speaker": speaker_id}, body=query)
        out = AUDIO_DIR / f"{pid}-{tier}.wav"
        out.write_bytes(wav)
    print(f"[{tier}] Done.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--list-speakers" in sys.argv:
        list_speakers()
    else:
        speaker_id = SPEAKER
        if "--speaker" in sys.argv:
            speaker_id = int(sys.argv[sys.argv.index("--speaker") + 1])

        if "--tier" in sys.argv:
            tier = sys.argv[sys.argv.index("--tier") + 1]
            speed_scale = TIER_SPEEDS[tier]
            if "--speed" in sys.argv:
                speed_scale = float(sys.argv[sys.argv.index("--speed") + 1])
            generate_tier(speaker_id, tier, speed_scale)
        else:
            for tier, speed_scale in TIER_SPEEDS.items():
                generate_tier(speaker_id, tier, speed_scale)
