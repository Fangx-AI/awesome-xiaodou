# 别人的项目如何整理，我们如何统计

调研日期：2026-11-24。以下是实际读取结果，不按搜索标题推测仓库内容。

| 项目 | 实际读到什么 | 如何统计 | 本库采用的方法 |
| --- | --- | --- | --- |
| [wowowuyun-boop/awesome-xiaodou](https://github.com/wowowuyun-boop/awesome-xiaodou) | README、贡献说明、案例目录、详细用例、记录模板、蓝皮书、橙皮书、白皮书、资源目录，共9份Markdown；另读LICENSE | 100个待实测用例，分10类；7个详细方案；仓库声明真机实测0条 | 稳定编号、分类、验收方法；保留[100项索引](external-tests.md)，与实际玩法分表 |
| [good1uck/xiaodou-codes](https://github.com/good1uck/xiaodou-codes) | README说明用codes.json更新数据，以code去重，记录状态和增量查询游标 | 邀请码条目，不能当作玩法数量 | 数据与页面分离；同一记录更新状态，避免重复累计 |
| [vingo/xiaodou-inviteCode](https://github.com/vingo/xiaodou-inviteCode) | README提供3种邀请码寻找渠道，其中链接到上一项目 | 渠道导航，未提供玩法案例统计 | 保留来源关系，不把互相引用当独立案例 |
| [Zou-git0324/xiaodou-codes](https://github.com/Zou-git0324/xiaodou-codes) | GitHub搜索命中；README.md请求404 | 无法确认内容结构 | 只记检索线索，不按名称认定为上述仓库的副本 |

## 100个测试点为什么不等于100个玩法

对方把“一次提醒、取消提醒、重设时间、重启后提醒、离线提醒、时区切换”等分别列为测试用例。这种细粒度适合验收可靠性；若要回答“可以拿小豆做什么”，这些可能只是同一提醒玩法的多种测试条件。

本库的单位是一个具有不同目标、输入或输出的场景。例如“从评论找选题”和“为评论拟回复”分别产生内容选题与回复草稿，分为两项；同一电话订位的多篇转载不增加玩法数。

## 本库统计口径

| 指标 | 定义 | 不能解释为 |
| --- | --- | --- |
| 玩法条目 | data/playbooks.json中唯一id；每条链接一个玩法文件 | 成功执行次数 |
| 来源记录 | data/sources.json中唯一id，含原作者、转载入口、项目参考和待追溯线索 | 独立实测作者数或实验数 |
| 外部待测用例 | 独立数据表中的原始XD编号 | 本库新增成功玩法 |
| 本项目真机实测 | 本项目实际运行、有环境和结果记录 | 读取文章或看见任务卡 |
| 搜索请求 | 本轮保留的36条查询 | 36个平台或36条有效资料 |

一个来源支持多项玩法不代表多次独立实测；同一作者跨平台发布归入同一来源关系。例如歸藏微博与X主帖内容重复，补充帖S18只记录新增上下文，不计第二次验证。手机话费充值的作者自述缺少回执，明确保留该限制。

## 可复核的数据

- [玩法 JSON](../data/playbooks.json) / [CSV](../data/playbooks.csv)
- [来源 JSON](../data/sources.json) / [阅读版](source-ledger.md)
- [外部测试 JSON](../data/external-tests.json) / [阅读版](external-tests.md)
- [搜索查询 JSON](../data/search-queries.json) / [阅读版](search-queries.md)

运行 `python scripts/build_catalog.py` 会校验编号、来源引用、玩法文件覆盖，并重新生成目录、CSV和外部测试索引。更新玩法时同时修改JSON和对应正文。
