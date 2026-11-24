# Awesome 小豆 🫘

**收集别人怎么用豆包旗下 AI 个人助理「小豆」：真实场景、作者出处、尝试指令和使用边界。**

**40 个玩法条目 · 23 项来源记录 · 100 个外部待测用例 · 本项目真机实测 0 条**

来源记录包含原作者、媒体、项目参考及待追溯线索；以上数字不能相加为成功案例数。

更新：2026-11-24（北京时间）

[完整目录](docs/catalog.md) · [别人怎么整理与统计](docs/project-comparison.md) · [100项测试清单](docs/external-tests.md) · [失败记录](docs/failures.md) · [来源登记](docs/source-ledger.md) · [搜索覆盖](docs/coverage-round3.md)

社区整理项目，与豆包官方无关联。这里的小豆指豆包旗下 AI 个人助理独立应用。

## 先看别人整理了什么

| 想看什么 | 阅读入口 |
| --- | --- |
| 创作者的日常组合玩法 | [歸藏：内测玩法分享](https://weibo.com/2/detail/5368835221753457) |
| 有执行结果和边界的媒体体验 | [智东西 / 36氪](https://www.36kr.com/p/4083578123184773)、[爱范儿](https://www.ifanr.com/1691355) |
| 电话订位记录 | [密度新闻](https://weibo.com/2/detail/5368859840217249) |
| 数据与消费场景 | [华尔街见闻·全天候科技](https://wallstreetcn.com/articles/3786572) |
| 另一份入门与测试资料库 | [wowowuyun-boop/awesome-xiaodou](https://github.com/wowowuyun-boop/awesome-xiaodou)（其 100 个场景标注为待实测） |

本轮还补充了向阳乔木、苍何、酱紫表、机智流、南都记者与 Linux DO 用户的记录。更多作者、转载关系和待追溯线索见[作者导航](docs/community.md)与[23项来源登记](docs/source-ledger.md)。

需要自己筛选？下载 [JSON](data/playbooks.json) 或 [CSV](data/playbooks.csv)，按分类、来源和证据状态筛选；修改数据后运行 `python scripts/build_catalog.py` 可重新生成目录。

## 玩法目录

**第三方体验 ≠ 本项目复测。** 下列提示词由本项目重新编写，不是原作者逐字指令；任务创建、实际触发和长期稳定执行也分开记录。权限、设备和版本可能影响可用范围。

### 🍜 生活与出行

| 玩法 | 用途 | 证据状态 |
| --- | --- | --- |
| [从抖音收藏找附近餐厅](playbooks/09-saved-restaurants.md) | 找回收藏里的店 | 作者体验分享 / 未复测 |
| [请小豆打电话问餐厅](playbooks/04-restaurant-call.md) | 询问门店及订位 | 第三方实测报道 / 未复测 |
| [用对话准备打车](playbooks/14-ride-hailing.md) | 准备出行订单 | 媒体体验 / 未复测 |
| [猫粮补货提醒](playbooks/05-restock.md) | 估算耗材余量 | 演示转述 / 待实测 |
| [搜索并播放音乐](playbooks/25-music.md) | 详见来源与尝试指令 | 作者体验（聚合页） / 未复测 |
| [查车次并发现目的地活动](playbooks/26-train-events.md) | 详见来源与尝试指令 | 作者体验（聚合页） / 未复测 |
| [拍照识别物品](playbooks/37-photo-object.md) | 详见来源与尝试指令 | 第三方体验 / 未复测 |

### 🛍️ 购物与消费

| 玩法 | 用途 | 证据状态 |
| --- | --- | --- |
| [商品降价提醒](playbooks/01-price-watch.md) | 跟进商品价格 | 媒体任务创建记录 / 未复测 |
| [团购券到期提醒](playbooks/02-coupon-reminder.md) | 避免忘记用券 | 发布报道 / 待实测 |
| [按需求选品并生成提单](playbooks/15-shopping-card.md) | 从需求走到提单 | 媒体体验 / 未复测 |
| [从历史订单查券价](playbooks/20-order-price-check.md) | 比较已买券与现价 | 媒体体验 / 未复测 |
| [用对话发起话费充值](playbooks/28-phone-credit.md) | 详见来源与尝试指令 | 作者自述，缺交易回执 / 未复测 |

### 🎬 创作与内容整理

| 玩法 | 用途 | 证据状态 |
| --- | --- | --- |
| [短视频作品复盘](playbooks/08-video-review.md) | 根据作品表现选题 | 作者体验与描述 / 未复测 |
| [拆解收藏的参考视频](playbooks/10-reference-video.md) | 提炼视频结构 | 作者体验分享 / 未复测 |
| [从评论反馈找选题](playbooks/24-comment-insights.md) | 发现观众问题 | 媒体功能描述 / 未复测 |
| [收藏整理进飞书多维表格](playbooks/12-collection-base.md) | 集中管理收藏 | 作者体验分享 / 未复测 |
| [生成一张图片](playbooks/31-native-image.md) | 详见来源与尝试指令 | 第三方实测文章 / 未复测 |
| [尝试调用 Seedance 生成视频](playbooks/34-seedance.md) | 详见来源与尝试指令 | 功能介绍，未见成品 / 未复测 |
| [查抖音热点辅助选题](playbooks/35-douyin-trends.md) | 详见来源与尝试指令 | 功能介绍，未见执行过程 / 未复测 |
| [为抖音评论拟回复](playbooks/39-comment-replies.md) | 详见来源与尝试指令 | 作者帖二次聚合，待原帖 / 未复测 |

### 🗓️ 办公与个人管理

| 玩法 | 用途 | 证据状态 |
| --- | --- | --- |
| [聊天截图变成日程](playbooks/11-screenshot-calendar.md) | 少手工录入约定 | 作者体验分享 / 未复测 |
| [日程冲突检查](playbooks/03-calendar-check.md) | 识别安排重叠 | 发布报道 / 待实测 |
| [在百度网盘找文件](playbooks/18-netdisk-search.md) | 定位已有文件 | 媒体功能描述 / 未复测 |
| [将行情数据整理为 Excel](playbooks/19-wind-excel.md) | 获取可用数据文件 | 媒体体验 / 未复测 |
| [纠正个人记忆与偏好](playbooks/23-memory-correction.md) | 修正个人背景 | 媒体功能描述 / 未复测 |
| [搜索和修改飞书文档](playbooks/27-feishu-docs.md) | 详见来源与尝试指令 | 作者功能体验描述（聚合页） / 未复测 |
| [查询自己的 GitHub 信息](playbooks/29-github-info.md) | 详见来源与尝试指令 | 作者自述，缺执行细节 / 未复测 |
| [将一件事拆成多阶段提醒](playbooks/30-staged-reminders.md) | 详见来源与尝试指令 | 媒体任务创建记录 / 未复测 |
| [等待生成时处理另一项任务](playbooks/32-parallel-tasks.md) | 详见来源与尝试指令 | 第三方实测文章 / 未复测 |
| [用自然语言调整回复风格](playbooks/33-reply-style.md) | 详见来源与尝试指令 | 第三方短期体验 / 未复测 |
| [用飞书资料生成工作周报](playbooks/36-weekly-report.md) | 详见来源与尝试指令 | 内置模板观察 / 未复测 |
| [按时间发送准备好的资料](playbooks/38-scheduled-file.md) | 详见来源与尝试指令 | 发布报道转述演示 / 未复测 |
| [围绕飞书资料做知识问答](playbooks/40-feishu-qa.md) | 详见来源与尝试指令 | 作者帖二次聚合，待原帖 / 未复测 |

### 🔔 长期跟进与兴趣

| 玩法 | 用途 | 证据状态 |
| --- | --- | --- |
| [行业动态早报](playbooks/07-daily-brief.md) | 定期关注行业 | 社区文章 / 待实测 |
| [跟进演出开票](playbooks/16-ticket-alert.md) | 等待新场次公告 | 媒体任务创建记录 / 未复测 |
| [播客更新主动提醒](playbooks/17-podcast-update.md) | 获知节目更新 | 媒体体验 / 未复测 |
| [追踪游戏和赛事动态](playbooks/13-interest-updates.md) | 跟进个人兴趣 | 作者体验分享 / 未复测 |
| [跟进指定政策公告](playbooks/22-policy-monitor.md) | 关注公告变化 | 模板观察 / 待验证 |
| [口述作息并建立回顾任务](playbooks/21-habit-log.md) | 持续记录作息 | 媒体任务创建记录 / 未复测 |
| [日常健康信息汇总](playbooks/06-health-summary.md) | 回顾活动记录 | 作者体验分享 / 未复测 |

## 第一次使用

小豆于 2026-11-24 开启邀请制公测，具体资格与额度以应用内显示为准。[发布报道](https://www.nbd.com.cn/articles/2026-11-24/4656943.html)

从 [App Store](https://apps.apple.com/cn/app/id6815582077) 找到应用；安卓用户可在应用商店搜索“小豆”，核对开发者“北京春田知韵科技有限公司”。

1. 选一个玩法，先看来源中实际做到了哪一步。
2. 替换指令里的方括号，按需要连接对应应用。
3. 核对结果：既看对话反馈，也看日历、订单、文件或任务页面。
4. 记录日期、版本和成功或失败现象，通过 Issue 分享。

## 什么内容会收录

- **作者体验 / 媒体实测**：有明确原帖或文章，准确说明作者报告的结果；不承诺普遍成功。
- **功能描述 / 模板观察**：能找到出处，但缺少执行结果，单独标注。
- **官方说明 / 演示转述**：用于认识场景，保留原始证据层级。
- **本项目真机实测**：需要环境、步骤和结果证据，目前为 0 条。
- **二次聚合中的具体场景**：可以保留为低置信度探索条目，明确标注未定位原帖；只剩笼统想法、结果冲突或缺少步骤的放入待追溯表。

本轮保留了 [36条公开搜索请求](docs/search-queries.md)，并逐份阅读其他 GitHub 项目文档；检索涉及社交平台、论坛、媒体、视频平台与聚合站。[本轮覆盖与缺口](docs/coverage-round3.md) · [历次检索记录](docs/research-log.md)

## 一起补充

[提交玩法或纠错](https://github.com/Fangx-AI/awesome-xiaodou/issues/new/choose) · [玩法模板](templates/playbook.md) · [贡献指南](CONTRIBUTING.md)

欢迎提供原作者链接、完整视频及失败记录。同一个案例的多次转载合并收录。原创文档采用 [CC BY 4.0](LICENSE)，第三方材料保留原作者权利。
