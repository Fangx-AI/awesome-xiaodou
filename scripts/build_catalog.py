"""Validate the source catalog and regenerate Markdown/CSV views (Python 3)."""
import csv
import json
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

def self_tested_ids(runs, known_ids):
    tested = set()
    for run in runs:
        assert run['case_id'] in known_ids, 'unknown case ID in self-test record'
        date.fromisoformat(run['date'])
        assert run['client'] == '小豆 App' and run['version'].strip(), 'record the real App version'
        assert run['outcome'] in {'通过', '部分通过', '未通过', '权限受限'}, 'record an observed outcome'
        evidence = (ROOT / run['evidence_path']).resolve()
        register = ROOT / 'docs' / 'field-tests'
        assert evidence.is_relative_to(register) and evidence != register / 'README.md' and evidence.is_file(), 'add redacted evidence'
        tested.add(run['case_id'])
    return tested

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
        w = csv.writer(f)
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
             '[复跑方法](../prompt-quality.md) · [提交结果](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=prompt-feedback.yml)', '']
    if runs:
        lines += ['| 日期 | 场景 | App 版本 | 结果 | 脱敏证据 |', '| --- | --- | --- | --- | --- |']
        for run in runs:
            evidence = Path(run['evidence_path']).relative_to('docs/field-tests').as_posix()
            lines.append(f"| {run['date']} | {run['case_id']} | {run['version']} | {run['outcome']} | [查看记录]({evidence}) |")
    else:
        lines.append('当前等待第一条小豆 App 实测。验收页的演示和预期结果单独存放。')
    (ROOT / 'docs/field-tests').mkdir(exist_ok=True)
    (ROOT / 'docs/field-tests/README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(json.dumps({'playbooks':len(cases), 'source_records':len(sources), 'external_tests':len(external), 'categories':dict(counts)}, ensure_ascii=True))

if __name__ == '__main__':
    build()
