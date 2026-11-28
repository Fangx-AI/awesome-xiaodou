# 使用小豆 Skill

## 小豆独立 App

### 下载和开通

- **iPhone / iPad**　中国区 App Store 列出「小豆 - 豆包旗下 AI 个人助理」，开发者是北京春田知韵科技有限公司，系统要求 iOS 或 iPadOS 15.0 及以上。[App Store](https://apps.apple.com/cn/app/%E5%B0%8F%E8%B1%86-%E8%B1%86%E5%8C%85%E6%97%97%E4%B8%8B-ai-%E4%B8%AA%E4%BA%BA%E5%8A%A9%E7%90%86/id6815582077)
- **Android**　先在手机自带应用商店搜索「小豆」，核对开发者。项目截至 2026 年 11 月 28 日尚未核实安卓商店直链。[小豆官方产品页](https://www.doubao.com/xiaodou/)
- **开通资格**　小豆于 11 月 24 日启动邀请制公测。打开 App 后按界面提示操作，能进入新对话再开始试用。[公测报道](https://www.beijing.gov.cn/fuwu/lqfw/gggs/202611/t20261124_4957049.html)

还进不了新对话？可以[参加首页冷读](field-tests/cold-read.md)，也可以[回报卡在哪一步][access-feedback]。只写设备、入口和页面提示，省略账号和邀请码。

### 发一条消息开局

打开小豆独立 App 的新对话，发送[首页的开局消息](../README.md#一句话在小豆里开始)。有目标可以一起写在消息末尾。之后在同一对话报进度或说出新的约束。

- **一条消息开局**：内含三省六部分工、冲突退回和进展续接的基本规则。
- **[完整版皇帝模式](../prompts/emperor-simulator.md)**：补充五个常见计划的处理方法、外部操作确认和御前问签。
- **整包提示词**：用于一段对话里选择多种场景，按下面的步骤使用。

1. 打开[9 条常用指令](../prompts/xiaodou-quick-pack.txt)或[完整 44 条](../prompts/xiaodou-paste-pack.txt)，点 GitHub 文件工具栏中的复制按钮，或打开 Raw 后全选复制。
2. 在小豆中新开一个对话，粘贴发送选好的提示词包。
3. 在同一个对话里说「开启皇帝模拟器」「帮我做个减肥计划」或「看菜单」。

也可以复制[单条提示词](../skills/xiaodou-skill/references/prompts.md)。一句话和提示词包都通过当前对话使用，小豆独立 App 的原生技能安装入口仍待核实。

这版正准备真机试用。[三步真机演练](field-tests/pilot-s0.md)可以直接复制；[实测登记](field-tests/README.md)记录已观察到的设备、版本和结果。

## 豆包工作 / 支持 Agent Skills 的客户端

1. 登录 GitHub，打开[S0 分支构建记录](https://github.com/Fangx-AI/awesome-xiaodou/actions/workflows/check-skill.yml?query=branch%3Acodex%2Fs0-pilot)，从通过的运行下载候选工件并解出 `xiaodou-skill.zip`。历史稳定版在 [Releases](https://github.com/Fangx-AI/awesome-xiaodou/releases)。
2. 解压，保留 `xiaodou-skill` 文件夹及其 `references`。在支持技能导入的客户端选择该技能文件夹，或按客户端要求上传技能。豆包工作的入口在「技能」中的本地导入。
3. 在已启用技能的对话中说「用小豆 Skill 帮我做个减肥计划」，或在技能选择器中选择它。

包内含说明、提示词、出处和九张人物图。不同客户端的导入格式和权限以实际界面为准。本版已检查 ZIP 结构，豆包工作及小豆客户端导入尚未实测。

候选工件同时附上两份开局纯文本、`CANDIDATE.txt` 和 `SHA256SUMS`。参加同一轮试用时，从 `CANDIDATE.txt` 打开固定版本页面。需要校验下载内容时，可在解开的工件目录运行 `sha256sum -c SHA256SUMS`，或用 PowerShell 的 `Get-FileHash -Algorithm SHA256` 核对文件。

[豆包工作官方技能说明](https://www.feishu.cn/content/article/7677519271848610746) · [Agent Skills 规范](https://agentskills.io/specification)

[access-feedback]: https://github.com/Fangx-AI/awesome-xiaodou/issues/new?title=%5B%E5%B0%8F%E8%B1%86%E5%87%86%E5%85%A5%5D%20&body=%E6%97%A5%E6%9C%9F%EF%BC%9A%0A%E8%AE%BE%E5%A4%87%E7%B3%BB%E7%BB%9F%E4%B8%8E%E7%89%88%E6%9C%AC%EF%BC%9A%0A%E5%B0%9D%E8%AF%95%E7%9A%84%E5%BA%94%E7%94%A8%E5%95%86%E5%BA%97%E6%88%96%E5%AE%98%E6%96%B9%E5%85%A5%E5%8F%A3%EF%BC%9A%0A%E5%8D%A1%E5%9C%A8%E5%93%AA%E4%B8%80%E6%AD%A5%EF%BC%88%E6%89%BE%E4%B8%8D%E5%88%B0%E5%B0%8F%E8%B1%86%20%2F%20%E6%97%A0%E6%B3%95%E5%AE%89%E8%A3%85%20%2F%20%E6%AD%A3%E7%AD%89%E5%BE%85%E5%BC%80%E9%80%9A%20%2F%20%E5%85%B6%E4%BB%96%EF%BC%89%EF%BC%9A%0A%0A%E8%AF%B7%E5%8F%AA%E5%86%99%E5%85%AC%E5%BC%80%E4%BF%A1%E6%81%AF%EF%BC%8C%E9%9A%90%E8%97%8F%E8%B4%A6%E5%8F%B7%E5%92%8C%E9%82%80%E8%AF%B7%E7%A0%81%E3%80%82
