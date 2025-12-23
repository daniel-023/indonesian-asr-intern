import json
import yaml
import logging
from pathlib import Path
import argparse

logging.basicConfig(level=logging.WARNING, format="%(message)s")


def is_any_a_in_b(list_a, list_b):
    """
    判断 list_a 中是否至少有一个元素在 list_b 中（忽略大小写）
    """
    normalized_set_b = set(str(item).lower() for item in list_b)
    return any(str(item).lower() in normalized_set_b for item in list_a)


def filter_info_file(config_path, info_file):
    # ==== 📄 加载配置 ====
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    filter_cfg = config.get("filter", {})

    enable_language_filter = filter_cfg.get("enable_language_filter", False)
    target_language_abbr = filter_cfg.get("target_language_abbr", [])

    enable_duration_filter = filter_cfg.get("enable_duration_filter", False)
    min_duration = filter_cfg.get("min_duration", 0)
    max_duration = filter_cfg.get("max_duration", 999999)

    enable_like_count_filter = filter_cfg.get("enable_like_count_filter", False)
    min_like_count = filter_cfg.get("min_like_count", 0)

    filter_no_subtitle = filter_cfg.get("filter_no_subtitle", False)
    filter_no_manual_subtitle = filter_cfg.get("filter_no_manual_subtitle", False)

    # === 输出新文件名 ===
    output_file = Path(info_file).with_name(
        Path(info_file).stem + "-filtered.jsonl"
    )

    with open(info_file, encoding="utf-8", errors="ignore") as f1, \
         open(output_file, "w", encoding="utf-8") as f2:

        for line_num, line in enumerate(f1, 1):
            try:
                info = json.loads(line)
            except json.JSONDecodeError:
                logging.warning(f"❌ 跳过：第 {line_num} 行不是合法 JSON")
                continue

            if enable_language_filter:
                if not is_any_a_in_b([info.get("language")], target_language_abbr):
                    logging.warning(f"❌ 跳过：语言 '{info.get('language')}' 不在 {target_language_abbr}")
                    continue

            if enable_duration_filter:
                duration = info.get("duration", 0)
                if not (min_duration <= duration <= max_duration):
                    logging.warning(f"❌ 跳过：Duration {duration} 不在 [{min_duration}, {max_duration}]")
                    continue

            if enable_like_count_filter:
                like_count = info.get("like_count")
                if like_count is not None and like_count < min_like_count:
                    logging.warning(f"❌ 跳过：点赞数 {like_count} 小于 {min_like_count}")
                    continue

            subtitles = info.get("subtitles", [])
            if filter_no_subtitle:
                if not subtitles:
                    logging.warning("❌ 跳过：没有字幕（subtitles 列表为空）")
                    continue

            if filter_no_manual_subtitle:
                has_manual = any(sub.get("type") == "manual" for sub in subtitles)
                if not has_manual:
                    logging.warning("❌ 跳过：无人工字幕（subtitles 中无 manual）")
                    continue

            fields_to_keep = [
                "channel_id",
                "id",
                "title",
                "description",
                "duration",
                "upload_date",
                "like_count",
                "language",
                "subtitles"
            ]
            filtered_info = {field: info.get(field) for field in fields_to_keep}
            f2.write(json.dumps(filtered_info, ensure_ascii=False) + "\n")

    print(f"✅ 过滤完成，新文件输出：{output_file}")


# ========= 🚀 入口 =========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="过滤 JSONL 元数据文件")
    parser.add_argument("--config", type=str, required=True, help="YAML 配置文件路径")
    args = parser.parse_args()

    config_path = args.config

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    channel = config.get("channel")
    if not channel:
        raise ValueError("❌ 配置中缺少 `channel` 字段")

    info_file = f"/content/drive/MyDrive/GigaSpeech2/id/raw_audio/Mono/{channel}/info/video_metadata.jsonl"

    filter_info_file(config_path=config_path, info_file=info_file)
