import json 
from pathlib import Path 
import jiwer
import numpy as np

CORPUS_DIR = Path("/scratch/users/ntu/daniel02/GigaSpeech2/id/work/podcastbahasaindonesiabers5467/corpus")
ALIGN_DIR = Path("/scratch/users/ntu/daniel02/GigaSpeech2/id/work/podcastbahasaindonesiabers5467/output_force_align")
REPORT_PATH = Path("/scratch/users/ntu/daniel02/GigaSpeech2/id/work/podcastbahasaindonesiabers5467/metrics/wer_report.txt")
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

wers = []
refs_all, hyps_all = [], []

tr = jiwer.Compose([
    jiwer.ToLowerCase(),
    jiwer.RemovePunctuation(),
    jiwer.RemoveMultipleSpaces(),
    jiwer.Strip(),
	jiwer.ReduceToListOfListOfWords()
])

for txt_file in CORPUS_DIR.glob("*.txt"):
	audio_id = txt_file.stem
	manifest = ALIGN_DIR/f"{audio_id}_manifest.jsonl"
	if not manifest.exists():
		continue
	reference = txt_file.read_text(encoding="utf-8").replace("\n", " ").strip()
	with manifest.open("r", encoding="utf-8") as f:
		hypothesis = " ".join(json.loads(line)["text"] for line in f)
		
	if reference:
		wers.append(jiwer.wer(reference, hypothesis, reference_transform=tr, hypothesis_transform=tr))
		refs_all.append(reference)
		hyps_all.append(hypothesis)

overall = jiwer.wer(" ".join(refs_all), " ".join(hyps_all), reference_transform=tr, hypothesis_transform=tr)
average = np.mean(wers) if wers else float("nan")

ref_transformed = tr(refs_all)
num_words = sum(len(words) for words in ref_transformed)

with REPORT_PATH.open("w", encoding="utf-8") as w:
	w.write(f"Pairs evaluated: {len(wers)}\n")
	w.write(f"Number of Words: {num_words}\n")
	w.write(f"Overall WER: {overall:.4%}\n")
	w.write(f"Average WER: {average:.4%}")