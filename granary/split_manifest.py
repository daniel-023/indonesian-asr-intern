# Split granary manifests by punctuation

import argparse
import re
from pathlib import Path

def split_on_punctuation(corpus_dir: Path):
    # Regex: split on punctuation marks followed by a space or end of line
    split_pattern = re.compile(r'(?<=[.!?])\s+')

    txt_files = list(corpus_dir.glob("*.txt"))
    print(f"Found {len(txt_files)} text files in {corpus_dir}")

    for txt_file in txt_files:
        text = txt_file.read_text(encoding="utf-8").strip()
        if not text:
            continue

        # Split into sentences
        sentences = [s.strip() for s in split_pattern.split(text) if s.strip()]
        if not sentences:
            continue

        # Overwrite the file with one sentence per line
        txt_file.write_text("\n".join(sentences) + "\n", encoding="utf-8")

    print("Finished splitting text files on punctuation.")

def main():
    parser = argparse.ArgumentParser(description="Split corpus .txt files on punctuation.")
    parser.add_argument("--corpus-dir", required=True, help="Path to corpus directory containing .wav and .txt pairs")
    args = parser.parse_args()

    corpus_dir = Path(args.corpus_dir).resolve()
    if not corpus_dir.exists():
        raise FileNotFoundError(f"Corpus directory not found: {corpus_dir}")

    split_on_punctuation(corpus_dir)

if __name__ == "__main__":
    main()