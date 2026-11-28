"""
test_paipan_verify.py — 八字排盘核验测试

测试基准：三个与任何真实命主无关的**虚构日期**，覆盖关键分支：
  - Case-A (2000-7-20 男)：庚辰年阳干男 → 大运顺行
  - Case-B (2013-10-1 男)：癸巳年阴干男 → 大运逆行
  - Case-C (2008-1-20 女)：立春前出生 → 年柱属上一年(丁亥)

每个虚构基准的四柱、藏干、纳音、旬空、大运方向均由权威历法库
lunar_python（天文精确节气）独立计算得出，避免"用脚本验证脚本"的循环。
JDN偏移量=49，经多命例交叉校准。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from paipan_verify import BaziEngine, TIANGAN, DIZHI, sexagenary


def test_case_a_yang_male_forward():
    """Case-A: 2000-7-20 10:30 男 — 庚辰/癸未/己卯/己巳，阳干男大运顺。
    期望值由 lunar_python 独立计算（庚阳干+男=顺行）。"""
    engine = BaziEngine()
    c = engine.cast(2000, 7, 20, 10.5, True, "Case-A")

    assert c.year_gz == "庚辰"
    assert c.month_gz == "癸未"
    assert c.day_gz == "己卯"
    assert c.hour_gz == "己巳"
    assert c.xunkong == ("申", "酉")
    assert c.dayun_forward is True  # 庚阳干男 → 顺
    assert c.dayun[0:5] == ["甲申", "乙酉", "丙戌", "丁亥", "戊子"]
    assert c.year_nayin == "白蜡金"
    assert c.month_nayin == "杨柳木"
    assert c.day_nayin == "城头土"
    assert c.hour_nayin == "大林木"
    assert c.year_zang == ["戊", "乙", "癸"]
    assert c.day_zang == ["乙"]

    print("✅ test_case_a_yang_male_forward 通过（庚辰/癸未/己卯/己巳，旬空申酉，大运顺甲申起）")


def test_case_b_yin_male_reverse():
    """Case-B: 2013-10-1 8:00 男 — 癸巳/辛酉/庚子/庚辰，阴干男大运逆。
    期望值由 lunar_python 独立计算（癸阴干+男=逆行）。"""
    engine = BaziEngine()
    c = engine.cast(2013, 10, 1, 8.0, True, "Case-B")

    assert c.year_gz == "癸巳"
    assert c.month_gz == "辛酉"
    assert c.day_gz == "庚子"
    assert c.hour_gz == "庚辰"
    assert c.xunkong == ("辰", "巳")
    assert c.dayun_forward is False  # 癸阴干男 → 逆
    assert c.dayun[0:5] == ["庚申", "己未", "戊午", "丁巳", "丙辰"]
    assert c.year_nayin == "长流水"
    assert c.day_nayin == "壁上土"

    print("✅ test_case_b_yin_male_reverse 通过（癸巳/辛酉/庚子/庚辰，旬空辰巳，大运逆庚申起）")


def test_case_c_lichun_boundary():
    """Case-C: 2008-1-20 6:00 女 — 立春前出生，年柱属上一年。
    公历2008-1-20在立春(2/4)前，年柱应为2007的丁亥而非2008的戊子。
    期望值由 lunar_python 独立计算（丁阴干+女=顺行）。"""
    engine = BaziEngine()
    c = engine.cast(2008, 1, 20, 6.0, False, "Case-C")

    assert c.year_gz == "丁亥"  # 立春分界关键：1月属上年
    assert c.month_gz == "癸丑"
    assert c.day_gz == "己未"
    assert c.hour_gz == "丁卯"
    assert c.xunkong == ("子", "丑")
    assert c.dayun_forward is True  # 丁阴干女 → 顺
    assert c.dayun[0:5] == ["甲寅", "乙卯", "丙辰", "丁巳", "戊午"]
    assert c.year_nayin == "屋上土"

    print("✅ test_case_c_lichun_boundary 通过（丁亥/癸丑/己未/丁卯，立春分界正确）")


def test_jdn_offset_cross_validation():
    """JDN偏移量交叉校验：三个虚构日期的日柱必须全部正确"""
    from paipan_verify import date_to_jdn, jdn_to_day_gz

    cases = [
        (2000, 7, 20, "己卯"),
        (2013, 10, 1, "庚子"),
        (2008, 1, 20, "己未"),
    ]
    for y, m, d, expected in cases:
        from datetime import datetime
        jdn = date_to_jdn(datetime(y, m, d))
        actual = jdn_to_day_gz(jdn)
        assert actual == expected, f"{y}-{m}-{d}: 得{actual}, 期望{expected}"

    print("✅ test_jdn_offset_cross_validation 通过（JDN偏移=49经三虚构日期校准）")


def test_sexagenary_cycle():
    """六十甲子完整性：60个干支各不相同且干支相配"""
    all_gz = [sexagenary(i) for i in range(60)]
    assert len(set(all_gz)) == 60  # 无重复
    # 阳干配阳支，阴干配阴支
    for i, gz in enumerate(all_gz):
        gan_yangyin = i % 2  # 0=阳(甲丙戊庚壬), 1=阴
        zhi_yangyin = i % 2
        assert TIANGAN.index(gz[0]) % 2 == gan_yangyin
        assert DIZHI.index(gz[1]) % 2 == zhi_yangyin

    print("✅ test_sexagenary_cycle 通过（六十甲子完整无重复）")


def test_xunkong_algorithm():
    """旬空算法验证"""
    from paipan_verify import get_xunkong

    # 庚戌(甲辰旬) → 旬空寅卯
    assert get_xunkong("庚戌") == ("寅", "卯")
    # 丙辰(甲寅旬) → 旬空子丑
    assert get_xunkong("丙辰") == ("子", "丑")
    # 甲子(甲子旬本身) → 旬空戌亥
    assert get_xunkong("甲子") == ("戌", "亥")

    print("✅ test_xunkong_algorithm 通过")


def test_nayin():
    """纳音查表验证"""
    from paipan_verify import get_nayin

    assert get_nayin("壬戌") == "大海水"
    assert get_nayin("癸卯") == "金箔金"
    assert get_nayin("丙辰") == "沙中土"
    assert get_nayin("甲子") == "海中金"
    assert get_nayin("己丑") == "霹雳火"

    print("✅ test_nayin 通过")


if __name__ == "__main__":
    print("=" * 60)
    print("八字排盘核验 测试套件")
    print("基准: 3个虚构日期（期望值由 lunar_python 独立计算）")
    print("=" * 60)
    print()

    test_case_a_yang_male_forward()
    test_case_b_yin_male_reverse()
    test_case_c_lichun_boundary()
    test_jdn_offset_cross_validation()
    test_sexagenary_cycle()
    test_xunkong_algorithm()
    test_nayin()

    print()
    print("=" * 60)
    print("🎉 全部测试通过！八字排盘核验与权威历法库完全一致。")
    print("=" * 60)
