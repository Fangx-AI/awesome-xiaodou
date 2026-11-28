import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import capture_github_metrics as metrics


class GithubMetricsTests(unittest.TestCase):
    def test_capture_keeps_assets_from_all_published_release_pages(self):
        stable = {
            "tag_name": "skill-v2.2.0", "id": 11, "published_at": "2026-11-28T08:30:00Z",
            "prerelease": False, "draft": False,
            "assets": [{"name": "xiaodou-skill.zip", "id": 301, "download_count": 4}],
        }
        previous = {
            **stable, "tag_name": "skill-v2.1.0", "id": 10,
            "assets": [{"name": "xiaodou-skill.zip", "id": 201, "download_count": 9}],
        }
        draft = {**stable, "tag_name": "private-draft", "draft": True}
        responses = {
            "": {"stargazers_count": 2, "forks_count": 0},
            "/traffic/views": {"uniques": 31},
            "/traffic/clones": {"uniques": 100},
            "/traffic/popular/paths": [],
            "/traffic/popular/referrers": [],
            "/releases/latest": stable,
            "/releases?per_page=100": [[stable, draft], [previous]],
        }
        with patch.object(metrics, "github", side_effect=lambda path="", **_: responses[path]) as github:
            observation = metrics.capture()
        github.assert_any_call("/releases?per_page=100", paginate=True)
        self.assertEqual(observation["latest_release"], {
            "tag": "skill-v2.2.0", "asset_downloads": {"xiaodou-skill.zip": 4},
        })
        releases = observation["published_releases"]
        self.assertEqual(set(releases), {"skill-v2.1.0", "skill-v2.2.0"})
        self.assertEqual(releases["skill-v2.1.0"]["assets"]["xiaodou-skill.zip"], {
            "id": 201, "download_count": 9,
        })

    def test_save_preserves_legacy_snapshots(self):
        old = {
            "observed_at_utc": "2026-11-27T13:30:00+00:00", "stars": 2,
            "latest_release": {"tag": "skill-v2.1.0", "asset_downloads": {"xiaodou-skill.zip": 1}},
        }
        new = {
            "observed_at_utc": "2026-11-28T08:30:00+00:00", "stars": 2,
            "latest_release": {"tag": "skill-v2.2.0", "asset_downloads": {"xiaodou-skill.zip": 1}},
            "published_releases": {"skill-v2.2.0": {"assets": {}}},
        }
        with TemporaryDirectory() as folder:
            path = Path(folder) / "metrics.json"
            metrics.save(path, old)
            metrics.save(path, new)
            snapshots = json.loads(path.read_text(encoding="utf-8"))["snapshots"]
            self.assertEqual(snapshots, {"2026-11-27": old, "2026-11-28": new})


if __name__ == "__main__":
    unittest.main()
