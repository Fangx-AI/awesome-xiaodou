# 小豆 Skill

![小豆 Skill · 把日常交给小豆](assets/xiaodou-skill-blue-cover.png)

**告诉小豆你想做什么，Skill 帮你选对提示词。** 减肥计划、抖音收藏找店、截图记日历、飞书写周报，内置 **41 条中文指令**。

[**复制到小豆**](prompts/xiaodou-paste-pack.txt) · [**下载技能 ZIP**](https://github.com/Fangx-AI/awesome-xiaodou/releases/latest/download/xiaodou-skill.zip) · [浏览全部提示词](skills/xiaodou-skill/references/prompts.md)

## 现在就试

- **小豆独立 App**：把[整包提示词](prompts/xiaodou-paste-pack.txt)复制到新对话，再说「帮我做个减肥计划」。App 原生导入入口待核实。
- **豆包工作 / 支持 Agent Skills 的客户端**：下载 ZIP 后使用客户端的技能导入入口。[导入步骤](docs/install.md)

![说出减肥需求，匹配体重管理提示词，得到七天安排和打卡复盘模板](assets/skill-flow.svg)

## 精选提示词

### 一周减肥计划

```text
帮我做份适合成年人的一周减肥计划。先问我的吃饭习惯、活动量、能腾出的时间和健康限制。根据我的回答选两个做得到的小目标，给我 7 天安排、外卖点单建议和 30 秒打卡模板。第 7 天我带着记录来，请根据完成情况帮我调整下一周。
```

[完整版：初次计划、打卡和每周复盘](prompts/41-weight-plan.md)

### 抖音收藏找餐厅

```text
从我授权的抖音收藏里，筛出离「杭州西湖」较近的三家餐厅。每家列菜系、地址和原视频链接。请标出查不到的营业信息；如果读不到收藏，先让我发几个收藏链接。
```

### 聊天截图记日历

```text
把这张聊天截图整理成日程。先列标题、日期、开始时间、地点和参加人。遇到「下周五」这种说法，请写成具体日期让我确认。我确认后再添加到指定日历。
```

### 飞书资料变周报

```text
仅用我提供的飞书文档写一份周报。按「本周完成、阻塞、下周计划」三栏整理，每项附上文档出处。信息缺失就列在「待补充」，让我检查后再定稿。
```

## 玩法目录

[全部 41 条提示词](skills/xiaodou-skill/references/prompts.md) · [40 个社区案例与出处](docs/catalog.md) · [最新线索](docs/radar.md)

## 贡献一个玩法

你用一句什么话，让小豆帮你做成了一件事？欢迎带着**原指令和结果**来分享。也可以给项目点个 **Star**，下次想找提示词时方便回来。

[投稿](https://github.com/Fangx-AI/awesome-xiaodou/issues/new/choose) · [贡献指南](CONTRIBUTING.md) · [分享项目到 X](https://twitter.com/intent/tweet?text=%E5%81%9A%E5%87%8F%E8%82%A5%E8%AE%A1%E5%88%92%E3%80%81%E4%BB%8E%E6%8A%96%E9%9F%B3%E6%94%B6%E8%97%8F%E6%89%BE%E5%BA%97%E3%80%81%E6%8A%8A%E6%88%AA%E5%9B%BE%E5%8F%98%E6%97%A5%E5%8E%86%E3%80%82%E5%B0%8F%E8%B1%86%20Skill%20%E5%86%85%E7%BD%AE%2041%20%E6%9D%A1%E4%B8%AD%E6%96%87%E6%8F%90%E7%A4%BA%E8%AF%8D%EF%BC%8C%E5%8F%AF%E4%BB%A5%E6%95%B4%E5%8C%85%E5%A4%8D%E5%88%B6%E5%88%B0%E5%B0%8F%E8%B1%86%E3%80%82&url=https%3A%2F%2Fgithub.com%2FFangx-AI%2Fawesome-xiaodou)

<details>
<summary>玩法研究与抓取记录</summary>

- [玩法雷达](docs/radar.md) · [抓取运行记录](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/radar.yml)
- [作者分享](docs/community.md) · [来源登记](docs/source-ledger.md) · [失败记录](docs/failures.md) · [使用边界](docs/limitations.md)
- [项目对照](docs/project-comparison.md) · [100 项外部测试用例](docs/external-tests.md) · [历次检索记录](docs/research-log.md)
- [玩法 CSV](data/playbooks.csv) · [玩法 JSON](data/playbooks.json)

</details>

社区项目 · [原创内容 CC BY 4.0](LICENSE) · [小豆 App 图标来源](https://apps.apple.com/cn/app/id6815582077)
