# 📦 YouTube Data Crawler & Processor

---

## 🚀 功能概述

本仓库提供一个**完整的 YouTube 数据抓取 ➜ 清洗 ➜ 下载 ➜ 按字幕切分**的自动化pipeline，支持从指定频道批量下载视频音频、字幕，并生成可用于后续ASR、TTS 任务的结构化语料。

运行前请确保已准备：

1. 可用的 Clash 代理（或其他vpn）

2. 有效的 YouTube 账号 & Cookies

整个流程分为四个阶段：

---

### ✅ **Stage 1｜抓取频道元数据**
- 使用 `yt-dlp` 抓取指定 YouTube 频道（或单个视频）的完整元数据信息。
- 可选范围：`start_index` ~ `end_index`。
- 保存为 `video_metadata.jsonl`。

---

### ✅ **Stage 2｜筛选与过滤**
- 使用配置文件中的条件对抓取到的元数据进行多轮筛选：
  1. ❌ 丢弃格式不合法的 JSON
  2. ❌ 丢弃语言非指定目标语言
  3. ❌ 丢弃 `media_type` 非 `video` 或正在直播的视频
  4. ❌ 丢弃时长不在 `[min_duration, max_duration]` 范围的视频
  5. ❌ 丢弃点赞数低于阈值的视频
  6. ❌ 可选丢弃无字幕或无人工字幕的视频
- ✅ 输出仅保留：
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

### ✅ **Stage 3｜下载音频与字幕**
- 调用 `yt-dlp` 自动下载：
  - 最佳音频流（`ba`）
  - 优先下载目标语言的**手动字幕**，若无则尝试自动字幕
- 所有已下载记录会保存到 `downloaded_ids.txt`，防止重复下载。

---

### ✅ **Stage 4｜按字幕切分音频**
- 使用 `.vtt` 字幕对音频文件进行精准切片（VAD）。
- 切分输出可自定义：
  - `slice_sample_rate`（默认 16kHz）
  - `slice_save_audio`（是否实际导出 `.wav`，仅保留 JSON 也可）
- 输出格式：
  ```plaintext
  output/{channel}/segments/{video_id}/
    ├── wav/            # 切片音频（可选）
    ├── segments.json   # JSON：记录每段起止时间、文本、文件路径

## 使用说明

- 所有参数配置均集中在 `config/` 文件夹下，可在 `run.sh` 中通过修改 `CONFIG_NAME` 选择使用哪套配置。

- 请将cookies保存至 `config/cookies.txt`

- 在 `run.sh` 中调整 `stage` 参数，即可切换执行到不同阶段（爬去 / 筛选 / 下载 / 切分）。

## ❓ FAQ

---

**Q: 如何导出 Cookies？**

<建议使用google浏览器！>

1. 登录 [youtube.com](https://www.youtube.com) 
2. 跳转到 https://www.youtube.com/robots.txt
3. 使用浏览器插件 **Get cookies.txt LOCALLY**  
4. 保存为 **Netscape 格式** 文件 `cookies.txt`  
5. 覆盖到 `config/` 中指定位置
6. **立刻退出账号，否则cookies会自动刷新**

---

**Q: yt-dlp报错当前视频 not available，或当前超出速率限制，或其他奇怪错误**  

请先按照以下顺序尝试：

1. 更换cookies。注意更换完成后立即退出账号，且不能登陆。
2. 更换ip节点，并检查curl -I youtube.com是否正常返回。
3. 升级yt-dlp到最新版。
4. 更换youtube账号。

如还不能解决，请尝试下载其他频道。

---

---

**Q: 如何避免重复下载？**  
已下载 ID 自动记录到 `downloaded_ids.txt`，多次执行不会重复下载相同视频。

---

**Q: 如何只要切片 JSON？**  
把 `slice_save_audio` 设置为 `false`，只会生成 JSON，不会实际导出 `.wav`。
