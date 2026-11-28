import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import build_catalog


class FieldTestCatalogTest(unittest.TestCase):
    def setUp(self):
        self.record = {
            'case_id': 'S0',
            'date': '2000-01-01',
            'client': '小豆 App',
            'version': 'test-app',
            'platform': 'iOS',
            'os_version': 'test-os',
            'candidate_commit': 'a' * 40,
            'checks': dict.fromkeys(build_catalog.S0_REQUIRED_CHECKS, '未测'),
        }
        self.record['checks']['opening'] = '通过'

    def test_trigger_requires_confirmed_creation(self):
        self.record['checks']['reminder_triggered'] = '通过'
        with self.assertRaisesRegex(AssertionError, 'confirmed task'):
            build_catalog.check_s0(self.record)
        self.record['checks']['reminder_created'] = '通过'
        build_catalog.check_s0(self.record)

    def test_unknown_check_is_rejected(self):
        self.record['checks']['unexpected'] = '通过'
        with self.assertRaisesRegex(AssertionError, 'known keys'):
            build_catalog.check_s0(self.record)

    def test_public_page_accepts_legacy_and_expiry_reports(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ('data', 'playbooks'):
                shutil.copytree(build_catalog.ROOT / name, root / name)
            register = root / 'docs/field-tests'
            register.mkdir(parents=True)
            runs = []
            for name, checks in (
                ('legacy', self.record['checks']),
                ('expiry', {**self.record['checks'], 'expired_preview': '通过'}),
            ):
                evidence = register / f'{name}.md'
                evidence.write_text('Synthetic regression fixture', encoding='utf-8')
                runs.append({**self.record, 'checks': checks,
                             'evidence_path': evidence.relative_to(root).as_posix()})
            (root / 'data/self-tests.json').write_text(
                json.dumps({'runs': runs}), encoding='utf-8')
            with patch.object(build_catalog, 'ROOT', root), patch('builtins.print'):
                build_catalog.build()
            page = (register / 'README.md').read_text(encoding='utf-8')
            self.assertIn('已登记 **2 次**', page)
            self.assertIn('过期确认未创建未测', page)
            self.assertIn('过期确认未创建通过', page)
            self.assertIn('?template=s0-pilot.yml', page)


if __name__ == '__main__':
    unittest.main()
