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
    "Google 新闻 · 知乎与视频社区": google(
        '"小豆" "豆包" (实测 OR 上手 OR 试用 OR 体验) '
        '(site:zhihu.com OR site:bilibili.com OR site:xiaohongshu.com OR site:x.com) when:7d'
    ),
    "Google 新闻 · 抖音与公众号": google(
        '"小豆" "豆包" (site:douyin.com OR site:mp.weixin.qq.com) when:7d'
    ),
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


def article_key(url):
    parts = urlsplit(canonical_url(url))
    host = parts.hostname
    if host in {"www.sohu.com", "m.sohu.com"} and re.fullmatch(r"/a/\d+_\d+/?", parts.path):
        return "sohu:" + parts.path.rstrip("/")
    if host in {"www.nbd.com.cn", "m.nbd.com.cn"} and re.fullmatch(r"/articles/\d{4}-\d{2}-\d{2}/\d+\.html", parts.path):
        return "nbd:" + parts.path
    if host in {"weibo.com", "www.weibo.com", "m.weibo.cn", "sina.cn", "www.sina.cn"}:
        post = re.fullmatch(r"/(?:\d+/|news/)?detail/(\d+)(?:\.html)?/?", parts.path)
        if post:
            return "weibo:" + post[1]
    if host in {"x.com", "www.x.com", "twitter.com", "mobile.twitter.com", "www.twitter.com"}:
        post = re.fullmatch(r"/[^/]+/status/(\d+)/?", parts.path)
        if post:
            return "x:" + post[1]
    return parts.geturl()


def google_article(url):
    parts = urlsplit(url)
    return parts.hostname == "news.google.com" and parts.path.startswith(("/rss/articles/", "/articles/"))


def classify_headline(title, publisher=""):
    if re.search(
        r"抓码站|买码|卖码|邀请码(出售|交易|接力|互助|主要靠)|求.{0,8}邀请码|"
        r"邀请码.{0,12}(元|块|套利|炒|卖到|被抢疯)|邀请码\s*[:：]\s*[A-Z0-9]{5,12}\b|"
        r"一码难求.{0,10}(全是黄牛|黄牛开价)",
        title,
    ):
        return None
    if re.search(r"内测招募|内测名额.{0,15}(手慢无|申请|招募)", title):
        return None
    if re.search(r"帮大家梳理.{0,18}实测|一手评测来了.{0,8}这个说|转述.{0,12}(测评|实测)|转载.{0,12}(测评|实测)", title):
        return "其他公开线索"
    if publisher.casefold() == "x" and not re.search(
        r"^实测|试用[了过]|试完|我.{0,12}(用小豆|让小豆|实测|刚用|刚试|测了)",
        title,
    ):
        return None
    if re.search(r"实测|上手|测评|玩法|复盘|搭建|整理|试用|体验(?:小豆|[:：])|怎么用|教程", title):
        return "上手体验线索"
    if re.search(r"公测|上线|发布", title):
        return None
    return "其他公开线索"


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
        try:
            link = canonical_url(item.findtext("link", ""))
            published = parsedate_to_datetime(item.findtext("pubDate", "")).astimezone(CHINA)
        except (ValueError, TypeError, OverflowError):
            continue
        if not publisher and article_key(link).startswith("x:"):
            publisher = "X"
        if classify_headline(headline, publisher) is None:
            continue
        if link and now - timedelta(days=7) <= published <= now + timedelta(hours=1):
            candidates.append({"title": headline[:140], "url": link,
                               "published": published.isoformat(timespec="minutes"),
                               "first_seen": now.isoformat(timespec="minutes"),
                               "feed": label, "publisher": publisher[:80]})
    return candidates


def markdown_text(value):
    return re.sub(r'([\\`*_\[\]~!|@])', r'\\\1', escape(value))


def output_page(rows, now, failures, candidate_counts=None):
    lines = [
        "# 小豆玩法雷达", "",
        "这里收集近 7 天的公开新闻和社区线索。按 15 分钟排程，首页、玩法或来源更新时也会扫描。GitHub 定时运行可能延迟。"
        "线索未变时，页面保留最近的内容快照。每次扫描的实际时间和读取结果见运行摘要。"
        "下方是检索入口索引的标题和发布时间（北京时间）。已读原文并纳入玩法的报道可在来源登记里查到。", "",
        "[回到玩法库](../README.md) · [查看最近一次扫描](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/radar.yml)"
        " · [仅看自动定时扫描](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/radar.yml?query=event%3Aschedule)"
        " · [提交新玩法](https://github.com/Fangx-AI/awesome-xiaodou/issues/new/choose)", "",
        "社区讨论：[观猹 · 小豆产品页](https://watcha.cn/products/xiao-dou) · [已整理的玩法更新](updates.md) · [来源登记](source-ledger.md)", "",
    ]
    succeeded = len(FEEDS) - len(failures)
    lines.extend([f"本次读到 {succeeded}/{len(FEEDS)} 个检索入口。", ""])
    scan = f"快照扫描时间：{now:%Y-%m-%d %H:%M}（北京时间）"
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    if re.fullmatch(r"[0-9]+", run_id):
        scan += f" · [生成此快照的扫描](https://github.com/Fangx-AI/awesome-xiaodou/actions/runs/{run_id})"
    lines.extend([scan, ""])
    if failures:
        labels = "、".join(markdown_text(name) for name in failures)
        lines.extend([f"本次未读到：{labels}。", ""])
    if candidate_counts is not None:
        lines.extend(["<details>", "<summary>查看各入口本轮命中的候选数</summary>", "",
                      "候选数为去重前的数量。读到 0 条表示本轮没有匹配，不代表平台上没有内容。", ""])
        for label in FEEDS:
            count = candidate_counts.get(label)
            status = "未读到" if count is None else f"{count} 条"
            lines.append(f"- {markdown_text(label)}　{status}")
        lines.extend(["", "</details>", ""])
    if not succeeded:
        lines.extend(["所有来源均未读到，以下保留上一次线索。", ""])
    groups = {"上手体验线索": [], "其他公开线索": []}
    for row in rows:
        category = classify_headline(row["title"], row["publisher"])
        if category:
            groups[category].append(row)
    latest = max((row["first_seen"] for leads in groups.values() for row in leads), default=None)
    if latest:
        lines.extend([f"最新入列：{latest[:16].replace('T', ' ')}（北京时间）", ""])
    for category, leads in groups.items():
        if not leads:
            continue
        lines.extend([f"## {category}", ""])
        for row in leads:
            link = quote(row["url"], safe=":/?&=%+-._~#")
            source = markdown_text(row["publisher"] or row["feed"])
            title = markdown_text(row["title"])
            lines.append(f'- {row["published"][:16].replace("T", " ")} · [{title}](<{link}>) · {source}')
        lines.append("")
    if not latest and not failures:
        lines.append("近 7 天暂无新线索。")
    elif not latest:
        lines.append("目前没有可展示的线索，仍有来源待检查。")
    return "\n".join(lines) + "\n"


def write_page(rows, now, failures, candidate_counts=None):
    page = output_page(rows, now, failures, candidate_counts)
    previous_page = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
    stamp = r"^快照扫描时间：(\d{4}-\d{2}-\d{2})[^\n]*"
    if re.sub(stamp, r"\1", page, flags=re.M) != re.sub(stamp, r"\1", previous_page, flags=re.M):
        PAGE.write_text(page, encoding="utf-8")


def merge_queue(previous, scanned, existing, now):
    reviewed_urls = {
        article_key(url)
        for source in existing
        for url in (source["url"], source.get("mirror"))
        if url
    }
    reviewed_titles = {normalize_title("豆包推出小豆，大厂争夺个人AI入口")}
    reviewed_titles.update(normalize_title(source["title"]) for source in existing if source.get("title"))
    by_title, by_url, queue = {}, {}, []
    for row in previous + scanned:
        if datetime.fromisoformat(row["published"]) < now - timedelta(days=7):
            continue
        title = normalize_title(row["title"])
        url = article_key(row["url"])
        publisher = "X" if url.startswith("x:") else row["publisher"]
        if title in reviewed_titles or url in reviewed_urls or classify_headline(row["title"], publisher) is None:
            continue
        position = by_url.get(url, by_title.get(title))
        if position is None:
            position = len(queue)
            queue.append({**row, "publisher": publisher})
        elif google_article(queue[position]["url"]) and not google_article(row["url"]):
            queue[position] = {**row, "publisher": publisher, "first_seen": queue[position]["first_seen"]}
        by_title[title] = by_url[url] = position
    queue.sort(key=lambda row: (row["published"], row["url"]), reverse=True)
    return queue[:80]


def main():
    now = datetime.now(CHINA)
    summary = []
    scanned = []
    failures = []
    candidate_counts = {}
    with ThreadPoolExecutor(max_workers=len(FEEDS)) as pool:
        jobs = {label: pool.submit(collect, label, url, now) for label, url in FEEDS.items()}
        for label, job in jobs.items():
            try:
                rows = job.result()
                scanned.extend(rows)
                candidate_counts[label] = len(rows)
                summary.append(f"- {label}：{len(rows)} 条候选")
            except (OSError, ValueError, ET.ParseError) as error:
                failures.append(label)
                summary.append(f"- {label}：失败 ({type(error).__name__})")
    print("\n".join(summary))
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as log:
            log.write(f"## 数据源扫描\n\n实际检查时间 {now:%Y-%m-%d %H:%M}（北京时间）。"
                      f"读到 {len(FEEDS) - len(failures)}/{len(FEEDS)} 个入口。\n\n"
                      + "\n".join(summary) + "\n")
    previous = json.loads(QUEUE.read_text(encoding="utf-8")) if QUEUE.exists() else []
    if len(failures) == len(FEEDS):
        write_page(previous, now, failures, candidate_counts)
        raise SystemExit("All feed requests failed; preserved the existing queue.")

    existing = json.loads((ROOT / "data/sources.json").read_text(encoding="utf-8"))
    queue = merge_queue(previous, scanned, existing, now)
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_page(queue, now, failures, candidate_counts)
    print(f"Radar: {len(queue)} leads in the rolling queue.")


if __name__ == "__main__":
    main()
