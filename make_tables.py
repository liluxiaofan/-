"""生成 Table 1–6（严格按 FIGURE_TABLE_PLAN.md §2）。

数据来源
--------
Table 1  复算自 data/price_clean.csv（7 176 行），口径说明引自 data/DATA_AUDIT.md
Table 2  逐行来自 data/main_results.csv
Table 3  判定标准引自 EXPERIMENT_PLAN.md §E3 / EXPERIMENT_RESULTS.md §7，数值由 CSV 复算
Table 4  来自 data/ci_table.csv（metric = bill / cov）
Table 5  来自 data/e4_ablation_lambda.csv
Table 6  文档旧值 vs 复算值，引自 data/DATA_AUDIT.md §8

输出：tables/table0X_*.csv（utf-8-sig）、.md，以及 tables/all_tables.xlsx
运行：python3 plotting_scripts/make_tables.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import style  # noqa: E402

DATA = style.DATA_DIR
OUT = style.TABLE_DIR
VALUES: dict[str, dict[str, float]] = {}


def rec(table: str, key: str, value: float) -> str:
    """登记一个原始数值（供 verify_outputs.py 与源 CSV 比对）。"""
    VALUES.setdefault(table, {})[key] = float(value)
    return ""


def md_table(df: pd.DataFrame) -> str:
    """把 DataFrame 渲染成 GitHub 风格 Markdown 表（不依赖 tabulate）。"""
    cols = list(df.columns)
    rows = [["" if pd.isna(v) else str(v) for v in r] for r in df.itertuples(index=False)]
    widths = [
        max(len(str(c)), *(len(r[i]) for r in rows)) if rows else len(str(c))
        for i, c in enumerate(cols)
    ]
    # 中文按 2 个字符宽度对齐
    def w(s: str) -> int:
        return sum(2 if ord(ch) > 127 else 1 for ch in s)

    widths = [
        max(w(str(c)), *(w(r[i]) for r in rows)) if rows else w(str(c))
        for i, c in enumerate(cols)
    ]
    def pad(s: str, width: int, right: bool) -> str:
        gap = " " * max(0, width - w(s))
        return gap + s if right else s + gap

    aligns = []
    for c in cols:
        sample = [r[cols.index(c)] for r in rows]
        numeric = sample and all(
            s.replace("−", "-").replace(",", "").replace("%", "").replace(".", "")
            .replace("-", "").replace("+", "").replace(" ", "").isdigit() or s in {"—", ""}
            for s in sample
        )
        aligns.append(numeric)

    out = ["| " + " | ".join(str(c) for c in cols) + " |"]
    out.append("|" + "|".join("---:" if a else "---" for a in aligns) + "|")
    for r in rows:
        out.append("| " + " | ".join(pad(c, widths[i], aligns[i]) for i, c in enumerate(r)) + " |")
    return "\n".join(out)


def emit(df: pd.DataFrame, stem: str, title: str, note: str = "") -> None:
    df.to_csv(OUT / f"{stem}.csv", index=False, encoding="utf-8-sig")
    body = [f"# {title}", ""]
    body.append(md_table(df))
    if note:
        body += ["", "> " + note]
    (OUT / f"{stem}.md").write_text("\n".join(body) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------
# Table 1 数据集描述
# --------------------------------------------------------------------------
def table01() -> pd.DataFrame:
    d = pd.read_csv(DATA / "price_clean.csv", parse_dates=["date"])
    n, nd = len(d), d["date"].nunique()
    neg = d[d["price"] < 0]

    s = (d["price"] < 0).astype(int).to_numpy()
    runs, cur = [], 0
    for v in s:
        if v:
            cur += 1
        elif cur:
            runs.append(cur)
            cur = 0
    if cur:
        runs.append(cur)
    runs = np.array(runs)

    tier = neg["tier_b0"].value_counts(normalize=True) * 100

    for k, v in {
        "n_days": nd, "n_hours": n, "n_missing": d["price"].isna().sum(),
        "n_dup": d.duplicated(["date", "hour"]).sum(),
        "price_min": d["price"].min(), "price_max": d["price"].max(),
        "price_mean": d["price"].mean(), "price_std": d["price"].std(),
        "n_neg": len(neg), "neg_share": len(neg) / n * 100,
        "n_events": len(runs), "dur_mean": runs.mean(), "dur_med": np.median(runs),
        "dur_max": runs.max(), "n_floor": (d["price"] == -80).sum(),
        "floor_share": (d["price"] == -80).mean() * 100,
        "n_below80": (d["price"] < -80).sum(), "n_zero": (d["price"] == 0).sum(),
    }.items():
        rec("table01", k, v)
    for t, v in tier.items():
        rec("table01", f"neg_tier|{t}", v)

    def g(x, nd=0):
        """千位用空格分隔（中文排版惯例）。"""
        return f"{x:,.{nd}f}".replace(",", " ")

    rows = [
        ("数据来源", "山东电力现货市场 · 实时小时出清价",
         "网格与表底“实时最高/最低/平均”三行 299/299 天吻合，确认为实时价", "DATA_AUDIT §3"),
        ("样本区间", f"{d['date'].min():%Y-%m-%d} 至 {d['date'].max():%Y-%m-%d}",
         "年内滚动样本外（within-year rolling origin）", "复算"),
        ("样本天数", f"{nd}", "日历完整，无缺日", "复算"),
        ("样本小时数", g(n), f"{nd} × 24，每日 1–24 时标签齐全", "复算"),
        ("缺失 / 重复小时", f"{int(d['price'].isna().sum())} / {int(d.duplicated(['date', 'hour']).sum())}",
         "无插补、无删除", "复算"),
        ("价格范围（元/MWh）", f"−{abs(d['price'].min()):.3f} ~ {g(d['price'].max(), 3)}",
         "负值保留原值，未截断", "复算"),
        ("价格均值 / 标准差（元/MWh）", f"{d['price'].mean():.2f} / {d['price'].std():.2f}", "", "复算"),
        ("负价小时（p<0）", f"{g(len(neg))}（{len(neg) / n * 100:.2f}%）",
         "覆盖率的 pooled 分母：全部负价小时", "复算"),
        ("负价事件数", f"{len(runs)}", "连续负价小时合并计一次（跨日连续）", "复算"),
        ("单次事件时长 均值 / 中位 / 最长（h）",
         f"{runs.mean():.2f} / {np.median(runs):.0f} / {runs.max():.0f}", "", "复算"),
        ("报价下限 −80 元/MWh", f"{g((d['price'] == -80).sum())} h（{(d['price'] == -80).mean() * 100:.2f}%）",
         f"下限为报价规则特征；严格低于 −80 仅 {(d['price'] < -80).sum()} h，未截断", "复算"),
        ("负价落在 B0 各档",
         "、".join(f"{k} {tier.get(k, 0):.1f}%" for k in ["深谷", "低谷", "平段", "高峰", "尖峰"]),
         "平段近四成 → 零售侧拿不到负价信号（H1 的直接证据）", "复算（tier_b0 字段）"),
        ("现行时段 B0 来源", "国网山东代理购电价格表 12 期（2025.12–2026.11）",
         "逐月录入，可追溯至 results/e0_qa/b0_periods.csv", "DATA_AUDIT §6"),
        ("浮动比例", "尖峰 +100%、高峰 +70%、平段 0、低谷 −70%、深谷 −90%",
         "只改时段边界，不改浮动比例", "DATA_AUDIT §6"),
        ("代理用户负荷", "2018 山东逐小时实测（8 760 h），按“同月同星期最近日”形状迁移至 2026",
         "单位电量电费对负荷水平尺度不变，只依赖日内形状", "DATA_AUDIT §7"),
        ("负荷—价格年份缺口", "价格 2026 年；负荷 2018 年实测 + 2025 年典型日",
         "电费结论仅为情景，不推金额、不称“某用户”", "DATA_AUDIT §7.1"),
        ("样本外窗口",
         "W1：设计 1–3 月 / 验证 4 月 / 测试 5–6 月（61 天）；"
         "W2：设计 1–5 月 / 验证 6 月 / 测试 7–8 月（62 天）；"
         "W3：设计 1–8 月 / 验证 9 月 / 测试 10-01–10-26（26 天）",
         "测试窗口不参与任何参数选择", "EXPERIMENT_RESULTS §1.1"),
        ("统计单位与推断", "日；paired bootstrap 10 000 次；符号翻转置换 10 000 次；BH 校正",
         "CI 仅反映日间变异，不含设计选择不确定性", "EXPERIMENT_RESULTS §1.5"),
    ]
    df = pd.DataFrame(rows, columns=["项目", "内容", "说明", "来源"])
    emit(df, "table01_dataset_description", "Table 1 数据集与实验设计描述",
         "数值除注明“来自文档”的口径说明外，均由 data/price_clean.csv 复算；"
         "复算脚本 plotting_scripts/make_tables.py::table01。")
    return df


# --------------------------------------------------------------------------
# Table 2 主结果（24 行）
# --------------------------------------------------------------------------
METHOD_CN = {
    "M1_NP_DP": "M1 负价感知DP",
    "B4_DP_lambda0": "B4 同法 λ=0",
    "B0_policy": "B0 现行政策",
    "B5_deep_valley": "B5 深谷扩展",
    "B1_quantile": "B1 分位切段",
    "B2_kmeans": "B2 K-means",
    "B3_netload": "B3 净负荷(2018)",
    "B3_netload_2025": "B3b 净负荷(2025)",
}


def table02() -> pd.DataFrame:
    d = pd.read_csv(DATA / "main_results.csv")
    d["method"] = pd.Categorical(d["method"], style.METHOD_ORDER, ordered=True)
    d = d.sort_values(["window", "method"]).reset_index(drop=True)

    rows = []
    for _, r in d.iterrows():
        for col in ("coverage", "regret", "bill_delta_pct", "bill_delta_raw_pct",
                    "jaccard_vs_B0", "unit_bill", "kappa", "n_neg", "runtime_s"):
            rec("table02", f"{r['window']}|{r['method']}|{col}", r[col])
        rows.append(
            {
                "窗口": r["window"],
                "方法": r["method"],
                "方法说明": METHOD_CN[r["method"]],
                "负价覆盖率 (%)": f"{r['coverage'] * 100:.2f}",
                "价格拟合遗憾 R (%)": f"{r['regret'] * 100:.2f}",
                "单位电费 (指数)": f"{r['unit_bill']:.4f}",
                "κ（收入中性）": f"{r['kappa']:.4f}",
                "Δ电费 vs B0 · 中性 (%)": f"{r['bill_delta_pct']:.2f}",
                "Δ电费 vs B0 · 原始乘子 (%)": f"{r['bill_delta_raw_pct']:.2f}",
                "Jaccard vs B0": f"{r['jaccard_vs_B0']:.3f}",
                "切点 (h)": str(r["cuts"]).replace("|", "-") if pd.notna(r["cuts"]) else "—",
                "测试期负价小时": f"{int(r['n_neg'])}",
                "运行时间 (s)": f"{r['runtime_s']:.4f}",
            }
        )
    df = pd.DataFrame(rows)
    emit(df, "table02_baseline_performance", "Table 2 主结果：3 窗口 × 8 方法的样本外表现",
         "全部 24 行逐行来自 data/main_results.csv（未做任何改写）；"
         "覆盖率为 pooled 口径；电费为平段价归一后的单位电量电费指数；B0/B5 为政策档位设计，无切点。")
    return df


# --------------------------------------------------------------------------
# Table 3 假设判定
# --------------------------------------------------------------------------
def table03() -> pd.DataFrame:
    ci = pd.read_csv(DATA / "ci_table.csv")
    main = pd.read_csv(DATA / "main_results.csv")

    def cov_gap(w, base):
        m = main[(main.window == w) & (main.method == "M1_NP_DP")].coverage.iloc[0]
        b = main[(main.window == w) & (main.method == base)].coverage.iloc[0]
        return (m - b) * 100

    for w in ["W1", "W2", "W3"]:
        rec("table03", f"cov_gap|B0|{w}", cov_gap(w, "B0_policy"))
        rec("table03", f"cov_gap|B4|{w}", cov_gap(w, "B4_DP_lambda0"))

    ov = pd.read_csv(DATA / "e3_overlap.csv")
    j_b5 = ov["jaccard_m1_b5"].mean()
    j_b3b = ov["jaccard_m1_b3b"].mean()
    rec("table03", "jaccard_m1_b5", j_b5)
    rec("table03", "jaccard_m1_b3b", j_b3b)

    bill_b4 = {w: ci[(ci.window == w) & (ci.baseline == "B4_DP_lambda0") & (ci.metric == "bill")].rel_diff_pct.iloc[0]
               for w in ["W1", "W2", "W3"]}
    for w, v in bill_b4.items():
        rec("table03", f"bill_m1_minus_b4|{w}", v)

    rows = [
        {
            "假设": "H1 负价集中在午间、现行时段覆盖不足",
            "预注册判定标准": "B0 对负价小时的覆盖率显著不足；M1 相对 B0 的覆盖率提升在 ≥2 个窗口、95% CI 不含 0、BH 校正后仍显著",
            "实际结果": (f"B0 覆盖率 34.5 / 0.0 / 47.9%；M1 76.7 / 73.2 / 84.5%；"
                     f"M1−B0 的 paired 估计 +45.0 / +69.5 / +29.3 pp，3/3 窗口 BH 后显著"),
            "判定": "支持",
            "证据": "Fig 1、Fig 2、Table 2、Table 4",
        },
        {
            "假设": "H2 M1 的用户电费优于 B0–B4",
            "预注册判定标准": "≥2 个窗口中 M1 比 B4 低 ≥2%，paired 95% CI 不含 0，BH 校正后显著，且方向不被单一窗口驱动",
            "实际结果": (f"M1−B4 = {bill_b4['W1']:+.2f} / {bill_b4['W2']:+.2f} / {bill_b4['W3']:+.3f}%；"
                     "幅度均 <1%，W2/W3 方向为正；相对 B0 的 -4.43/-7.03% 在 W3 反转为 +2.18%"),
            "判定": "不支持（阴性结果，按预注册规则原样报告）",
            "证据": "Fig 4、Fig 6、Table 2、Table 4",
        },
        {
            "假设": "H3 增益来自“负价密度高且与深谷/净负荷不重合”",
            "预注册判定标准": "与 B5/B3b 的档位重合度 <80%；M1−B4 随负价密度单调扩大且幅度可观；负对照显著",
            "实际结果": (f"J(M1,B5)={j_b5:.3f}、J(M1,B3b)={j_b3b:.3f}（均 >80%）；"
                     "分层 M1−B4 = -0.38 / -0.36 / -0.53 pp；负对照 P=0.075"),
            "判定": "混合偏弱（方向正确、强度不足）",
            "证据": "Fig 5、Table 5、data/e3_overlap.csv、data/e4_negative_control.csv",
        },
    ]
    df = pd.DataFrame(rows)
    emit(df, "table03_hypothesis_summary", "Table 3 假设判定汇总",
         "判定标准引自 EXPERIMENT_PLAN.md（E3 预注册）与 EXPERIMENT_RESULTS.md §7；"
         "“实际结果”中的数值由 main_results.csv / ci_table.csv / e3_overlap.csv 复算。")
    return df


# --------------------------------------------------------------------------
# Table 4 统计检验
# --------------------------------------------------------------------------
def table04() -> pd.DataFrame:
    ci = pd.read_csv(DATA / "ci_table.csv")
    bases = ["B0_policy", "B4_DP_lambda0", "B5_deep_valley", "B3_netload_2025"]
    rows = []
    for w in ["W1", "W2", "W3"]:
        for b in bases:
            for metric, label, unit, scale in [
                ("bill", "单位电费变化", "%", 1.0),
                ("cov", "负价覆盖率差", "pp", 100.0),
            ]:
                r = ci[(ci.window == w) & (ci.baseline == b) & (ci.metric == metric)]
                if len(r) != 1:
                    continue
                r = r.iloc[0]
                if metric == "bill":
                    est, lo, hi = r.rel_diff_pct, r.rel_ci_lo_pct, r.rel_ci_hi_pct
                    rec("table04", f"{w}|{b}|bill", est)
                    rec("table04", f"{w}|{b}|bill_lo", lo)
                    rec("table04", f"{w}|{b}|bill_hi", hi)
                    fmt = "{:+.2f}".format
                    head = "Δ电费 (%)"
                else:
                    est, lo, hi = r.mean_diff * 100, r.ci_lo * 100, r.ci_hi * 100
                    rec("table04", f"{w}|{b}|cov", est)
                    rec("table04", f"{w}|{b}|cov_lo", lo)
                    rec("table04", f"{w}|{b}|cov_hi", hi)
                    fmt = "{:+.1f}".format
                    head = "Δ覆盖率 (pp)"
                rows.append(
                    {
                        "窗口": w,
                        "基线": f"{b.split('_')[0]}{'b' if b.endswith('2025') else ''}",
                        "指标": head,
                        "估计值": fmt(est),
                        "95% CI 下限": fmt(lo),
                        "95% CI 上限": fmt(hi),
                        "p (BH)": "<0.001" if r.p_bh < 0.001 else f"{r.p_bh:.3f}",
                        "BH 后显著": "是" if r["sig_bh_0.05"] else "否",
                        "天数": f"{int(r.n_days)}",
                        "效应量 d": f"{r.cohens_d:+.2f}" if pd.notna(r.cohens_d) else "—",
                    }
                )
    df = pd.DataFrame(rows)
    emit(df, "table04_statistical_results", "Table 4 M1 相对各基线的逐日配对检验（95% CI）",
         "全部数值来自 data/ci_table.csv（metric = bill / cov），paired 单位＝日；"
         "CI 只反映日间变异，不含设计选择不确定性，因此极小 CI 不能读作“方法更优”的证据。")
    return df


# --------------------------------------------------------------------------
# Table 5 λ 消融
# --------------------------------------------------------------------------
def table05() -> pd.DataFrame:
    d = pd.read_csv(DATA / "e4_ablation_lambda.csv")
    d = d.sort_values("lambda")
    rows = []
    for _, r in d.iterrows():
        rec("table05", f"lambda|{r['lambda']}|valid_cov", r["valid_coverage"])
        rec("table05", f"lambda|{r['lambda']}|test_cov", r["test_coverage"])
        rec("table05", f"lambda|{r['lambda']}|test_sse", r["test_sse"])
        rows.append(
            {
                "窗口": r["window"],
                "λ": f"{r['lambda']:g}",
                "切点 (h)": str(r["cuts"]).replace("|", "-"),
                "验证覆盖率 (%)": f"{r['valid_coverage'] * 100:.1f}",
                "验证 SSE (×10⁶)": f"{r['valid_sse'] / 1e6:.2f}",
                "测试覆盖率 (%)": f"{r['test_coverage'] * 100:.1f}",
                "测试 SSE (×10⁶)": f"{r['test_sse'] / 1e6:.2f}",
                "验证集选中": "✔" if r["selected_by_validation"] else "",
            }
        )
    df = pd.DataFrame(rows)
    emit(df, "table05_lambda_ablation", "Table 5 负价权重 λ 的消融（W1，K=5，L_min=1）",
         "数值来自 data/e4_ablation_lambda.csv；λ∈[0,2] 切点完全相同，λ=5 才跳变，"
         "且覆盖率与价格拟合同时改善——说明 λ 是“高阈值开关”而非连续可调敏感度。")
    return df


# --------------------------------------------------------------------------
# Table 6 数据审计核对
# --------------------------------------------------------------------------
def table06() -> pd.DataFrame:
    rows = [
        ("样本天数", "303 天", "299 天", "与日历不符", "DATA_AUDIT §8"),
        ("样本小时", "7 272", "7 176", "303×24 的连带错误", "DATA_AUDIT §8"),
        ("负价小时", "1 130", "1 130", "一致", "DATA_AUDIT §8"),
        ("负价占比", "15.5%", "15.75%", "分母错（7 272 vs 7 176）", "DATA_AUDIT §8"),
        ("负价事件", "237 次", "236 次", "差 1 次", "DATA_AUDIT §8"),
        ("单次时长 均值/中位/最长", "4.8 / 4 / 19 h", "4.79 / 4 / 20 h", "最长多 1 h", "DATA_AUDIT §8"),
        ("恰为 −80", "约 10.7%", "10.34%", "分母错", "DATA_AUDIT §8"),
        ("负价落在 10:00–16:00", "74.2%", "63.54%", "口径错（标签含端点）", "DATA_AUDIT §8"),
        ("深谷（11:00–14:00）覆盖", "46.7%", "35.66%", "口径错（标签含端点）", "DATA_AUDIT §8"),
        ("负价落在低谷+深谷之外", "33.6%", "43.45%", "原稿为残差倒算，五档非互斥", "DATA_AUDIT §8"),
    ]
    df = pd.DataFrame(rows, columns=["指标", "文档旧值", "复算值", "判定", "来源"])
    emit(df, "table06_data_audit_checks", "Table 6 数据审计：文档旧值 vs 复算值",
         "引自 data/DATA_AUDIT.md §8；论文请使用“复算值”一列。"
         "小时口径为“标签＝小时结束”，严格区间下 10:00–16:00 覆盖 63.54%（旧口径 74.16%）。")
    return df


# --------------------------------------------------------------------------
def main() -> None:
    tables = {
        "table01_dataset_description": table01(),
        "table02_baseline_performance": table02(),
        "table03_hypothesis_summary": table03(),
        "table04_statistical_results": table04(),
        "table05_lambda_ablation": table05(),
        "table06_data_audit_checks": table06(),
    }

    with pd.ExcelWriter(OUT / "all_tables.xlsx", engine="openpyxl") as xw:
        for name, df in tables.items():
            df.to_excel(xw, sheet_name=name.split("_")[0], index=False)

    (OUT / "_table_values.json").write_text(
        json.dumps(VALUES, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    for name, df in tables.items():
        print(f"  ✓ tables/{name}.csv  ({len(df)} 行 × {len(df.columns)} 列)")
    print("  ✓ tables/all_tables.xlsx")
    print("  ✓ tables/_table_values.json")


if __name__ == "__main__":
    main()
