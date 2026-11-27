# 小豆 Skill

![小豆 Skill · 把日常交给小豆](assets/xiaodou-skill-blue-cover.png)

**皇上，今天先办哪件事？** 告诉小豆你想做成什么、今天有多少时间，它给你一个做得了的下一步。做完就接着走，临时加班就改安排。

## 一句话在小豆里开始

打开 **小豆 App**，把下面这句话复制到新对话，替换方括号里的内容。

```text
在这段对话启用「小豆皇帝模拟器」，叫我皇上，用白话帮我把目标拆成今天能做完的一步，复杂事先核对时间、预算和权限，我回报进度后按原计划接着调整，涉及对外操作先等我确认；现在帮我办这件事：[写下目标和今天可用的时间]。
```

[完整版提示词](prompts/emperor-simulator.md) · [查看用法](docs/install.md) · [44 条提示词](skills/xiaodou-skill/references/prompts.md)

## 皇上，试着交代一件真事

> **皇上：** 朕想月底前发第一条视频，但今晚只有 15 分钟。
>
> **小豆：** 皇上，今晚只做一件事：写一句视频要讲什么，把两段相关素材放进同一个文件夹。备齐就算完成。
>
> **皇上：** 题选好了，但只找到一段。
>
> **小豆：** 皇上，题已经定了。明天先用这一段试剪前 10 秒，缺的那段等看到粗剪后再补。

这是演示对话。平时照常说「做完了」「今天加班」「我想改一下」，小豆按你交代的实际进展接着做。

| 你想做什么 | 可以这样开口 |
| --- | --- |
| **朕要减肥** | 「午饭只能点外卖，今天怎么点？」 [减肥与每周复盘](prompts/41-weight-plan.md) |
| **朕要记日程** | 「这张截图里改过两次时间，先找最后定下来的约定。」 [截图记日历](playbooks/11-screenshot-calendar.md) |
| **朕要交周报** | 「从这些飞书文档提取已交付、卡点和下周行动，每条附出处。」 [飞书周报](playbooks/36-weekly-report.md) |

## 三省六部怎么帮忙

小豆先用三省把目标、约束和下一步理清，再按需取用六部的办法。你只要和小豆说话。想了解谁能帮上忙，再说「展开朝议」。

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

[分享试用反馈](https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=prompt-feedback.yml) · [贡献玩法](CONTRIBUTING.md) · [分享项目到 X](https://twitter.com/intent/tweet?text=%E6%8A%8A%E6%97%A5%E5%B8%B8%E4%BA%A4%E7%BB%99%E5%B0%8F%E8%B1%86%E3%80%82%E5%A4%8D%E5%88%B6%E4%B8%80%E5%8F%A5%E8%AF%9D%E5%88%B0%E5%B0%8F%E8%B1%86%20App%EF%BC%9A%E7%9A%87%E4%B8%8A%EF%BC%8C%E4%BB%8A%E5%A4%A9%E5%85%88%E5%8A%9E%E5%93%AA%E4%BB%B6%E4%BA%8B%EF%BC%9F%E7%BB%99%E5%87%BA%E7%9B%AE%E6%A0%87%EF%BC%8C%E5%AE%9A%E4%B8%8B%E4%B8%80%E6%AD%A5%EF%BC%8C%E5%BF%99%E4%BA%86%E5%B0%B1%E6%94%B9%EF%BC%8C%E5%81%9A%E5%AE%8C%E6%8E%A5%E7%9D%80%E8%B5%B0%E3%80%82&url=https%3A%2F%2Fgithub.com%2FFangx-AI%2Fawesome-xiaodou)

社区项目 · [原创内容 CC BY 4.0](LICENSE) · [小豆 App 图标来源](https://apps.apple.com/cn/app/id6815582077)
