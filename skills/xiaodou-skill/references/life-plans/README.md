# 小豆的 30 个生活计划

在小豆里说 **「帮我制定一个减肥计划」**、**「我想从零开始跑步」** 或 **「帮我排一下留学申请」**。小豆先问关键情况，再给你能用的计划。说出自己的目标就行。

## 怎么使用

- **小豆 App 聊天**　打开分类页，点 GitHub 的 Raw 或复制正文。和你的目标一起发到小豆的新对话，例如「按下面的流程帮我排个计划」。需要多个分类时，可以用[生活计划整包](https://github.com/Fangx-AI/awesome-xiaodou/blob/main/prompts/xiaodou-life-plans.txt)。
- **支持 Agent Skills 的客户端**　导入包含本目录的小豆 Skill。说自然话就会按目标选择计划。有多个目标时，先确认你要优先推进哪一个。

## 选一个你想做的计划

| 分类 | 可直接使用的计划 |
| --- | --- |
| [健康与运动](health.md) | [减肥与体重管理](health.md#p01--减肥与体重管理) · [新手力量与体能](health.md#p02--新手力量与体能) · [走跑交替](health.md#p03--从走跑交替开始) · [睡眠作息](health.md#p04--睡眠作息整理) · [一周备餐](health.md#p05--一周备餐与购物) · [久坐活动](health.md#p06--久坐活动间歇) |
| [学习与成长](learning.md) | [英语陪练](learning.md#p07--英语真实场景陪练) · [考试复习](learning.md#p08--考试倒排与错题复习) · [阅读理解](learning.md#p09--阅读理解与输出) · [零基础自学](learning.md#p10--零基础自学一项技能) · [留学申请](learning.md#p11--留学申请与选校) · [写作交稿](learning.md#p12--从选题到交稿) |
| [职业与工作](career.md) | [职业探索](career.md#p13--职业方向探索) · [转岗过渡](career.md#p14--转岗过渡与能力补齐) · [求职投递](career.md#p15--求职投递与跟进) · [简历与作品集](career.md#p16--简历与作品集) · [面试备战](career.md#p17--面试备战和模拟) · [项目里程碑](career.md#p18--工作项目里程碑) |
| [财务与生活事务](household.md) | [月度预算](household.md#p19--个人月度预算) · [应急金](household.md#p20--应急金与存钱计划) · [偿还债务](household.md#p21--债务偿还顺序) · [旅行筹备](household.md#p22--旅行筹备与日程) · [搬家倒排](household.md#p23--搬家倒排) · [家务整理](household.md#p24--家务整理与物品去留) |
| [习惯、关系与复盘](habits.md) | [建立习惯](habits.md#p25--建立一个可持续的习惯) · [拖延起步](habits.md#p26--拖延任务的起步) · [减少屏幕干扰](habits.md#p27--降低手机与屏幕干扰) · [重要沟通](habits.md#p28--重要对话与冲突沟通) · [家庭分工](habits.md#p29--家庭分工和交接) · [每周复盘](habits.md#p30--每周回顾与下周安排) |

## 小豆按这套流程办

1. 选一个最接近用户当前目标的计划，只读对应章节。问还缺的、会改变方案的问题。已经给过的信息直接用。只想问眼前一餐或做一件简单事时，直接按当前请求处理。
2. 中书立案，门下核对资料、时间、预算、权限与可行性。健康、财务、政策和入境要求以合适的专业或当地官方来源为准；缺数据就标待核，避免把估计写成已确认。
3. 尚书选用必要的部，并交付本计划规定的成果、第一步、完成标准和复盘时机。设置提醒、发消息、提交、支付等外部操作按现有确认规则执行。
4. 用用户实际回报复盘。条件变了保留已完成，调整受影响的安排。默认用白话，用户要求「展开朝议」时再讲分工与退回。

## 借鉴来源

- **Edict** 提供三省拟案、审议与交办的分工参考。小豆由同一个 Agent 扮演相关角色。 [Edict 流转设计](https://github.com/cft0808/edict/blob/main/docs/task-dispatch-architecture.md)
- **Anthropic Skills** 的分层结构用于按任务加载资料。**Superpowers** 的计划写法用于明确产物和检验步骤。 [Skill Creator](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) · [Writing Plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md)
- **prompts.chat** 提供自然开场的样例，职业方向另参考开源 **Career Skills** 的先核证据再出稿。每个计划的专业依据在自己章节末尾。 [prompts.chat](https://github.com/f/prompts.chat) · [Career Skills](https://github.com/basseko/career-skills)
