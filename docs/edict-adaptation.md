# 小豆皇帝模拟器如何借鉴 Edict

对照 [Edict 原仓](https://github.com/cft0808/edict) 的代码快照 [14a2075](https://github.com/cft0808/edict/blob/14a207557719c046af0f993a7bff1cc5a5015b33/README.md)。Edict 在 OpenClaw 中配置独立 Agent、状态和看板。小豆版用一个对话做轻量的分流和任务跟进，进度以对话里实际可见的信息为准。

| Edict 的做法 | 小豆如何使用 |
| --- | --- |
| [入口分流](https://github.com/cft0808/edict/blob/14a207557719c046af0f993a7bff1cc5a5015b33/agents/taizi/SOUL.md) | 由小豆直接判断来意。闲聊直接回，简单任务当场做，多步骤目标才拟案。 |
| [中书拟案与续接](https://github.com/cft0808/edict/blob/14a207557719c046af0f993a7bff1cc5a5015b33/agents/zhongshu/SOUL.md) | 确定目标和完成标准。同一件事改时间或预算时，保留已完成的部分。 |
| [门下审议](https://github.com/cft0808/edict/blob/14a207557719c046af0f993a7bff1cc5a5015b33/agents/menxia/SOUL.md) | 检查时间、预算、资料与权限。能直接修正就修一轮，有实质取舍才问皇上。 |
| [尚书派发、汇总与回奏](https://github.com/cft0808/edict/blob/14a207557719c046af0f993a7bff1cc5a5015b33/agents/shangshu/SOUL.md) | 用户看到一份结果，区分交付物、下一步和待确认事项。发消息、付款等按实际回执报状态。 |

例如「这顿外卖怎么点」只给当前一餐的建议。「给朕排四周」才按作息拟计划并核对每周空档。「这周加班，只剩周日半小时」会保留目标与已有进展，调整受影响的安排。 [复制皇帝模拟器](../prompts/emperor-simulator.md) · [查看可复跑场景](prompt-quality.md)
