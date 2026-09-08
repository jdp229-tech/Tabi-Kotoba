"""Extract (id, jp) pairs from the PHRASES array in ../index.html.

Not a full JS parser -- the PHRASES array's formatting is simple and
consistent enough that a targeted regex is more robust than trying to
convert it to JSON. Re-run this (or just import phrases() from it)
whenever phrases are added, to regenerate audio for the new ones.
"""
import re
from pathlib import Path

INDEX_HTML = Path(__file__).parent.parent / "index.html"
ENTRY_RE = re.compile(r'\{id:"(p\d+)".*?jp:"([^"]+)"', re.DOTALL)


def phrases():
    html = INDEX_HTML.read_text(encoding="utf-8")
    start = html.index("const PHRASES = [")
    end = html.index("\n];", start)
    array_text = html[start:end]
    pairs = ENTRY_RE.findall(array_text)
    if not pairs:
        raise RuntimeError("No phrases matched -- has the PHRASES format changed?")
    return pairs


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    pairs = phrases()
    print(f"Found {len(pairs)} phrases")
    for pid, jp in pairs[:5]:
        print(f"  {pid}: {jp}")
    print("  ...")
