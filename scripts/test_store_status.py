import unittest

from collect_store_status import apple_metadata, merge, render, xiaomi_metadata


class AppStoreTests(unittest.TestCase):
    def test_apple_selects_exact_product_and_omits_legacy_rating(self):
        payload = '''{"results": [{"trackId": 5, "version": "1.0"},
            {"trackId": 6815582077, "version": "15.9.0",
             "minimumOsVersion": "15.0", "contentAdvisoryRating": "17+"}]}'''
        self.assertEqual(apple_metadata(payload), {"version": "15.9.0", "minimum_ios": "15.0"})
        with self.assertRaises(ValueError):
            apple_metadata('{"results": []}')

    def test_xiaomi_needs_both_package_identity_and_structured_version(self):
        entry = '<div>com.larus.doubaom</div><div>版本号</div>\n<div style="float:right">16.0.0</div>'
        button = '<a id="maintenanceDownloadBtn" class="download">维护中</a>'
        self.assertEqual(xiaomi_metadata(entry + button), {"version": "16.0.0", "download_maintenance": True})
        self.assertFalse(xiaomi_metadata(entry + '<p>评论说维护中</p>')["download_maintenance"])
        with self.assertRaises(ValueError):
            xiaomi_metadata(entry.replace("com.larus.doubaom", "example.app"))

    def test_unavailable_check_preserves_last_success_without_claiming_a_new_read(self):
        yesterday = {"version": "15.9.0", "minimum_ios": "15.0"}
        android = {"version": "16.0.0", "download_maintenance": True}
        before = merge({}, {"apple": yesterday}, "2026-11-27")
        after = merge(before, {"xiaomi": android}, "2026-11-28")
        self.assertEqual(after["apple"], {"check": "unavailable", "observed_on": "2026-11-27", "listing": yesterday})
        self.assertEqual(merge(after, {"xiaomi": android}, "2026-11-28"), after)
        page = render(after)
        self.assertIn("15.9.0 · 最低 iOS 15.0 | 2026-11-27 | 暂未读到", page)
        self.assertIn("16.0.0 · 网页显示维护中 | 2026-11-28 | 已读到", page)
        self.assertNotIn("可安装", page)


if __name__ == "__main__":
    unittest.main()
