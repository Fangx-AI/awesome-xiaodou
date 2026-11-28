import io
import json
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import collect_radar as radar


class RadarTests(unittest.TestCase):
    def test_empty_results_distinguish_failed_sources(self):
        now = datetime.now(radar.CHINA)
        clean = radar.output_page([], now, [])
        partial = radar.output_page([], now, ["Bing 新闻"])
        self.assertIn("近 7 天暂无新线索", clean)
        self.assertIn("本次未读到：Bing 新闻", partial)
        self.assertNotIn("近 7 天暂无新线索", partial)

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
