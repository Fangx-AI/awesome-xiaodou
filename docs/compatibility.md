# 小豆皇帝模拟器 · 使用状态

要开始，请先[下载和开通小豆独立 App](install.md#下载和开通)。能在新对话里发消息后，再从 GitHub 复制开局。商店能打开、能登录、Skill 能跑通和外部动作能执行，各有自己的验证记录。

## 小豆独立 App

| 环节 | 验证状态 | 对应证据 |
| --- | --- | --- |
| 下载入口 | 已核对中国区 App Store 和小米应用商店的公开条目，手机下载安装待实测 | [商店版本和网页状态](app-stores.md) · [下载步骤](install.md#下载和开通) |
| 登录和开通 | 豆包官方宣布 11 月 24 日启动邀请制公测。账号进度以 App 显示为准 | [豆包官方公告](https://sina.cn/news/detail/5368723595591761.html) · [等候与开通](install.md#没有邀请码怎么办) |
| 一条消息开局、报进度、门下改案 | 已有本地对话回放，小豆独立 App 仍待实测 | [本地回放](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/prompt-quality.md#本地候选回放) |
| 原生提醒 | 创建、读取回执、实际触发与撤销仍待实测 | [真机结果](field-tests/README.md) |
| 截图记日历、飞书周报 | 文字回放覆盖日程预览和周报草稿。图片识别、日历写入和飞书连接器仍待实测 | [截图日历](../playbooks/11-screenshot-calendar.md) · [飞书周报](../playbooks/36-weekly-report.md) |
| App 内原生技能导入 | 待确认导入入口。当前公开用法是复制开局到新对话 | [复制开局](../README.md#一句话在小豆里开始) |

## GitHub 入口验证

在 Chrome 打开 GitHub 仓库的公开首页，检查了 1440px 浅色、390px 浅色和 320px 深色三个视口。都能点到开局、展开并复制，剪贴板内容与对应提交的文本一致，下载入口也能跳到公开指南。320px 下长行在代码框内横向滚动。 [核对过的 README 版本](https://github.com/Fangx-AI/awesome-xiaodou/blob/43bf9023069a46222df6e133fab1da20f5a9b8de/README.md)

## 下载技能文件

v2.3.0 的技能 ZIP 含 30 个生活计划、48 条提示词和九张人物图。发布页另有五份能直接复制的场景开局。已核对 ZIP 结构和开局文本。各客户端的实际导入与权限仍待复测。 [下载 v2.3.0](https://github.com/Fangx-AI/awesome-xiaodou/releases/tag/skill-v2.3.0) · [候选包构建记录](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/check-skill.yml?query=branch%3Acodex%2Fs0-pilot) · [导入步骤](install.md#豆包工作--支持-agent-skills-的客户端)
