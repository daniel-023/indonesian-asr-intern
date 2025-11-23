# Indonesian ASR @ NTU Speech & Language Lab
Large-scale crawling and processing Southeast Asian speech into clean ASR training datasets for downstream model training.

## Project Components:
- YouTube crawling with [yt-dlp](https://github.com/yt-dlp/yt-dlp) on Google Colab
- Large-scale audio processing on NSCC ASPIRE 2A
- Automatic transcription / segmentation via:
  - [GigaSpeech2](https://github.com/SpeechColab/GigaSpeech2)
  - [NeMo SDP (Granary)](https://github.com/NVIDIA/NeMo-speech-data-processor/tree/main/dataset_configs/multilingual/granary)
- Segment normalisation, filtering, and dataset export for ASR training

## Goals
1. Collect large-scale speech data from YouTube
   - Covering Bahasa Indonesia, Indonesian–English code-switching, and Southeast Asian English accents (Indonesian, Filipino, Indian).
3. Run scalable ASR processing on NSCC
   - Reproduce and adapt the GigaSpeech2 and NeMo SDP / Granary pipelines for Indonesian and SEA data.
5. Produce clean, trainable ASR datasets 
   - Generate segmented audio + transcripts with consistent normalisation, filtering, and manifests ready for downstream ASR training.
   
## High-Level Pipeline
1. Crawl audio & metadata on Google Colab using yt-dlp (with rate limiting / VPN or cookie handling as needed).
2. Sync crawled data to NSCC via `scp` / `rsync` into `/scratch` directory.
3. Run speech processing pipelines:
   - GigaSpeech2
   - NeMo SDP / Granary
4. Apply text normalisation and filtering (language, numbers/dates, etc.)
5. Export manifests (JSONL/TXT) listing audio paths, timestamps, durations, and cleaned transcripts.
