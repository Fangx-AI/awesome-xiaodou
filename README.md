# 小豆 Skill

![小豆 Skill · 把日常交给小豆](assets/xiaodou-skill-blue-cover.png)

**告诉小豆你想做什么，Skill 帮你选对提示词。** 从皇帝模拟器、减肥计划，到截图记日历、查高铁，内置 **44 条中文指令**。

[**开启皇帝模拟器**](prompts/emperor-simulator.md) · [复制 9 条常用指令](prompts/xiaodou-quick-pack.txt) · [下载技能 ZIP](https://github.com/Fangx-AI/awesome-xiaodou/releases/latest/download/xiaodou-skill.zip)

## 小豆皇帝模拟器

**你下旨，朝廷把事情拆到今天。** 中书省拟案、门下省挑漏洞、尚书省派活，六部各管分工、预算、沟通、推进、边界和建设。

> 下旨：我想用一个月学会剪短视频，每周只有 3 小时，预算 200 元。月底要独立做出 1 条 60 秒成片。先安排今晚做什么。

用「准奏」定方案，「晚朝」复盘，「存档」把进度带到下次对话。 [复制皇帝模拟器提示词](prompts/emperor-simulator.md) · [分享这套玩法](https://twitter.com/intent/tweet?text=%E5%B0%8F%E8%B1%86%E7%9A%87%E5%B8%9D%E6%A8%A1%E6%8B%9F%E5%99%A8%EF%BC%9A%E4%BD%A0%E4%B8%8B%E6%97%A8%EF%BC%8C%E4%B8%89%E7%9C%81%E6%8B%9F%E6%A1%88%E3%80%81%E5%AE%A1%E6%A0%B8%E3%80%81%E6%B4%BE%E6%B4%BB%EF%BC%8C%E5%85%AD%E9%83%A8%E6%8A%8A%E4%BA%8B%E6%8B%86%E6%88%90%E4%BB%8A%E5%A4%A9%E8%83%BD%E5%81%9A%E7%9A%84%E4%B8%8B%E4%B8%80%E6%AD%A5%E3%80%82%E5%A4%8D%E5%88%B6%E6%8F%90%E7%A4%BA%E8%AF%8D%EF%BC%8C%E5%BC%80%E7%AC%AC%E4%B8%80%E5%9C%BA%E6%97%A9%E6%9C%9D%E3%80%82&url=https%3A%2F%2Fgithub.com%2FFangx-AI%2Fawesome-xiaodou%2Fblob%2Fmain%2Fprompts%2Femperor-simulator.md)

**11 月 27 日更新**：[发测试邮件](playbooks/41-mail-confirm-send.md) · [高铁待支付订单](playbooks/42-rail-order-preview.md) · [更新记录](docs/updates.md)

## 现在就试

- **小豆独立 App**：把短版或[完整 44 条](prompts/xiaodou-paste-pack.txt)粘贴到新对话，再说「开启皇帝模拟器」或「帮我做个减肥计划」。App 原生导入入口待核实。
- **豆包工作 / 支持 Agent Skills 的客户端**：下载 ZIP 后使用客户端的技能导入入口。[导入步骤](docs/install.md)

![说出减肥需求，生成四周路线图、首周安排和打卡复盘模板](assets/skill-flow.svg)

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
