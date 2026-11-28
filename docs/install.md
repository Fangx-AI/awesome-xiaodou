# 使用小豆 Skill

## 小豆独立 App

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

[豆包工作官方技能说明](https://www.feishu.cn/content/article/7677519271848610746) · [Agent Skills 规范](https://agentskills.io/specification)
