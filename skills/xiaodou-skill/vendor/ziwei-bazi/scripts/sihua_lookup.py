"""
sihua_lookup.py — 十天干四化查表 + 自化五步判定 + 飞星层推算

这是命理排盘核验的"四化层"工具。紫微斗数的十天干四化是固定查表，
自化判定是固定的集合匹配逻辑——两者都是确定性计算，必须脚本化以消灭
LLM 在这两道工序上的高幻觉。

用法:
    from sihua_lookup import SihuaEngine
    engine = SihuaEngine()

    # 1. 查某天干的四化
    engine.lookup("壬")  # -> {"禄": "天梁", "权": "紫微", "科": "左辅", "忌": "武曲"}

    # 2. 自化五步判定（给一个宫的天干 + 宫内主星列表）
    engine.self_transform("庚", ["武曲"])  # -> "自化权"
    engine.self_transform("丙", ["左辅"])  # -> "无自化"

    # 3. 飞星层（某宫宫干飞化落入哪些宫的哪些星）
    engine.flying("壬")  # -> {"禄": "天梁", "权": "紫微", ...}（需配合宫位星曜表）

庚干派别分歧说明:
    庚干化科与化忌存在派别分歧（见 SOP）。本表默认采中州/三合口径
    （科=太阴，忌=天同）。武曲恒在庚干"权"列，不受分歧影响。
"""

from typing import Optional


# ─── 十天干四化固定查表（焊入系统，禁止凭记忆）──────────────────────────
# 数据来源：紫微斗数标准十天干四化口诀
# 庚干科忌采中州/三合口径（科=太阴，忌=天同）
SIHUA_TABLE = {
    "甲": {"禄": "廉贞", "权": "破军", "科": "武曲", "忌": "太阳"},
    "乙": {"禄": "天机", "权": "天梁", "科": "紫微", "忌": "太阴"},
    "丙": {"禄": "天同", "权": "天机", "科": "文昌", "忌": "廉贞"},
    "丁": {"禄": "太阴", "权": "天同", "科": "天机", "忌": "巨门"},
    "戊": {"禄": "贪狼", "权": "太阴", "科": "右弼", "忌": "天机"},
    "己": {"禄": "武曲", "权": "贪狼", "科": "天梁", "忌": "文曲"},
    "庚": {"禄": "太阳", "权": "武曲", "科": "太阴", "忌": "天同"},  # 中州口径；飞星派科=天同
    "辛": {"禄": "巨门", "权": "太阳", "科": "文曲", "忌": "文昌"},
    "壬": {"禄": "天梁", "权": "紫微", "科": "左辅", "忌": "武曲"},
    "癸": {"禄": "破军", "权": "巨门", "科": "太阴", "忌": "贪狼"},
}

# 庚干派别分歧声明（用于报告输出时提示）
GENG_FACTION_NOTE = (
    "庚干化科与化忌存在派别分歧："
    "中州/三合（科=太阴，忌=天同）；"
    "飞星/部分钦天（科=天同，忌=天同，天同同抵科忌）；"
    "另有古本（忌=天相）。"
    "本系统默认中州口径。武曲恒在庚干'权'列，不受分歧影响。"
)

# 十四主星全集（用于自化集合匹配的边界校验）
FOURTEEN_MAIN_STARS = {
    "紫微", "天机", "太阳", "武曲", "天同", "廉贞", "天府",
    "太阴", "贪狼", "巨门", "天相", "天梁", "七杀", "破军",
}

# 四象顺序（报告输出用）
XIANG_ORDER = ["禄", "权", "科", "忌"]


class SihuaError(Exception):
    """四化查表/自化判定中的错误"""


class SihuaEngine:
    """四化查表 + 自化判定 + 飞星层推算引擎"""

    def __init__(self, geng_faction: str = "zhongzhou"):
        """
        Args:
            geng_faction: 庚干口径。"zhongzhou"(默认)=科太阴忌天同;
                          "feixing"=科天同忌天同。
        """
        self.table = dict(SIHUA_TABLE)
        if geng_faction == "feixing":
            self.table["庚"] = {"禄": "太阳", "权": "武曲", "科": "天同", "忌": "天同"}
        self.geng_faction = geng_faction

    # ─── 1. 基础查表 ──────────────────────────────────────────────

    def lookup(self, stem: str) -> dict:
        """
        查某天干的完整四化。

        Returns: {"禄": "天梁", "权": "紫微", "科": "左辅", "忌": "武曲"}
        """
        if stem not in self.table:
            raise SihuaError(f"无效天干: {stem}（应为 甲~癸）")
        return dict(self.table[stem])

    def lookup_star(self, stem: str, xiang: str) -> str:
        """查某天干某象对应哪颗星。例 lookup_star("壬", "忌") → "武曲" """
        if xiang not in XIANG_ORDER:
            raise SihuaError(f"无效象: {xiang}（应为 禄/权/科/忌）")
        return self.lookup(stem)[xiang]

    def find_xiang_of_star(self, stem: str, star: str) -> Optional[str]:
        """
        查某星在某天干中化什么象。
        Returns: "权" / "忌" / ... 或 None（该星不在该干四化中）
        例 find_xiang_of_star("庚", "武曲") → "权"
        """
        four = self.lookup(stem)
        for xiang, s in four.items():
            if s == star:
                return xiang
        return None

    # ─── 2. 自化五步硬核验证 ──────────────────────────────────────

    def self_transform(self, palace_stem: str, stars_in_palace: list) -> list:
        """
        自化五步判定（对应 SOP 的"自化五步硬核验证"）。

        五步:
          1. 写宫干 = palace_stem
          2. 写四星全集 = 查表得 {禄,权,科,忌} 四星
          3. 列宫内星 = stars_in_palace
          4. 集合匹配 = 宫内星是否等于四星之一
          5. 判定 = 等于则自化该象，否则无自化

        一个宫内可能有多颗主星，每颗独立判定。

        Args:
            palace_stem: 该宫天干（甲~癸）
            stars_in_palace: 该宫内主星列表，如 ["武曲"] 或 ["廉贞", "天相"]

        Returns:
            自化结果列表，每个元素:
              {"star": "武曲", "xiang": "权", "type": "自化权"}
            无自化的星返回:
              {"star": "天相", "xiang": None, "type": "无自化"}
        """
        four_stars = self.lookup(palace_stem)  # 第②步：四星全集
        four_star_set = set(four_stars.values())

        results = []
        for star in stars_in_palace:
            if star not in FOURTEEN_MAIN_STARS:
                # 非十四主星（如左辅右弼文昌文曲天魁天钺禄存天马等）
                # 在标准四化表中也可能出现（左辅/右弼/文昌/文曲）
                # 这里不做限制，允许任何星参与匹配
                pass

            xiang = self.find_xiang_of_star(palace_stem, star)  # 第④步集合匹配
            if xiang is not None:
                results.append({
                    "star": star,
                    "xiang": xiang,
                    "type": f"自化{xiang}",
                    "four_star_set": dict(four_stars),  # 留痕第②步
                })
            else:
                results.append({
                    "star": star,
                    "xiang": None,
                    "type": "无自化",
                    "four_star_set": dict(four_stars),
                })

        return results

    def self_transform_verbose(self, palace_stem: str, stars_in_palace: list) -> str:
        """
        自化五步判定的完整文字输出（用于报告中的"五步验证留痕"）。
        格式严格对齐 SOP 要求。
        """
        four = self.lookup(palace_stem)
        four_str = f"禄={four['禄']},权={four['权']},科={four['科']},忌={four['忌']}"
        results = self.self_transform(palace_stem, stars_in_palace)

        lines = []
        lines.append(f"  第①步 写宫干：{palace_stem}")
        lines.append(f"  第②步 写四星全集：{{{four_str}}}")
        lines.append(f"  第③步 列宫内星：{', '.join(stars_in_palace)}")

        for r in results:
            if r["xiang"] is not None:
                lines.append(
                    f"  第④⑤步 集合匹配：{r['star']}={four[r['xiang']]}∈四星全集，"
                    f"在'{r['xiang']}'列 → {r['type']}"
                )
            else:
                lines.append(
                    f"  第④⑤步 集合匹配：{r['star']}∉四星全集"
                    f"{{{four_str}}} → 无自化"
                )
        return "\n".join(lines)

    # ─── 3. 飞星层（某宫宫干飞化）──────────────────────────────────

    def flying(self, palace_stem: str) -> dict:
        """
        某宫宫干飞化：飞禄/飞权/飞科/飞忌分别使哪颗星化象。
        （要确定飞入哪个宫，需配合"星曜落宫表"在调用方完成。）

        Returns: {"飞禄": ("天梁", "化禄"), "飞忌": ("武曲", "化忌"), ...}
        """
        four = self.lookup(palace_stem)
        return {
            "飞禄": (four["禄"], "化禄"),
            "飞权": (four["权"], "化权"),
            "飞科": (four["科"], "化科"),
            "飞忌": (four["忌"], "化忌"),
        }

    def flying_to_palaces(
        self, palace_stem: str, star_to_palace: dict
    ) -> list:
        """
        完整飞星层：宫干飞化 + 星曜落宫 → 飞入哪个宫。

        Args:
            palace_stem: 起飞宫的天干
            star_to_palace: {星曜: 落宫地支}，如 {"天梁": "未", "武曲": "戌"}

        Returns:
            [{"象": "飞忌", "星": "武曲", "落宫": "戌", "描述": "飞忌武曲→戌"}, ...]
        """
        four = self.lookup(palace_stem)
        results = []
        for xiang in XIANG_ORDER:
            star = four[xiang]
            palace = star_to_palace.get(star, "?")
            results.append({
                "象": f"飞{xiang}",
                "星": star,
                "落宫": palace,
                "描述": f"飞{xiang}{star}→{palace}",
            })
        return results

    # ─── 4. 生年四化转移偏见检查 ──────────────────────────────────

    def check_transfer_bias(
        self, natal_stem: str, natal_xiang: str, star: str,
        palace_stem: str,
    ) -> dict:
        """
        生年四化转移偏见检查。

        场景：某星是生年某象（如生年忌=武曲），落入某宫后，
        该宫天干是否使它自化同名象？

        典型陷阱：
          生年忌=武曲 → 看到庚戌武曲误判"自化忌"
          但查庚干，武曲在权列 → 实为自化权！

        Args:
            natal_stem: 生年天干
            natal_xiang: 该星在生年四化中的象（"禄"/"权"/"科"/"忌"）
            star: 被检查的星
            palace_stem: 该星所在宫的天干

        Returns:
            {"natal_xiang": "忌", "actual_self_xiang": "权",
             "bias_detected": True, "warning": "..."}
        """
        actual = self.find_xiang_of_star(palace_stem, star)
        bias = (actual is not None and actual != natal_xiang)

        return {
            "star": star,
            "natal_xiang": natal_xiang,
            "palace_stem": palace_stem,
            "actual_self_xiang": actual,  # None=无自化
            "bias_detected": bias,
            "warning": (
                f"⚠️ 转移偏见：{star}生年{natal_xiang}，"
                f"但在{palace_stem}干下实为自化{actual}（非自化{natal_xiang}！）"
                if bias else
                "无转移偏见"
            ),
        }


# ─── 命令行入口 ──────────────────────────────────────────────────

def main():
    """命令行交互：查表 / 自化判定 / 飞星层"""
    import sys
    engine = SihuaEngine()

    if len(sys.argv) < 2:
        print("用法:")
        print("  python sihua_lookup.py lookup <天干>          查四化")
        print("  python sihua_lookup.py self <宫干> <星1> [星2...]  自化判定")
        print("  python sihua_lookup.py fly <宫干>             飞星层")
        print("  python sihua_lookup.py bias <生年干> <生年象> <星> <宫干>  转移偏见检查")
        print("  python sihua_lookup.py geng                   庚干派别分歧声明")
        print()
        print(GENG_FACTION_NOTE)
        return

    cmd = sys.argv[1]

    if cmd == "lookup":
        stem = sys.argv[2]
        result = engine.lookup(stem)
        print(f"【{stem}干四化】", end="  ")
        for xiang in XIANG_ORDER:
            print(f"{xiang}={result[xiang]}", end="  ")
        print()

    elif cmd == "self":
        stem = sys.argv[2]
        stars = sys.argv[3:]
        if not stars:
            print("请提供宫内主星")
            return
        print(f"【{stem}干宫·自化五步验证】")
        print(engine.self_transform_verbose(stem, stars))
        results = engine.self_transform(stem, stars)
        print("\n裁定：", end="")
        for r in results:
            print(f"{r['star']}={r['type']}", end="  ")
        print()

    elif cmd == "fly":
        stem = sys.argv[2]
        result = engine.flying(stem)
        print(f"【{stem}干·飞星层】")
        for key, (star, hua) in result.items():
            print(f"  {key}：{star}{hua}")

    elif cmd == "bias":
        natal_stem, natal_xiang, star, palace_stem = sys.argv[2:6]
        result = engine.check_transfer_bias(natal_stem, natal_xiang, star, palace_stem)
        print(result["warning"])

    elif cmd == "geng":
        print(GENG_FACTION_NOTE)

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
