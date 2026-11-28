# 贡献指南

谢谢你分享小豆的真实使用经验！失败、限制和失效记录同样有用。

## 提交方式

1. 搜索现有玩法和 Issue，避免重复。
2. 通过“分享一个玩法”表单提交，或复制 `templates/playbook.md` 到 `playbooks/`。
3. 同步更新 `data/playbooks.json` 和 README 的玩法数量。新增来源登记到 `data/sources.json`。优先提供原帖，只有聚合或镜像时说明访问方式及缺失证据。
4. 运行 `python scripts/build_catalog.py`，提交生成的目录、来源表和 CSV。外部待测用例保留在独立表中，不与玩法数相加。
5. 更新提示词后，运行 `python scripts/build_skill.py <输出目录>`，提交更新后的提示词库和整包文本。每个玩法的可复制指令使用一个 `text` 代码块。
6. 发布前运行 `python scripts/check_release.py <输出目录>/xiaodou-skill.zip`。CI 会重新构建并检查生成内容是否与仓库同步。

## 收录要求

- 明确是“小豆”中的体验，不把豆包主应用能力直接推定为小豆能力。
- 标明依据类型和验证状态；转载的体验标记“第三方实测报道”或“作者体验分享”；只有亲自操作并提供环境与结果证据，才能提交为“本项目真机实测”。
- 记录测试日期、系统、应用版本、所需连接和套餐条件；未知项写“未知”。
- 提供可以复制的完整指令和实际结果；如果失败，请写明失败在哪一步。
- 截图或录屏隐去私人号码、地址、账号信息和他人消息。
- 原创说明优先，引用外部案例保留作者和来源，不整篇搬运。
- 仅有想法的条目先进入 Issue，标记“创意待验证”。

维护者会核对资料及证据后更新状态。旧玩法失效时保留记录，注明失效日期及版本。

## 登记小豆 App 真机结果

只想回报一次结果，可以用[公开反馈表](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=prompt-feedback.yml)。请写明复现需要的开局和实际回复。若涉及外部操作，分别记录是否看到本次操作的回执，以及后来有没有收到提醒、日历有没有出现对应事件、或收件箱有没有收到邮件。只观察到创建回执时，把实际触发或送达标为未核对。

在 `docs/field-tests/` 中添加脱敏 Markdown，写下实际输入、输出、回执或观察结果。然后在 `data/self-tests.json` 添加 `case_id`、`date`（YYYY-MM-DD）、`client`（小豆 App）、`version`、`outcome`（通过、部分通过、未通过、权限受限之一）和 `evidence_path`（相对仓库路径）。目录内的玩法同步将 `self_tested` 设为 true，再运行目录生成器。G01 和 H01 直接登记，不用改目录数据。

跑完「今晚只剩五分钟」后，用 `case_id: S0` 登记，沿用日期、客户端、App 版本和脱敏证据路径。再填写 `platform`、`os_version`、候选工件的完整 `candidate_commit` 和下表的 `checks`，逐项填「通过」「未通过」「权限受限」或「未测」。过期确认一项可选。S0 以逐项结果展示，省略汇总 `outcome`。每次演练单独留一份证据，实际触发需与已确认创建的同一条提醒对应。

| 字段 | 核对的结果 |
| --- | --- |
| `opening` | 一条开局消息收到可做的首步 |
| `replan` | 说明原计划为何退回，保留第一句并按五分钟重排 |
| `progress` | 保留已完成和卡点，给出下次从哪里继续 |
| `withdrawal` | 预览后撤回，任务列表没有新建该条提醒 |
| `expired_preview` | 预览过期后再确认，任务列表没有新建该条提醒（可选） |
| `reminder_preview` | 先预览内容和时间，再等用户确认 |
| `reminder_created` | 确认后可在任务列表核对创建结果 |
| `reminder_triggered` | 到点实际收到该条提醒 |

[真机演练](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/field-tests/pilot-s0.md) · [提交脱敏结果](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=s0-pilot.yml)
