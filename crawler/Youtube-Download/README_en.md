# 📦 YouTube Data Crawler & Processor

---

## 🚀 Overview

This repository provides a **complete automated pipeline for YouTube data collection ➜ cleaning ➜ downloading ➜ subtitle-based segmentation**.  
It supports batch downloading of videos, audios, and subtitles from specified channels, and generates structured corpora for downstream ASR and TTS tasks.

Before running, please make sure you have:

1. A working Clash proxy (or other VPN)
2. A valid YouTube account & Cookies

The whole pipeline consists of four stages:

---

### ✅ **Stage 1｜Fetch Channel Metadata**
- Use `yt-dlp` to fetch the full metadata of a specified YouTube channel (or a single video).
- Optional range: `start_index` ~ `end_index`.
- Save results to `video_metadata.jsonl`.

---

### ✅ **Stage 2｜Filtering**
- Apply multiple rounds of filtering to the collected metadata based on config file rules:
  1. ❌ Discard invalid JSON records
  2. ❌ Discard videos not in the target language
  3. ❌ Discard entries where `media_type` ≠ `video` or live streams
  4. ❌ Discard videos outside the `[min_duration, max_duration]` range
  5. ❌ Discard videos with likes below threshold
  6. ❌ Optionally discard videos without subtitles or without manual subtitles
- ✅ The final metadata keeps only:
  - `channel_id`
  - `id`
  - `title`
  - `description`
  - `duration`
  - `upload_date`
  - `like_count`
  - `language`
  - `auto_subtitle`
  - `manual_subtitle`

---

### ✅ **Stage 3｜Download Audio & Subtitles**
- Use `yt-dlp` to automatically download:
  - Best available audio stream (`ba`)
  - Prefer manual subtitles in the target language; if unavailable, fall back to auto-generated subtitles
- All downloaded IDs are logged in `downloaded_ids.txt` to avoid duplication.

---

### ✅ **Stage 4｜Segment Audio by Subtitles**
- Use `.vtt` subtitles to precisely segment audio files (VAD-based).
- Segmentation output is configurable:
  - `slice_sample_rate` (default: 16kHz)
  - `slice_save_audio` (whether to actually export `.wav` files, or keep JSON only)
- Output format:
  ```plaintext
  output/{channel}/segments/{video_id}/
    ├── wav/            # Segmented audio files (optional)
    ├── segments.json   # JSON: records each segment's start/end time, text, file path
  ```

## 📖 Usage Instructions

- All parameter configurations are centralized in the `config/` folder.  
  You can switch configuration sets by modifying `CONFIG_NAME` in `run.sh`.

- Save cookies to `config/cookies.txt`.

- Adjust the `stage` parameter in `run.sh` to control which stage to run (crawling / filtering / downloading / segmentation).

## ❓ FAQ

---

**Q: How do I export Cookies?**

<Recommended: use Google Chrome!>

1. Log in to [youtube.com](https://www.youtube.com)  
2. Go to [https://www.youtube.com/robots.txt](https://www.youtube.com/robots.txt)  
3. Use the browser plugin **Get cookies.txt LOCALLY**  
4. Save the cookies as a **Netscape format** file named `cookies.txt`  
5. Place it into the `config/` folder  
6. **Immediately log out of your account**, otherwise cookies will auto-refresh

---

**Q: yt-dlp reports "video not available", "rate limit exceeded", or other errors**  

Please try the following steps in order:

1. Replace cookies. After replacement, log out immediately and do not log in again.  
2. Change your IP node, and verify `curl -I youtube.com` returns normally.  
3. Upgrade `yt-dlp` to the latest version.  
4. Switch to a different YouTube account.  

If the issue persists, try downloading from another channel.

---

**Q: How to avoid duplicate downloads?**  
All downloaded IDs are automatically logged in `downloaded_ids.txt`. Running multiple times will not re-download the same videos.

---

**Q: How to output only segmentation JSON (without audio)?**  
Set `slice_save_audio` to `false`. This will generate only JSON files without exporting `.wav` audio files.
