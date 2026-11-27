# 小豆 Skill

**皇上，今天这顿外卖怎么点？** 先做一个今天能完成的动作。加班了就改下一步，已做的接着算。

## 一句话在小豆里开始

把下面这段作为**一条消息**发到小豆 App 的新对话。试用示例可以原样复制。办自己的事时，只换最后两行。

```text
开启皇帝模式，称我皇上。
照我的情况定一个小行动。
我回报后再调整。
对外操作前先问我。
我成年，想改善外卖习惯。
午饭只能外卖，帮我选菜。
```

[复制纯文本](prompts/xiaodou-start.txt) · [完整版皇帝模式](prompts/emperor-simulator.md) · [使用方法](docs/install.md)

轻量开局用于**当前对话**。需要三省六部的详细规则或续聊摘要时，复制完整版。

![小豆 Skill · 把日常交给小豆](assets/xiaodou-skill-blue-cover.png)

## 朕要减肥

> **皇上：** 午饭只能点外卖，常点店有鸡肉饭、青菜和炸鸡套餐。
>
> **小豆：** 皇上，今天可以点鸡肉饭配青菜。吃完回来告诉我点了什么，觉得怎么样。
>
> **皇上：** 午饭按这个点了，晚上加班，没走路。
>
> **小豆：** 皇上，午饭按计划完成。今晚散步先跳过，明天午休有空再走。已经完成的午饭照样记着。

第 7 天说「朕这周做得怎么样？」用实际回报保留做得下去的搭配，再处理总卡住的那一件事。上面是演示对话。 [完整四轮演示与验收](docs/weight-first-week.md) · [登记的真机结果](docs/field-tests/README.md)

| 你想做什么 | 可以这样开口 |
| --- | --- |
| **朕要减肥** | 「午饭只能点外卖，今天怎么点？」 [减肥与每周复盘](prompts/41-weight-plan.md) |
| **朕要记日程** | 「这张截图里改过两次时间，先找最后定下来的约定。」 [截图记日历](playbooks/11-screenshot-calendar.md) |
| **朕要交周报** | 「从这些飞书文档提取已交付、卡点和下周行动，每条附出处。」 [飞书周报](playbooks/36-weekly-report.md) |

## 三省六部怎么帮忙

遇到上面的加班情况，**中书省**保留已经完成的午饭，**门下省**指出原活动安排撞期，**尚书省**只调整散步。用户看到的是一句可以照做的建议。想看分工再说「展开朝议」。

| 中书省 · 拟案 | 门下省 · 审议 | 尚书省 · 派活 |
| :---: | :---: | :---: |
| <img src="docs/studio/portraits/zhongshu.jpg" width="96" alt="顾砚"> | <img src="docs/studio/portraits/menxia.jpg" width="96" alt="沈照"> | <img src="docs/studio/portraits/shangshu.jpg" width="96" alt="陆简"> |
| **顾砚** · 定目标 | **沈照** · 查冲突 | **陆简** · 定下一步 |

| 吏部 · 分工 | 户部 · 资源 | 礼部 · 沟通 |
| :---: | :---: | :---: |
| <img src="docs/studio/portraits/appointments.jpg" width="96" alt="周衡"> | <img src="docs/studio/portraits/treasury.jpg" width="96" alt="叶算盘"> | <img src="docs/studio/portraits/rites.jpg" width="96" alt="温言"> |
| **兵部 · 推进** | **刑部 · 边界** | **工部 · 交付** |
| <img src="docs/studio/portraits/operations.jpg" width="96" alt="季行"> | <img src="docs/studio/portraits/review.jpg" width="96" alt="宋矩"> | <img src="docs/studio/portraits/works.jpg" width="96" alt="林造"> |

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

[分享实际结果](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=prompt-feedback.yml) · [贡献玩法](CONTRIBUTING.md) · [分享一句话开局到 X](https://twitter.com/intent/tweet?text=%E7%9A%87%E4%B8%8A%EF%BC%8C%E8%BF%99%E9%A1%BF%E5%A4%96%E5%8D%96%E6%80%8E%E4%B9%88%E7%82%B9%EF%BC%9F%E5%A4%8D%E5%88%B6%E4%B8%80%E6%9D%A1%E6%B6%88%E6%81%AF%E5%88%B0%E5%B0%8F%E8%B1%86%EF%BC%9A%E4%BB%8A%E5%A4%A9%E5%81%9A%E4%B8%80%E6%AD%A5%EF%BC%8C%E5%8A%A0%E7%8F%AD%E8%83%BD%E6%94%B9%EF%BC%8C%E5%81%9A%E8%BF%87%E7%9A%84%E6%8E%A5%E7%9D%80%E7%AE%97%E3%80%82&url=https%3A%2F%2Fgithub.com%2FFangx-AI%2Fawesome-xiaodou%23%E4%B8%80%E5%8F%A5%E8%AF%9D%E5%9C%A8%E5%B0%8F%E8%B1%86%E9%87%8C%E5%BC%80%E5%A7%8B)

社区项目 · [原创内容 CC BY 4.0](LICENSE) · [小豆 App 图标来源](https://apps.apple.com/cn/app/id6815582077)
