# 小豆 Skill

![小豆 Skill · 把日常交给小豆](assets/xiaodou-skill-blue-cover.png)

**皇上，今天先办哪件事？** 减肥、做视频、约朋友，先定今天能做的一步。做完可以记，临时有事就重新排。

[**打开今日御案**](https://fangx-ai.github.io/awesome-xiaodou/studio/) · [**复制到小豆**](prompts/emperor-simulator.md) · [下载技能 ZIP](https://github.com/Fangx-AI/awesome-xiaodou/releases/latest/download/xiaodou-skill.zip)

## 先把一件事做起来

> **皇上：** 朕想月底前发出第一条视频，但今晚只有 15 分钟。
>
> **小豆的示例回复：** 皇上，先写一句视频要讲什么，再把两段能说明这个主题的素材放进同一文件夹。备齐就算今天完成。

在网页里选一个场景、定一步、回报完成或卡住。进度保存在当前浏览器，可一键复制给小豆续聊。网页建议按预设规则生成。 [在线体验](https://fangx-ai.github.io/awesome-xiaodou/studio/)

试试 **「朕想减肥，但午饭只能点外卖。今天先怎么吃？」** 从这一餐开始，忙时换个做法，想要完整计划再说「给朕排四周」。 [复制减肥玩法](prompts/41-weight-plan.md) · [分享项目](https://twitter.com/intent/tweet?text=%E7%9A%87%E4%B8%8A%EF%BC%8C%E4%BB%8A%E5%A4%A9%E5%85%88%E5%8A%9E%E5%93%AA%E4%BB%B6%E4%BA%8B%EF%BC%9F%E5%B0%8F%E8%B1%86%E6%8A%8A%E7%9B%AE%E6%A0%87%E6%8B%86%E6%88%90%E4%BB%8A%E5%A4%A9%E8%83%BD%E5%AE%8C%E6%88%90%E7%9A%84%E4%B8%80%E6%AD%A5%E3%80%82%E5%BF%99%E4%BA%86%E5%8F%AF%E4%BB%A5%E6%94%B9%EF%BC%8C%E5%81%9A%E5%AE%8C%E5%8F%AF%E4%BB%A5%E8%AE%B0%EF%BC%8C%E5%A4%8D%E5%88%B6%E8%BF%9B%E5%BA%A6%E6%8E%A5%E7%9D%80%E8%81%8A%E3%80%82&url=https%3A%2F%2Fgithub.com%2FFangx-AI%2Fawesome-xiaodou)

**其他实用场景**：[发测试邮件](playbooks/41-mail-confirm-send.md) · [高铁待支付订单](playbooks/42-rail-order-preview.md) · [更新记录](docs/updates.md)

## 现在就试

- **小豆独立 App**：把短版或[完整 44 条](prompts/xiaodou-paste-pack.txt)粘贴到新对话，再说「开启皇帝模拟器」或「帮我做个减肥计划」。App 原生导入入口待核实。
- **豆包工作 / 支持 Agent Skills 的客户端**：下载 ZIP 后使用客户端的技能导入入口。[导入步骤](docs/install.md)

## 三省六部怎么帮忙

**三省把计划理清，六部按需帮忙。** 目标怎么定、时间够不够、下一步谁做，这些先由小豆处理。想查分工，再展开人物卡。

| 中书省 · 拟案 | 门下省 · 审议 | 尚书省 · 派活 |
| :--: | :--: | :--: |
| <img src="docs/studio/portraits/zhongshu.jpg" width="96" alt="顾砚"> | <img src="docs/studio/portraits/menxia.jpg" width="96" alt="沈照"> | <img src="docs/studio/portraits/shangshu.jpg" width="96" alt="陆简"> |

| 吏部 · 分工 | 户部 · 时间和预算 | 礼部 · 沟通 |
| :--: | :--: | :--: |
| <img src="docs/studio/portraits/appointments.jpg" width="96" alt="周衡"> | <img src="docs/studio/portraits/treasury.jpg" width="96" alt="叶算盘"> | <img src="docs/studio/portraits/rites.jpg" width="96" alt="温言"> |
| **兵部 · 推进行动** | **刑部 · 核对边界** | **工部 · 做出交付物** |
| <img src="docs/studio/portraits/operations.jpg" width="96" alt="季行"> | <img src="docs/studio/portraits/review.jpg" width="96" alt="宋矩"> | <img src="docs/studio/portraits/works.jpg" width="96" alt="林造"> |

[看人物介绍和各部门的使用示例](https://fangx-ai.github.io/awesome-xiaodou/studio/#court-title) · [Edict 适配说明](docs/edict-adaptation.md) · [完整建设计划与验收标准](docs/roadmap.md)

## 精选提示词

[看提示词出处](skills/xiaodou-skill/references/prompt-sources.md) · [看试用案例和验收方法](docs/prompt-quality.md)

### 一个月减肥计划

```text
帮我做一个月的减肥计划。我是成年人，午饭常点外卖，周二和周四晚上各有 25 分钟，不去健身房。先确认我缺少的关键信息，再给四周目标和首周行动表。写清楚每天几点能做什么、外卖怎么点、加班如何简化。第 7 天我带着打卡回来，根据实际完成情况帮我排下一周。
```

[完整版：填入自己的情况，生成四周计划与复盘](prompts/41-weight-plan.md)

### 抖音收藏找餐厅

```text
从我授权的抖音收藏里，筛出离「杭州西湖」较近的三家餐厅。每家列菜系、地址和原视频链接。请标出查不到的营业信息；如果读不到收藏，先让我发几个收藏链接。
```

[完整版：按预算筛店，核对同名分店](playbooks/09-saved-restaurants.md)

### 聊天截图记日历

```text
把这张聊天截图整理成日程。先找最后定下的时间，把取消和改期单独列出。遇到「下周五」时，用原消息日期换算，缺日期就问我。给我看时间、地点和原话，我确认后再添加。
```

[完整版：确认日期、检查重复、写入日历](playbooks/11-screenshot-calendar.md)

### 飞书资料变周报

```text
用我提供的飞书文档写一份给直属负责人的周报。按「交付成果、阻塞与所需支持、下周行动」三栏整理，每项附出处。讨论中的计划标为待定，没写负责人或截止时间的地方留待确认。
```

[完整版：合并重复进展并逐条附出处](playbooks/36-weekly-report.md)

## 玩法目录

[全部 44 条提示词](skills/xiaodou-skill/references/prompts.md) · [42 个社区案例与出处](docs/catalog.md) · [最新线索](docs/radar.md)

[复制 9 条常用指令](prompts/xiaodou-quick-pack.txt) · [查看版本记录](docs/updates.md)

## 贡献一个玩法

你用一句什么话，让小豆帮你做成了一件事？欢迎带着**原指令和结果**来分享。也可以给项目点个 **Star**，下次想找提示词时方便回来。

[投稿](https://github.com/Fangx-AI/awesome-xiaodou/issues/new/choose) · [贡献指南](CONTRIBUTING.md) · [分享项目到 X](https://twitter.com/intent/tweet?text=%E6%8A%8A%E6%97%A5%E5%B8%B8%E4%BA%A4%E7%BB%99%E5%B0%8F%E8%B1%86%E3%80%82%E5%B0%8F%E8%B1%86%20Skill%20%E6%94%B6%E5%BD%95%2044%20%E6%9D%A1%E4%B8%AD%E6%96%87%E6%8F%90%E7%A4%BA%E8%AF%8D%EF%BC%8C%E6%9C%89%E5%87%8F%E8%82%A5%E8%AE%A1%E5%88%92%E3%80%81%E6%88%AA%E5%9B%BE%E8%AE%B0%E6%97%A5%E5%8E%86%E3%80%81%E5%8F%91%E9%82%AE%E4%BB%B6%E5%92%8C%E9%AB%98%E9%93%81%E6%9F%A5%E7%A5%A8%E3%80%82&url=https%3A%2F%2Fgithub.com%2FFangx-AI%2Fawesome-xiaodou)

<details>
<summary>玩法研究与抓取记录</summary>

- [玩法雷达](docs/radar.md) · [抓取运行记录](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/radar.yml)
- [作者分享](docs/community.md) · [来源登记](docs/source-ledger.md) · [失败记录](docs/failures.md) · [使用边界](docs/limitations.md)
- [项目对照](docs/project-comparison.md) · [100 项外部测试用例](docs/external-tests.md) · [历次检索记录](docs/research-log.md)
- [玩法 CSV](data/playbooks.csv) · [玩法 JSON](data/playbooks.json)

</details>

社区项目 · [原创内容 CC BY 4.0](LICENSE) · [小豆 App 图标来源](https://apps.apple.com/cn/app/id6815582077)
