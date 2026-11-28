# 使用小豆 Skill

[查看下载、回放和真机使用状态](compatibility.md)

## 小豆独立 App

### 下载和开通

1. **下载小豆独立 App。** 搜「小豆 - 豆包旗下 AI 个人助理」，认准开发者**北京春田知韵科技有限公司**。
   - **iPhone / iPad**　打开中国区 App Store 条目，系统要求 iOS 或 iPadOS 15.0 起，商店年龄分级为 18+。 [App Store 中国区](https://apps.apple.com/cn/app/%E5%B0%8F%E8%B1%86-%E8%B1%86%E5%8C%85%E6%97%97%E4%B8%8B-ai-%E4%B8%AA%E4%BA%BA%E5%8A%A9%E7%90%86/id6815582077)
   - **Android**　在手机自带的应用商店搜索「小豆」。小米官网已列出该应用，11 月 28 日网页显示部分下载服务维护，可在小米手机的应用商店搜索。 [小米应用商店](https://app.mi.com/details?id=com.larus.doubaom)
2. **打开小豆，按 App 提示登录和开通。** 11 月 24 日公测以邀请制启动。页面显示等待或要求邀请码时，以 App 当前的提示为准。能打开新对话并发消息，就可以使用下方的开局。 [小豆产品页](https://www.doubao.com/xiaodou/) · [首都之窗公测报道](https://www.beijing.gov.cn/fuwu/lqfw/gggs/202611/t20261124_4957049.html)

如果商店能打开却装不上、已经登录却还不能开通，或已开通却发不出消息，可以[回报卡住的步骤][access-feedback]。只需选一步，留下系统、商店和日期。

### 发一条消息开局

打开小豆独立 App 的新对话，发送[首页的开局消息](../README.md#一句话在小豆里开始)。有目标可以一起写在消息末尾。之后在同一对话报进度或说出新的约束。

- **一条消息开局**：内含三省六部分工、冲突退回和进展续接的基本规则。
- **[完整版皇帝模式](../prompts/emperor-simulator.md)**：补充五个常见计划的处理方法、外部操作确认和御前问签。
- **[30 个生活计划](../skills/xiaodou-skill/references/life-plans/README.md)**：在小豆 App 里复制对应分类或计划整包，带上自己的目标发送；支持 Agent Skills 的客户端可按任务读取同一套资料。
- **整包提示词**：用于一段对话里选择多种场景，按下面的步骤使用。

1. 打开[9 条常用指令](../prompts/xiaodou-quick-pack.txt)或[完整 46 条](../prompts/xiaodou-paste-pack.txt)，点 GitHub 文件工具栏中的复制按钮，或打开 Raw 后全选复制。
2. 在小豆中新开一个对话，粘贴发送选好的提示词包。
3. 在同一个对话里说「开启皇帝模拟器」「帮我做个减肥计划」或「看菜单」。

也可以复制[单条提示词](../skills/xiaodou-skill/references/prompts.md)。一句话和提示词包都通过当前对话使用，小豆独立 App 的原生技能安装入口仍待核实。

这版正准备真机试用。[三步真机演练](field-tests/pilot-s0.md)可以直接复制；[实测登记](field-tests/README.md)记录已观察到的设备、版本和结果。

## 豆包工作 / 支持 Agent Skills 的客户端

1. 登录 GitHub，打开最近一次通过的[候选构建](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/check-skill.yml?query=branch%3Acodex%2Fs0-pilot)。在运行摘要的「小豆候选包」下点下载，打开压缩包里的 `xiaodou-skill.zip`。早期构建可在 Artifacts 区下载，过期后可选更新的构建。旧版可在 [Releases](https://github.com/Fangx-AI/awesome-xiaodou/releases) 取得。
2. 解压，保留 `xiaodou-skill` 文件夹及其 `references`。在支持技能导入的客户端选择该技能文件夹，或按客户端要求上传技能。豆包工作的入口在「技能」中的本地导入。
3. 在已启用技能的对话中说「用小豆 Skill 帮我做个减肥计划」，或在技能选择器中选择它。

包内含说明、提示词、出处和九张人物图。不同客户端的导入格式和权限以实际界面为准。本版已检查 ZIP 结构，豆包工作及小豆客户端导入尚未实测。

候选工件附有两份开局纯文本、生活计划整包和 `life-plans/` 下的五个分类复制版。真机演练从 `CANDIDATE.txt` 打开 `pilot`，首页冷读打开 `public_readme`。七天试用可从 `STARTERS.tsv` 选通用开局、计划整包或一个分类的固定版本。

在仓库根目录，用 Python 3.11 或更新版本运行 `python scripts/verify_candidate.py <解开的候选工件目录> --commit <Actions 上显示的完整提交号>`。它核对新候选包的文件校验值、版本和固定链接。历史候选包可在解压目录运行 `sha256sum -c SHA256SUMS` 查看当时登记的校验值。

[豆包工作官方技能说明](https://www.feishu.cn/content/article/7677519271848610746) · [Agent Skills 规范](https://agentskills.io/specification)

[access-feedback]: https://github.com/Fangx-AI/awesome-xiaodou/issues/new?template=app-access.yml
