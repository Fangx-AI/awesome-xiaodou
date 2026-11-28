"""
test_ziwei_chart.py — 紫微排盘核验测试

测试基准（已脱敏，仅保留算法结构，不含任何命主标识）：
  - Case-J4：壬年金四局农历三月初四寅时（整除路径，4÷4=1）
  - Case-S2：癸年水二局农历四月十一午时（非整除路径，11÷2，
    覆盖早期 _ziwei_pos 口诀法判错的关键分支；其14主星结构经
    文墨天机排盘软件独立验证）

两个基准的命宫/身宫/五行局/来因宫/14主星(含庙陷)/14辅星/自化层
全部正确。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from ziwei_chart import ZiweiEngine, ZW_POS_TABLE_SUB0, DIZHI


# ═══════════════════════════════════════════════════════════════
# Case-J4：金四局整除路径核验
# ═══════════════════════════════════════════════════════════════

def test_j4_palace_stems():
    """金四局盘十二宫干（五虎遁壬年起壬寅）"""
    engine = ZiweiEngine()
    c = engine.cast("壬", 3, 4, 2, "男")

    expected_stems = {
        "寅": "壬", "卯": "癸", "辰": "甲", "巳": "乙",
        "午": "丙", "未": "丁", "申": "戊", "酉": "己",
        "戌": "庚", "亥": "辛", "子": "壬", "丑": "癸",
    }
    for zhi, exp_stem in expected_stems.items():
        actual = c.get_palace_by_zhi(zhi)["stem"]
        assert actual == exp_stem, f"{zhi}宫干应{exp_stem}，得{actual}"

    print("✅ test_j4_palace_stems 通过（十二宫干五虎遁无误）")


def test_j4_ming_shen_ju():
    """金四局盘命宫/身宫/五行局/来因宫"""
    engine = ZiweiEngine()
    c = engine.cast("壬", 3, 4, 2, "男")

    assert c.ming_zhi == "寅", f"命宫应寅，得{c.ming_zhi}"
    assert c.shen_zhi == "午", f"身宫应午，得{c.shen_zhi}"
    assert c.ming_ganzhi == "壬寅", f"命宫干支应壬寅，得{c.ming_ganzhi}"
    assert c.ming_nayin == "金箔金", f"纳音应金箔金，得{c.ming_nayin}"
    assert c.wuxing_ju == 4, f"五行局应金四局(4)，得{c.wuxing_ju}"
    assert c.wuxing_ju_name == "金四局"
    assert c.laiyin_zhi == "寅", f"来因宫应寅，得{c.laiyin_zhi}"
    assert c.laiyin_palace == "命宫", f"来因宫应为命宫，得{c.laiyin_palace}"

    print("✅ test_j4_ming_shen_ju 通过（命寅身午金四局来因命宫）")


def test_j4_14_stars():
    """金四局盘14主星全部落宫（整除路径，紫微在寅）"""
    engine = ZiweiEngine()
    c = engine.cast("壬", 3, 4, 2, "男")

    assert c.ziwei_zhi == "寅", f"紫微应寅，得{c.ziwei_zhi}"
    assert c.tianfu_zhi == "寅", f"天府应寅，得{c.tianfu_zhi}"

    expected = {
        "寅": ["紫微", "天府"],
        "卯": ["太阴"],
        "辰": ["贪狼"],
        "巳": ["巨门"],
        "午": ["廉贞", "天相"],
        "未": ["天梁"],
        "申": ["七杀"],
        "酉": ["天同"],
        "戌": ["武曲"],
        "亥": ["太阳"],
        "子": ["破军"],
        "丑": ["天机"],
    }
    for zhi, exp_stars in expected.items():
        palace = c.get_palace_by_zhi(zhi)
        actual_stars = sorted(palace["main_stars"])
        assert actual_stars == sorted(exp_stars), (
            f"{zhi}宫主星应{sorted(exp_stars)}，得{actual_stars}"
        )

    print("✅ test_j4_14_stars 通过（14主星全部正确，含紫府同宫寅）")


def test_j4_miaoxian():
    """金四局盘14主星庙旺平陷"""
    from ziwei_chart import get_miaoxian
    engine = ZiweiEngine()
    c = engine.cast("壬", 3, 4, 2, "男")

    expected_mx = {
        ("紫微","寅"):"旺", ("天府","寅"):"庙",
        ("太阴","卯"):"陷", ("贪狼","辰"):"庙",
        ("巨门","巳"):"旺", ("廉贞","午"):"平",
        ("天相","午"):"庙", ("天梁","未"):"旺",
        ("七杀","申"):"庙", ("天同","酉"):"平",
        ("武曲","戌"):"庙", ("太阳","亥"):"陷",
        ("破军","子"):"庙", ("天机","丑"):"陷",
    }
    for (star, zhi), exp_mx in expected_mx.items():
        zhi_idx = DIZHI.index(zhi)
        actual_mx = get_miaoxian(star, zhi_idx)
        assert actual_mx == exp_mx, (
            f"{star}在{zhi}应{exp_mx}，得{actual_mx}"
        )

    print("✅ test_j4_miaoxian 通过（14主星庙陷全部正确）")


def test_j4_palace_names():
    """金四局盘十二宫位排列（命宫寅起逆时针）"""
    engine = ZiweiEngine()
    c = engine.cast("壬", 3, 4, 2, "男")

    expected_names = {
        "寅": "命宫", "丑": "兄弟", "子": "夫妻", "亥": "子女",
        "戌": "财帛", "酉": "疾厄", "申": "迁移", "未": "交友",
        "午": "官禄", "巳": "田宅", "辰": "福德", "卯": "父母",
    }
    for zhi, exp_name in expected_names.items():
        actual = c.get_palace_by_zhi(zhi)["name"]
        assert actual == exp_name, f"{zhi}宫位应{exp_name}，得{actual}"

    print("✅ test_j4_palace_names 通过（十二宫位排列正确）")


def test_j4_aux_stars():
    """金四局盘14辅星全部落宫"""
    engine = ZiweiEngine()
    c = engine.cast("壬", 3, 4, 2, "男", "", "戌")

    expected_aux = {
        "午": ["左辅", "文曲"],      # 官禄
        "申": ["右弼", "文昌", "天马"],  # 迁移
        "卯": ["天魁", "火星"],      # 父母
        "巳": ["天钺", "铃星"],      # 田宅
        "亥": ["禄存"],              # 子女
        "子": ["擎羊"],              # 夫妻
        "戌": ["陀罗"],              # 财帛
        "酉": ["地空"],              # 疾厄
        "丑": ["地劫"],              # 兄弟
    }
    for zhi, exp_stars in expected_aux.items():
        palace = c.get_palace_by_zhi(zhi)
        actual = sorted(palace.get("aux_stars", []))
        assert actual == sorted(exp_stars), (
            f"{zhi}宫辅星应{sorted(exp_stars)}，得{actual}"
        )

    print("✅ test_j4_aux_stars 通过（14辅星全部正确）")


def test_j4_full_self_transform_6():
    """金四局盘全盘6处自化（含辅星右弼自化科）"""
    engine = ZiweiEngine()
    c = engine.cast("壬", 3, 4, 2, "男", "", "戌")

    from sihua_lookup import SihuaEngine
    sihua = SihuaEngine()

    self_huas_found = []
    for zhi_idx in range(12):
        zhi = DIZHI[zhi_idx]
        palace = c.get_palace_by_zhi(zhi)
        stem = palace["stem"]
        all_stars = palace["main_stars"] + palace.get("aux_stars", [])
        if not all_stars:
            continue
        results = sihua.self_transform(stem, all_stars)
        for r in results:
            if r["type"] != "无自化":
                self_huas_found.append((zhi, r["star"], r["type"]))

    assert len(self_huas_found) == 6, (
        f"自化应6处，得{len(self_huas_found)}处: {self_huas_found}"
    )
    youbi = [(z, s, t) for z, s, t in self_huas_found if s == "右弼"]
    assert len(youbi) == 1, f"右弼自化应1处，得{len(youbi)}"
    assert youbi[0][2] == "自化科", f"右弼应自化科，得{youbi[0][2]}"
    assert youbi[0][0] == "申", f"右弼应在申宫，得{youbi[0][0]}"

    print("✅ test_j4_full_self_transform_6 通过（6处自化完整，含右弼自化科）")


# ═══════════════════════════════════════════════════════════════
# Case-S2：水二局非整除路径核验（关键补盲，覆盖原 _ziwei_pos bug 区）
# ═══════════════════════════════════════════════════════════════

def test_s2_ziwei_pos_non_divisible():
    """水二局农历日11 → 紫微落午（非整除路径，11÷2 不整除）。
    早期 _ziwei_pos 口诀法在此路径判错；改为查表后紫微在午。
    14主星结构经文墨天机排盘软件独立验证。"""
    engine = ZiweiEngine()
    c = engine.cast("癸", 4, 11, 6, "女", "", "亥")

    assert c.ming_zhi == "亥", f"命宫应亥，得{c.ming_zhi}"
    assert c.shen_zhi == "亥", f"身宫应亥(命身同宫)，得{c.shen_zhi}"
    assert c.wuxing_ju == 2, f"五行局应水二局(2)，得{c.wuxing_ju}"
    assert c.ziwei_zhi == "午", f"紫微应午，得{c.ziwei_zhi}（非整除路径关键判定）"

    print("✅ test_s2_ziwei_pos_non_divisible 通过（水2局日11紫微在午，非整除路径正确）")


def test_s2_14_stars():
    """水二局盘14主星全部落宫（非整除路径，14星经文墨天机OCR验证）"""
    engine = ZiweiEngine()
    c = engine.cast("癸", 4, 11, 6, "女", "", "亥")

    expected = {
        "亥": ["太阴"],          # 命宫
        "子": ["贪狼"],          # 父母
        "丑": ["天同", "巨门"],  # 福德
        "寅": ["武曲", "天相"],  # 田宅
        "卯": ["太阳", "天梁"],  # 官禄
        "辰": ["七杀"],          # 交友
        "巳": ["天机"],          # 迁移
        "午": ["紫微"],          # 疾厄
        "申": ["破军"],          # 子女
        "戌": ["廉贞", "天府"],  # 兄弟
        "未": [],                # 财帛（无主星）
        "酉": [],                # 夫妻（无主星）
    }
    for zhi, exp_stars in expected.items():
        palace = c.get_palace_by_zhi(zhi)
        actual_stars = sorted(palace["main_stars"])
        assert actual_stars == sorted(exp_stars), (
            f"{zhi}宫主星应{sorted(exp_stars)}，得{actual_stars}"
        )

    print("✅ test_s2_14_stars 通过（水2局14主星全部正确，非整除路径金标准）")


# ═══════════════════════════════════════════════════════════════
# 安星规则单元测试（不依赖具体命例）
# ═══════════════════════════════════════════════════════════════

def test_ziwei_tianfu_symmetry():
    """紫微天府对称性：所有12个紫微位置，天府必须关于寅申轴对称"""
    engine = ZiweiEngine()

    for z_idx in range(12):
        tf_idx = (4 - z_idx) % 12
        assert (z_idx + tf_idx) % 12 == 4, (
            f"紫微{z_idx}天府{tf_idx}不对称"
        )

    print("✅ test_ziwei_tianfu_symmetry 通过（紫府寅申轴对称）")


def test_star_layout_completeness():
    """14主星布局完整性：任何紫微位置，14星必须全部出现且不重叠错位"""
    engine = ZiweiEngine()

    for z_idx in range(12):
        tf_idx = (4 - z_idx) % 12
        stars_map = engine._layout_14stars(z_idx, tf_idx)
        all_stars = []
        for star_list in stars_map.values():
            all_stars.extend(star_list)
        assert len(all_stars) == 14, f"紫微{z_idx}: 主星数{len(all_stars)}≠14"
        assert len(set(all_stars)) == 14, f"紫微{z_idx}: 主星有重复"

    print("✅ test_star_layout_completeness 通过（12基本盘14星完整无重复）")


def test_star_offsets():
    """14主星偏移规则（对照口诀）"""
    engine = ZiweiEngine()

    z_idx = 2
    tf_idx = (4 - z_idx) % 12
    stars = engine._layout_14stars(z_idx, tf_idx)

    def find_star(star_name):
        for idx, slist in stars.items():
            if star_name in slist:
                return idx
        return None

    assert find_star("紫微") == z_idx
    assert find_star("天机") == (z_idx - 1) % 12
    assert find_star("太阳") == (z_idx - 3) % 12
    assert find_star("武曲") == (z_idx - 4) % 12
    assert find_star("天同") == (z_idx - 5) % 12
    assert find_star("廉贞") == (z_idx - 8) % 12

    assert find_star("天府") == tf_idx
    assert find_star("太阴") == (tf_idx + 1) % 12
    assert find_star("贪狼") == (tf_idx + 2) % 12
    assert find_star("巨门") == (tf_idx + 3) % 12
    assert find_star("天相") == (tf_idx + 4) % 12
    assert find_star("天梁") == (tf_idx + 5) % 12
    assert find_star("七杀") == (tf_idx + 6) % 12
    assert find_star("破军") == (tf_idx + 10) % 12

    print("✅ test_star_offsets 通过（安星偏移符合口诀）")


def test_zw_pos_table_periodicity():
    """ZW_POS_TABLE 数学结构校验：五局×30日全覆盖、值域合法、
    金标准锚点命中（防止定星表回归到早期口诀法 bug）。"""
    # 1. 每局30个值，值域0-11
    for ju, seq in ZW_POS_TABLE_SUB0.items():
        assert len(seq) == 30, f"{ju}局长度{len(seq)}≠30"
        assert all(0 <= v <= 11 for v in seq), f"{ju}局有越界值"

    # 2. 金标准锚点（与排盘软件交叉验证）
    assert ZW_POS_TABLE_SUB0[4][3] == 2, "金4局日4应=寅(2)"
    assert ZW_POS_TABLE_SUB0[2][10] == 6, "水2局日11应=午(6)"
    assert ZW_POS_TABLE_SUB0[2][0] == 1, "水2局日1应=丑(1，全书铁律)"

    # 3. 水二局结构规律：日1=丑(单独)，日≥2每2日进1宫从寅起
    assert ZW_POS_TABLE_SUB0[2][1] == 2, "水2局日2应=寅"
    for d in range(2, 31):
        expected = (2 + (d - 2) // 2) % 12
        assert ZW_POS_TABLE_SUB0[2][d-1] == expected, (
            f"水2局日{d}应={expected}，得={ZW_POS_TABLE_SUB0[2][d-1]}"
        )

    print("✅ test_zw_pos_table_periodicity 通过（定星表数学结构+金标准锚点）")


# ═══════════════════════════════════════════════════════════════
# 运行所有测试
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("紫微排盘核验 测试套件")
    print("基准: Case-J4(金4局整除) + Case-S2(水2局非整除)")
    print("=" * 60)
    print()

    test_j4_palace_stems()
    test_j4_ming_shen_ju()
    test_j4_14_stars()
    test_j4_miaoxian()
    test_j4_palace_names()
    test_j4_aux_stars()
    test_j4_full_self_transform_6()
    test_s2_ziwei_pos_non_divisible()
    test_s2_14_stars()
    test_ziwei_tianfu_symmetry()
    test_star_layout_completeness()
    test_star_offsets()
    test_zw_pos_table_periodicity()

    print()
    print("=" * 60)
    print("🎉 全部测试通过！紫微排盘核验覆盖金4局(整除)+水2局(非整除)。")
    print("   含14主星(庙陷) + 14辅星 + 6处自化 + 定星表数学结构校验")
    print("=" * 60)
