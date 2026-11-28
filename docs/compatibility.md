# 小豆皇帝模拟器 · 使用状态

要开始，请先[下载和开通小豆独立 App](install.md#下载和开通)。能在新对话里发消息后，再从 GitHub 复制开局。商店能打开、能登录、Skill 能跑通和外部动作能执行，各有自己的验证记录。

## 小豆独立 App

| 环节 | 验证状态 | 对应证据 |
| --- | --- | --- |
| 下载入口 | 已核对中国区 App Store 和小米应用商店的公开条目，手机下载安装待实测 | [商店版本和网页状态](app-stores.md) · [下载步骤](install.md#下载和开通) |
| 登录和开通 | 豆包官方宣布 11 月 24 日启动邀请制公测。账号进度以 App 显示为准 | [豆包官方公告](https://sina.cn/news/detail/5368723595591761.html) · [等候与开通](install.md#没有邀请码怎么办) |
| 一条消息开局、报进度、门下改案 | 已有本地对话回放，小豆独立 App 仍待实测 | [本地回放](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/prompt-quality.md#本地候选回放) |
| 原生提醒 | 小豆官网介绍可跟进任务、到点提醒，以及按需改停。本项目待核对创建、任务卡、实际到点消息与系统通知 | [小豆官网](https://www.doubao.com/xiaodou/) · [真机结果](field-tests/README.md) |
| 猫粮补货 | 官方演示包含估算余量、确认后补货。玩法给出用量变化后的重算和旧提醒核对步骤。原生改提醒、实际送达和下单仍待实测 | [猫粮补货玩法](../playbooks/05-restock.md) |
| 截图记日历、飞书周报 | 文字回放覆盖日程预览和周报草稿。图片识别、日历写入和飞书连接器仍待实测 | [截图日历](../playbooks/11-screenshot-calendar.md) · [飞书周报](../playbooks/36-weekly-report.md) |
| App 内原生技能导入 | 小豆官网和商店说明中尚未核对到导入第三方技能包的步骤。当前公开用法是把开局发到新对话。豆包工作另有本地导入说明 | [小豆官网](https://www.doubao.com/xiaodou/) · [复制开局](../README.md#一句话在小豆里开始) · [豆包工作官方技能说明](https://www.feishu.cn/content/article/7677519271848610746) |

## GitHub 入口验证

在 Chrome 打开 GitHub 仓库的公开首页，检查了 1440px 浅色、390px 浅色和 320px 深色三个视口。都能点到开局、展开并复制，剪贴板内容与对应提交的文本一致，下载入口也能跳到公开指南。320px 下长行在代码框内横向滚动。 [核对过的 README 版本](https://github.com/Fangx-AI/awesome-xiaodou/blob/43bf9023069a46222df6e133fab1da20f5a9b8de/README.md)

新版首页在 Chrome 的 1440px 浅色、390px 浅色和 320px 深色视口下，均能从首屏跳到开局、复制完整指令，并从开局区跳到 30 个生活计划。窄屏以触摸模式核对复制。 [本轮验证的首页版本](https://github.com/Fangx-AI/awesome-xiaodou/blob/837421e8135fcb96501a1cf8cf99821e32dc787e/README.md)

## 下载技能文件

v2.5.1 的 App 开局 ZIP 收录 30 个单独开局、五个分类的自填目标、通用开局和整包。技能 ZIP 随附五类重点计划手册、30 个生活计划、48 条提示词、九张人物图、百签和排盘工具。已从解压包核对签文和历法输出。客户端原生导入与权限仍待真机验证。 [下载 v2.5.1](https://github.com/Fangx-AI/awesome-xiaodou/releases/tag/skill-v2.5.1) · [候选包构建记录](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/check-skill.yml?query=branch%3Acodex%2Fs0-pilot) · [导入步骤](install.md#豆包工作--支持-agent-skills-的客户端)
