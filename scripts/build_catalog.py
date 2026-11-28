"""Validate the source catalog and regenerate Markdown/CSV views (Python 3)."""
import csv
import json
import re
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S0_CHECKS = {
    'opening': '开局',
    'replan': '门下退回与改案',
    'progress': '报进度',
    'withdrawal': '撤回后未创建',
    'expired_preview': '过期确认未创建',
    'reminder_preview': '确认前预览',
    'reminder_created': '确认后创建',
    'reminder_triggered': '到点触发',
}
S0_REQUIRED_CHECKS = S0_CHECKS.keys() - {'expired_preview'}
S0_STATUSES = {'通过', '未通过', '权限受限', '未测'}

def read(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

def self_tested_ids(runs, known_ids):
    tested = set()
    pilot_evidence = set()
    for run in runs:
        case_id = run['case_id']
        assert case_id in known_ids or case_id == 'S0', 'unknown case ID in self-test record'
        date.fromisoformat(run['date'])
        assert run['client'] == '小豆 App' and run['version'].strip(), 'record the real App version'
        evidence = (ROOT / run['evidence_path']).resolve()
        register = ROOT / 'docs' / 'field-tests'
        reserved = {register / name for name in ('README.md', 'pilot-s0.md', 'pilot-observer.md', 'cold-read.md', 'seven-day.md')}
        assert evidence.is_relative_to(register) and evidence not in reserved and evidence.is_file(), 'add redacted evidence'
        if case_id == 'S0':
            assert evidence not in pilot_evidence, 'S0 runs require distinct evidence records'
            pilot_evidence.add(evidence)
            check_s0(run)
        else:
            assert run['outcome'] in {'通过', '部分通过', '未通过', '权限受限'}, 'record an observed outcome'
            tested.add(case_id)
    return tested


def check_s0(run):
    assert run.get('platform') in {'iOS', 'iPadOS', 'Android'}, 'S0 requires the device platform'
    os_version = run.get('os_version')
    assert isinstance(os_version, str) and os_version.strip(), 'S0 requires the observed OS version'
    commit = run.get('candidate_commit')
    assert isinstance(commit, str) and re.fullmatch(r'[0-9a-f]{40}', commit), 'S0 requires a pinned candidate commit'
    checks = run.get('checks')
    assert isinstance(checks, dict) and S0_REQUIRED_CHECKS <= checks.keys() <= S0_CHECKS.keys(), 'record required S0 checks and use known keys'
    assert all(isinstance(status, str) and status in S0_STATUSES for status in checks.values()), 'unknown S0 check status'
    assert any(status != '未测' for status in checks.values()), 'S0 requires at least one observed result'
    assert checks['reminder_triggered'] != '通过' or checks['reminder_created'] == '通过', 'check the trigger against a confirmed task'

def build():
    cases = read('playbooks.json')
    sources = read('sources.json')
    external = read('external-tests.json')['tests']
    source_ids = {s['id'] for s in sources}
    case_ids = {c['id'] for c in cases}
    runs = read('self-tests.json')['runs']
    tested = self_tested_ids(runs, case_ids | {'G01', 'H01'})
    assert len(source_ids) == len(sources), 'duplicate source ID'
    assert len({c['id'] for c in cases}) == len(cases), 'duplicate case ID'
    assert len({c['path'] for c in cases}) == len(cases), 'duplicate case file'
    assert len({t['id'] for t in external}) == len(external), 'duplicate external ID'
    for c in cases:
        assert c['sources'] and set(c['sources']) <= source_ids, c['id']
        assert (ROOT / c['path']).is_file(), c['path']
        assert c['self_tested'] == (c['id'] in tested), 'self_tested must match the evidence register'
    assert {c['path'] for c in cases} == {str(p.relative_to(ROOT)).replace('\\', '/') for p in (ROOT / 'playbooks').glob('*.md')}
    counts = Counter(c['category'] for c in cases)
    lines = ['# 小豆玩法目录', '', f'**{len(cases)} 个小豆玩法**', '',
             '[回到首页](../README.md) · [最新线索](radar.md) · [下载 CSV](../data/playbooks.csv) · [来源登记](source-ledger.md)', '']
    lines += [f'已登记真机试用：{len(tested & case_ids)} 个目录场景。 [查看结果](field-tests/README.md)', '']
    for category in counts:
        lines += [f'## {category}', '', '| 编号 | 玩法 | 证据状态 | 来源 |', '| --- | --- | --- | --- |']
        for c in cases:
            if c['category'] == category:
                evidence = c['evidence'] + ('，另有[真机记录](field-tests/README.md)' if c['self_tested'] else '')
                lines.append(f"| {c['id']} | [{c['title']}](../{c['path']}) | {evidence} | {', '.join(c['sources'])} |")
        lines.append('')
    (ROOT / 'docs/catalog.md').write_text('\n'.join(lines), encoding='utf-8')
    with (ROOT / 'data/playbooks.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['id', 'title', 'category', 'evidence', 'sources', 'self_tested', 'path'])
        for c in cases:
            w.writerow([c['id'], c['title'], c['category'], c['evidence'], ';'.join(c['sources']), c['self_tested'], c['path']])
    checked = max(s['checked'] for s in sources)
    lines = ['# 来源登记表', '', f'最近来源核对：{checked}。访问方式见下表。', '', '| ID | 作者或项目 | 访问方式 | 支持范围与限制 |', '| --- | --- | --- | --- |']
    for s in sources:
        mirror = f" [读取页面]({s['mirror']})" if s.get('mirror') else ''
        lines.append(f"| {s['id']} | [{s['author']}]({s['url']}) | {s['access']}{mirror} | {s['note']} |")
    (ROOT / 'docs/source-ledger.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    lines = ['# 外部项目的 100 项待实测用例索引', '', '作者：[wowowuyun-boop/awesome-xiaodou contributors](https://github.com/wowowuyun-boop/awesome-xiaodou)。', '',
             '来源：[原始案例目录](https://github.com/wowowuyun-boop/awesome-xiaodou/blob/main/cases/README.md)。许可：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)。材料按现状提供，不作保证。', '',
             '修改说明：提取原编号、分类、标题，添加统一状态和跳转链接；未复制验收正文。所有条目均为待实测假设，与本库玩法有交集，不能直接加总。详细测法请访问原库。', '']
    for category in dict.fromkeys(t['category'] for t in external):
        lines += [f'## {category}', '', '| 编号 | 测试主题 | 状态 |', '| --- | --- | --- |']
        for t in external:
            if t['category'] == category:
                lines.append(f"| [{t['id']}]({t['source']}) | {t['title']} | 待实测 |")
        lines.append('')
    (ROOT / 'docs/external-tests.md').write_text('\n'.join(lines), encoding='utf-8')
    lines = ['# 小豆 App 真机结果', '', f'已登记 **{len(runs)} 次**真机试用。', '',
             '[已核对的下载入口](../install.md#下载和开通) · '
             '[真机演练](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/field-tests/pilot-s0.md) · '
             '[提交真机结果](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=s0-pilot.yml) · '
             '[其他玩法反馈](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=prompt-feedback.yml) · '
             '[本地回放](../prompt-quality.md#本地候选回放)', '']
    pilot = [run for run in runs if run['case_id'] == 'S0']
    other = [run for run in runs if run['case_id'] != 'S0']
    if pilot:
        lines += ['## S0 真机演练', '', '| 日期 | 系统与 App 版本 | 候选 | 对话结果 | 提醒结果 | 证据 |',
                  '| --- | --- | --- | --- | --- | --- |']
        for run in pilot:
            evidence = Path(run['evidence_path']).relative_to('docs/field-tests').as_posix()
            commit = run['candidate_commit']
            candidate = f'[{commit[:7]}](https://github.com/Fangx-AI/awesome-xiaodou/tree/{commit})'
            checks = run['checks']
            conversation = '、'.join(f'{S0_CHECKS[name]}{checks[name]}' for name in ('opening', 'replan', 'progress'))
            reminder = '、'.join(f"{S0_CHECKS[name]}{checks.get(name, '未测')}" for name in
                                 ('reminder_preview', 'withdrawal', 'expired_preview', 'reminder_created', 'reminder_triggered'))
            environment = f"{run['platform']} {run['os_version']} / 小豆 {run['version']}"
            lines.append(f"| {run['date']} | {environment} | {candidate} | {conversation} | {reminder} | [查看记录]({evidence}) |")
        lines.append('')
    if other:
        if pilot:
            lines += ['## 玩法试用', '']
        lines += ['| 日期 | 场景 | App 版本 | 结果 | 脱敏证据 |', '| --- | --- | --- | --- | --- |']
        for run in other:
            evidence = Path(run['evidence_path']).relative_to('docs/field-tests').as_posix()
            lines.append(f"| {run['date']} | {run['case_id']} | {run['version']} | {run['outcome']} | [查看记录]({evidence}) |")
    if not runs:
        lines.append('当前等待第一条小豆 App 实测。安装、开通、发送开局及提醒创建与触发分别记录。')
    (ROOT / 'docs/field-tests').mkdir(exist_ok=True)
    (ROOT / 'docs/field-tests/README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'playbooks':len(cases), 'source_records':len(sources), 'external_tests':len(external), 'categories':dict(counts)}, ensure_ascii=True))

if __name__ == '__main__':
    build()
