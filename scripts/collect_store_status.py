"""Capture storefront metadata from the public Apple and Xiaomi listings."""
import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/app-stores.json"
PAGE = ROOT / "docs/app-stores.md"
APPLE_PAGE = "https://apps.apple.com/cn/app/id6815582077"
XIAOMI_PAGE = "https://app.mi.com/details?id=com.larus.doubaom"
VERSION = r"[0-9]{1,4}(?:\.[0-9]{1,4}){1,3}"


def version(value):
    if not isinstance(value, str) or not re.fullmatch(VERSION, value):
        raise ValueError("Unrecognized version")
    return value


def apple_metadata(payload):
    result = next((row for row in json.loads(payload)["results"]
                   if row.get("trackId") == 6815582077), None)
    if result is None:
        raise ValueError("App Store lookup did not return Xiaodou")
    return {"version": version(result["version"]),
            "minimum_ios": version(result["minimumOsVersion"])}


def xiaomi_metadata(payload):
    label = re.search(r">\s*版本号\s*</div>\s*<div[^>]*>\s*(" + VERSION + r")\s*</div>", payload)
    if not label or not re.search(r">\s*com\.larus\.doubaom\s*<", payload):
        raise ValueError("Xiaomi listing identity or version not found")
    maintenance = re.search(r'<a\b[^>]*\bid=["\']maintenanceDownloadBtn["\'][^>]*>\s*维护中\s*</a>', payload)
    return {"version": label[1], "download_maintenance": bool(maintenance)}


SOURCES = {
    "apple": ("https://itunes.apple.com/lookup?id=6815582077&country=cn", apple_metadata),
    "xiaomi": (XIAOMI_PAGE, xiaomi_metadata),
}


def fetch(url, parse):
    request = Request(url, headers={"User-Agent": "AwesomeXiaodou-StoreStatus/1.0"})
    with urlopen(request, timeout=12) as response:
        body = response.read(2_000_001)
    if len(body) > 2_000_000:
        raise ValueError("Store response exceeded the size limit")
    return parse(body.decode("utf-8"))


def merge(previous, scanned, today):
    return {
        key: {"check": "success", "observed_on": today, "listing": scanned[key]}
        if key in scanned else {**previous.get(key, {}), "check": "unavailable"}
        for key in SOURCES
    }


def listing_text(key, row):
    listing = row.get("listing")
    if not listing:
        return "暂无可核对的版本"
    if key == "apple":
        return f"{listing['version']} · 最低 iOS {listing['minimum_ios']}"
    state = "网页显示维护中" if listing["download_maintenance"] else "网页下载状态待核"
    return f"{listing['version']} · {state}"


def render(snapshots):
    lines = [
        "# 小豆公开商店条目", "",
        "[下载和开通](install.md#下载和开通) · [真机使用记录](field-tests/README.md)", "",
        "随玩法雷达检查两个公开商店条目。设备能否安装、账号能否开通，以及 Skill 能否执行任务，按各自的实际结果登记。", "",
        "| 商店 | 商店显示 | 上次成功读取（北京时间） | 本轮检查 |", "| --- | --- | --- | --- |",
    ]
    links = {"apple": f"[中国区 App Store]({APPLE_PAGE})",
             "xiaomi": f"[小米应用商店]({XIAOMI_PAGE})"}
    for key, link in links.items():
        row = snapshots[key]
        check = "已读到" if row["check"] == "success" else "暂未读到"
        lines.append(f"| {link} | {listing_text(key, row)} | {row.get('observed_on', '暂无')} | {check} |")
    return "\n".join(lines) + "\n"


def write_if_changed(path, content):
    if not path.exists() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8", newline="\n")


def main():
    today = datetime.now(timezone(timedelta(hours=8))).date().isoformat()
    previous = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else {}
    scanned = {}
    with ThreadPoolExecutor(max_workers=len(SOURCES)) as pool:
        jobs = {key: pool.submit(fetch, *source) for key, source in SOURCES.items()}
        for key, job in jobs.items():
            try:
                scanned[key] = job.result()
            except (OSError, ValueError, TypeError, KeyError, AttributeError) as error:
                print(f"{key}: listing unavailable ({type(error).__name__})")
            else:
                print(f"{key}: {scanned[key]['version']}")
    snapshots = merge(previous, scanned, today)
    write_if_changed(DATA, json.dumps(snapshots, ensure_ascii=False, indent=2) + "\n")
    write_if_changed(PAGE, render(snapshots))


if __name__ == "__main__":
    main()
