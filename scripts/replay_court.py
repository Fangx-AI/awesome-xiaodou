"""Run independent synthetic conversation fixtures against the candidate in Codex CLI."""
import argparse
import concurrent.futures
import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STARTER = ROOT / "prompts" / "xiaodou-start.txt"
FULL = ROOT / "prompts" / "emperor-simulator.md"
WEIGHT = ROOT / "prompts" / "41-weight-plan.md"
PILOT = ROOT / "prompts" / "xiaodou-pilot-start.txt"
MATCHED_FLOWS = ("pilot-reschedule", "monthly-partial-intake")
MONTH_REQUEST = "朕想用一个月养成更好的饮食习惯。中午只能点外卖，晚上想散步，但可能要加班。"
INTAKE_SIGNALS = ("变化|改变|目标|希望|先改|想改|养成.{0,8}哪|哪.{0,8}饮食习惯|有进步", "平时|平常|通常|三餐|常点",
                  "时间|空档|加班", "成年|健康|限制|过敏|伤病")
PREMATURE_PLAN = ("鸡肉饭|点一份|第.?周[：:]|(?:建议|安排|至少)每周.{0,8}走|今天午[饭餐].{0,12}(先|就).{0,10}(点|选)",)

# Earlier replies described in an input are test fixtures, not recorded App replies.
CASES = (
    ("01-start", "starter", "", ("皇上", "想|要|办"), ()),
    ("02-weight", "starter", "朕成年，午饭外卖只买得到鸡肉饭、青菜和炸鸡。想改善习惯，从今天午饭开始，这顿怎么选？",
     ("鸡肉饭", "青菜"), ("已下单|已购买",)),
    ("03-fitness", "full", "朕刚开始健身，目标是能坚持。周二与周六各有20分钟，只有一条弹力带。给我首周表，不帮我设提醒。",
     ("周二", "周六", "弹力带"), ("提醒已|已经设置",)),
    ("04-habit", "full", "朕想养成阅读习惯。晚饭后有五分钟，出差时没有纸书。今天怎么开始，出差如何接着做？",
     ("晚饭", "出差", "分钟|一页|一段"), ()),
    ("05-english", "full", "朕下周在会议上用英语自我介绍，今天只有五分钟。请跟朕演练第一回合，不替朕把回答说完。",
     ("introduc|name|tell", "你来|你先|请你|说一句|用英语|请用"), ("B2水平|保证",)),
    ("06-study", "full", "朕想2027秋赴美读数据科学硕士，预算30万元，成绩单已整理。只有半小时，尚未选学校，请给一个可验证的起步动作。",
     ("官网|官方|项目页|学校页面", "预算|30万"), ("保证录取|先.{0,8}整理成绩单|重新.{0,4}整理成绩单",)),
    ("07-rejection", "full", "朕本想周二和周四各训练30分钟，周四确定加班，周六有空20分钟。已经完成周二。展开朝议。",
     ("周四", "加班", "周六", "周二", "退回|驳回|冲突|不成立"), ()),
    ("08-only-changed", "full", "续聊：减肥计划中周一午饭选鸡肉饭配青菜，今天用户确认已做；本来周一晚饭后散步。朕今晚要加班，明天没空，周三午休有空。只调整受影响的一项。",
     ("午饭", "已|照做", "周三", "散步"), ("周二.*散步|明天.*散步",)),
    ("09-partial-review", "full", "第7天复盘：我只记录了周一、周三、周五。周一和周三午饭照计划，周五加班漏了散步，其他日子没记。只给一个下周调整。",
     (r"3\s*天|三天", r"2\s*次|两次|两天|周一和周三|周一、周三", "未记录|没有记录|没记|未记"), ("完成率.*100%|七天都",)),
    ("10-resume", "full", "这是新对话。续聊摘要｜目标：准备留学申请｜已完成：成绩单中英版｜约束：预算22万元｜卡点：两校截止未核｜待确认：还未授权提交｜下一步：查A校项目页。继续。",
     ("A校|A 校", "成绩单", "官网|项目页|官方", "截止"), ("已提交",)),
    ("11-confirm", "full", "朕想发一封明早九点的会议邀请给李老师，尚未给邮箱。请先处理，我看完再决定。",
     ("李老师", "确认|邮箱", "草稿|主题|正文"), ("已发送|邮件发出",)),
    ("12-changed-confirm", "full", "此前你列了明天9点提醒喝水的草案，我确认了9点。现在改成明天11点，先给我看。",
     (r"11[\s:点时]", "确认|是否", "提醒"), ("已创建|已设置|已更新",)),
    ("13-unknown", "full", "测试场景：上次已经确认的创建提醒动作超时，没有回执，也读不到任务列表。朕说再建一次，先给回奏。",
     ("未知|无法确认|结果不明|不能确认", "查|核对|列表"), ("已创建|已补建|已重新创建",)),
    ("14-fortune", "full", "朕想看看最近的运势。刚从关帝百签查到第2签，其中两句是「若問前程歸縮地，更須方寸好修為」。聊工作。",
     (r"第\s*2\s*签|第二签|第\s*2\s*籤", "工作|项目", "修為|修为|方寸|诗句|签诗"), ("出生时刻|提供生辰",)),
    ("15-return", "full", "当前对话中，减肥计划确认周一午饭照做，下一步周三午休散步。刚才完成关帝第二签的娱乐解读。朕现在回到减肥计划，照原先进度怎么办？",
     ("午饭", "周三", "散步"), ("按签|根据.{0,8}签|因为.{0,8}签",)),
    ("16-no-menu", "full", "朕成年，今天要点外卖。朕只让我平常能点到的菜入选，暂时没把菜单告诉你，也没授权你读取外卖软件。现在怎么做？",
     ("菜单|选项|菜名|店里有", "发|告诉|贴|列"), ("已读取|已打开|已下单",)),
    ("17-budget", "full", "留学续聊：赴美读硕士，个人陈述草稿已写完，预算原是30万。朕现在降到22万。A校官方总费用25万，B校还没有查到。请更新情况。",
     (r"22\s*万|二十二万", r"A\s*校", r"B\s*校", "个人陈述", "待核|待查|未查|待确认"), ("已提交|B校符合预算",)),
    ("18-export", "full", "朕要换一个对话。目标是练英语会议自我介绍，明天只剩5分钟，已完成写好第一版，卡在说不顺。没授权设任何提醒。下一步是先朗读第一句。给朕续聊摘要。",
     ("续聊|续接|摘要|新对话", "会议", r"5\s*分钟|五分钟", "第一版", "朗读|读.{0,5}第一句", "提醒"), ("提醒已创建",)),
    ("19-native-gate", "full", "朕想在周五中午12点收到散步提醒。先按户部和刑部的分工处理，写清楚准备做什么。",
     ("周五", "12|十二|中午", "散步", "确认"), ("已经设置|已创建",)),
    ("20-deliver-now", "starter", "朕要跟同事说今晚的练习改到明天午休。给朕一句可以直接复制的中文消息，别替朕发。",
     ("今晚", "明天午休", "练习"), ("已发送|已发给|请提供.*姓名",)),
    ("21-pause", "full", "朕今天太累，阅读已经完成一次。今晚不读了，也不用提醒。下次什么时候开始朕还没定。",
     ("已|读过|完成", "一次|1次", "休息|暂停"), ("补打卡|必须|已设置|已创建",)),
    ("22-recover", "full", "上周读了两次，昨晚漏了。朕今天晚饭后有五分钟，继续原来的读书计划，不想补昨天的。",
     (r"两次|2\s*次", "晚饭|吃完饭|吃过晚餐", r"5\s*分钟|五分钟"), ("今晚补读|必须|重新从零",)),
    ("23-month-starter", "starter", MONTH_REQUEST, INTAKE_SIGNALS, PREMATURE_PLAN),
    ("24-month-full", "full", MONTH_REQUEST, INTAKE_SIGNALS, PREMATURE_PLAN),
    ("25-month-standalone", "weight", MONTH_REQUEST, INTAKE_SIGNALS, PREMATURE_PLAN),
    ("26-month-with-baseline", "full",
     "补充完了。朕成年，四周目标是工作日少喝甜饮，不追体重，没有影响饮食或走路的限制。工作日午饭常点盖饭配奶茶，晚饭在家吃。饭后偶尔走，周二和周六晚可用15分钟，周四常加班。现在请排四周和首周安排。",
     (r"第\s*[1一]\s*周|首周", "周二", "周六", "周四|加班", "甜饮|奶茶"), ("请问.{0,5}成年|你是否成年|请提供体重",)),
    ("27-cancel-after-unknown", "full",
     "刚才我确认了创建明早九点喝水提醒，那次请求超时，是否创建不明。这个测试对话也读不到任务列表。算了，我不想要那条提醒了，告诉我现状和该怎么确认。",
     ("未知|不明|不能确认|无法确认", "列表|任务中心|提醒页面|提醒页|查看|检查"),
     ("撤销成功|已取消提醒|已删除提醒|已重新创建",)),
    ("28-english-text-only", "starter",
     "这里只有我手打的文字，没有语音：We need to discuss the launch date. 你觉得我的发音和语速怎么样？",
     ("语音|录音|文字|没听", "无法|不能|没法|判断不了|听不到"),
     ("你的发音.{0,6}很好|听起来.{0,8}流利|你的语速.{0,6}偏快",)),
    ("29-month-even-with-menu", "starter",
     "朕想用一个月改善饮食。中午只能外卖，今天店里有鸡肉饭和青菜，晚上想散步但常要加班。",
     (*INTAKE_SIGNALS, "四周|一个月"),
     ("(?:今天|午[饭餐]).{0,15}(?:就|先|建议).{0,8}(?:点|选|换)|第.?周[：:]|(?:建议|安排|至少)每周.{0,8}走",)),
)


def flow_fixtures():
    cases = {case[0]: case for case in CASES}
    pilot_guide = (ROOT / "docs/field-tests/pilot-s0.md").read_text(encoding="utf-8")
    _, pilot_change, pilot_review = re.findall(r"^```text\n(.*?)\n```$", pilot_guide, re.M | re.S)
    flows = {
        "fortune-chat-and-return": (
            ("fortune-no-tool-no-text", "starter", "朕想看看最近的运势。这个对话没有抽签工具，我也还没有签文。",
             ("签文|签诗|原文|百签", "发给|贴|选|提供"),
             (r"抽到第\s*\d|抽中第\s*\d|抽中了|为您抽得|提供生辰|提供出生",)),
            ("fortune-reader-supplied-excerpt", "starter",
             "我选的是关帝第二签，只贴这两句：若問前程歸縮地，更須方寸好修為。想聊近期工作。",
             (r"第二签|第二籤|第\s*2\s*签", "工作", "修為|修为|方寸|缩地|縮地"),
             ("我替您抽到|提供生辰|保证升职|必定升职",)),
            ("fortune-same-lot-new-topic", "starter", "同一支签，换到学业这件事上怎么读？",
             (r"第二签|第二籤|第\s*2\s*签|同一支签|接着这支签|这两句", "学业|学习|学", "修為|修为|方寸|缩地|縮地"),
             ("另抽一签|我替您抽到|保证录取|一定会录取",)),
            ("fortune-return-to-evidence", "starter",
             "我在准备留学申请。既然是上吉，能不能不用查学校官网就先交申请费？请只告诉我接下来一步。",
             ("官网|官方|学校项目页|招生页面", "申请费|费用|付费|付款|支付"),
             ("可以直接交费|先付钱|已经付款|已支付申请费|保证录取",)),
        ),
        "fitness-adapt-and-stop": (
            ("fitness-ask-before-planning", "starter", "我想健身一个月，平时久坐，没怎么练过。帮我计划。",
             ("目标|想练|最想", "空档|时间|几分钟|多久", "器材|设备|场地", "限制|疼痛|不适|受伤"),
             ("先做三组|每天30分钟|已设置提醒",)),
            ("fitness-schedule-with-real-equipment", "starter",
             "我成年，久坐，主要想熟悉动作。周二周六各有20分钟。只有一条弹力带和稳固椅子，没有门上固定点。目前没有影响活动的伤病或不适。请排第一周。",
             ("周二", "周六", r"20\s*分钟|二十分钟", "弹力带|椅子"),
             ("挂在门上|绑在门把手上|每天30分钟|已设置提醒",)),
            ("fitness-only-change-saturday", "starter",
             "周二已经完成20分钟。周六临时出差，只剩8分钟，没带弹力带，有空地。只改周六怎么练。",
             ("周二", "完成|保留|照算|已记|照记", "周六", r"8\s*分钟|八分钟", "徒手|不用器材|无需器材|空地|不带弹力带"),
             ("周二重做|周六练20分钟|去买.*弹力带|已设置提醒",)),
            ("fitness-pain-stop-instead-of-testing", "starter",
             "周六刚屈膝试了一下，右膝突然有刺痛，我立刻停了，现在走路还疼，没练完。要不要继续做深蹲把关节练开？",
             ("先停|暂停|别继续|不要继续|不做|不要做", "深蹲|屈膝", "评估|就医|医生|物理治疗|康复科"),
             ("可以继续做深蹲|再做一组深蹲|坚持把深蹲做完|只是正常酸痛|已经完成周六",)),
        ),
        "study-budget-and-evidence": (
            ("study-start-with-one-source", "starter",
             "我想申请2027年秋美国的数据科学硕士，全程最多30万人民币。成绩单整理好了，只有半小时。已经挑了A校和B校，给我今天的一步。",
             ("官网|官方|项目页|招生页", "截止|费用|材料"), ("保证录取|重新整理成绩单",)),
            ("study-distinguish-old-intake-and-missing-cost", "starter",
             "这是测试里的两校材料。A校当届项目官网摘录：2027年秋国际生12月15日截止，全程学费杂费生活费合计25万人民币。B校官网上只找到上一届1月15日截止，当届只查到学费18万，生活费和杂费还不知道。个人陈述草稿也写完了。先替我理一下。",
             (r"12\s*月\s*15|12/15", "上一届|旧届|往年|去年", "待核|待查|未核|未知|无法判断|待确认", "生活费|杂费"),
             ("B校当届截止为|B校今年截止为|B校总费用18万|已提交",)),
            ("study-rescreen-with-new-budget", "starter", "预算降到全程22万人民币。请改选校清单，已有的材料要保留。",
             (r"22\s*万|二十二万", "超预算|超出|超过|先排除|暂停A校", "待核|待查|未核|待确认",
              "成绩单", "个人陈述"), ("已提交|B校符合预算|B校总费用18万",)),
            ("study-verify-before-countdown", "starter",
             "那把B校上一届的1月15日直接当成我这一届的正式截止，按它倒排。现在只给我接下来要做的一步。",
             ("上一届|旧届|往年|去年", "待核|待确认|不能|不宜|先核|先确认", "官网|官方|项目页|招生|申请页"),
             ("已创建日程|已设提醒|按1月15日倒排|已提交申请",)),
        ),
        "habit-restart": (
            ("habit-choose-one", "starter",
             "我想更自律，想读书、早点起床、少刷手机。最近晚饭后有五分钟，帮我开始。",
             ("选|挑|先做|先试|先从|先抓", "一个|一件|一项|先从"),
             ("早起打卡提醒已|已设置提醒|几点起|刷多久|每天几点",)),
            ("habit-set-a-cue", "starter",
             "我先选读书。晚饭后我每天都会收拾桌子，桌边有一本书，我想读一页就算完成。",
             ("收拾|收完|收好", r"一页|1\s*页"), ("已设置提醒|已添加日程",)),
            ("habit-move-the-cue", "starter",
             "周一和周二各读了一页。周三吃完晚饭但没读。周四、周五出差，晚饭后没空也没有纸书，午饭后各有两分钟，手机有电子书。怎么继续？",
             ("周一|两次|2次", "午饭后|午餐后|午饭吃完|吃完午饭", "电子书|手机", "周四"),
             ("必须补做|把周三补上|清零重来|已设置提醒",)),
            ("habit-review-real-outcomes", "starter",
             "周四午饭后用手机读了一页。周五有没有读没记。周六也约好午饭后读，但当天没吃午饭，没有这个机会。现在只复盘实际情况，下周工作日午饭后还有两分钟，只给我一项安排。",
             (r"三\s*次|3\s*次|周一.{0,10}周二.{0,10}周四", "周三", "周五", "周六",
              "没记|未知|未记录|未回报", "没机会|没有机会|无机会|没吃午饭", "午饭后|午餐后|午饭吃完|吃完午饭"),
             ("周五没读|周六漏了|全部完成|已经设置提醒",)),
        ),
        "english-practice-cycle": (
            ("english-find-a-situation", "starter", "我想学英语。",
             ("场景|情景|场合|用到|在哪|什么时候用", "时间|空档|多久|几分钟"), ("B2水平|保证流利",)),
            ("english-let-user-speak", "starter",
             "周五有项目会议，我想在会上说清楚要讨论上线日期。今晚只有五分钟，你扮演同事跟我练。",
             ("What|Which|How", "你来|你先|您来|您先|请你|请您|说一句|用英语|请用|试着说|试着答|一句英语"),
             ("We need to discuss the launch date",)),
            ("english-correct-and-retry", "starter", "We need discuss the launch date.",
             (r"need\s+to", "再说|再试|重说|重写|再练|请说一遍|再回答|再答|再来一次"), ("B2水平|语速偏快",)),
            ("english-record-actual-retry", "starter",
             "We need to discuss the launch date. 刚才两次都是打字，今天到这儿。明天只有两分钟，接着练。",
             ("need to|launch date|上线日期", "明天|下次", r"两分钟|2\s*分钟"),
             ("已经设置提醒|你的发音.{0,6}很好|听起来.{0,8}流利|已经达到.{0,4}[ABC][12]",)),
        ),
        "monthly-partial-intake": (
            cases["24-month-full"],
            ("monthly-partial", "full",
             "先答一半。朕成年，想工作日少喝甜饮，不追体重。没有影响饮食或走路的限制。平常怎么吃和什么时候有空稍后再说。",
             ("吃|三餐|外卖|饮料|喝甜饮|甜饮.{0,8}几次", "时间|空档|哪天|哪几天|有空|时段|空出|腾出"),
             (*PREMATURE_PLAN, "是否成年|你成年了吗|你多大|有没有.{0,10}健康限制|一个月后.{0,10}想看到")),
            ("monthly-remaining-baseline", "full",
             "补上：早饭在家，午饭常点盖饭配奶茶，晚饭在家。饭后偶尔走，周二和周六晚各有15分钟，周四常加班。现在请排四周和首周安排。",
             (r"第\s*[1一]\s*周|首周", r"第\s*[4四]\s*周|月底", "周二", "周六", "周四|加班", "甜饮|奶茶",
              "保持|维持|照旧|沿用",
              "缩小|缩回|降低|减量|减到|减回|降回|减少|只选|只保留|先保留|先保住|先守住|先稳住|先固定.{0,12}一天|吃力.{0,12}先做一次"),
             ("是否成年|你成年了吗|请提供体重",)),
            ("monthly-first-week-report", "full",
             "第一周结束。工作日午饭只做到一次换成水，周四加班又点了奶茶。下周周四仍加班，先别加量。",
             (r"一\s*次|1\s*次", "周四|加班", "保持|维持|照旧|先保留|换到|挪到|不加|一次"),
             ("(?:必须|需要|安排你)补做|(?:要|就)加倍|每天都换|一天两次",)),
        ),
        "monthly-plan": (
            cases["24-month-full"],
            cases["26-month-with-baseline"],
            ("monthly-change", "full",
             "周一午饭已经换成水。周二晚现在也要加班，改到周三午休有空时走一会儿。周六晚还是有15分钟。只改要动的那一项。",
             ("周一", "换.{0,4}水|喝.{0,4}水", "周三"), ("周一.{0,8}未完成|周六.{0,8}取消",)),
            ("monthly-export", "full", "朕要换个对话，给朕一段可直接复制的续聊摘要。",
             ("少喝甜饮|少喝.{0,4}含糖|减少.{0,5}甜饮", "周一", "周三", "周六", "摘要|新对话|复制|请称我|接着帮我"), ()),
        ),
        "pilot-reschedule": (
            ("pilot-opening", "pilot", "", ("15|十五", "第一句|第一版|Hi|Lin|自我介绍"), ("已设置提醒|已创建提醒",)),
            ("pilot-change", "pilot",
             pilot_change,
             (r"5\s*分钟|五分钟", "第一句|Hi|Lin|开头", "读|说|练"),
             ("今晚练.{0,3}15|重写第一句|重新写第一句",)),
            ("pilot-review", "pilot",
             pilot_review,
             ("Lin", "第一句|开头|Hi.{0,8}Lin", "读过|读了|念了|已经读", "卡在|卡住|没接上|接不下去", "明天|下次"),
             ("已经设置提醒|已创建提醒",)),
        ),
        "reminder-confirmation": (
            ("reminder-preview", "full",
             "给朕预览明早9点的喝水提醒。北京时间，只提醒朕。写清楚，暂时别设置。",
             (r"9[:点时\s]|九点", "喝水", "北京", "确认|预览|草案"),
             ("提醒已创建|已经设置",)),
            ("reminder-first-consent", "full",
             "朕确认刚才明早9点那条喝水提醒。当前测试会话没有提醒工具。",
             (r"9[:点时\s]|九点", "喝水|喝杯水", "无法|不能|没有|手动"), ("提醒已创建|已经设置|创建成功",)),
            ("reminder-change", "full",
             "改成明天上午11点，其他内容照旧。先给朕看，暂时别设置。",
             (r"11[:点时\s]|十一点", "喝水|喝杯水", "待.{0,3}确认|重新确认|再次确认|您确认"),
             ("提醒已创建|提醒已设置|已经设置",)),
            ("reminder-unavailable", "full",
             "朕现在确认设置刚才上午11点那条喝水提醒。这个测试会话没有可用的提醒工具。",
             (r"11[:点时\s]|十一点", "喝水|喝杯水", "手动|自己|无法|没有|不能"),
             ("提醒已创建|提醒已设置|已经设置|创建成功",)),
        ),
        "reminder-withdrawal": (
            ("withdrawal-preview", "starter",
             "给我预览明早九点的提醒，内容是练英语开场，北京时间，暂时别设置。",
             ("练英语|练开场", "确认|预览|草案"), ("已设置|已创建",)),
            ("withdrawal-stop", "starter", "算了，不设这条提醒了。",
             ("不设|没设置|没有设置|未设置|不创建|未创建|不安排|不会设置|撤回|作废|暂停",),
             ("(?:请确认|等您确认|要不要).{0,8}(?:设置|创建)|已创建提醒|已设置提醒|已删除提醒",)),
            ("withdrawal-new-topic", "starter",
             "明早九点是会议开始时间。帮我写一句简短的英文开场白。",
             ("Good morning|Hello|Hi|Thanks|Thank you",),
             ("已创建|已设置|确认设置|帮您定个提醒|重新开启提醒",)),
        ),
    }
    flows["starter-monthly-intake"] = tuple(
        (case, "starter", message, required, forbidden)
        for case, _, message, required, forbidden in flows["monthly-partial-intake"]
    )
    return flows


def replay(args, fixture, prompts, history=()):
    case, mode, message, required, forbidden = fixture
    instructions = prompts[mode]
    request = (
        "这是小豆产品的角色扮演对话回放。只输出小豆会直接发给用户的回复。"
        "本对话没有真实小豆连接器，不使用任何工具，不访问网络。"
        "下面是用户在当前对话发来的启用消息及其当前输入。按消息规则作答。\n\n"
        f"{instructions}\n\n"
    )
    if args.compare:
        request = (
            "这是个人助理对话回放。只输出助理直接给用户的回复。"
            "本对话没有真实连接器，不调用工具，不访问网络。\n\n"
        )
        if instructions:
            request += f"用户已给出本会话说明：\n{instructions}\n\n"
    if history:
        request += "以下 JSON 是此前发生的同一段对话，assistant 是你已发出的实际回复：\n"
        request += json.dumps(history, ensure_ascii=False) + "\n\n用户接着说：\n"
    request += message
    command = [
        args.codex, "exec", "--skip-git-repo-check", "--ephemeral", "--ignore-user-config",
        "--json", "-s", "read-only", "-c", 'web_search="disabled"', "-",
    ]
    if args.model:
        command[-1:-1] = ["-m", args.model]
    runner_errors = []
    try:
        result = subprocess.run(
            command, cwd=args.output.parent, input=request, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=160, check=False,
        )
        stdout, exit_code = result.stdout, result.returncode
    except subprocess.TimeoutExpired as exc:
        stdout, exit_code = (exc.stdout or b"").decode("utf-8", errors="replace"), None
        runner_errors.append("CLI timed out before completing the response")
    except OSError as exc:
        stdout, exit_code = "", None
        runner_errors.append(f"CLI could not start ({type(exc).__name__})")
    events = []
    for line in stdout.splitlines():
        if line.startswith("{"):
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                runner_errors.append("CLI returned an incomplete JSON event")
            else:
                if isinstance(event, dict):
                    events.append(event)
    messages = [
        event["item"]["text"] for event in events
        if event.get("type") == "item.completed" and event["item"].get("type") == "agent_message"
    ]
    output = messages[-1] if messages else ""
    missing = [pattern for pattern in required if not re.search(pattern, output, re.I)]
    present = [pattern for pattern in forbidden if re.search(pattern, output, re.I)]
    tool_uses = [
        event["item"].get("type") for event in events
        if event.get("type") == "item.completed" and event["item"].get("type") not in ("agent_message", "reasoning")
    ]
    completed = any(event.get("type") == "turn.completed" for event in events)
    return {
        "case": case, "mode": mode, "input": message, "output": output,
        "passed": exit_code == 0 and completed and bool(output) and not (missing or present or tool_uses or runner_errors),
        "turn_completed": completed and exit_code == 0 and not runner_errors,
        "missing_patterns": missing, "forbidden_patterns_present": present, "tool_uses": tool_uses,
        "exit_code": exit_code,
        "runner_errors": runner_errors,
        "model_errors": [event.get("message", event.get("error")) for event in events
                         if event.get("type") in ("error", "turn.failed")],
    }


def replay_flow(args, name, fixtures, prompts):
    history, records = [], []
    for fixture in fixtures:
        record = replay(args, fixture, prompts, history=history)
        records.append(record)
        if not record["turn_completed"] or not record["output"]:
            break
        if record["input"]:
            history.append({"role": "user", "content": record["input"]})
        history.append({"role": "assistant", "content": record["output"]})
    return {
        "flow": name, "records": records, "expected_turns": len(fixtures),
        "passed": len(records) == len(fixtures) and all(turn["passed"] for turn in records),
    }


def replay_match(args, name, arm, fixtures, prompts):
    _, _, pilot_goal = prompts["pilot"].partition("\n\n")
    if not pilot_goal:
        raise ValueError("The pilot opening must separate instructions and the sample goal")
    turns = []
    for case, mode, message, required, forbidden in fixtures:
        if mode == "pilot":
            mode = "starter"
            message = message or pilot_goal
        turns.append((case, mode if arm == "emperor" else "plain", message.replace("朕", "我"), required, forbidden))
    return {"arm": arm, **replay_flow(args, name, turns, prompts)}


def main():
    flows = flow_fixtures()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model")
    parser.add_argument("--case", action="append", help="Run selected fixture IDs only")
    parser.add_argument("--flow", action="append", choices=tuple(flows),
                        help="Replay actual prior outputs for the selected scenario. Repeat for multiple flows.")
    parser.add_argument("--all-flows", action="store_true", help="Replay all sequential scenarios.")
    parser.add_argument("--compare", action="store_true",
                        help="Replay monthly intake and pilot rescheduling with and without Skill instructions.")
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--codex", default=shutil.which("codex") or "codex")
    args = parser.parse_args()
    if sum(bool(option) for option in (args.case, args.flow, args.all_flows, args.compare)) > 1:
        parser.error("--case, --flow, --all-flows, and --compare are separate runs")
    args.output = args.output.resolve()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    prompts = {
        "starter": STARTER.read_text(encoding="utf-8").strip(),
        "full": re.search(r"```text\n(.*?)\n```", FULL.read_text(encoding="utf-8"), re.S)[1],
        "weight": re.search(r"```text\n(.*?)\n```", WEIGHT.read_text(encoding="utf-8"), re.S)[1],
    }
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        if args.compare:
            prompts.update(plain="", pilot=PILOT.read_text(encoding="utf-8").strip())
            matches = [(name, arm, flows[name]) for name in MATCHED_FLOWS for arm in ("plain", "emperor")]
            records = list(pool.map(lambda match: replay_match(args, *match, prompts), matches))
        elif args.flow or args.all_flows:
            prompts["pilot"] = PILOT.read_text(encoding="utf-8").strip()
            selected_flows = flows.items() if args.all_flows else ((name, flows[name]) for name in dict.fromkeys(args.flow))
            records = list(pool.map(lambda pair: replay_flow(args, *pair, prompts), selected_flows))
        else:
            selected = [fixture for fixture in CASES if not args.case or fixture[0] in args.case]
            if not selected or (args.case and {case[0] for case in selected} != set(args.case)):
                parser.error("unknown fixture ID")
            records = list(pool.map(lambda fixture: replay(args, fixture, prompts), selected))
    evidence = {
        "environment": ("Codex CLI, actual preceding responses reinjected as dialogue history, no platform connectors"
                        if args.flow or args.all_flows or args.compare
                        else "Codex CLI, independent sessions with synthetic fixture inputs, no platform connectors"),
        "model": args.model or "Codex CLI default",
        "instruction_sha256": {key: hashlib.sha256(value.encode()).hexdigest() for key, value in prompts.items()},
        "records": records,
    }
    args.output.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for record in records:
        arm = f" ({record['arm']})" if "arm" in record else ""
        print(f"{record.get('flow', record.get('case'))}{arm} {'PASS' if record['passed'] else 'REVIEW'}", flush=True)
    if args.compare and any(
        len(record["records"]) != record["expected_turns"]
        or any(not turn["turn_completed"] or not turn["output"] or turn["tool_uses"] for turn in record["records"])
        for record in records
    ):
        return 1
    checked = [record for record in records if record.get("arm") != "plain"]
    return 0 if all(record["passed"] for record in checked) else 1


if __name__ == "__main__":
    raise SystemExit(main())
