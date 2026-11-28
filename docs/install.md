# 使用小豆 Skill

[查看下载、回放和真机使用状态](compatibility.md)

## 小豆独立 App

### 下载和开通

1. **下载小豆独立 App。** 搜「小豆 - 豆包旗下 AI 个人助理」，认准开发者**北京春田知韵科技有限公司**。
   - **iPhone / iPad**　先打开中国区 App Store 的小豆条目。页面提示当前地区不可用时，在你正在使用的商店里搜完整应用名。 [App Store 中国区](https://apps.apple.com/cn/app/id6815582077)
   - **Android**　打开手机自带的应用商店搜「小豆」。小米网页显示维护时，也可以在手机里的小米应用商店搜索。 [小米应用商店](https://app.mi.com/details?id=com.larus.doubaom)
2. **打开小豆，按 App 提示登录。** 正在等候或需要输入邀请码时，见下一节。已经能在新对话发消息时，直接[发一条消息开局](#发一条消息开局)。

查看两家商店的[版本和网页下载状态](app-stores.md)。

### 没有邀请码怎么办

小豆在 11 月 24 日启动邀请制公测。收到朋友分享的邀请码后，回小豆独立 App 按页面提示开通。App 提供等候登记时，可以先登记。 [豆包官方公测公告](https://sina.cn/news/detail/5368723595591761.html) · [小豆产品介绍](https://www.doubao.com/xiaodou/)

豆包在公测公告中说明，受邀用户可获得一定免费额度。开通后可以先用对话制定计划；如果 App 提示某个任务会扣额度或需要购买，按当时显示的额度和确认页判断。 [豆包公测公告](https://sina.cn/news/detail/5368723595591761.html) · [App Store 套餐与购买项](https://apps.apple.com/cn/app/id6815582077)

等候期间可以先[选一份场景开局](share-cards.md)、看[减肥计划示例](weight-first-week.md)，或[反馈首页是否好懂](field-tests/cold-read.md)。

如果搜不到、装不上、登录失败、开通遇阻或消息发不出去，可以[回报卡住的步骤][access-feedback]。填设备、系统、应用商店和日期即可。表单需要 GitHub 账号，留言会公开，避免填写邀请码或手机号。

### 发一条消息开局

想直接试减肥、健身、自律阅读、英语或留学，可以[选一份带目标的开局](share-cards.md)。

打开小豆新对话，复制[首页的开局消息](../README.md#一句话在小豆里开始)，在末尾加上自己的目标，整段一次发出。

- **[开局纯文本](../prompts/xiaodou-start.txt)**：复制后加上你的目标，发成一条消息。
- **[正式版完整指令](../prompts/emperor-simulator.md)**：包含三省六部分工、进展更新和跨对话续聊摘要。
- **[30 个生活计划](../skills/xiaodou-skill/references/life-plans/README.md)**：可在线逐条复制，也可[下载小豆 App 开局包](https://github.com/Fangx-AI/awesome-xiaodou/releases/download/skill-v2.4.0/xiaodou-app-starters.zip)。解压后打开「先读这里.txt」，按文件名选一个计划，把全文发到小豆新对话。
- **整包提示词**：用于一段对话里选择多种场景，按下面的步骤使用。

1. 打开[9 条常用指令](../prompts/xiaodou-quick-pack.txt)或[完整 48 条](../prompts/xiaodou-paste-pack.txt)，点 GitHub 文件工具栏中的复制按钮，或打开 Raw 后全选复制。
2. 在小豆中新开一个对话，粘贴发送选好的提示词包。
3. 在同一个对话里说「开启皇帝模拟器」「帮我做个减肥计划」或「看菜单」。

也可以复制[单条提示词](../skills/xiaodou-skill/references/prompts.md)。一句话和提示词包都通过当前对话使用，小豆独立 App 的原生技能安装入口仍待核实。

## 豆包工作 / 支持 Agent Skills 的客户端

1. 下载 [v2.4.0 技能 ZIP](https://github.com/Fangx-AI/awesome-xiaodou/releases/download/skill-v2.4.0/xiaodou-skill.zip)。 [版本与校验值](https://github.com/Fangx-AI/awesome-xiaodou/releases/tag/skill-v2.4.0)
2. 解压，保留 `xiaodou-skill` 文件夹及其 `references`。在支持技能导入的客户端选择该技能文件夹，或按客户端要求上传技能。豆包工作的入口在「技能」中的本地导入。
3. 在已启用技能的对话中说「用小豆 Skill 帮我做个减肥计划」，或在技能选择器中选择它。

包内含说明、提示词、出处和九张人物图。不同客户端的导入格式和权限以实际界面为准。本版已检查 ZIP 结构，豆包工作及小豆客户端导入尚未实测。

要参加固定版本试用，在候选构建摘要的「手机可复制的固定开局」选一个目标。观察者可以把对应的固定链接发给参与者。下载候选工件验证文本时，需要登录 GitHub。 [打开候选构建](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/check-skill.yml?query=branch%3Acodex%2Fs0-pilot)

下载新候选包后，可在仓库根目录用 Python 3.11 或更新版本运行 `python scripts/verify_candidate.py <解压目录> --commit <Actions 上显示的完整提交号>`，核对文件校验值和固定版本链接。

[豆包工作官方技能说明](https://www.feishu.cn/content/article/7677519271848610746) · [Agent Skills 规范](https://agentskills.io/specification)

[access-feedback]: https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=app-access.yml
