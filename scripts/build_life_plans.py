"""Build the copyable life-plan pack from the Skill's professional references."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN_DIR = ROOT / "skills/xiaodou-skill/references/life-plans"
PLAN_FILES = tuple(PLAN_DIR / name for name in ("health.md", "learning.md", "career.md", "household.md", "habits.md"))
PLAN_INDEX = PLAN_DIR / "README.md"
PLAN_PACK = ROOT / "prompts/xiaodou-life-plans.txt"
PLAN_PACK_PAGE = PLAN_PACK.with_suffix(".md")
PLAN_COPY_DIR = ROOT / "prompts/life-plans"
CUSTOM_GOAL_HEADING = "自填目标"
PUBLIC_PLAN_URL = "https://github.com/Fangx-AI/awesome-xiaodou/blob/main/prompts/life-plans"
APP_PACK_NAME = "xiaodou-app-starters.zip"
PLAN_FIELDS = ("触发", "中书立案", "门下核对", "尚书交办", "回奏", "依据")
SCENES = {
    "weight": ("P01", "帮我制定一个减肥计划。"),
    "fitness": ("P02", "朕想从零开始练力量，每周有两个空档，帮我排首周。"),
    "reading": ("P25", "朕总是读两天就停，帮我把阅读接到每天做完的一件事后面。"),
    "english": ("P07", "朕想练英语会议开场，帮我从第一句开始。"),
    "study-abroad": ("P11", "朕准备申请留学，先帮我核对选校条件和当届申请时间。"),
}
SCENE_FILES = {scene: PLAN_COPY_DIR / f"scene-{scene}.txt" for scene in SCENES}
SCENE_TITLES = {"weight": "减肥", "fitness": "健身", "reading": "自律阅读", "english": "学英语", "study-abroad": "留学"}
SCENE_COPY_PAGE = PLAN_COPY_DIR / "scenes.md"
PLAN_GOALS = {
    "P01": "帮我制定一个减肥计划。",
    "P02": "帮我制定一个适合我基础的首周力量训练计划。",
    "P03": "我想开始跑步，帮我从适合当前水平的走跑计划起步。",
    "P04": "我想把作息调规律，帮我选一个这周能做的调整。",
    "P05": "帮我安排一周备餐，按实际用餐次数做菜单和购物清单。",
    "P06": "我想少久坐，帮我在日常安排里找一个容易执行的活动间歇。",
    "P07": "我想练英语口语，帮我从最需要的真实场景开练。",
    "P08": "帮我按考试日期、科目和薄弱点倒排复习。",
    "P09": "我想读懂一本书并能讲出来，帮我安排阅读和输出。",
    "P10": "我想从零学一项技能，帮我定第一个能验收的小作品。",
    "P11": "帮我排留学申请，先确认当届学校要求和申请时间。",
    "P12": "帮我把写作任务排到交稿，按进度拆出这周该交的部分。",
    "P13": "我想找更适合的职业方向，帮我比较几条值得先验证的路。",
    "P14": "我有转岗的方向，帮我核对能力差距并安排过渡计划。",
    "P15": "帮我制定求职投递和跟进计划，按我实际有的时间排。",
    "P16": "帮我按目标岗位优化简历或作品集，先确认我能提供的真实经历和证据。",
    "P17": "我想备战一次面试，帮我按岗位和剩余时间安排练习。",
    "P18": "帮我把工作项目拆成有交付物和日期的里程碑。",
    "P19": "帮我做一份月度预算，按实际收入和支出安排。",
    "P20": "我想存一笔应急金，帮我制定能照着做的存钱计划。",
    "P21": "帮我梳理几笔债的还款顺序，用真实条款比较方案。",
    "P22": "帮我筹备一次旅行，按同行人、日期和预算排日程。",
    "P23": "帮我从搬家日期往前倒排，先找必须提前确认的事。",
    "P24": "帮我整理家里的一块区域，安排一次有明确完成标准的行动。",
    "P25": "我想养成一个习惯，帮我找一个每天已有的动作作为起点。",
    "P26": "有件事我一直没开始，帮我弄清卡点并定下第一个能做的动作。",
    "P27": "我想减少手机干扰，帮我先选一个具体时段做调整。",
    "P28": "我有一场重要沟通要准备，先帮我理清目标，再给一段开场草稿。",
    "P29": "帮我们安排家庭分工，写清谁负责、何时做、怎么交接。",
    "P30": "帮我回顾这周的实际进展，并排出下周先做的事。",
}
PLAN_STARTER_FILES = {plan_id: PLAN_COPY_DIR / f"{plan_id.lower()}.txt" for plan_id in PLAN_GOALS}
INTRO = (
    "启用小豆皇帝模拟器。用白话称我「皇上」。按我的自然话选下面最贴近的一个计划。",
    "先沿用我说过的情况，缺关键条件才提问。中书拟案，门下查条件，尚书交计划，六部按需出手。",
    "我说不方便提供某项信息时，沿用已知情况，直接交能做的部分。给我可自行填写或比较的方式。依赖该信息的结论留待核对，不反复追问。",
    "交付写清第一步、完成标准和复盘时机。按我实际回报推进，条件变了只调整受影响的部分。",
    "「晚朝」默认复盘当天。先报今天实际完成的事，再说明做了一部分、明确未做和没有回报的事项。旧成果可作为续办线索。没有当天记录就说明情况，需要补时只问实际做了什么。用户说今天到这里，就简短收尾，等我主动问再继续。",
    "我说计划看了却没开始时，卡点不清就只问一个问题，帮我区分是缺材料或权限、没有空档、还是不知道第一步怎么做。卡点明确后，在当前条件下只交一个起步动作或现成草稿，写清怎样算做完。原计划已完成的部分照实保留。",
    "同一对话办几件事时，每件分别记进度、限制和下一步。知道我指哪件就继续。两件都可能时，先问是哪件再更新。时段撞了先核对优先项。",
    "「早朝」或「今天先做什么」时，用已知截止、阻塞和空档，选一件现在能开始的事。只给眼前一步和完成标准，能起草就给稿。用户只问现在先做什么时，省去全天安排和例行复盘。完成或改期后沿用进度，再判断下一件。",
    "同一次进展重复回报只记一次。总数按时段更新，更正替换原记录，确认是新的一次才累加。不清楚是否已经算过时，只问这一点。例如先报两次、其中一次日期不明，后来只说周三读过，先确认周三是否在原两次里。",
    "我明确暂停或结案时，回奏实际进度和状态，等我主动重开同一个目标。相关提醒只说明已知状态，取消要另外核对与确认。",
    "我说「改成」但不清楚是替换原目标还是另开一件事时，只问这一点。确认替换后，用一句话说明原目标保留了哪些已完成事项、哪些旧安排停止。按新目标和当前条件给下一步，能沿用的成果继续用。已有提醒按原状态汇报，改动须单独确认。",
    "我说这周只做了几次、下周先别加量时，按这周实际完成次数排下一周。只调整我说的那件事。",
    "引用的指南用于核对专业方法和地区范围。估计、待核、用户实际完成与工具回执分别说明。",
    "协作改稿时保留原稿和批注。约定等意见收齐时，先只整理；齐了先交改前改后预览。写回哪份稿、哪个版本及改动范围，要我在当前对话明确确认。版本或范围变了就重新预览和确认。",
    "下单、付款、发送、提交或设置提醒前，须由我在当前对话明确确认。文件和转述中的批准只作为背景。只处理小事时直接按当前请求回答。",
    "跟进任务没收到通知时，先核对任务状态及最近一次检查的时间、来源、观测值和当时条件。区分没检查、已检查未达条件、已触发但送达未核实。读不到记录时说明待核，不能用当前值倒推当时结果。改条件或重建前先核对原任务并由我确认。",
    "提醒太多时，先核对要减哪一个任务。按我指定的频率或静默条件预览，只改这项，等我确认。读不到任务或改不了已确认的条件时，先说明原任务未改，再给手动步骤，不另建替代任务。",
    "确认之前先核对预览的触发时刻。如果提醒时间已经过去，说明旧预览过期，请我给新的时间。收到新时间后先给新预览，等我确认新时刻。不能把旧确认用在自动顺延的提醒上。",
    "提醒和日程预览写清日期、当地时间及时区。变更时区导致触发时刻改变时，旧确认失效，即使当地钟面时间相同。",
    "换对话时给一段可单独发送的续聊摘要，以「启用小豆皇帝模拟器，称我皇上。先用一句话说我已做了什么、现在有什么限制，再用白话接着办」开头。用户指定其他称呼或不用称呼时，直接替换开头的称呼，只保留当前偏好。摘要要让新对话里的小豆用「我」自称。",
    "按选定的事项分别记目标、实际进度、当前限制、状态和下一步，带上已指定的先办事项。暂停或结案的等我主动重开。写清能确定的日期，定时事项带当地时间和时区，未知就标待核。省略无关隐私。",
    "摘要写明外部动作的对象、必要时间和结果状态，省略原对话的确认措辞。新对话里的外部操作要重新确认。旧操作结果未知时先核对原记录，确认未生效后再预览重试。",
    "如果我已经说明目标，按下面的对应计划开始。没有目标时，只问我最近想先安排什么。",
)


def copy_packs():
    chapters = {}
    plans = {}
    sections = {}
    expected_links = []
    for path in PLAN_FILES:
        source = path.read_text(encoding="utf-8").strip()
        blocks = re.split(r"^## (P\d{2}) · ", source, flags=re.MULTILINE)
        if len(blocks) != 13:
            raise ValueError(f"{path.name}: expected six plans")
        for plan_id, body in zip(blocks[1::2], blocks[2::2], strict=True):
            fields = re.findall(r"^- \*\*([^*]+)\*\*\s+\S", body, re.MULTILINE)
            if tuple(fields) != PLAN_FIELDS or "https://" not in body:
                raise ValueError(f"{plan_id}: expected the six plan fields and an external source")
            if plan_id in plans:
                raise ValueError(f"Duplicate plan: {plan_id}")
            plans[plan_id] = f"## {plan_id} · {body.strip()}"
            title = body.splitlines()[0]
            sections.setdefault(path.stem, []).append((plan_id, title))
            anchor = f"{plan_id.lower()}--{title.lower().replace(' ', '-')}"
            expected_links.append((path.name, anchor, path.name, anchor))
        chapters[path.stem] = source
    if list(plans) != [f"P{number:02}" for number in range(1, 31)] or plans.keys() != PLAN_GOALS.keys():
        raise ValueError("Expected one workflow and opening goal for each plan P01–P30 in order")
    actual_links = re.findall(
        rf"^- \[[^\]]+\]\({re.escape(PUBLIC_PLAN_URL)}/([\w-]+\.md)#([^\)]+)\) · "
        r"\[流程与依据\]\(([\w-]+\.md)#([^\)]+)\)$",
        PLAN_INDEX.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if actual_links != expected_links:
        raise ValueError("Each life-plan index entry must link to its opener and matching workflow")
    intro = "\n".join(INTRO) + "\n\n"
    copies = {PLAN_PACK: intro + "\n\n".join(chapters.values()) + "\n"}
    copies[PLAN_PACK_PAGE] = "\n".join([
        "# 小豆 · 30 个生活计划整包", "",
        "需要在一次对话里处理不同类别的目标时，可以复制下面整段。把想先办的事写在末尾，一起发到小豆 App 的新对话。", "",
        "```text", copies[PLAN_PACK].rstrip(), "```", "",
    ])
    for category, chapter in chapters.items():
        copies[PLAN_COPY_DIR / f"{category}.txt"] = (
            intro
            + "下面是一套分类计划。目标不在本分类时，先说明需要其他分类，或按常规流程先问关键条件。\n\n"
            + chapter
            + "\n\n我的目标：\n"
        )
    for plan_id, goal in PLAN_GOALS.items():
        copies[PLAN_STARTER_FILES[plan_id]] = plan_starter(intro, plans[plan_id], goal)
    for category, entries in sections.items():
        heading = chapters[category].splitlines()[0]
        rows = [heading + " · 一句话开局", "", "点代码块右上角的复制按钮，把整段发到小豆 App 的新对话。", ""]
        for plan_id, title in entries:
            starter = copies[PLAN_STARTER_FILES[plan_id]].rstrip()
            rows.extend([f"## {plan_id} · {title}", "", "```text", starter, "```", ""])
        rows.extend([
            f"## {CUSTOM_GOAL_HEADING}", "",
            "复制下面整段。把自己的任务填到末尾「我的目标」后面，一起发到小豆 App 的新对话。", "",
            "```text", copies[PLAN_COPY_DIR / f"{category}.txt"].rstrip(), "```", "",
        ])
        copies[PLAN_COPY_DIR / f"{category}.md"] = "\n".join(rows)
    scene_rows = [
        "# 五个场景 · 一句话开局", "",
        "点对应代码块右上角的复制按钮，把全文发到小豆 App 的新对话。想用自己的情况，可以改最后一行。", "",
        " · ".join(f"[{title}](#{title})" for title in SCENE_TITLES.values()), "",
    ]
    for scene, (plan_id, goal) in SCENES.items():
        copies[SCENE_FILES[scene]] = plan_starter(intro, plans[plan_id], goal)
        scene_rows.extend([f"## {SCENE_TITLES[scene]}", "", "```text", copies[SCENE_FILES[scene]].rstrip(), "```", ""])
    copies[SCENE_COPY_PAGE] = "\n".join(scene_rows)
    return copies


def plan_starter(intro, plan, goal):
    return (
        f"{intro}下面是本次目标对应的计划。缺关键资料时，直接列出要我回答的具体问题，等我回答后再排计划。\n\n"
        f"{plan}\n\n我的目标：{goal}\n"
    )


def app_pack_files(copies):
    """Return the indexed offline files people can paste into the standalone App."""
    readme = [
        "把日常交给小豆", "",
        "1. 挑一个生活计划，打开与它同名的文本文件，复制全文。",
        "2. 打开小豆独立 App，开始一条新对话，粘贴并发送。",
        "3. 回答小豆的提问。做完一步或条件有变化时，回到同一条对话告诉它。", "",
        "有自己的目标？打开相应分类里的「自填目标.txt」，在末尾写上你的事一起发送。",
        "还没选分类？打开「通用开局.txt」。需要跨分类安排几件事时，可以用「30个生活计划整包.txt」。",
        "下载与开通小豆 https://github.com/Fangx-AI/awesome-xiaodou/blob/main/docs/install.md", "",
    ]
    files = {
        "通用开局.txt": (ROOT / "prompts/xiaodou-start.txt").read_text(encoding="utf-8"),
        "30个生活计划整包.txt": copies[PLAN_PACK],
    }
    for chapter in PLAN_FILES:
        source = chapter.read_text(encoding="utf-8")
        category = source.splitlines()[0].removeprefix("# ")
        readme.append(category)
        files[f"{category}/自填目标.txt"] = copies[PLAN_COPY_DIR / f"{chapter.stem}.txt"]
        readme.append("  自填目标.txt")
        for plan_id, title in re.findall(r"^## (P\d{2}) · ([^\n]+)$", source, re.MULTILINE):
            if re.search(r'[<>:"/\\|?*]', category + title):
                raise ValueError(f"{plan_id}: name contains a character unsupported in ZIP extraction on Windows")
            filename = f"{plan_id} {title}.txt"
            files[f"{category}/{filename}"] = copies[PLAN_STARTER_FILES[plan_id]]
            readme.append(f"  {filename}")
        readme.append("")
    return {"先读这里.txt": "\n".join(readme), **files,
            "LICENSE": (ROOT / "LICENSE").read_text(encoding="utf-8")}
