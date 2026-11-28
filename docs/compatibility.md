# 小豆皇帝模拟器 · 使用状态

要开始，请先[下载和开通小豆独立 App](install.md#下载和开通)。能在新对话里发消息后，再从 GitHub 复制开局。商店能打开、能登录、Skill 能跑通和外部动作能执行，各有自己的验证记录。

## 小豆独立 App

| 环节 | 截至 2026 年 11 月 28 日 | 对应证据 |
| --- | --- | --- |
| iPhone、iPad 下载入口 | 中国区 App Store 有公开条目，系统要求 15.0 或更新版本 | [Apple 条目](https://apps.apple.com/cn/app/%E5%B0%8F%E8%B1%86-%E8%B1%86%E5%8C%85%E6%97%97%E4%B8%8B-ai-%E4%B8%AA%E4%BA%BA%E5%8A%A9%E7%90%86/id6815582077) |
| Android 下载入口 | 小米应用商店有公开条目。网页提示部分下载服务维护，手机内能否下载仍待试 | [小米应用商店](https://app.mi.com/details?id=com.larus.doubaom) |
| 登录和开通 | 11 月 24 日公测以邀请制启动。账号能否开通以 App 所示为准 | [首都之窗公测报道](https://www.beijing.gov.cn/fuwu/lqfw/gggs/202611/t20261124_4957049.html) |
| 一条消息开局、报进度、门下改案 | 已有本地对话回放，小豆独立 App 仍待实测 | [本地回放](https://github.com/Fangx-AI/awesome-xiaodou/blob/codex/s0-pilot/docs/prompt-quality.md#本地候选回放) |
| 原生提醒 | 创建、读取回执、实际触发与撤销仍待实测 | [真机结果](field-tests/README.md) |
| 截图记日历、飞书周报 | 文字回放覆盖日程预览和周报草稿。图片识别、日历写入和飞书连接器仍待实测 | [截图日历](../playbooks/11-screenshot-calendar.md) · [飞书周报](../playbooks/36-weekly-report.md) |
| App 内原生技能导入 | 待确认导入入口。当前公开用法是复制开局到新对话 | [复制开局](../README.md#一句话在小豆里开始) |

## GitHub 入口验证

在 Chrome 打开 GitHub 仓库的公开首页，检查了 1440px 浅色、390px 浅色和 320px 深色三个视口。都能点到开局、展开并复制，剪贴板内容与对应提交的文本一致，下载入口也能跳到公开指南。320px 下长行在代码框内横向滚动。 [核对过的 README 版本](https://github.com/Fangx-AI/awesome-xiaodou/blob/43bf9023069a46222df6e133fab1da20f5a9b8de/README.md)

## 下载技能文件

支持 Agent Skills 的客户端可用候选 ZIP 尝试导入。候选构建已经核对 ZIP 结构、九张人物图、30 个生活计划和开局文本。各客户端的实际导入与权限仍待复测。历史 Release 对应旧版本，30 个生活计划从当前候选构建获取。 [候选包构建记录](https://github.com/Fangx-AI/awesome-xiaodou/actions/runs/46116228555) · [导入步骤](install.md#豆包工作--支持-agent-skills-的客户端) · [历史 Release](https://github.com/Fangx-AI/awesome-xiaodou/releases/tag/skill-v2.1.0)
