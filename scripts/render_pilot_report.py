"""Render publishable aggregate trial evidence, without participant-level material."""


def fraction(metric):
    n, total = metric["numerator"], metric["denominator"]
    value = metric["percent"]
    return f"{n}/{total}（{value:g}%）" if value is not None else "暂无可评分样本"


def signed(value, unit):
    return f"{value:+g} {unit}" if value is not None else "—"


def pair_line(label, result):
    counts = (f"皇帝模式 {result['emperor_only']}，普通小豆 {result['regular_only']}，"
              f"都通过 {result['both']}，都未通过 {result['neither']}")
    coverage = f"{result['pairs']} 可评分，{result['unscored_pairs']} 无法配对"
    return f"| {label} | {coverage} | {counts} | {signed(result['emperor_minus_regular_pp'], '个百分点')} |"


def comparison_lines(result):
    follow_up = result["follow_up_questions"]
    delta = signed(follow_up["emperor_minus_regular_mean"], "个")
    return [
        "| 指标 | 配对样本 | 各组通过情况 | 皇帝模式与普通小豆的差 |",
        "| --- | --- | --- | --- |",
        pair_line("拿到可做的第一步", result["outcomes"]["first_action"]),
        pair_line("计划变了仍能继续", result["outcomes"]["replan"]),
        pair_line("保留已完成", result["replan_checks"]["preserved"]),
        pair_line("只改相关事项", result["replan_checks"]["affected_only"]),
        pair_line("给出可做的下一步", result["replan_checks"]["replan_actionable"]),
        "",
        f"追问数有 {follow_up['pairs']} 个完整配对，{follow_up['unscored_pairs']} 个无法配对，"
        f"每人平均追问数之差为 {delta}。首步通过情况见上表。",
        "",
    ]


def render(report):
    lines = ["# 小豆七天试用汇总", "", f"统计截至 {report['as_of']}。", ""]
    base = "https://github.com/Fangx-AI/awesome-xiaodou"
    for key, label, path in (("candidate_commit", "试用候选版本", ""),
                             ("public_readme_commit", "首页冷读固定版本", "#readme")):
        if commit := report[key]:
            lines.append(f"- [{label} {commit[:7]}]({base}/tree/{commit}{path})")
    if lines[-1]:
        lines.append("")
    started = report["first_action"]["denominator"]
    unreported = report["seven_day_unreported"]
    incomplete = report["seven_day_reported_incomplete"]
    pending = report["pending_seven_day_window"]
    lines.extend([
        "## 从开局到完成", "",
        "| 观察项 | 汇总 |",
        "| --- | --- |",
        f"| 首页冷读 | {fraction(report['cold_read'])} |",
        f"| 已确认发出开局 | {started} 人 |",
        f"| 拿到可做的第一步 | {fraction(report['first_action'])} |",
        f"| 七天内实际完成第一步（已到期） | {fraction(report['seven_day_completion'])} |",
        f"| 改案保留进度且能继续 | {fraction(report['replanning'])} |",
        f"| 第 6–8 天主动回访 | {fraction(report['unprompted_return'])} |",
        "",
        f"七天窗口还有 {pending} 人未到期。已到期者中，{unreported} 人未回报，"
        f"{incomplete} 人明确到期未完成或到期后才完成。"
        f"计划变动中有 {report['replanning_unscored']} 次材料不足，保留在分母。",
        "",
        "## 普通小豆与皇帝模式", "",
    ])
    compared = report["matched_comparison"]
    if not compared["enrolled"]:
        return "\n".join([*lines, "暂无真实配对结果。", ""])
    counts = compared["carryover_counts"]
    scenarios = "、".join(f"{label} {count} 人" for label, count in compared["scenario_counts"].items())
    lines.extend([
        f"共登记 {compared['enrolled']} 人参加配对。场景分布为 {scenarios}。"
        f"两段对话核对后，{counts['none']} 人未发现具体内容沿用，"
        f"{counts['first_action']} 人在首步前发现沿用，{counts['replan']} 人在改案时发现沿用，"
        f"{counts['unknown']} 人尚未核对。样本数小或顺序结果不一致时，暂不判断哪个模式更好。", "",
        "### 全样本", "", *comparison_lines(compared),
        "### 已核对对话沿用的样本", "",
        "把首步前已受影响的配对留在全样本。到改案才发现沿用的配对，在这里保留首步评分。", "",
        *comparison_lines(compared["carryover_screened"]),
    ])
    for arm, label in (("regular", "先试普通小豆"), ("emperor", "先试皇帝模式")):
        order = compared["by_order"][arm]
        lines.extend([f"### {label}（{order['enrolled']} 人）", "", *comparison_lines(order),
                      "**已核对对话沿用的样本**", "", *comparison_lines(order["carryover_screened"])])
    return "\n".join(lines)
