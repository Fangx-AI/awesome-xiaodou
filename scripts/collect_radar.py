"""Collect public headlines for the XiaoDou editorial queue."""
import json
import os
import re
import unicodedata
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html import escape, unescape
from pathlib import Path
from urllib.parse import parse_qs, quote, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "data/radar.json"
PAGE = ROOT / "docs/radar.md"
CHINA = timezone(timedelta(hours=8))


def google(query):
    return "https://news.google.com/rss/search?" + urlencode(
        {"q": query, "hl": "zh-CN", "gl": "CN", "ceid": "CN:zh-Hans"}
    )


FEEDS = {
    "Google 新闻 · 实测": google('"小豆" "豆包" (实测 OR 体验 OR 玩法) when:7d'),
    "Google 新闻 · 工作流": google('"小豆" "豆包" (抖音 OR 飞书 OR 提示词) when:7d'),
    "Google 新闻 · 社区": google('"小豆" "豆包" (site:linux.do OR site:weibo.com OR site:watcha.cn OR site:github.com) when:7d'),
    "Bing 新闻": "https://www.bing.com/news/search?" + urlencode(
        {"q": '"豆包" "小豆" 实测 玩法', "format": "rss"}
    ),
    "华尔街见闻": "https://dedicated.wallstreetcn.com/rss.xml",
    "IT之家": "https://www.ithome.com/rss/",
}


def canonical_url(url):
    parts = urlsplit(url.strip())
    if parts.hostname and parts.hostname.endswith(".bing.com"):
        destination = parse_qs(parts.query).get("url", [""])[0]
        if destination:
            parts = urlsplit(destination)
    if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username is not None:
        return ""
    params = parse_qs(parts.query, keep_blank_values=True)
    for name in list(params):
        if name.lower().startswith("utm_") or name in {"gclid", "fbclid", "oc"}:
            del params[name]
    return urlunsplit((parts.scheme, parts.netloc.lower(), parts.path or "/", urlencode(params, doseq=True), ""))


def normalize_title(title):
    return re.sub(r"[^\w]+", "", unicodedata.normalize("NFKC", title).casefold())


def is_playbook_lead(title):
    if re.search(r"邀请码(出售|交易|接力|互助)|求.{0,8}邀请码|邀请码.{0,12}(元|套利|炒)", title):
        return False
    if re.search(r"公测|上线|发布", title):
        return bool(re.search(r"实测|上手|测评|玩法|复盘|搭建|整理|体验[:：]|怎么用|教程", title))
    return True


def collect(label, url, now):
    request = Request(url, headers={"User-Agent": "AwesomeXiaodou-Radar/1.0"})
    with urlopen(request, timeout=18) as response:
        body = response.read(8_000_001)
    if len(body) > 8_000_000 or b"<!DOCTYPE" in body.upper():
        raise ValueError("unsupported feed document")
    tree = ET.fromstring(body)
    channel = tree.find("channel")
    if channel is None:
        raise ValueError("expected an RSS channel")
    candidates = []
    for item in channel.findall("item"):
        headline = " ".join(unescape(item.findtext("title", "")).split())
        publisher = " ".join(item.findtext("source", "").split())
        suffix = " - " + publisher
        if publisher and headline.endswith(suffix):
            headline = headline[:-len(suffix)]
        description = item.findtext("description", "")[:1500]
        text = headline + " " + description
        if "小豆" not in headline or not any(term in text for term in ("豆包", "字节", "个人助理", "Personal Agent")):
            continue
        if not is_playbook_lead(headline):
            continue
        try:
            link = canonical_url(item.findtext("link", ""))
            published = parsedate_to_datetime(item.findtext("pubDate", "")).astimezone(CHINA)
        except (ValueError, TypeError, OverflowError):
            continue
        if link and now - timedelta(days=7) <= published <= now + timedelta(hours=1):
            candidates.append({"title": headline[:140], "url": link,
                               "published": published.isoformat(timespec="minutes"),
                               "first_seen": now.isoformat(timespec="minutes"),
                               "feed": label, "publisher": publisher[:80]})
    return candidates


def markdown_text(value):
    return re.sub(r'([\\`*_\[\]~!|@])', r'\\\1', escape(value))


def output_page(rows, now, failures):
    lines = [
        "# 小豆玩法雷达", "",
        "这里收集近 7 天的公开新闻和社区线索。GitHub Actions 每 15 分钟排程，实际运行可能晚于排程。"
        "下方时间为来源发布时间（北京时间）。", "",
        "[回到玩法库](../README.md) · [抓取记录](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/radar.yml)"
        " · [提交新玩法](https://github.com/Fangx-AI/awesome-xiaodou/issues/new/choose)", "",
        "社区讨论：[观猹 · 小豆产品页](https://watcha.cn/products/xiao-dou) · [已经整理成指令的更新](updates.md)", "",
    ]
    succeeded = len(FEEDS) - len(failures)
    lines.extend([f"扫描日期：{now.date()}（北京时间）。本次读到 {succeeded}/{len(FEEDS)} 个配置来源。", ""])
    if failures:
        labels = "、".join(markdown_text(name) for name in failures)
        lines.extend([f"本次未读到：{labels}。", ""])
    if not succeeded:
        lines.extend(["所有来源均未读到，以下保留上一次线索。", ""])
    if rows:
        latest = max(row["first_seen"] for row in rows)
        lines.extend([f"最新入列：{latest[:16].replace('T', ' ')}（北京时间）", ""])
    for row in rows:
        link = quote(row["url"], safe=":/?&=%+-._~#")
        source = markdown_text(row["publisher"] or row["feed"])
        title = markdown_text(row["title"])
        lines.append(f'- {row["published"][:16].replace("T", " ")} · [{title}](<{link}>) · {source}')
    if not rows and not failures:
        lines.append("近 7 天暂无新线索。")
    elif not rows:
        lines.append("目前没有可展示的线索，仍有来源待检查。")
    return "\n".join(lines) + "\n"


def main():
    now = datetime.now(CHINA)
    summary = []
    scanned = []
    failures = []
    with ThreadPoolExecutor(max_workers=len(FEEDS)) as pool:
        jobs = {label: pool.submit(collect, label, url, now) for label, url in FEEDS.items()}
        for label, job in jobs.items():
            try:
                rows = job.result()
                scanned.extend(rows)
                summary.append(f"- {label}：{len(rows)} 条候选")
            except (OSError, ValueError, ET.ParseError) as error:
                failures.append(label)
                summary.append(f"- {label}：失败 ({type(error).__name__})")
    print("\n".join(summary))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as log:
            log.write("## 数据源扫描\n\n" + "\n".join(summary) + "\n")
    previous = json.loads(QUEUE.read_text(encoding="utf-8")) if QUEUE.exists() else []
    if len(failures) == len(FEEDS):
        PAGE.write_text(output_page(previous, now, failures), encoding="utf-8")
        raise SystemExit("All feed requests failed; preserved the existing queue.")

    existing = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
    urls = {canonical_url(source["url"]) for source in existing}
    titles = {normalize_title("豆包推出小豆，大厂争夺个人AI入口")}
    queue = []
    # Keep prior metadata stable across scans and retain results through partial outages.
    for row in previous + scanned:
        if datetime.fromisoformat(row["published"]) < now - timedelta(days=7):
            continue
        if not is_playbook_lead(row["title"]):
            continue
        title = normalize_title(row["title"])
        if title in titles or row["url"] in urls:
            continue
        titles.add(title)
        urls.add(row["url"])
        queue.append(row)
    queue.sort(key=lambda row: (row["published"], row["url"]), reverse=True)
    queue = queue[:80]
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PAGE.write_text(output_page(queue, now, failures), encoding="utf-8")
    print(f"Radar: {len(queue)} leads in the rolling queue.")


if __name__ == "__main__":
    main()
