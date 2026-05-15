import os
import re
import requests
from datetime import datetime, timedelta, timezone
from typing import Optional

from config import YOUTUBE_API_KEY, BASE_URL, MAX_RESULTS

# Proxy: use env vars if set (cloud servers usually direct), otherwise try local proxy
PROXY = os.environ.get("HTTP_PROXY") or os.environ.get("HTTPS_PROXY") or ""
PROXIES = {"http": PROXY, "https": PROXY} if PROXY else {}

DURATION_MAP = {
    "all": "any",
    "short": "short",
    "medium": "medium",
    "long": "long",
}

TIME_MAP = {
    "last week": timedelta(days=7),
    "last month": timedelta(days=30),
    "last year": timedelta(days=365),
}

# Chinese trending/evergreen keywords for automatic fallback when lang=zh and results are sparse
ZH_FALLBACK_KEYWORDS = [
    "心理 成长 人生",
    "赚钱 理财 投资",
    "AI 人工智能",
    "健身 健康 运动",
    "旅行 美食 生活",
    "职场 创业 商业",
    "教育 学习 知识",
    "科技 数码 手机",
]


def _has_chinese(text: str) -> bool:
    return bool(re.search(r"[一-鿿㐀-䶿]", text))


def _detect_lang_flag(title: str, language: str) -> str:
    if language == "zh":
        return "[CN]"
    elif language == "en":
        return "[EN]"
    return "[CN]" if _has_chinese(title) else "[EN]"


def _published_after(time_range: str) -> str:
    days = TIME_MAP.get(time_range)
    if days is None:
        return ""
    after = datetime.now(timezone.utc) - days
    return after.strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_duration(iso_duration: str) -> str:
    """Convert ISO 8601 duration (PT4M30S) to readable format (4:30)."""
    import re
    m = re.search(r"PT?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_duration)
    if not m:
        return iso_duration
    h, mi, s = m.groups()
    parts = []
    if h:
        parts.append(h)
    mi = mi or "0"
    parts.append(mi.zfill(2) if h else mi)
    s = s or "0"
    parts.append(s.zfill(2))
    return ":".join(parts)


def search_videos(
    keyword: str,
    time_range: str = "",
    max_results: int = MAX_RESULTS,
    language: str = "zh",
    duration: str = "all",
) -> list[dict]:
    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "order": "viewCount",
        "maxResults": min(max_results, 50),
        "key": YOUTUBE_API_KEY,
    }
    if language in ("zh", "en"):
        params["relevanceLanguage"] = language
    duration_param = DURATION_MAP.get(duration, "any")
    if duration_param != "any":
        params["videoDuration"] = duration_param

    published_after = _published_after(time_range)
    if published_after:
        params["publishedAfter"] = published_after

    resp = requests.get(f"{BASE_URL}/search", params=params, proxies=PROXIES)
    resp.raise_for_status()
    data = resp.json()

    items = data.get("items", [])
    if not items:
        return []

    video_ids = [item["id"]["videoId"] for item in items]

    stats_params = {
        "part": "statistics,contentDetails",
        "id": ",".join(video_ids),
        "key": YOUTUBE_API_KEY,
    }
    stats_resp = requests.get(f"{BASE_URL}/videos", params=stats_params, proxies=PROXIES)
    stats_resp.raise_for_status()
    stats_data = stats_resp.json()

    stats_map = {}
    for item in stats_data.get("items", []):
        stats_map[item["id"]] = {
            "statistics": item.get("statistics", {}),
            "contentDetails": item.get("contentDetails", {}),
        }

    results = []
    for item in items:
        vid = item["id"]["videoId"]
        snippet = item["snippet"]
        combined = stats_map.get(vid, {})
        stat = combined.get("statistics", {})
        details = combined.get("contentDetails", {})
        try:
            view_count = int(stat.get("viewCount", 0))
        except (ValueError, TypeError):
            view_count = 0

        results.append({
            "title": snippet["title"],
            "video_id": vid,
            "url": f"https://www.youtube.com/watch?v={vid}",
            "channel": snippet["channelTitle"],
            "published_at": snippet["publishedAt"],
            "view_count": view_count,
            "duration": _parse_duration(details.get("duration", "")),
            "lang_flag": _detect_lang_flag(snippet["title"], language),
        })

    results.sort(key=lambda x: x["view_count"], reverse=True)
    return results


def search_multiple_keywords(
    keywords: list[str],
    time_range: str = "",
    max_results: int = MAX_RESULTS,
    language: str = "zh",
    duration: str = "all",
) -> dict[str, list[dict]]:
    result = {}
    for kw in keywords:
        result[kw] = search_videos(kw.strip(), time_range, max_results, language, duration)

    # Chinese automatic fallback: when results are sparse, supplement with trending topics
    if language == "zh":
        total_results = sum(len(v) for v in result.values())
        if total_results < len(keywords) * 3:
            for fw in ZH_FALLBACK_KEYWORDS:
                if fw not in keywords:
                    result[fw] = search_videos(fw, time_range, max_results, language, duration)

    return result


def check_api_key() -> bool:
    params = {
        "part": "snippet",
        "q": "test",
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY,
    }
    resp = requests.get(f"{BASE_URL}/search", params=params, proxies=PROXIES)
    return resp.status_code == 200
