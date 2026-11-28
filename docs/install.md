# 使用小豆 Skill

[查看下载、回放和真机使用状态](compatibility.md)

## 小豆独立 App

### 下载和开通

认准开发者**北京春田知韵科技有限公司**。同一款独立 App 在两个商店的显示名称不同。

- **iPhone / iPad**　打开中国区 App Store 的「小豆 - 豆包旗下 AI 个人助理」条目。商店标注 iOS 或 iPadOS 15.0 起，年龄分级 18+。如果链接打开失败，可以在手机的 App Store 里搜「小豆」。 [App Store 中国区](https://apps.apple.com/cn/app/小豆-豆包旗下-ai-个人助理/id6815582077)
- **Android**　打开手机自带的应用商店搜「小豆」。小米所列包名是 `com.larus.doubaom`。小米网页提示维护时，按网页提示到小米手机里的应用商店查看是否可以安装。 [小米应用商店](https://app.mi.com/details?id=com.larus.doubaom)

装好后，打开小豆，按 App 提示登录。页面要求邀请码或还在等候时，见下一节。已经能发消息时，可以直接[在新对话开局](#发一条消息开局)。

查看两家商店的[版本和网页下载状态](app-stores.md)。

### 没有邀请码怎么办

小豆在 11 月 24 日启动邀请制公测。收到朋友分享的邀请码后，回小豆独立 App 按页面提示开通。App 提供等候登记时，可以先登记。 [豆包官方公测公告](https://sina.cn/news/detail/5368723595591761.html) · [小豆产品介绍](https://www.doubao.com/xiaodou/)

豆包在公测公告中说明，受邀用户可获得一定免费额度。开通后可以先用对话制定计划；如果 App 提示某个任务会扣额度或需要购买，按当时显示的额度和确认页判断。 [豆包公测公告](https://sina.cn/news/detail/5368723595591761.html) · [App Store 套餐与购买项](https://apps.apple.com/cn/app/id6815582077)

等候期间可以先[选一份场景开局](share-cards.md)、看[减肥计划示例](weight-first-week.md)，或[反馈首页是否好懂](field-tests/cold-read.md)。

### 开通或发送卡住了

- 找不到或装不上，先核对[对应商店的名称和开发者](#下载和开通)。
- 登录后看见邀请或等待提示，查看[邀请码与等候说明](#没有邀请码怎么办)。
- 已开通但发不出第一条消息，先确认能否在新对话发送一条普通消息。如果普通消息能发，回报你复制的是哪份开局。

[回报卡住的步骤][access-feedback]。填设备、系统、应用商店和日期即可。留言会公开显示你的 GitHub 账号，请省略邀请码和手机号。有人邀请你试用时，也可以把卡住的步骤直接告诉对方。

### 发一条消息开局

想直接试减肥、健身、自律阅读、英语或留学，可以[选一份带目标的开局](../prompts/life-plans/scenes.md)。

打开小豆独立 App 的新对话，粘贴[首页的开局消息](../README.md#一句话在小豆里开始)。把想做的事填在「我的目标」后面，一起发出。之后在同一对话报进度或说出新的约束。

- **一条消息开局**：内含三省六部分工、冲突退回和进展续接的基本规则。
- **[完整版皇帝模式](../prompts/emperor-simulator.md)**：补充五个常见计划的处理方法、外部操作确认和御前问签。
- **[30 个生活计划](../skills/xiaodou-skill/references/life-plans/README.md)**　可在线逐条复制，也可[下载小豆 App 开局包](https://github.com/Fangx-AI/awesome-xiaodou/releases/latest/download/xiaodou-app-starters.zip)。解压后可从「五个常用开局」选一个现成目标，或按「先读这里.txt」找其他计划。有自己的目标时，可以打开对应分类的「自填目标.txt」。
- **整包提示词**：用于一段对话里选择多种场景，按下面的步骤使用。

1. 打开[9 条常用指令](../prompts/xiaodou-quick-pack.txt)或[完整 48 条](../prompts/xiaodou-paste-pack.txt)，点 GitHub 文件工具栏中的复制按钮，或打开 Raw 后全选复制。
2. 在小豆中新开一个对话，粘贴发送选好的提示词包。
3. 在同一个对话里说「开启皇帝模拟器」「帮我做个减肥计划」或「看菜单」。

也可以复制[单条提示词](../skills/xiaodou-skill/references/prompts.md)。一句话和提示词包都通过当前对话使用，小豆独立 App 的原生技能安装入口仍待核实。

这版正准备真机试用。[三步真机演练](field-tests/pilot-s0.md)可以直接复制；[实测登记](field-tests/README.md)记录已观察到的设备、版本和结果。

## 豆包工作 / 支持 Agent Skills 的客户端

1. 下载 [最新技能 ZIP](https://github.com/Fangx-AI/awesome-xiaodou/releases/latest/download/xiaodou-skill.zip)。 [版本与校验值](https://github.com/Fangx-AI/awesome-xiaodou/releases/latest)
2. 解压，保留 `xiaodou-skill` 文件夹及其 `references`。在支持技能导入的客户端选择该技能文件夹，或按客户端要求上传技能。豆包工作的入口在「技能」中的本地导入。
3. 在已启用技能的对话中说「用小豆 Skill 帮我做个减肥计划」，或在技能选择器中选择它。

技能 ZIP 内含五类重点计划手册、关帝百签，以及有脚本权限时可用的紫微斗数与八字排盘工具。 [问签与排盘说明](../skills/xiaodou-skill/references/divination.md)

不同客户端的导入格式和权限以实际界面为准。本版已检查 ZIP 结构，豆包工作及小豆客户端导入尚未实测。

固定版本的七天试用，在候选构建摘要的「手机可复制的固定开局」里选目标。观察者也可以把工件内 `STARTERS.md` 里的固定链接发给参与者。每条开局的纯文本版本见 `STARTERS.tsv`。真机演练从 `CANDIDATE.txt` 打开 `pilot`，首页冷读打开 `public_readme`。

要参加固定版本试用，打开[通过的候选构建](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/check-skill.yml?query=branch%3Acodex%2Fs0-pilot)，在运行摘要的「小豆候选包」下载工件。该入口需要 GitHub 登录。

在仓库根目录，用 Python 3.11 或更新版本运行 `python scripts/verify_candidate.py <解开的候选工件目录> --commit <Actions 上显示的完整提交号>`。它核对新候选包的文件校验值、版本和固定链接。历史候选包可在解压目录运行 `sha256sum -c SHA256SUMS` 查看当时登记的校验值。

[豆包工作官方技能说明](https://www.feishu.cn/content/article/7677519271848610746) · [Agent Skills 规范](https://agentskills.io/specification)

[access-feedback]: https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=app-access.yml
