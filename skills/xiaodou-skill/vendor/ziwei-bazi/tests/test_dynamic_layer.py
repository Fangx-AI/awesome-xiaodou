"""
test_dynamic_layer.py — 流年动态层测试

测试基准：金四局基准盘（壬戌年）
  - 本命流曜对照（壬年禄存/擎羊/陀罗/天魁/天钺）
  - 2026丙午流年切片（流曜 + 叠宫 + 三叠同位验证）
  - 大限叠宫（午宫大限）
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from paipan_verify import DIZHI
from ziwei_chart import ZiweiEngine, LUCUN_TABLE, KUI_YUE_TABLE
from dynamic_layer import DynamicEngine


def _make_j4_chart():
    """构建金四局基准盘（壬年农历三月初四寅时，年支戌）"""
    zw = ZiweiEngine().cast("壬", 3, 4, 2, "男", "", "戌")
    return zw, DynamicEngine(zw)


# ═══════════════════════════════════════════════════════════════
# 一、流曜算法验证（本命对照）
# ═══════════════════════════════════════════════════════════════

def test_natal_yao_consistency():
    """流曜算法与本命曜规则一致（壬年对照）"""
    zw, dyn = _make_j4_chart()

    # 用流年壬，应与本命壬年曜相同
    yao = dyn.flow_yao("壬")
    assert yao["流禄"] == "亥", f"流禄应亥，得{yao['流禄']}"
    assert yao["流羊"] == "子", f"流羊应子，得{yao['流羊']}"
    assert yao["流陀"] == "戌", f"流陀应戌，得{yao['流陀']}"
    assert yao["流魁"] == "卯", f"流魁应卯，得{yao['流魁']}"
    assert yao["流钺"] == "巳", f"流钺应巳，得{yao['流钺']}"

    print("✅ test_natal_yao_consistency 通过（壬年流曜与本命曜一致）")


def test_2026_flow_yao():
    """2026丙年流曜落宫"""
    zw, dyn = _make_j4_chart()
    yao = dyn.flow_yao("丙")

    # 丙年禄存=巳(查表)，擎羊=午，陀罗=辰
    assert yao["流禄"] == "巳", f"丙年流禄应巳，得{yao['流禄']}"
    assert yao["流羊"] == "午", f"丙年流羊应午，得{yao['流羊']}"
    assert yao["流陀"] == "辰", f"丙年流陀应辰，得{yao['流陀']}"
    # 丙年贵人：天魁=亥，天钺=酉
    assert yao["流魁"] == "亥", f"丙年流魁应亥，得{yao['流魁']}"
    assert yao["流钺"] == "酉", f"丙年流钺应酉，得{yao['流钺']}"

    print("✅ test_2026_flow_yao 通过（2026丙年流曜落宫正确）")


# ═══════════════════════════════════════════════════════════════
# 二、大限叠宫验证
# ═══════════════════════════════════════════════════════════════

def test_daxian_overlay():
    """金四局基准盘午宫大限叠宫（关键：大限财帛=原命宫紫微三权）"""
    zw, dyn = _make_j4_chart()
    overlay = dyn.daxian_overlay("午")

    # 大限命宫=午=原官禄
    assert overlay["大限命宫"]["zhi"] == "午"
    assert overlay["大限命宫"]["原盘宫位"] == "官禄"

    # 大限财帛=寅=原命宫（紫微三权坐此）
    assert overlay["大限财帛"]["zhi"] == "寅"
    assert overlay["大限财帛"]["原盘宫位"] == "命宫"
    assert "紫微" in overlay["大限财帛"]["原盘主星"]

    # 大限官禄=戌=原财帛（武曲五重交战区）
    assert overlay["大限官禄"]["zhi"] == "戌"
    assert overlay["大限官禄"]["原盘宫位"] == "财帛"
    assert "武曲" in overlay["大限官禄"]["原盘主星"]

    # 大限田宅=酉=原疾厄（天同+地空）
    assert overlay["大限田宅"]["zhi"] == "酉"
    assert "地空" in overlay["大限田宅"]["原盘辅星"]

    print("✅ test_daxian_overlay 通过（午宫大限叠宫正确，紫微三权坐大限财帛）")


# ═══════════════════════════════════════════════════════════════
# 三、流年叠宫验证（三叠同位）
# ═══════════════════════════════════════════════════════════════

def test_flow_year_overlay():
    """2026丙午流年叠宫（流年命=大限命=原官禄，三叠同位）"""
    zw, dyn = _make_j4_chart()
    result = dyn.flow_year("丙", "午", "午")

    # 流年命宫=午=大限命宫=原官禄（三叠同位）
    liu_ming = result["流年叠宫"]["流年命宫"]
    assert liu_ming["zhi"] == "午"
    assert liu_ming["原盘宫位"] == "官禄"
    assert liu_ming["大限宫位"] == "命宫"

    # 流年财帛=寅=大限财帛=原命宫
    liu_cai = result["流年叠宫"]["流年财帛"]
    assert liu_cai["zhi"] == "寅"
    assert liu_cai["原盘宫位"] == "命宫"
    assert liu_cai["大限宫位"] == "财帛"

    # 流年官禄=戌=大限官禄=原财帛
    liu_guan = result["流年叠宫"]["流年官禄"]
    assert liu_guan["zhi"] == "戌"
    assert liu_guan["原盘宫位"] == "财帛"
    assert liu_guan["大限宫位"] == "官禄"

    print("✅ test_flow_year_overlay 通过（三叠同位正确，紫微三权坐流年财帛）")


def test_flow_year_feihua():
    """2026丙年流年飞化（丙忌廉贞，与四重廉贞忌分析一致）"""
    zw, dyn = _make_j4_chart()
    result = dyn.flow_year("丙", "午", "午")

    fly = result["流年飞化"]
    assert fly["飞忌"] == ("廉贞", "化忌"), f"丙忌应廉贞，得{fly['飞忌']}"
    assert fly["飞禄"] == ("天同", "化禄")
    assert fly["飞权"] == ("天机", "化权")
    assert fly["飞科"] == ("文昌", "化科")

    print("✅ test_flow_year_feihua 通过（丙忌廉贞，印证四重廉贞忌分析）")


def test_flow_yao_palace_mapping():
    """流曜落到哪个宫+该宫星曜"""
    zw, dyn = _make_j4_chart()
    result = dyn.flow_year("丙", "午", "午")

    # 流禄入巳(田宅·巨门)
    assert result["流曜落宫"]["流禄"]["落宫"] == "巳"
    assert result["流曜落宫"]["流禄"]["该宫原盘位"] == "田宅"
    assert "巨门" in result["流曜落宫"]["流禄"]["该宫主星"]

    # 流羊入午(官禄·廉贞天相) — 流羊冲廉贞
    assert result["流曜落宫"]["流羊"]["落宫"] == "午"
    assert "廉贞" in result["流曜落宫"]["流羊"]["该宫主星"]

    print("✅ test_flow_yao_palace_mapping 通过（流曜落宫星曜映射正确）")


# ═══════════════════════════════════════════════════════════════
# 运行所有测试
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("流年动态层 测试套件")
    print("基准: 金四局基准盘(壬戌年) + 2026丙午流年")
    print("=" * 60)
    print()

    test_natal_yao_consistency()
    test_2026_flow_yao()
    test_daxian_overlay()
    test_flow_year_overlay()
    test_flow_year_feihua()
    test_flow_yao_palace_mapping()

    print()
    print("=" * 60)
    print("🎉 全部测试通过！流年动态层与金四局基准盘分析完全一致。")
    print("   含流曜(禄/羊/陀/魁/钺) + 大限叠宫 + 流年叠宫 + 流年飞化")
    print("=" * 60)
