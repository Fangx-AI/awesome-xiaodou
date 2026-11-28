# 小豆皇帝模拟器

**皇上，您定目标，三省六部帮您办。**

一个在小豆独立 App 里使用的个人助理 Skill。以明代朝堂为设定，借唐代三省走流程、明代六部分事务。小事直接办，做月计划先问清您的情况。临时加班或预算变了，改受影响的安排，已完成的照样算。

**中书省拟案 → 门下省审议 → 尚书省交办 → 六部按需出手。**

**在小豆里试用**　[跟着「今晚只剩五分钟」试一次](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/field-tests/pilot-s0.md) · [带自己的目标试七天](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/field-tests/seven-day.md)

[复制一句话开局](#一句话在小豆里开始) · [看朕怎么减肥](#朕要减肥) · [看三省六部怎么帮忙](#三省六部怎么帮忙)

[S0 试用版说明](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/README.md) · [没有小豆 App？参加页面冷读](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/field-tests/cold-read.md)

![明代朝堂风格插画，殿前案上陈放奏折、卷轴和朱印](assets/xiaodou-imperial-court.jpg)

## 一句话在小豆里开始

把下面这段作为**一条消息**发到小豆 App 的新对话。示例只解决今天这一餐。要做自己的事，换掉最后两行；要排一个月，可以按[下面的月计划例子](#朕要减肥)开口。

```text
开启皇帝模式，称我皇上。
照我的情况定一个小行动。
我回报后再调整。
对外操作前先问我。
我成年，想改善外卖习惯。
午饭只能外卖，帮我选菜。
```

[复制纯文本](prompts/xiaodou-start.txt) · [完整版皇帝模式](prompts/emperor-simulator.md) · [使用方法](docs/install.md)

这条消息用于当前对话。要按三省六部走一轮完整朝议，用上面的完整版。

## 朕要减肥

**S0 试用版的月计划开局演示**

> **皇上**「朕想用一个月养成更好的饮食习惯。中午只能点外卖，晚上想散步，但可能要加班。」
>
> **小豆**「皇上，午饭只能外卖、晚上可能加班，我记下了。排四周之前，我想先了解几件事：」
>
> - 一个月后，你最想看到什么变化？
> - 平时三餐和饮料怎么吃？午饭常点哪些外卖？
> - 现在一般怎么活动？一周哪些时间有空，通常哪几天加班？
> - 是否成年？有没有影响饮食或活动的限制？身高、体重可以不填。

补齐信息后，中书拟四周计划，门下核对能不能排进生活，尚书交付具体的首周安排，并留一个加班版本。

第 7 天问「朕这周做得怎么样？」小豆按实际回报找出能坚持的做法，给下周留一个调整。 [看从立案到改期的演示](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/weight-first-week.md) · [真机记录](docs/field-tests/README.md)

| 你想做什么 | 可以这样开口 |
| --- | --- |
| **朕要改善饮食** | 「朕想改善一个月的饮食习惯。午饭只能点外卖，先问清楚再帮我排。」 [看四周计划怎么推进](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/weight-first-week.md) |
| **朕要记日程** | 「这张截图里改过两次时间，先找最后定下来的约定。」 [截图记日历](playbooks/11-screenshot-calendar.md) |
| **朕要交周报** | 「从这些飞书文档提取已交付、卡点和下周行动，每条附出处。」 [飞书周报](playbooks/36-weekly-report.md) |

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
| 加班后重排任务 | 执行前核对权限 | 交可复制的清单 |

[三省六部人物志](skills/xiaodou-skill/references/court.md) · [Edict 适配说明](docs/edict-adaptation.md)

## 玩法目录

[44 条提示词](skills/xiaodou-skill/references/prompts.md) · [9 条常用指令整包](prompts/xiaodou-quick-pack.txt) · [42 个社区案例与出处](docs/catalog.md)

<details>
<summary>下载、试用记录与建设计划</summary>

- [Agent Skills ZIP](https://github.com/Fangx-AI/awesome-xiaodou/releases/latest/download/xiaodou-skill.zip) · [版本记录](docs/updates.md)
- [试用案例](docs/prompt-quality.md) · [提示词出处](skills/xiaodou-skill/references/prompt-sources.md) · [建设计划](docs/roadmap.md)
- [玩法雷达](docs/radar.md) · [作者分享](docs/community.md) · [失败记录](docs/failures.md) · [来源登记](docs/source-ledger.md)

</details>

**哪件事被小豆帮你办成了？** 欢迎分享你说的那句话和实际结果。觉得有用，点个 Star，下次需要时回来找。

[分享实际结果](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=prompt-feedback.yml) · [贡献玩法](CONTRIBUTING.md) · [分享一句话开局到 X](https://twitter.com/intent/tweet?text=%E5%B0%8F%E8%B1%86%E7%9A%87%E5%B8%9D%E6%A8%A1%E6%8B%9F%E5%99%A8%EF%BD%9C%E7%9A%87%E4%B8%8A%E5%AE%9A%E7%9B%AE%E6%A0%87%EF%BC%8C%E4%B8%89%E7%9C%81%E5%85%AD%E9%83%A8%E6%9D%A5%E5%8A%9E%E3%80%82%E6%9C%95%E6%83%B3%E5%87%8F%E8%82%A5%EF%BC%9F%E5%85%88%E4%BB%8E%E4%BB%8A%E5%A4%A9%E8%BF%99%E9%A1%BF%E5%A4%96%E5%8D%96%E5%BC%80%E5%A7%8B%E3%80%82&url=https%3A%2F%2Fgithub.com%2FFangx-AI%2Fawesome-xiaodou%2Fblob%2Fmain%2FREADME.md%23%E4%B8%80%E5%8F%A5%E8%AF%9D%E5%9C%A8%E5%B0%8F%E8%B1%86%E9%87%8C%E5%BC%80%E5%A7%8B)

社区项目 · [原创内容 CC BY 4.0](LICENSE)
