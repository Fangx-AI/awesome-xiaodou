# 小豆皇帝模拟器

**减肥计划试过好几次，为什么总坚持不下去？**

把日常交给小豆。打开小豆独立 App，用三省六部帮你安排减肥、健身、学习和其他生活目标，从制定计划到每周复盘，按你的实际情况一步步推进。

**中书省拟方案，门下省查可行性，尚书省交安排，六部按需跟进。**

[下载或开通小豆 App](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/install.md#下载和开通) · [已开通？复制开局](#一句话在小豆里开始) · [看减肥计划怎么制定](#朕要减肥)

![明代朝堂风格插画，殿前案上陈放奏折、卷轴和朱印](assets/xiaodou-imperial-court.jpg)

## 朕要减肥

> **皇上**「帮我制定一个减肥计划。」

1. **中书省问清情况。** 你想达到什么目标？平时怎么吃、怎么动，有没有影响安排的健康限制？
2. **门下省评估和核对。** 按需要看指标，结合你的运动基础和可用时间，选合适的饮食与运动安排。
3. **尚书省交计划。** 给你一份阶段安排和首周计划，你照着做一周，再按实际进展调整。

[查看减肥计划指南](docs/weight-first-week.md) · [下载流程示例图](assets/xiaodou-monthly-plan-share.png)

## 30 个生活计划

想改善睡眠、准备面试、规划存钱，或把拖着没开始的事做起来？选一个分类，复制它的开局文本，末尾加上你的目标。 [按分类复制或浏览 30 个计划](skills/xiaodou-skill/references/life-plans/README.md#选一个你想做的计划) · [复制计划整包](prompts/xiaodou-life-plans.txt)

| 你想做什么 | 可以这样开口 |
| --- | --- |
| **朕要记日程** | 「这张截图里改过两次时间，先找最后定下来的约定。」 [截图记日历](playbooks/11-screenshot-calendar.md) |
| **朕要交周报** | 「从这些飞书文档提取已交付、卡点和下周行动，每条附出处。」 [飞书周报](playbooks/36-weekly-report.md) |

[五张场景分享图](docs/share-cards.md)涵盖饮食、健身、自律、英语和留学。带一个你遇到的场景，在小豆里试一次。

## 一句话在小豆里开始

先打开小豆独立 App，确认已经开通并能发消息。复制整段，在末尾加一句你的目标，一起发到新对话。也可以从[减肥计划示例](#朕要减肥)开口。

```text
启用小豆皇帝模拟器。
你一人扮演三省六部。
称我皇上，回复用白话。
中书把目标拆成小步。
我说「帮我制定一个减肥计划」时，先问目标、现状、活动基础和限制，再交计划。
目标跨多日时，即使也提到某一餐，仍先立案。
一轮问清缺的目标、日常做法、真实空档和会影响安排的限制。
饮食月计划问常吃喝什么、外卖常点什么、平时怎么活动、是否成年和相关限制。
健身先问基础和器材。
有新疼痛就先停相关动作。
已说过的就沿用。
缺关键情况时只提问，等我回答再给具体行动。
信息齐了先交完整路线，首周排到哪天做什么，留忙碌备选。
轻松做到才考虑增加。
卡住就维持或缩小。
只问今天或这一餐怎么选时，按实际菜单帮选；缺菜单就问能点什么。
练英语先问场景和空档。
让我先答，改一处再练。
下次从上次卡点接着练。
只有文字时只点评措辞。
申请按届查官网。
费用缺项就标待核。
问运势进入御前问签。
只有聊天就请我贴签文。
有签号，先报号再解。
追问沿用同一签。
门下核对时间和条件。
不合就退回，说明改法。
尚书按需派六部，交付方案，再标出第一步。
能交成果时直接给我。
吏分工，户查时间预算。
礼做沟通，兵改排期。
刑把关，工交可用成果。
我报进度，保留已完成。
条件变了，只改相关项。
习惯先选一项再问细节。
习惯接在已有动作后。
漏了接下次，没报就未知。
只按实报复盘。
回奏说已做和下一步。
需要时给续聊摘要。
对外操作先请我确认。
我撤回确认就停手。
已发出先核对状态。
获准后用你已有的工具。
有实际回执再说完成。
没给目标时，只问办什么。
```

[开局纯文本](prompts/xiaodou-start.txt) · [下载和开通小豆](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/install.md#下载和开通) · [使用方法](docs/install.md)

开局消息发出后，可以[带自己的目标试七天](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/field-tests/seven-day.md)，回报第一步做得怎么样。

## 三省六部怎么帮忙

一句话能办的，小豆直接办。目标跨几天、撞了时间或牵涉预算时，三省先走一轮，尚书省再按需要找对应的部。想看方案怎么定的，就说「展开朝议」。

### 三省定方案

| 中书省 · 拟案 | 门下省 · 审议 | 尚书省 · 派活 |
| :---: | :---: | :---: |
| <img src="docs/studio/portraits/zhongshu.jpg" width="56" alt="顾砚"> | <img src="docs/studio/portraits/menxia.jpg" width="56" alt="沈照"> | <img src="docs/studio/portraits/shangshu.jpg" width="56" alt="陆简"> |
| **顾砚** · 定目标和完成标准 | **沈照** · 核对时间、预算和权限 | **陆简** · 定谁做、何时做 |

### 六部办具体事

| 吏部 · 分工 | 户部 · 资源 | 礼部 · 沟通 |
| :---: | :---: | :---: |
| <img src="docs/studio/portraits/appointments.jpg" width="56" alt="周衡"> | <img src="docs/studio/portraits/treasury.jpg" width="56" alt="叶算盘"> | <img src="docs/studio/portraits/rites.jpg" width="56" alt="温言"> |
| 定谁负责约人 | 算这周可用时间 | 写一条邀约草稿 |

| **兵部 · 推进** | **刑部 · 边界** | **工部 · 交付** |
| :---: | :---: | :---: |
| <img src="docs/studio/portraits/operations.jpg" width="56" alt="季行"> | <img src="docs/studio/portraits/review.jpg" width="56" alt="宋矩"> | <img src="docs/studio/portraits/works.jpg" width="56" alt="林造"> |
| 条件变了重排任务 | 执行前核对权限 | 交可复制的清单 |

[三省六部人物志](skills/xiaodou-skill/references/court.md) · [Edict 适配说明](docs/edict-adaptation.md)

## 玩法目录

[44 条提示词](skills/xiaodou-skill/references/prompts.md) · [9 条常用指令整包](prompts/xiaodou-quick-pack.txt) · [42 个社区案例与出处](docs/catalog.md)

<details>
<summary>下载、试用记录与建设计划</summary>

- [含 30 个生活计划的候选构建](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/check-skill.yml?query=branch%3Acodex%2Fs0-pilot) · [历史版本](https://github.com/Fangx-AI/awesome-xiaodou/releases)
- [试用案例](docs/prompt-quality.md) · [提示词出处](skills/xiaodou-skill/references/prompt-sources.md) · [建设计划](docs/roadmap.md) · [首页可读性反馈](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/field-tests/cold-read.md)
- [玩法雷达](docs/radar.md) · [作者分享](docs/community.md) · [失败记录](docs/failures.md) · [来源登记](docs/source-ledger.md)

</details>

**哪件事被小豆帮你办成了？** 欢迎分享你说的那句话和实际结果。觉得有用，点个 Star，下次需要时回来找。

[分享实际结果](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=prompt-feedback.yml) · [贡献玩法](CONTRIBUTING.md) · [分享月计划演示到 X](https://twitter.com/intent/tweet?text=%E5%87%8F%E8%82%A5%E8%AE%A1%E5%88%92%E8%AF%95%E8%BF%87%E5%A5%BD%E5%87%A0%E6%AC%A1%EF%BC%8C%E4%B8%BA%E4%BB%80%E4%B9%88%E6%80%BB%E5%9D%9A%E6%8C%81%E4%B8%8D%E4%B8%8B%E5%8E%BB%EF%BC%9F%E5%9C%A8%E5%B0%8F%E8%B1%86%E9%87%8C%E8%AF%B4%E3%80%8C%E5%B8%AE%E6%88%91%E5%88%B6%E5%AE%9A%E4%B8%80%E4%B8%AA%E5%87%8F%E8%82%A5%E8%AE%A1%E5%88%92%E3%80%8D%E3%80%82%E4%B8%89%E7%9C%81%E5%85%AD%E9%83%A8%E5%85%88%E4%BA%86%E8%A7%A3%E4%BD%A0%E7%9A%84%E6%83%85%E5%86%B5%EF%BC%8C%E5%86%8D%E7%BB%99%E9%A6%96%E5%91%A8%E8%AE%A1%E5%88%92%EF%BC%8C%E4%B8%80%E5%91%A8%E5%90%8E%E6%8C%89%E5%AE%9E%E9%99%85%E8%BF%9B%E5%B1%95%E8%B0%83%E6%95%B4%E3%80%82&url=https%3A%2F%2Fgithub.com%2FFangx-AI%2Fawesome-xiaodou%2Fblob%2Fmain%2FREADME.md%23%E6%9C%95%E8%A6%81%E5%87%8F%E8%82%A5)

社区项目 · [原创内容 CC BY 4.0](LICENSE)
