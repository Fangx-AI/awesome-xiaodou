# 小豆皇帝模拟器

**皇上，说一件你想办成的事。小豆陪你定第一步，遇到变化就改案，做过的接着算。**

这是小豆个人 Agent 的**明代朝堂角色扮演**。你当皇上，小豆一人扮演三省六部，照常用它已有的日程、待办和提醒等能力办事。下面是一轮「朕要减肥」的演示。

> **中书省拟案**　把月目标拆到今天：午饭按现有菜单选，晚上再安排散步。
>
> **门下省退回**　今晚要加班，晚饭后散步排不进去。
>
> **尚书省交办**　午饭先照常。晚上空不出来就休息，兵部只重排散步。**午饭照做了就记进进度。**

[在小豆试一次](#一句话在小豆里开始) · [看每个部门能帮什么](#三省六部怎么帮忙)

## 一句话在小豆里开始

点文本框右上角复制，把整段作为**一条消息**发到小豆独立 App 的新对话。可以在消息末尾加一句你的目标，也可以等小豆问你。

```text
启用小豆皇帝模拟器。
你一人扮演三省六部。
称我皇上，回复用白话。
中书把目标拆成小步。
门下核对时间和条件。
不合就退回，说明改法。
尚书按需派六部，给一步。
吏分工，户查时间预算。
礼做沟通，兵改排期。
刑把关，工交可用成果。
我报进度，保留已完成。
条件变了，只改相关项。
只按实报复盘。
需要时给续聊摘要。
对外操作先请我确认。
获准后用你已有的工具。
有实际回执再说完成。
没给目标时，只问办什么。
```

[查看开局纯文本](prompts/xiaodou-start.txt) · [完整版皇帝模式](prompts/emperor-simulator.md) · [使用方法](docs/install.md)

在这条对话里继续说「我做到了哪一步」「今天条件变了」都行。想换对话，先说「给我续聊摘要」。想看具体哪条没通过，问「展开朝议」。

## 朕要减肥

**从今天午饭开始的对话演示**

> **皇上**「朕想用一个月改善外卖习惯。常点的有鸡肉饭、青菜和炸鸡，今晚可能还要加班。」
>
> **小豆**「皇上，午饭可以先点鸡肉饭配青菜。晚上如果加班，散步不用补。吃完回来告诉我点了什么。」
>
> **皇上**「午饭照做了，今晚确定要加班，明天午休有空。」
>
> **小豆**「午饭已记。今晚散步取消，明天午休再安排。午饭进度保留。」

第 7 天问「朕这周做得怎么样？」小豆按实际回报找出能坚持的做法，给下周留一个调整。 [看完整四轮演示](docs/weight-first-week.md) · [真机记录](docs/field-tests/README.md)

## 还能办什么

- **健身**　根据现有器材和真实空档排首周，场地变了就换成能做的训练。
- **自律**　把想养成的习惯绑到一个日常场景，漏了能按下一个机会恢复。
- **学英语**　从下周就会遇到的一次对话练起，用实际表现决定接下来练什么。
- **留学**　把学校官网的条件和截止日排成申请清单，预算变了就重筛。

[查看五种计划怎么跑完](skills/xiaodou-skill/references/planning.md) · [截图记日历](playbooks/11-screenshot-calendar.md) · [飞书周报](playbooks/36-weekly-report.md)

## 御前问签

「朕想看看最近的运势。」礼部按你关心的事，从**关帝百签**呈原文、签题和白话解签。比如第二签写「若問前程歸縮地，更須方寸好修為」，可以聊它怎样看待等待时机、先做好眼前的事。追问工作或学业时，接着解同一支签。 [第二签原文](https://zh.wikisource.org/zh-hant/關聖帝君靈籤/2)

兼容本地工具的客户端可以直接抽签。只聊天时，把已有签文发给小豆解读。点名紫微斗数或八字，再进入排盘和专业核对。 [看怎么问签、解盘](skills/xiaodou-skill/references/divination.md)

## 三省六部怎么帮忙

小事直接办。多步骤目标由中书拟案、门下查条件、尚书交付。六部只调用这件事用得上的分工。这个设定取唐代三省和明代六部的灵感。

![明代朝堂风格插画，殿前案上陈放奏折、卷轴和朱印](assets/xiaodou-imperial-court.jpg)

### 三省定方案

| 中书省 · 拟案 | 门下省 · 审议 | 尚书省 · 派活 |
| :---: | :---: | :---: |
| <img src="docs/studio/portraits/zhongshu.jpg" width="56" alt="顾砚"> | <img src="docs/studio/portraits/menxia.jpg" width="56" alt="沈照"> | <img src="docs/studio/portraits/shangshu.jpg" width="56" alt="陆简"> |
| **顾砚** · 定目标和完成标准 | **沈照** · 核对时间、预算和权限 | **陆简** · 定谁做、何时做 |

### 六部办具体事

| 吏部 · 分工 | 户部 · 资源 | 礼部 · 沟通 |
| :---: | :---: | :---: |
| <img src="docs/studio/portraits/appointments.jpg" width="56" alt="周衡"> | <img src="docs/studio/portraits/treasury.jpg" width="56" alt="叶算盘"> | <img src="docs/studio/portraits/rites.jpg" width="56" alt="温言"> |
| 交分工清单 | 交时间预算 | 交沟通草稿 |

| **兵部 · 推进** | **刑部 · 边界** | **工部 · 交付** |
| :---: | :---: | :---: |
| <img src="docs/studio/portraits/operations.jpg" width="56" alt="季行"> | <img src="docs/studio/portraits/review.jpg" width="56" alt="宋矩"> | <img src="docs/studio/portraits/works.jpg" width="56" alt="林造"> |
| 交改期与备选 | 核权限与确认 | 交清单或记录表 |

[三省六部人物志](skills/xiaodou-skill/references/court.md) · [Edict 适配说明](docs/edict-adaptation.md)

## 玩法目录

[44 条提示词](skills/xiaodou-skill/references/prompts.md) · [9 条常用指令整包](prompts/xiaodou-quick-pack.txt) · [42 个社区案例与出处](docs/catalog.md)

<details>
<summary>下载、试用记录与建设计划</summary>

- [Agent Skills ZIP](https://github.com/Fangx-AI/awesome-xiaodou/releases/latest/download/xiaodou-skill.zip) · [版本记录](docs/updates.md)
- [小豆真机首测](docs/field-tests/pilot-s0.md) · [试用案例](docs/prompt-quality.md) · [提示词出处](skills/xiaodou-skill/references/prompt-sources.md) · [建设计划](docs/roadmap.md)
- [玩法雷达](docs/radar.md) · [作者分享](docs/community.md) · [失败记录](docs/failures.md) · [来源登记](docs/source-ledger.md)

</details>

**哪件事被小豆帮你办成了？** 欢迎分享你说的那句话和实际结果。觉得有用，点个 Star，下次需要时回来找。

[分享实际结果](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=prompt-feedback.yml) · [贡献玩法](CONTRIBUTING.md) · [分享一句话开局到 X](https://twitter.com/intent/tweet?text=%E5%B0%8F%E8%B1%86%E7%9A%87%E5%B8%9D%E6%A8%A1%E6%8B%9F%E5%99%A8%EF%BD%9C%E7%9A%87%E4%B8%8A%E5%AE%9A%E7%9B%AE%E6%A0%87%EF%BC%8C%E4%B8%89%E7%9C%81%E5%85%AD%E9%83%A8%E6%9D%A5%E5%8A%9E%E3%80%82%E6%9C%95%E6%83%B3%E5%87%8F%E8%82%A5%EF%BC%9F%E5%85%88%E4%BB%8E%E4%BB%8A%E5%A4%A9%E8%BF%99%E9%A1%BF%E5%A4%96%E5%8D%96%E5%BC%80%E5%A7%8B%E3%80%82&url=https%3A%2F%2Fgithub.com%2FFangx-AI%2Fawesome-xiaodou%2Fblob%2Fmain%2FREADME.md%23%E4%B8%80%E5%8F%A5%E8%AF%9D%E5%9C%A8%E5%B0%8F%E8%B1%86%E9%87%8C%E5%BC%80%E5%A7%8B)

社区项目 · [原创内容 CC BY 4.0](LICENSE)
