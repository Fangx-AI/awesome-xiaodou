"""Validate the source catalog and regenerate Markdown/CSV views (Python 3)."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))

def build():
    cases = read('playbooks.json')
    sources = read('sources.json')
    external = read('external-tests.json')['tests']
    source_ids = {s['id'] for s in sources}
    assert len(source_ids) == len(sources), 'duplicate source ID'
    assert len({c['id'] for c in cases}) == len(cases), 'duplicate case ID'
    assert len({c['path'] for c in cases}) == len(cases), 'duplicate case file'
    assert len({t['id'] for t in external}) == len(external), 'duplicate external ID'
    for c in cases:
        assert c['sources'] and set(c['sources']) <= source_ids, c['id']
        assert (ROOT / c['path']).is_file(), c['path']
        assert c['self_tested'] is False, 'add actual test evidence before changing this rule'
    assert {c['path'] for c in cases} == {str(p.relative_to(ROOT)).replace('\\', '/') for p in (ROOT / 'playbooks').glob('*.md')}
    counts = Counter(c['category'] for c in cases)
    lines = ['# 小豆玩法目录', '', f'**{len(cases)} 个小豆玩法**', '',
             '[回到首页](../README.md) · [最新线索](radar.md) · [下载 CSV](../data/playbooks.csv) · [来源登记](source-ledger.md)', '']
    for category in counts:
        lines += [f'## {category}', '', '| 编号 | 玩法 | 证据状态 | 来源 |', '| --- | --- | --- | --- |']
        for c in cases:
            if c['category'] == category:
                lines.append(f"| {c['id']} | [{c['title']}](../{c['path']}) | {c['evidence']} | {', '.join(c['sources'])} |")
        lines.append('')
    (ROOT / 'docs/catalog.md').write_text('\n'.join(lines), encoding='utf-8')
    with (ROOT / 'data/playbooks.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['id', 'title', 'category', 'evidence', 'sources', 'self_tested', 'path'])
        for c in cases:
            w.writerow([c['id'], c['title'], c['category'], c['evidence'], ';'.join(c['sources']), c['self_tested'], c['path']])
    lines = ['# 来源登记表', '', '更新：2026-11-24。访问方式单独记录；聚合、镜像、转载不升级为原帖实测。', '', '| ID | 作者或项目 | 访问方式 | 支持范围与限制 |', '| --- | --- | --- | --- |']
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
    print(json.dumps({'playbooks':len(cases), 'source_records':len(sources), 'external_tests':len(external), 'categories':dict(counts)}, ensure_ascii=True))

if __name__ == '__main__':
    build()
