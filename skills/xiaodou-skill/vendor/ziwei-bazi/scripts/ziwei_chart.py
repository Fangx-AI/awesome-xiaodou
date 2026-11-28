"""
ziwei_chart.py — 紫微斗数排盘核验引擎

将紫微排盘中"LLM 几乎必错"的确定性计算工序脚本化：
  - 命宫/身宫定位（农历月 + 时辰）
  - 五行局（命宫干支纳音）
  - 紫微星落宫（局数 + 生日 → 定局表）
  - 十四主星布局（紫微系逆行 + 天府系顺行）
  - 十二宫天干（五虎遁起寅）
  - 十二宫位排列（命宫起，逆时针布十二宫）
  - 来因宫（生年干所落之宫）

基准锚点（金标准交叉校验，已脱敏）：
  - 金四局（农历初四，寅时）：14主星全部验证通过 ✓
  - 水二局（农历十一，午时）：14主星全部验证通过 ✓（覆盖非整除路径）

安星口诀（标准）：
  紫微系(逆): 紫→天机→[隔1]→太阳→武曲→天同→[隔2]→廉贞
  天府系(顺): 府→太阴→贪狼→巨门→天相→天梁→七杀→[隔3]→破军
  天府 = 紫微以寅申轴镜像（序号取负 mod 12）

用法:
    from ziwei_chart import ZiweiEngine
    engine = ZiweiEngine()
    chart = engine.cast(
        year_gan="壬", lunar_month=3, lunar_day=4,
        zhi_hour_idx=2,  # 寅时=2
        gender="男",
    )
    print(chart.summary())
"""

from typing import Optional
from paipan_verify import TIANGAN, DIZHI, get_nayin


# 十二宫位名称（从命宫起，逆时针）
# 顺序: 命宫→兄弟→夫妻→子女→财帛→疾厄→迁移→交友→官禄→田宅→福德→父母
PALACE_NAMES_ORDER = [
    "命宫", "兄弟", "夫妻", "子女", "财帛", "疾厄",
    "迁移", "交友", "官禄", "田宅", "福德", "父母",
]

# 地支（从寅起顺数，因为命宫算法以寅为基准）
# 但十二宫排布的地支取决于命宫地支
PALACE_LIST = list(DIZHI)  # 子丑寅卯辰巳午未申酉戌亥

# ─── 五虎遁（年干 → 寅宫天干）──────────────────────────────────
YEAR_TO_YINGAN = {
    "甲": 2, "己": 2,   # 丙
    "乙": 4, "庚": 4,   # 戊
    "丙": 6, "辛": 6,   # 庚
    "丁": 8, "壬": 8,   # 壬
    "戊": 0, "癸": 0,   # 甲
}

# ─── 紫微定星表（局数 + 生日 → 紫微落宫，子=0基准）─────────────
# 固定查表，数据来源：《紫微斗数全书》安紫微诀（与文墨天机等排盘软件一致）。
# 表值 = 紫微星在十二地支宫的序号（子=0,丑=1,...,亥=11）。
#
# 验证基准（金标准交叉校验）：
#   - 金四局日4 → 寅(2)：与已验证命例金标准一致
#   - 水二局日11 → 午(6)：与已验证命例金标准一致，14主星全对
#   - 水二局日1 → 丑(1)：全书铁律
#   - 五局×30日=150个值逐点覆盖，无冲突、无遗漏
ZW_POS_TABLE_SUB0 = {
    2: [1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 0, 0, 1, 1, 2, 2, 3, 3, 4],
    3: [4, 1, 2, 5, 2, 3, 6, 3, 4, 7, 4, 5, 8, 5, 6, 9, 6, 7, 10, 7, 8, 11, 8, 9, 0, 9, 10, 1, 10, 11],
    4: [11, 4, 1, 2, 0, 5, 2, 3, 1, 6, 3, 4, 2, 7, 4, 5, 3, 8, 5, 6, 4, 9, 6, 7, 5, 10, 7, 8, 6, 11],
    5: [6, 11, 4, 1, 2, 7, 0, 5, 2, 3, 8, 1, 6, 3, 4, 9, 2, 7, 4, 5, 10, 3, 8, 5, 6, 11, 4, 9, 6, 7],
    6: [9, 6, 11, 4, 1, 2, 10, 7, 0, 5, 2, 3, 11, 8, 1, 6, 3, 4, 0, 9, 2, 7, 4, 5, 1, 10, 3, 8, 5, 6],
}

def _ziwei_pos(ju: int, day: int) -> int:
    """
    紫微定星 — 返回落宫序号（寅=0基准）。
    查 ZW_POS_TABLE_SUB0（子=0基准）后转换为寅=0基准。

    本表替代早期版本基于"商奇余偶进退"口诀的算法实现。
    口诀法在非整除路径（day 不被 ju 整除）上判定错误，
    例如火六局序列会在寅卯之间反复横跳，违反"每局数日紫微前进"的
    基本规律。紫微定星本质是千年固定查表数据，与 SIHUA_TABLE 同源，
    故改为直接焊入查表以消灭该路径的幻觉。
    """
    if ju not in ZW_POS_TABLE_SUB0:
        raise ValueError(f"无效局数: {ju}（应为 2/3/4/5/6）")
    if not 1 <= day <= 30:
        raise ValueError(f"无效农历日: {day}（应为 1-30）")
    return (ZW_POS_TABLE_SUB0[ju][day - 1] - 2) % 12  # 子0基准 → 寅0基准

# ─── 五行局判定（命宫干支 → 纳音 → 局）─────────────────────────
NAYIN_TO_JU = {
    "水": 2,  # 水二局
    "木": 3,  # 木三局
    "金": 4,  # 金四局
    "土": 5,  # 土五局
    "火": 6,  # 火六局
}

def _nayin_to_ju(nayin: str) -> int:
    """纳音 → 五行局数。如 '金箔金' → 4"""
    for element, ju in NAYIN_TO_JU.items():
        if element in nayin:
            return ju
    raise ValueError(f"无法从纳音'{nayin}'判定五行局")


# ─── 辅星排布查表（14辅星：六吉六煞+禄存天马）──────────────────

# 天魁天钺：年干查表（贵人星）
KUI_YUE_TABLE = {
    "甲": ("丑", "未"), "戊": ("丑", "未"), "庚": ("丑", "未"),
    "乙": ("子", "申"), "己": ("子", "申"),
    "丙": ("亥", "酉"), "丁": ("亥", "酉"),
    "辛": ("午", "寅"),
    "壬": ("卯", "巳"), "癸": ("卯", "巳"),
}

# 禄存：年干查表（财库星）
LUCUN_TABLE = {
    "甲": "寅", "乙": "卯", "丙": "巳", "戊": "巳", "丁": "午", "己": "午",
    "庚": "申", "辛": "酉", "壬": "亥", "癸": "子",
}

# 天马：年支三合查表（驿马星）
TIANMA_TABLE = {
    "寅": "申", "午": "申", "戌": "申",
    "申": "寅", "子": "寅", "辰": "寅",
    "巳": "亥", "酉": "亥", "丑": "亥",
    "亥": "巳", "卯": "巳", "未": "巳",
}

# 火星铃星起点：年支三合分组 → 起始地支序号
HUO_START = {  # 寅午戌→丑(1), 申子辰→寅(2), 巳酉丑→卯(3), 亥卯未→戌(10)
    "寅": 1, "午": 1, "戌": 1,
    "申": 2, "子": 2, "辰": 2,
    "巳": 3, "酉": 3, "丑": 3,
    "亥": 10, "卯": 10, "未": 10,
}
LING_START = {  # 寅午戌→卯(3), 申子辰→辰(4), 巳酉丑→巳(5), 亥卯未→子(0)
    "寅": 3, "午": 3, "戌": 3,
    "申": 4, "子": 4, "辰": 4,
    "巳": 5, "酉": 5, "丑": 5,
    "亥": 0, "卯": 0, "未": 0,
}

# ─── 十四主星庙旺平陷查表 ──────────────────────────────────────
# 读法: STAR_MIAOXIAN[星][地支序号(子0丑1...亥11)] → 庙/旺/得/利/平/陷
# 7级标准: 庙(最亮)>旺>得>利>平>不>陷(最暗), 本表合并为5档(得→旺,不→平)
# 验证基准: 已验证命例盘14个已知点全部正确（金四局整除路径）
STAR_MIAOXIAN = {
    "紫微":  {0:"平",1:"平",2:"旺",3:"旺",4:"旺",5:"旺",6:"庙",7:"庙",8:"庙",9:"庙",10:"庙",11:"旺"},
    "天机":  {0:"旺",1:"陷",2:"利",3:"庙",4:"旺",5:"平",6:"陷",7:"陷",8:"得",9:"旺",10:"利",11:"平"},
    "太阳":  {0:"陷",1:"陷",2:"陷",3:"陷",4:"旺",5:"庙",6:"庙",7:"庙",8:"旺",9:"平",10:"利",11:"陷"},
    "武曲":  {0:"庙",1:"庙",2:"平",3:"平",4:"庙",5:"庙",6:"旺",7:"旺",8:"利",9:"利",10:"庙",11:"陷"},
    "天同":  {0:"旺",1:"庙",2:"利",3:"平",4:"陷",5:"陷",6:"庙",7:"旺",8:"平",9:"平",10:"利",11:"旺"},
    "廉贞":  {0:"庙",1:"庙",2:"庙",3:"陷",4:"陷",5:"陷",6:"平",7:"平",8:"庙",9:"陷",10:"利",11:"利"},
    "天府":  {0:"庙",1:"庙",2:"庙",3:"旺",4:"平",5:"平",6:"平",7:"平",8:"旺",9:"旺",10:"庙",11:"庙"},
    "太阴":  {0:"庙",1:"庙",2:"旺",3:"陷",4:"陷",5:"陷",6:"陷",7:"陷",8:"陷",9:"利",10:"庙",11:"庙"},
    "贪狼":  {0:"陷",1:"陷",2:"平",3:"陷",4:"庙",5:"旺",6:"旺",7:"庙",8:"陷",9:"陷",10:"庙",11:"平"},
    "巨门":  {0:"陷",1:"陷",2:"陷",3:"陷",4:"陷",5:"旺",6:"陷",7:"陷",8:"庙",9:"庙",10:"庙",11:"平"},
    "天相":  {0:"庙",1:"庙",2:"利",3:"陷",4:"陷",5:"庙",6:"庙",7:"平",8:"平",9:"陷",10:"陷",11:"陷"},
    "天梁":  {0:"陷",1:"陷",2:"陷",3:"陷",4:"庙",5:"陷",6:"陷",7:"旺",8:"陷",9:"庙",10:"陷",11:"陷"},
    "七杀":  {0:"陷",1:"陷",2:"庙",3:"陷",4:"陷",5:"旺",6:"庙",7:"陷",8:"庙",9:"平",10:"旺",11:"陷"},
    "破军":  {0:"庙",1:"陷",2:"庙",3:"平",4:"陷",5:"陷",6:"平",7:"陷",8:"庙",9:"平",10:"庙",11:"平"},
}

def get_miaoxian(star: str, zhi_idx: int) -> str:
    """查主星在地支宫位的庙旺平陷。返回 庙/旺/得/利/平/陷 或 None(非主星)"""
    if star in STAR_MIAOXIAN:
        return STAR_MIAOXIAN[star].get(zhi_idx)
    return None


# ═══════════════════════════════════════════════════════════════
# ZiweiChart: 排盘结果
# ═══════════════════════════════════════════════════════════════

class ZiweiChart:
    """紫微排盘结果"""

    def __init__(self, data: dict):
        self.data = data

    def __getattr__(self, name):
        return self.data.get(name)

    def get_palace(self, palace_name: str) -> dict:
        """按宫位名查询（命宫/财帛/...）"""
        return self.data["palaces"].get(palace_name, {})

    def get_palace_by_zhi(self, zhi: str) -> dict:
        """按地支查询（寅/卯/...）"""
        return self.data["palaces_by_zhi"].get(zhi, {})

    def summary(self) -> str:
        d = self.data
        lines = []
        lines.append(f"命主: {d.get('note', '?')}")
        lines.append(f"年干: {d['year_gan']}  农历: {d['lunar_month']}月{d['lunar_day']}日  时辰: {DIZHI[d['zhi_hour_idx']]}时")
        lines.append(f"命宫: {d['ming_zhi']}  身宫: {d['shen_zhi']}")
        lines.append(f"命宫干支: {d['ming_ganzhi']} → 纳音{d['ming_nayin']} → {d['wuxing_ju_name']}")
        lines.append(f"紫微星: {d['ziwei_zhi']}  天府星: {d['tianfu_zhi']}")
        lines.append(f"来因宫: {d['laiyin_palace']}({d['laiyin_zhi']})")
        lines.append("")
        lines.append("=== 十二宫主星(庙陷)+辅星 ===")
        for zhi_idx in range(12):
            zhi = DIZHI[zhi_idx]
            palace = self.get_palace_by_zhi(zhi)
            name = palace.get("name", "")
            main_detail = palace.get("main_stars_detail", [])
            aux_stars = palace.get("aux_stars", [])
            stem = palace.get("stem", "")
            if main_detail:
                stars_str = "+".join(s["display"] for s in main_detail)
            else:
                stars_str = "（无主星）"
            aux_str = " ".join(aux_stars) if aux_stars else ""
            lines.append(f"  {zhi}宫({stem}{zhi}) [{name}]: {stars_str}" +
                        (f" ｜ 辅: {aux_str}" if aux_str else ""))
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# ZiweiEngine: 排盘引擎
# ═══════════════════════════════════════════════════════════════

class ZiweiEngine:

    def cast(self, year_gan: str, lunar_month: int, lunar_day: int,
             zhi_hour_idx: int, gender: str, note: str = "",
             year_zhi: str = "") -> ZiweiChart:
        """
        紫微排盘。

        Args:
            year_gan: 生年天干（甲~癸）。注意：以立春为年界。
            lunar_month: 农历月（1=正月）
            lunar_day: 农历日（1-30）
            zhi_hour_idx: 时辰地支序号（子0丑1寅2...）
            gender: "男"/"女"
            note: 命主备注
            year_zhi: 生年地支（子~亥）。用于辅星排布（天马/火星/铃星）。
                     如不提供，辅星中依赖年支的三颗(天马/火星/铃星)将无法排布。
        """
        # === 命宫/身宫 ===
        # 月支：正月=寅(2)，顺推
        month_zhi_idx = (2 + lunar_month - 1) % 12
        # 命宫：从月支逆数生时
        ming_idx = (month_zhi_idx - zhi_hour_idx) % 12
        # 身宫：从月支顺数生时
        shen_idx = (month_zhi_idx + zhi_hour_idx) % 12
        ming_zhi = DIZHI[ming_idx]
        shen_zhi = DIZHI[shen_idx]

        # === 十二宫干（五虎遁起寅）===
        yin_gan_idx = YEAR_TO_YINGAN[year_gan]
        palace_stems = {}
        for i in range(12):
            zhi = DIZHI[(2 + i) % 12]  # 从寅起
            gan = TIANGAN[(yin_gan_idx + i) % 10]
            palace_stems[zhi] = gan
        ming_stem = palace_stems[ming_zhi]
        ming_ganzhi = ming_stem + ming_zhi

        # === 五行局（命宫纳音）===
        ming_nayin = get_nayin(ming_ganzhi)
        wuxing_ju = _nayin_to_ju(ming_nayin)
        wuxing_ju_name = {2: "水二局", 3: "木三局", 4: "金四局",
                          5: "土五局", 6: "火六局"}[wuxing_ju]

        # === 紫微星落宫 ===
        # 定局表用寅=0基准
        ziwei_pos_yin_base = _ziwei_pos(wuxing_ju, lunar_day)
        # 转为标准地支序号
        ziwei_idx = (2 + ziwei_pos_yin_base) % 12
        ziwei_zhi = DIZHI[ziwei_idx]

        # === 天府星（紫微镜像）===
        tianfu_idx = (4 - ziwei_idx) % 12  # 紫微+天府关于寅申轴，序号和=4(对应寅+寅=2+2=4)
        # 更准确：天府序 = (4 - 紫微序) % 12。已验证：紫微寅(2)→天府(4-2=2)=寅 ✓
        tianfu_zhi = DIZHI[tianfu_idx]

        # === 十四主星布局 ===
        stars_map = self._layout_14stars(ziwei_idx, tianfu_idx)

        # === 辅星排布（14辅星）===
        aux_stars_map = self._layout_aux_stars(
            year_gan, year_zhi, lunar_month, zhi_hour_idx
        )

        # === 十二宫位排列（命宫起逆时针）===
        # 命宫在ming_idx，逆时针(序号递减)布十二宫
        palaces = {}
        palaces_by_zhi = {}
        for i, pname in enumerate(PALACE_NAMES_ORDER):
            p_idx = (ming_idx - i) % 12  # 逆时针
            zhi = DIZHI[p_idx]
            stem = palace_stems[zhi]
            main_stars = stars_map.get(p_idx, [])
            aux_stars = aux_stars_map.get(p_idx, [])
            # 主星庙陷
            main_stars_with_mx = []
            for star in main_stars:
                mx = get_miaoxian(star, p_idx)
                main_stars_with_mx.append({
                    "star": star,
                    "miaoxian": mx or "",
                    "display": f"{star}({mx})" if mx else star,
                })
            palace_data = {
                "name": pname,
                "zhi": zhi,
                "stem": stem,
                "ganzhi": stem + zhi,
                "main_stars": main_stars,
                "main_stars_detail": main_stars_with_mx,
                "aux_stars": aux_stars,
                "is_ming": (pname == "命宫"),
                "is_shen": (zhi == shen_zhi),
            }
            palaces[pname] = palace_data
            palaces_by_zhi[zhi] = palace_data

        # === 来因宫（生年干所落之宫）===
        year_gan_idx = TIANGAN.index(year_gan)
        laiyin_palace = None
        laiyin_zhi = None
        for zhi, stem in palace_stems.items():
            if TIANGAN.index(stem) == year_gan_idx:
                laiyin_zhi = zhi
                laiyin_palace = palaces_by_zhi[zhi]["name"]
                break

        return ZiweiChart({
            "note": note,
            "year_gan": year_gan,
            "year_zhi": year_zhi,
            "lunar_month": lunar_month,
            "lunar_day": lunar_day,
            "zhi_hour_idx": zhi_hour_idx,
            "gender": gender,
            "ming_zhi": ming_zhi,
            "shen_zhi": shen_zhi,
            "ming_ganzhi": ming_ganzhi,
            "ming_nayin": ming_nayin,
            "wuxing_ju": wuxing_ju,
            "wuxing_ju_name": wuxing_ju_name,
            "ziwei_idx": ziwei_idx,
            "ziwei_zhi": ziwei_zhi,
            "tianfu_idx": tianfu_idx,
            "tianfu_zhi": tianfu_zhi,
            "laiyin_palace": laiyin_palace,
            "laiyin_zhi": laiyin_zhi,
            "palaces": palaces,
            "palaces_by_zhi": palaces_by_zhi,
            "stars_map": stars_map,
            "aux_stars_map": aux_stars_map,
        })

    def _layout_14stars(self, ziwei_idx: int, tianfu_idx: int) -> dict:
        """
        十四主星布局。
        返回 {宫位序号(0-11标准): [星曜列表]}

        紫微系(逆): 紫→天机→[隔1]→太阳→武曲→天同→[隔2]→廉贞
        天府系(顺): 府→太阴→贪狼→巨门→天相→天梁→七杀→[隔3]→破军
        """
        result = {}

        def add_star(idx, star):
            idx = idx % 12
            if idx not in result:
                result[idx] = []
            result[idx].append(star)

        # 紫微系（逆时针，从紫微起序号递减）
        add_star(ziwei_idx, "紫微")
        add_star(ziwei_idx - 1, "天机")
        # 隔1 → 太阳
        add_star(ziwei_idx - 3, "太阳")
        add_star(ziwei_idx - 4, "武曲")
        add_star(ziwei_idx - 5, "天同")
        # 隔2 → 廉贞
        add_star(ziwei_idx - 8, "廉贞")

        # 天府系（顺时针，从天府起序号递增）
        add_star(tianfu_idx, "天府")
        add_star(tianfu_idx + 1, "太阴")
        add_star(tianfu_idx + 2, "贪狼")
        add_star(tianfu_idx + 3, "巨门")
        add_star(tianfu_idx + 4, "天相")
        add_star(tianfu_idx + 5, "天梁")
        add_star(tianfu_idx + 6, "七杀")
        # 隔3 → 破军
        add_star(tianfu_idx + 10, "破军")

        return result

    def _layout_aux_stars(self, year_gan: str, year_zhi: str,
                          lunar_month: int, zhi_hour_idx: int) -> dict:
        """
        14辅星排布。返回 {宫位序号(0-11标准): [辅星列表]}

        安星规则（标准）：
          左辅: 从辰起正月，顺数到生月
          右弼: 从戌起正月，逆数到生月
          文昌: 从戌起子时，逆数到生时
          文曲: 从辰起子时，顺数到生时
          天魁/天钺: 年干查表（贵人星）
          禄存: 年干查表（财库星）
          天马: 年支三合查表（驿马星）
          擎羊: 禄存前一位
          陀罗: 禄存后一位
          地空: 从亥起子时，逆数到生时
          地劫: 从亥起子时，顺数到生时
          火星/铃星: 年支三合定起点 + 顺数到生时

        验证：已验证命例盘14辅星全部正确（金四局整除路径）。
        """
        result = {}

        def add_star(idx, star):
            idx = idx % 12
            if idx not in result:
                result[idx] = []
            result[idx].append(star)

        # 辰=4, 戌=10, 亥=11
        # 左辅: 辰起正月顺数
        add_star(4 + lunar_month - 1, "左辅")
        # 右弼: 戌起正月逆数
        add_star(10 - (lunar_month - 1), "右弼")
        # 文昌: 戌起子时逆数
        add_star(10 - zhi_hour_idx, "文昌")
        # 文曲: 辰起子时顺数
        add_star(4 + zhi_hour_idx, "文曲")

        # 天魁天钺（年干查表）
        if year_gan in KUI_YUE_TABLE:
            kui, yue = KUI_YUE_TABLE[year_gan]
            add_star(DIZHI.index(kui), "天魁")
            add_star(DIZHI.index(yue), "天钺")

        # 禄存（年干查表）
        if year_gan in LUCUN_TABLE:
            lucun_zhi = LUCUN_TABLE[year_gan]
            lucun_idx = DIZHI.index(lucun_zhi)
            add_star(lucun_idx, "禄存")
            # 擎羊: 禄存前一位（顺时针下一宫）
            add_star((lucun_idx + 1) % 12, "擎羊")
            # 陀罗: 禄存后一位（逆时针上一宫）
            add_star((lucun_idx - 1) % 12, "陀罗")

        # 天马（年支三合查表）
        if year_zhi and year_zhi in TIANMA_TABLE:
            add_star(DIZHI.index(TIANMA_TABLE[year_zhi]), "天马")

        # 地空地劫（从亥起子时）
        add_star(11 - zhi_hour_idx, "地空")
        add_star(11 + zhi_hour_idx, "地劫")

        # 火星铃星（年支三合定起点 + 顺数到生时）
        if year_zhi and year_zhi in HUO_START:
            huo_idx = (HUO_START[year_zhi] + zhi_hour_idx) % 12
            ling_idx = (LING_START[year_zhi] + zhi_hour_idx) % 12
            add_star(huo_idx, "火星")
            add_star(ling_idx, "铃星")

        return result


# ─── 命令行入口 ──────────────────────────────────────────────────

def main():
    import sys
    if len(sys.argv) < 6:
        print("用法: python ziwei_chart.py <年干> <农历月> <农历日> <时辰地支> <男/女> [年支] [备注]")
        print("时辰地支: 子/丑/寅/卯/辰/巳/午/未/申/酉/戌/亥")
        print("年支用于辅星排布(天马/火星/铃星),建议提供")
        print("例: python ziwei_chart.py 壬 3 4 寅 男 戌 案例")
        return

    year_gan = sys.argv[1]
    lunar_month = int(sys.argv[2])
    lunar_day = int(sys.argv[3])
    zhi_hour = sys.argv[4]
    gender = sys.argv[5]
    year_zhi = ""
    note = ""
    # 第6个参数可能是年支也可能是备注
    if len(sys.argv) > 6:
        if sys.argv[6] in DIZHI:
            year_zhi = sys.argv[6]
            note = sys.argv[7] if len(sys.argv) > 7 else ""
        else:
            note = sys.argv[6]
    zhi_hour_idx = DIZHI.index(zhi_hour)

    engine = ZiweiEngine()
    chart = engine.cast(year_gan, lunar_month, lunar_day, zhi_hour_idx, gender, note, year_zhi)
    print(chart.summary())


if __name__ == "__main__":
    main()
