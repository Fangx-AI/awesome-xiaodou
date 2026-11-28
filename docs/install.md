# 使用小豆 Skill

[查看下载、回放和真机使用状态](compatibility.md)

## 小豆独立 App

### 下载和开通

1. **下载小豆独立 App。** 搜「小豆 - 豆包旗下 AI 个人助理」，认准开发者**北京春田知韵科技有限公司**。
   - **iPhone / iPad**　打开中国区 App Store 条目，系统要求 15.0 或更新版本。 [App Store 中国区](https://apps.apple.com/cn/app/%E5%B0%8F%E8%B1%86-%E8%B1%86%E5%8C%85%E6%97%97%E4%B8%8B-ai-%E4%B8%AA%E4%BA%BA%E5%8A%A9%E7%90%86/id6815582077)
   - **Android**　在手机自带的应用商店搜索「小豆」。小米官网已列出该应用，11 月 28 日网页显示部分下载服务维护，可在小米手机的应用商店搜索。 [小米应用商店](https://app.mi.com/details?id=com.larus.doubaom)
2. **打开小豆，按 App 提示登录和开通。** 11 月 24 日公测以邀请制启动。页面显示等待或要求邀请码时，以 App 当前的提示为准。能打开新对话并发消息，就可以使用下方的开局。 [小豆产品页](https://www.doubao.com/xiaodou/) · [首都之窗公测报道](https://www.beijing.gov.cn/fuwu/lqfw/gggs/202611/t20261124_4957049.html)

卡在搜索、安装、登录、开通或发消息时，可以[回报卡住的步骤][access-feedback]。只写手机系统、商店和页面提示，省略账号、邀请链接和邀请码。

### 发一条消息开局

打开小豆新对话，复制[首页的开局消息](../README.md#一句话在小豆里开始)，在末尾加上自己的目标，整段一次发出。

- **[开局纯文本](../prompts/xiaodou-start.txt)**：复制后加上你的目标，发成一条消息。
- **[正式版完整指令](../prompts/emperor-simulator.md)**：包含三省六部分工、进展更新和跨对话续聊摘要。
- **[30 个生活计划](../skills/xiaodou-skill/references/life-plans/README.md)**：在小豆 App 里复制对应分类或计划整包，带上自己的目标发送。
- **整包提示词**：用于一段对话里选择多种场景，按下面的步骤使用。

1. 打开[9 条常用指令](../prompts/xiaodou-quick-pack.txt)或[完整 44 条](../prompts/xiaodou-paste-pack.txt)，点 GitHub 文件工具栏中的复制按钮，或打开 Raw 后全选复制。
2. 在小豆中新开一个对话，粘贴发送选好的提示词包。
3. 在同一个对话里说「开启皇帝模拟器」「帮我做个减肥计划」或「看菜单」。

也可以复制[单条提示词](../skills/xiaodou-skill/references/prompts.md)。一句话和提示词包都通过当前对话使用，小豆独立 App 的原生技能安装入口仍待核实。

## 豆包工作 / 支持 Agent Skills 的客户端

1. 从[候选构建](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/check-skill.yml?query=branch%3Acodex%2Fs0-pilot)下载通过校验的工件，解出含 30 个生活计划的 `xiaodou-skill.zip`。旧版在 [Releases](https://github.com/Fangx-AI/awesome-xiaodou/releases)。
2. 解压，保留 `xiaodou-skill` 文件夹及其 `references`。在支持技能导入的客户端选择该技能文件夹，或按客户端要求上传技能。豆包工作的入口在「技能」中的本地导入。
3. 在已启用技能的对话中说「用小豆 Skill 帮我做个减肥计划」，或在技能选择器中选择它。

包内含说明、提示词、出处和九张人物图。不同客户端的导入格式和权限以实际界面为准。本版已检查 ZIP 结构，豆包工作及小豆客户端导入尚未实测。

[豆包工作官方技能说明](https://www.feishu.cn/content/article/7677519271848610746) · [Agent Skills 规范](https://agentskills.io/specification)

[access-feedback]: https://github.com/Fangx-AI/awesome-xiaodou/issues/new?title=%5B%E5%B0%8F%E8%B1%86%E5%87%86%E5%85%A5%5D%20&body=%E6%89%8B%E6%9C%BA%E4%B8%8E%E7%B3%BB%E7%BB%9F%EF%BC%9A%0A%E4%BD%BF%E7%94%A8%E7%9A%84%E5%BA%94%E7%94%A8%E5%95%86%E5%BA%97%EF%BC%9A%0A%E5%8D%A1%E5%9C%A8%E5%93%AA%E4%B8%80%E6%AD%A5%EF%BC%9A%0A%E9%A1%B5%E9%9D%A2%E6%98%BE%E7%A4%BA%EF%BC%9A%0A
