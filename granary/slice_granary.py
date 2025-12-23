#!/usr/bin/env python3
import json, subprocess
from pathlib import Path
import argparse

def main():
    ap = argparse.ArgumentParser(description="Cut clips from a Granary JSONL.")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()

    manifest = Path(args.manifest)
    out_dir = Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)

    with open(manifest, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip(): 
                continue
            ex = json.loads(line)
            src = Path(ex["audio_filepath"]).resolve()
            off = float(ex["offset"]); dur = float(ex["duration"])
            seg = ex.get("segment_id", 0)
            stem = src.stem
            out = out_dir / f"{stem}_seg{seg}_o{int(off*1000)}ms_d{int(dur*1000)}ms.wav"
            if out.exists():
                continue
            subprocess.run([
                "ffmpeg","-hide_banner","-loglevel","error","-y",
                "-ss", f"{off:.6f}", "-t", f"{dur:.6f}",
                "-i", str(src), "-ar","16000","-ac","1", str(out)
            ], check=True)
            # sidecar text if present
            txt = (ex.get("text") or "").strip()
            if txt:
                (out.with_suffix(".txt")).write_text(txt + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()