import argparse
import sys

from youtube_api import search_videos, search_multiple_keywords, check_api_key
from config import YOUTUBE_API_KEY

LANG_LABELS = {"zh": "中文", "en": "English", "all": "不限"}
DURATION_LABELS = {"all": "不限", "short": "Shorts / 短视频 (≤4分钟)", "medium": "中等 (4-20分钟)", "long": "长视频 (>20分钟)"}


def print_table(results: list[dict], keyword: str):
    if not results:
        print(f"  [{keyword}] No results found.\n")
        return
    print(f"\n{'='*130}")
    print(f"  Keyword: {keyword}")
    print(f"{'='*130}")
    header = f"{'#':<4} {'Title':<55} {'Views':<14} {'Duration':<10} {'Channel':<20} {'Published':<22}"
    print(header)
    print("-" * len(header))
    for i, v in enumerate(results, 1):
        flag = v.get("lang_flag", "")
        title_base = v["title"]
        title_with_flag = f"{title_base} {flag}" if flag else title_base
        title_disp = (
            title_with_flag[:53] + ".."
            if len(title_with_flag) > 53
            else title_with_flag
        )
        views = f"{v['view_count']:,}"
        print(
            f"{i:<4} {title_disp:<55} {views:<14} {v['duration']:<10} {v['channel']:<20} {v['published_at'][:10]}"
        )
    print()


def main():
    parser = argparse.ArgumentParser(
        description="YouTube Trending Topic Scraper"
    )
    parser.add_argument("keywords", nargs="+", help="Keywords to search")
    parser.add_argument(
        "--time", "-t",
        choices=["last week", "last month", "last year"],
        default="",
        help="Time range filter"
    )
    parser.add_argument(
        "--max", "-m",
        type=int,
        default=10,
        help="Max results per keyword (default: 10)"
    )
    parser.add_argument(
        "--lang", "-l",
        choices=["zh", "en", "all"],
        default="zh",
        help="Language filter: zh (Chinese), en (English), all (unlimited)  (default: zh)"
    )
    parser.add_argument(
        "--duration", "-d",
        choices=["all", "short", "medium", "long"],
        default="all",
        help="Video duration filter: all (unlimited), short (≤4min), medium (4-20min), long (>20min)  (default: all)"
    )
    parser.add_argument(
        "--check-key",
        action="store_true",
        help="Only check if API key is valid, then exit"
    )

    args = parser.parse_args()

    if YOUTUBE_API_KEY == "YOUR_API_KEY_HERE":
        print("ERROR: Please set your YouTube API key.")
        print("       Option 1: Create a .env file with YOUTUBE_API_KEY=your_key")
        print("       Option 2: Export environment variable: export YOUTUBE_API_KEY=your_key")
        print("       Get your API key at: https://console.cloud.google.com/apis/credentials")
        sys.exit(1)

    if args.check_key:
        ok = check_api_key()
        print("API key is valid." if ok else "API key is INVALID.")
        sys.exit(0 if ok else 1)

    lang_label = LANG_LABELS.get(args.lang, args.lang)
    print(f"\nLanguage filter: {lang_label} ({args.lang})")

    duration_label = DURATION_LABELS.get(args.duration, args.duration)
    print(f"Duration filter: {duration_label} ({args.duration})")

    results = search_multiple_keywords(args.keywords, args.time, args.max, args.lang, args.duration)
    for kw, items in results.items():
        print_table(items, kw)


if __name__ == "__main__":
    main()
