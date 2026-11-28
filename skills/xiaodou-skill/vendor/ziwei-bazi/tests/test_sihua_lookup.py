"""
test_sihua_lookup.py — 四化查表/自化判定/飞星层测试

测试基准：十天干四化固定查表 + 自化集合匹配的算法性质。
断言不依赖任何命主——`self_transform("壬", ["紫微","天府"])` 测的是
"壬干宫有紫微天府时的自化"，这是纯算法确定性，与命主无关。

这些是"金标准"——脚本的输出必须与已验证的算法结构完全一致。
任何破坏这些断言的改动都是回归。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from sihua_lookup import SihuaEngine, GENG_FACTION_NOTE


# ═══════════════════════════════════════════════════════════════
# 一、基础查表测试（十天干四化全量）
# ═══════════════════════════════════════════════════════════════

EXPECTED_TABLE = {
    "甲": {"禄": "廉贞", "权": "破军", "科": "武曲", "忌": "太阳"},
    "乙": {"禄": "天机", "权": "天梁", "科": "紫微", "忌": "太阴"},
    "丙": {"禄": "天同", "权": "天机", "科": "文昌", "忌": "廉贞"},
    "丁": {"禄": "太阴", "权": "天同", "科": "天机", "忌": "巨门"},
    "戊": {"禄": "贪狼", "权": "太阴", "科": "右弼", "忌": "天机"},
    "己": {"禄": "武曲", "权": "贪狼", "科": "天梁", "忌": "文曲"},
    "庚": {"禄": "太阳", "权": "武曲", "科": "太阴", "忌": "天同"},
    "辛": {"禄": "巨门", "权": "太阳", "科": "文曲", "忌": "文昌"},
    "壬": {"禄": "天梁", "权": "紫微", "科": "左辅", "忌": "武曲"},
    "癸": {"禄": "破军", "权": "巨门", "科": "太阴", "忌": "贪狼"},
}


def test_basic_lookup_all_stems():
    """全量查表：十个天干的四化必须与固定查表完全一致"""
    engine = SihuaEngine()
    for stem, expected in EXPECTED_TABLE.items():
        result = engine.lookup(stem)
        for xiang, star in expected.items():
            assert result[xiang] == star, (
                f"{stem}干{xiang}应为{star}，实得{result[xiang]}"
            )
    print("✅ test_basic_lookup_all_stems 通过")


def test_lookup_star():
    """单星查询"""
    engine = SihuaEngine()
    assert engine.lookup_star("壬", "忌") == "武曲"
    assert engine.lookup_star("丙", "忌") == "廉贞"
    assert engine.lookup_star("庚", "权") == "武曲"
    assert engine.lookup_star("甲", "禄") == "廉贞"
    print("✅ test_lookup_star 通过")


def test_geng_feixing_faction():
    """飞星派庚干口径：科=天同，忌=天同"""
    engine = SihuaEngine(geng_faction="feixing")
    assert engine.lookup("庚")["科"] == "天同"
    assert engine.lookup("庚")["忌"] == "天同"
    # 武曲恒在权列，不受派别影响
    assert engine.lookup("庚")["权"] == "武曲"
    print("✅ test_geng_feixing_faction 通过")


# ═══════════════════════════════════════════════════════════════
# 二、金四局基准盘自化层测试（6处金标准）
# ═══════════════════════════════════════════════════════════════

def test_j4_self_transform_6_points():
    """
    金四局基准盘自化层6处（壬干起十二宫干分布）：
      寅(壬): 紫微自化权
      午(丙): 廉贞自化忌
      戌(庚): 武曲自化权  ← 最高频幻觉点！
      卯(癸): 太阴自化科
      亥(辛): 太阳自化权
      申(戊): 右弼自化科
    """
    engine = SihuaEngine()

    # 寅(壬): 紫微自化权，天府无自化
    r = engine.self_transform("壬", ["紫微", "天府"])
    assert r[0] == {"star": "紫微", "xiang": "权", "type": "自化权", "four_star_set": engine.lookup("壬")}
    assert r[1]["type"] == "无自化"

    # 午(丙): 廉贞自化忌，天相/左辅/文曲无自化
    r = engine.self_transform("丙", ["廉贞", "天相", "左辅", "文曲"])
    assert r[0]["type"] == "自化忌" and r[0]["star"] == "廉贞"
    assert r[1]["type"] == "无自化"  # 天相
    assert r[2]["type"] == "无自化"  # 左辅 ← 生年科转移偏见高危点
    assert r[3]["type"] == "无自化"  # 文曲

    # 戌(庚): 武曲自化权（非忌！）
    r = engine.self_transform("庚", ["武曲"])
    assert r[0]["type"] == "自化权", f"武曲应为自化权，实得{r[0]['type']}"
    assert r[0]["xiang"] == "权"

    # 卯(癸): 太阴自化科
    r = engine.self_transform("癸", ["太阴"])
    assert r[0]["type"] == "自化科"

    # 亥(辛): 太阳自化权
    r = engine.self_transform("辛", ["太阳"])
    assert r[0]["type"] == "自化权"

    # 申(戊): 右弼自化科
    r = engine.self_transform("戊", ["右弼"])
    assert r[0]["type"] == "自化科"

    print("✅ test_j4_self_transform_6_points 通过（含庚戌武曲自化权关键判定）")


def test_j4_no_self_transform_palaces():
    """金四局基准盘无自化的6个宫也必须正确报无自化"""
    engine = SihuaEngine()

    # 辰(甲): 贪狼无自化
    r = engine.self_transform("甲", ["贪狼"])
    assert r[0]["type"] == "无自化"

    # 巳(乙): 巨门无自化
    r = engine.self_transform("乙", ["巨门"])
    assert r[0]["type"] == "无自化"

    # 未(丁): 天梁无自化 ← 生年禄转移偏见高危点
    r = engine.self_transform("丁", ["天梁"])
    assert r[0]["type"] == "无自化"

    # 酉(己): 天同无自化
    r = engine.self_transform("己", ["天同"])
    assert r[0]["type"] == "无自化"

    # 子(壬): 破军无自化
    r = engine.self_transform("壬", ["破军"])
    assert r[0]["type"] == "无自化"

    # 丑(癸): 天机无自化
    r = engine.self_transform("癸", ["天机"])
    assert r[0]["type"] == "无自化"

    print("✅ test_j4_no_self_transform_palaces 通过")


# ═══════════════════════════════════════════════════════════════
# 三、生年四化转移偏见检查（三个高危点）
# ═══════════════════════════════════════════════════════════════

def test_transfer_bias_three_traps():
    """
    三个转移偏见高危点（生年四化的星在宫干下是否被误判为同名自化）：
      武曲(生年忌) 在庚戌 → 应报警：实为自化权
      天梁(生年禄) 在丁未  → 无偏见（天梁不在丁干四星集）
      左辅(生年科) 在丙午  → 无偏见（左辅不在丙干四星集）
    """
    engine = SihuaEngine()

    # 武曲：应触发偏见告警
    r = engine.check_transfer_bias("壬", "忌", "武曲", "庚")
    assert r["bias_detected"] is True
    assert r["actual_self_xiang"] == "权"

    # 天梁：无偏见（无自化）
    r = engine.check_transfer_bias("壬", "禄", "天梁", "丁")
    assert r["bias_detected"] is False
    assert r["actual_self_xiang"] is None

    # 左辅：无偏见（无自化）
    r = engine.check_transfer_bias("壬", "科", "左辅", "丙")
    assert r["bias_detected"] is False
    assert r["actual_self_xiang"] is None

    print("✅ test_transfer_bias_three_traps 通过")


# ═══════════════════════════════════════════════════════════════
# 四、飞星层测试
# ═══════════════════════════════════════════════════════════════

def test_flying_layer():
    """飞星层：命宫/财帛/官禄/夫妻四宫干飞化"""
    engine = SihuaEngine()

    # 壬干飞化（命宫寅 + 夫妻宫子 同干）
    fly = engine.flying("壬")
    assert fly["飞禄"] == ("天梁", "化禄")
    assert fly["飞权"] == ("紫微", "化权")
    assert fly["飞科"] == ("左辅", "化科")
    assert fly["飞忌"] == ("武曲", "化忌")

    # 庚干飞化（财帛宫戌）
    fly = engine.flying("庚")
    assert fly["飞忌"] == ("天同", "化忌")  # 不是武曲！
    assert fly["飞权"] == ("武曲", "化权")  # 武曲在权列

    # 丙干飞化（官禄宫午）
    fly = engine.flying("丙")
    assert fly["飞忌"] == ("廉贞", "化忌")

    print("✅ test_flying_layer 通过")


def test_flying_to_palaces_j4():
    """
    金四局基准盘命宫(壬寅)飞星层完整推演：
      飞禄天梁→未(交友), 飞权紫微→寅(命宫·自化),
      飞科左辅→午(官禄), 飞忌武曲→戌(财帛)
    """
    engine = SihuaEngine()

    # 金四局基准盘的星曜落宫表
    star_to_palace = {
        "天梁": "未", "紫微": "寅", "左辅": "午", "武曲": "戌",
    }

    results = engine.flying_to_palaces("壬", star_to_palace)

    # 找飞忌
    fei_ji = next(r for r in results if r["象"] == "飞忌")
    assert fei_ji["星"] == "武曲"
    assert fei_ji["落宫"] == "戌"

    # 找飞权
    fei_quan = next(r for r in results if r["象"] == "飞权")
    assert fei_quan["星"] == "紫微"
    assert fei_quan["落宫"] == "寅"  # 命宫自化

    print("✅ test_flying_to_palaces_j4 通过")


# ═══════════════════════════════════════════════════════════════
# 五、自化五步留痕输出格式测试
# ═══════════════════════════════════════════════════════════════

def test_self_transform_verbose_format():
    """五步留痕输出必须包含所有五步"""
    engine = SihuaEngine()
    output = engine.self_transform_verbose("庚", ["武曲"])

    assert "第①步" in output and "庚" in output
    assert "第②步" in output and "四星全集" in output
    assert "第③步" in output and "武曲" in output
    assert "第④⑤步" in output
    assert "自化权" in output  # 关键结论
    print("✅ test_self_transform_verbose_format 通过")


# ═══════════════════════════════════════════════════════════════
# 运行所有测试
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("四化查表/自化判定/飞星层 测试套件")
    print("基准: 十天干四化固定表 + 自化集合匹配算法性质")
    print("=" * 60)
    print()

    test_basic_lookup_all_stems()
    test_lookup_star()
    test_geng_feixing_faction()
    test_j4_self_transform_6_points()
    test_j4_no_self_transform_palaces()
    test_transfer_bias_three_traps()
    test_flying_layer()
    test_flying_to_palaces_j4()
    test_self_transform_verbose_format()

    print()
    print("=" * 60)
    print("🎉 全部测试通过！四化层脚本算法性质验证一致。")
    print("=" * 60)
