"""
dynamic_layer.py — 流年动态层引擎（流曜 + 大限叠宫 + 流年叠宫）

将 SOP v2.0 38维度中第16-30项的动态层计算脚本化：
  - 流禄/流羊/流陀（流年禄存/擎羊/陀罗）
  - 流魁/流钺（流年天魁/天钺）
  - 大限叠宫（大限命宫起，逆布十二宫，叠原盘）
  - 流年叠宫（流年太岁坐宫，叠原盘+大限）
  - 流年天干飞化（复用 sihua_lookup）

算法验证基准：壬戌年金四局命例，本命流曜对照全部正确，
大限/流年叠宫与历史手工分析完全一致。

用法:
    from dynamic_layer import DynamicEngine
    from ziwei_chart import ZiweiEngine
    from sihua_lookup import SihuaEngine

    zw = ZiweiEngine().cast("壬", 3, 4, 2, "男", "案例", "戌")
    dyn = DynamicEngine(zw)
    overlay = dyn.daxian_overlay(daxian_ming_zhi="午")
    liu = dyn.flow_year(flow_gan="丙", flow_zhi="午")
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Optional
from paipan_verify import DIZHI
from ziwei_chart import (
    ZiweiChart, KUI_YUE_TABLE, LUCUN_TABLE,
    PALACE_NAMES_ORDER,
)
from sihua_lookup import SihuaEngine


# 十二地支序号映射
DIZHI_IDX = {zhi: i for i, zhi in enumerate(DIZHI)}


class DynamicEngine:
    """流年动态层引擎：流曜 + 叠宫 + 流年飞化"""

    def __init__(self, natal_chart: ZiweiChart):
        """
        Args:
            natal_chart: 本命排盘结果（ZiweiChart 实例）
        """
        self.natal = natal_chart
        self.sihua = SihuaEngine()

    # ─── 1. 流曜（流年禄存/擎羊/陀罗/天魁/天钺）──────────────

    def flow_yao(self, flow_gan: str) -> dict:
        """
        流年五曜：流禄/流羊/流陀/流魁/流钺。
        规则与本命曜相同，只是用流年天干替换生年天干。

        Args:
            flow_gan: 流年天干（甲~癸）

        Returns: {流禄, 流羊, 流陀, 流魁, 流钺}
        """
        # 流禄（流年禄存）
        lu = LUCUN_TABLE[flow_gan]
        lu_idx = DIZHI_IDX[lu]
        # 流羊（流年擎羊）：流禄前一位（顺时针）
        yang = DIZHI[(lu_idx + 1) % 12]
        # 流陀（流年陀罗）：流禄后一位（逆时针）
        tuo = DIZHI[(lu_idx - 1) % 12]
        # 流魁流钺（流年贵人）
        kui, yue = KUI_YUE_TABLE[flow_gan]

        return {
            "流禄": lu,
            "流羊": yang,
            "流陀": tuo,
            "流魁": kui,
            "流钺": yue,
        }

    # ─── 2. 大限叠宫 ──────────────────────────────────────────

    def daxian_overlay(self, daxian_ming_zhi: str) -> dict:
        """
        大限叠宫：以大限命宫地支为基准，逆布十二宫，叠原盘地支。

        Args:
            daxian_ming_zhi: 大限命宫地支（如"午"）

        Returns: {
            "大限命宫": {"zhi":"午","原盘":"官禄","原盘星":[...]},
            "大限财帛": {"zhi":"寅","原盘":"命宫","原盘星":[...]},
            ...
        }
        """
        daxian_ming_idx = DIZHI_IDX[daxian_ming_zhi]
        # 原盘命宫地支
        orig_ming_idx = DIZHI_IDX[self.natal.ming_zhi]

        result = {}
        for i, pname in enumerate(PALACE_NAMES_ORDER):
            # 大限该宫的地支（从大限命宫逆布）
            daxian_p_idx = (daxian_ming_idx - i) % 12
            daxian_zhi = DIZHI[daxian_p_idx]
            # 该地支在原盘对应什么宫位
            orig_palace_idx = (orig_ming_idx - daxian_p_idx) % 12
            orig_palace_name = PALACE_NAMES_ORDER[orig_palace_idx]
            # 该地支在原盘的星曜
            orig_palace = self.natal.get_palace_by_zhi(daxian_zhi)

            result[f"大限{pname}"] = {
                "zhi": daxian_zhi,
                "原盘宫位": orig_palace_name,
                "原盘主星": orig_palace.get("main_stars", []),
                "原盘主星详情": orig_palace.get("main_stars_detail", []),
                "原盘辅星": orig_palace.get("aux_stars", []),
                "原盘宫干": orig_palace.get("stem", ""),
            }

        return result

    # ─── 3. 流年叠宫 ──────────────────────────────────────────

    def flow_year(self, flow_gan: str, flow_zhi: str,
                  daxian_ming_zhi: str = None) -> dict:
        """
        流年完整切片：流曜 + 流年叠宫（叠原盘+大限）+ 流年飞化。

        Args:
            flow_gan: 流年天干（甲~癸）
            flow_zhi: 流年地支（子~亥，即太岁坐宫）
            daxian_ming_zhi: 当下大限命宫地支（如不提供，仅叠原盘）

        Returns: {
            "流年干支": "丙午",
            "流曜": {...},
            "流年叠宫": {...},
            "流年飞化": {...},
        }
        """
        # 流曜
        yao = self.flow_yao(flow_gan)

        # 流年叠宫（从太岁宫起逆布十二宫）
        flow_ming_idx = DIZHI_IDX[flow_zhi]
        orig_ming_idx = DIZHI_IDX[self.natal.ming_zhi]
        daxian_ming_idx = DIZHI_IDX[daxian_ming_zhi] if daxian_ming_zhi else None

        flow_palaces = {}
        for i, pname in enumerate(PALACE_NAMES_ORDER):
            p_idx = (flow_ming_idx - i) % 12
            zhi = DIZHI[p_idx]
            orig_pal_idx = (orig_ming_idx - p_idx) % 12
            orig_pal_name = PALACE_NAMES_ORDER[orig_pal_idx]
            orig_palace = self.natal.get_palace_by_zhi(zhi)

            entry = {
                "zhi": zhi,
                "原盘宫位": orig_pal_name,
                "原盘主星": orig_palace.get("main_stars", []),
                "原盘主星详情": orig_palace.get("main_stars_detail", []),
                "原盘宫干": orig_palace.get("stem", ""),
            }

            if daxian_ming_idx is not None:
                daxian_pal_idx = (daxian_ming_idx - p_idx) % 12
                daxian_pal_name = PALACE_NAMES_ORDER[daxian_pal_idx]
                entry["大限宫位"] = daxian_pal_name

            flow_palaces[f"流年{pname}"] = entry

        # 流年飞化（复用 sihua_lookup）
        fly = self.sihua.flying(flow_gan)

        # 流曜落到哪些宫
        yao_palaces = {}
        for yao_name, yao_zhi in yao.items():
            pal = self.natal.get_palace_by_zhi(yao_zhi)
            yao_palaces[yao_name] = {
                "落宫": yao_zhi,
                "该宫原盘位": pal.get("name", ""),
                "该宫主星": pal.get("main_stars", []),
            }

        return {
            "流年干支": flow_gan + flow_zhi,
            "流曜落宫": yao_palaces,
            "流年叠宫": flow_palaces,
            "流年飞化": fly,
        }

    # ─── 4. 流年叠宫应力摘要（用于报告输出）──────────────────

    def flow_year_summary(self, flow_gan: str, flow_zhi: str,
                          daxian_ming_zhi: str = None) -> str:
        """流年切片的文字摘要（用于报告输出）"""
        result = self.flow_year(flow_gan, flow_zhi, daxian_ming_zhi)
        lines = []
        lines.append(f"流年 {result['流年干支']} 动态层切片")
        lines.append("=" * 50)

        # 流曜
        lines.append("\n【流曜落宫】")
        for yao_name, info in result["流曜落宫"].items():
            stars = "+".join(info["该宫主星"]) if info["该宫主星"] else "无主星"
            lines.append(f"  {yao_name} → {info['落宫']}宫"
                        f"({info['该宫原盘位']}, {stars})")

        # 流年飞化
        lines.append(f"\n【{flow_gan}干流年飞化】")
        fly = result["流年飞化"]
        for key, (star, hua) in fly.items():
            lines.append(f"  {key}: {star}{hua}")

        # 流年叠宫（只显示命/财/官/疾/迁五个核心宫）
        lines.append("\n【流年叠宫（核心五宫）】")
        core = ["命宫", "财帛", "官禄", "疾厄", "迁移"]
        for pname in core:
            key = f"流年{pname}"
            if key in result["流年叠宫"]:
                entry = result["流年叠宫"][key]
                stars = "+".join(
                    s["display"] for s in entry.get("原盘主星详情", [])
                ) or "无主星"
                overlay_info = f"{entry['zhi']}宫(原{entry['原盘宫位']}"
                if "大限宫位" in entry:
                    overlay_info += f"/大限{entry['大限宫位']}"
                overlay_info += ")"
                lines.append(f"  流年{pname}: {overlay_info} [{stars}]")

        return "\n".join(lines)


# ─── 命令行入口 ──────────────────────────────────────────────────

def main():
    import sys
    if len(sys.argv) < 10:
        print("用法: python dynamic_layer.py <年干> <农历月> <农历日> <时辰地支> <男/女> <年支> <流年干> <流年地支> [大限命宫地支] [备注]")
        print("例: python dynamic_layer.py 壬 3 4 寅 男 戌 丙 午 午 案例")
        print("  生辰: 壬年3月初4寅时男戌(年支)")
        print("  流年: 丙午年")
        print("  大限: 午宫")
        return

    year_gan = sys.argv[1]
    lunar_month = int(sys.argv[2])
    lunar_day = int(sys.argv[3])
    zhi_hour = sys.argv[4]
    gender = sys.argv[5]
    year_zhi = sys.argv[6]
    flow_gan = sys.argv[7]
    flow_zhi = sys.argv[8]
    daxian_ming = sys.argv[9] if len(sys.argv) > 9 else None
    note = sys.argv[10] if len(sys.argv) > 10 else ""

    zhi_hour_idx = DIZHI.index(zhi_hour)
    # 在函数内重新导入，避免命名空间问题
    from ziwei_chart import ZiweiEngine as _ZW
    zw = _ZW().cast(year_gan, lunar_month, lunar_day, zhi_hour_idx,
                    gender, note, year_zhi)
    dyn = DynamicEngine(zw)

    if daxian_ming:
        print(dyn.flow_year_summary(flow_gan, flow_zhi, daxian_ming))
    else:
        print(dyn.flow_year_summary(flow_gan, flow_zhi))


if __name__ == "__main__":
    main()
