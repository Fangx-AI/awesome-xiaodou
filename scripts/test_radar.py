import io
import json
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import collect_radar as radar


class RadarTests(unittest.TestCase):
    def test_invite_code_boards_are_removed_without_hiding_experiences(self):
        self.assertIsNone(radar.classify_headline("小豆邀请码抓码站（社区收集）"))
        self.assertIsNone(radar.classify_headline("求小豆邀请码"))
        self.assertIsNone(radar.classify_headline("豆包小豆邀请码被抢疯了"))
        self.assertIsNone(radar.classify_headline("小豆实测：邀请码：DEMO123 有效至明天"))
        self.assertIsNone(radar.classify_headline("豆包小豆怎么注册：买码别交押金"))
        self.assertIsNone(radar.classify_headline("豆包小豆 500 个内测名额，自己填表申请"))
        self.assertIsNone(radar.classify_headline("豆包新 AI 助理小豆一码难求！全是黄牛！"))
        self.assertEqual(radar.classify_headline("试用了豆包小豆，读取授权账号概况"), "上手体验线索")
        self.assertEqual(radar.classify_headline("小豆首发实测：一码难求但玩法不少"), "上手体验线索")
        self.assertEqual(radar.classify_headline("体验小豆App：支持主动AI"), "上手体验线索")
        self.assertEqual(radar.classify_headline("小豆 · 官方邀请开通说明"), "其他公开线索")

    def test_x_retains_hands_on_reports_over_reactions(self):
        self.assertIsNone(radar.classify_headline("豆包小豆来了，试用名额很多", "X"))
        self.assertIsNone(radar.classify_headline("小豆邀请码都卖到了80块，附深度测评", "X"))
        self.assertEqual(radar.classify_headline("试用了小豆，总结抖音私信还不行", "X"), "上手体验线索")
        self.assertEqual(radar.classify_headline("实测小豆：替我打电话", "X"), "上手体验线索")
        self.assertEqual(radar.classify_headline("小豆帮大家梳理一下别人文章里的实测", "X"), "其他公开线索")

    def test_mobile_urls_and_already_cataloged_headlines_are_deduplicated(self):
        now = datetime(2026, 11, 28, 12, 10, tzinfo=radar.CHINA)
        reviewed = [{"url": "https://www.sohu.com/a/1105688835_161795",
                     "title": "豆包个人AI助理“小豆”公测，记者实测下达定时提醒任务"}]
        sources = [
            {"title": "豆包个人AI助理「小豆」公测：记者实测下达定时提醒任务",
             "url": "https://news.google.com/rss/articles/test"},
            {"title": "另一标题：实测小豆定时提醒", "url": "https://m.sohu.com/a/1105688835_161795?utm_source=test"},
            {"title": "小豆实测总结", "url": "https://m.sohu.com/a/1105688836_161795"},
        ]
        rows = [{**row, "first_seen": now.isoformat(), "published": now.isoformat(), "publisher": "Sohu"} for row in sources]
        self.assertEqual(radar.merge_queue(rows, [], reviewed, now), rows[-1:])

    def test_prefers_the_direct_link_and_preserves_the_original_detection_time(self):
        now = datetime(2026, 11, 28, 12, 10, tzinfo=radar.CHINA)
        detected = (now - timedelta(hours=1)).isoformat()
        previous = {"title": "实测小豆：替我打电话", "url": "https://news.google.com/rss/articles/test",
                    "published": detected, "first_seen": detected, "publisher": "X", "feed": "Google"}
        new_link = {**previous, "url": "https://x.com/example/status/1234", "first_seen": now.isoformat(), "feed": "Bing"}
        mirror = {**new_link, "title": "实测小豆电话", "url": "https://twitter.com/example/status/1234?s=20"}
        result = radar.merge_queue([previous], [new_link, mirror], [], now)
        self.assertEqual(result, [{**new_link, "first_seen": detected}])
        self.assertEqual(radar.merge_queue(result, [previous], [], now), result)

    def test_empty_results_distinguish_failed_sources(self):
        now = datetime.now(radar.CHINA)
        clean = radar.output_page([], now, [])
        counts = {label: 0 for label in radar.FEEDS if label != "Bing 新闻"}
        counts["Google 新闻 · 实测"] = 2
        partial = radar.output_page([], now, ["Bing 新闻"], counts)
        self.assertIn("Google 新闻 · 实测　2 条", partial)
        self.assertIn("Google 新闻 · 抖音与公众号　0 条", partial)
        self.assertIn("Bing 新闻　未读到", partial)
        self.assertIn("近 7 天暂无新线索", clean)
        self.assertIn("本次未读到：Bing 新闻", partial)
        self.assertNotIn("近 7 天暂无新线索", partial)

    def test_snapshot_updates_only_on_new_day_or_changed_content(self):
        now = datetime(2026, 11, 28, 12, 10, tzinfo=radar.CHINA)
        with TemporaryDirectory() as folder:
            page = Path(folder) / "radar.md"
            with patch.object(radar, "PAGE", page):
                with patch.dict(radar.os.environ, {"GITHUB_RUN_ID": "101"}):
                    radar.write_page([], now, [])
                first = page.read_text(encoding="utf-8")
                self.assertIn("12:10", first)
                self.assertIn("/runs/101)", first)
                with patch.dict(radar.os.environ, {"GITHUB_RUN_ID": "102"}):
                    radar.write_page([], now + timedelta(minutes=15), [])
                    self.assertEqual(page.read_text(encoding="utf-8"), first)
                    radar.write_page([], now + timedelta(minutes=15), ["Bing 新闻"])
                    second = page.read_text(encoding="utf-8")
                    self.assertIn("12:25", second)
                    self.assertIn("/runs/102)", second)
                    radar.write_page([], now + timedelta(days=1), ["Bing 新闻"])
                self.assertIn("2026-11-29", page.read_text(encoding="utf-8"))

    def test_total_failure_refreshes_status_without_rewriting_queue(self):
        now = datetime.now(radar.CHINA).isoformat(timespec="minutes")
        old_rows = [{"title": "小豆已有体验笔记", "url": "https://example.invalid/old",
                     "published": now, "first_seen": now, "feed": "Bing 新闻", "publisher": ""}]
        baseline = json.dumps(old_rows, ensure_ascii=False)
        with TemporaryDirectory() as folder:
            queue = Path(folder) / "radar.json"
            page = Path(folder) / "radar.md"
            queue.write_text(baseline, encoding="utf-8")
            with patch.multiple(radar, QUEUE=queue, PAGE=page), redirect_stdout(io.StringIO()):
                with patch.object(radar, "collect", side_effect=OSError), self.assertRaises(SystemExit):
                    radar.main()
            self.assertEqual(queue.read_text(encoding="utf-8"), baseline)
            status = page.read_text(encoding="utf-8")
            self.assertIn("本次读到 0/", status)
            self.assertIn("所有来源均未读到", status)
            self.assertIn("小豆已有体验笔记", status)


if __name__ == "__main__":
    unittest.main()
