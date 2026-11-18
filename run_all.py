"""一键复跑：审计 → E1 → E2/E5（3 窗口）→ E3（用户电费）→ E4（消融/负对照/敏感性）→ 图表。

用法：
    cd code && python3 run_all.py            # 全流程（约 1–3 分钟）
    cd code && python3 run_all.py --quick    # 负对照只做 20 次、情景表只跑主 τ
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from datetime import datetime

import numpy as np
import pandas as pd

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))

from np_tou import audit, baselines as B, config as C, experiments as E, figures as F
from np_tou import metrics as M, segment as S


class Tee:
    def __init__(self, path):
        self.f = open(path, "w", encoding="utf-8")
        self.stdout = sys.stdout

    def write(self, s):
        self.stdout.write(s)
        self.f.write(s)

    def flush(self):
        self.stdout.flush()
        self.f.flush()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = C.LOG_DIR / f"run_{ts}.log"
    tee = Tee(log_path)
    sys.stdout = tee

    t_start = time.perf_counter()
    print("=" * 78)
    print(f"NP-TOU 复跑 v2   {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"Python {platform.python_version()} | numpy {np.__version__} | pandas {pd.__version__}")
    print(f"价格：{C.RAW_PRICE_FILE}")
    print(f"负荷：{C.LOAD_FILE}")
    print("=" * 78)

    # ---------------------------------------------------------- 自检
    print("\n[0] 算法自检：DP vs 暴力枚举")
    rng = np.random.default_rng(C.SEED)
    checks = []
    for T, K, L in [(8, 3, 1), (10, 4, 1), (9, 3, 2)]:
        toy = rng.normal(0, 1, size=(6, T))
        toy[0, :3] = -1.5
        for lam in (0.0, 1.0, 2.0):
            r = S.fit_dp(toy, lam, K, L)
            bf = S.brute_force_loss(toy, lam, K, L)
            checks.append({"T": T, "K": K, "L_min": L, "lambda": lam,
                           "dp_loss": r.loss, "brute_loss": bf,
                           "rel_err": abs(r.loss - bf) / max(abs(bf), 1e-12)})
    chk = pd.DataFrame(checks)
    chk.to_csv(C.RESULTS_DIR / "e0_algorithm_selftest.csv", index=False)
    print(chk.to_string(index=False, float_format=lambda v: f"{v:.6g}"))
    assert chk["rel_err"].max() < 1e-9, "DP 与暴力枚举不一致！"
    print("  ✓ 全部一致（最大相对误差 < 1e-9）")

    # ---------------------------------------------------------- E0 审计
    panel = E.load_panel()
    print("\n[E0] 数据审计")
    qa = audit.run_audit(panel)
    print(f"  价格样本：{qa['n_days']} 天 × 24 = {qa['n_hours']} 小时；"
          f"缺失 {qa['n_missing']}；重复 {qa['n_dup']}；负价 {qa['n_neg']}（{qa['neg_share']*100:.2f}%）")
    print(f"  网格 vs 原表“实时”统计行一致：{qa['grid_matches_realtime_rows']}")
    print(f"  负荷：2018 逐小时 8760 h（代理，映射到 2026 日期）；净负荷同源；"
          f"同一年份？{qa['load_same_year_as_price']}")

    # ---------------------------------------------------------- E1
    print("\n[E1] 负价画像与现行时段覆盖")
    e1 = E.e1_descriptive(panel)
    print(f"  负价事件 {e1['n_events']} 次；均值 {e1['events'].mean():.2f} h；"
          f"中位 {e1['events'].median():.0f} h；最长 {e1['events'].max():.0f} h")
    ov = e1["overall_by_tier"]
    deep = float(ov.get("深谷", 0.0))
    deep_low = float(ov.get("深谷+低谷", 0.0))
    print(f"  B0 深谷覆盖 {deep*100:.1f}%；深谷+低谷 {deep_low*100:.1f}%；"
          f"平段 {ov.get('平段',0)*100:.1f}%；峰段 {(ov.get('高峰',0)+ov.get('尖峰',0))*100:.1f}%")

    # ---------------------------------------------------------- E2/E5
    print("\n[E2/E5] 三个滚动窗口（λ 由验证集选择）")
    runs, main_rows = {}, []
    lam_rows = []
    for w in C.WINDOWS:
        run = E.run_window(panel, w)
        runs[w] = run
        lam_rows.append(run["lambda_table"])
        print(f"  {w}: 设计 {C.WINDOWS[w]['design'][0]}~{C.WINDOWS[w]['design'][1]} | "
              f"测试 {C.WINDOWS[w]['test'][0]}~{C.WINDOWS[w]['test'][1]}（{len(run['dates'])} 天）"
              f" | 选中 λ*={run['lambda']:g}")
        for name, r in run["results"].items():
            main_rows.append(r)
            print(f"    {name:16s} 覆盖率={r['coverage']*100:5.1f}%  R={r['regret']*100:+6.1f}%  "
                  f"电费={r['unit_bill']:.4f} ({r['bill_delta_pct']:+.2f}%)  切点={r['cuts'] or '—'}")
    main = pd.DataFrame(main_rows)
    main.to_csv(C.RESULTS_DIR / "main_results.csv", index=False)
    pd.concat(lam_rows, ignore_index=True).to_csv(
        C.RESULTS_DIR / "e2_lambda_selection.csv", index=False)

    # 边界表
    design_rows = []
    for w, run in runs.items():
        for name, d in run["designs"].items():
            design_rows.append({"window": w, "method": name, "kind": d.kind,
                                "cuts": "|".join(map(str, d.cuts)) if d.kind == "partition" else "",
                                "labels_24h": "".join(str(x) for x in d.labels_for(5)),
                                "lambda": d.meta.get("lambda", ""),
                                "source": d.meta.get("source", d.meta.get("spec", d.meta.get("rule", "")))})
    pd.DataFrame(design_rows).to_csv(C.RESULTS_DIR / "designs_boundaries.csv", index=False)

    # 稳定性
    stab = []
    for name in ["M1_NP_DP", "B4_DP_lambda0", "B1_quantile", "B2_kmeans", "B3_netload"]:
        bl = [list(map(int, runs[w]["results"][name]["cuts"].split("|"))) for w in C.WINDOWS]
        stab.append({"method": name,
                     "boundaries": ";".join("-".join(map(str, b)) for b in bl),
                     "stability": M.boundary_stability(bl)})
    stab = pd.DataFrame(stab)
    stab.to_csv(C.RESULTS_DIR / "boundary_stability.csv", index=False)
    print("\n  边界稳定性 S：")
    print(stab.to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    # ---------------------------------------------------------- 配对检验
    print("\n[stats] M1 相对各基线的逐日配对检验（bootstrap 10,000 + 符号翻转 10,000）")
    paired = E.paired_table(runs)
    paired.to_csv(C.RESULTS_DIR / "ci_table.csv", index=False)
    show = paired[(paired.metric == "bill")][
        ["window", "baseline", "rel_diff_pct", "rel_ci_lo_pct", "rel_ci_hi_pct", "p_bh", "n_days"]].copy()
    show["p_bh"] = show["p_bh"].map(lambda v: "<0.001" if (pd.notna(v) and v < 0.001) else
                                    ("—" if pd.isna(v) else f"{v:.3f}"))
    print("  —— 单位电量电费（主口径：收支中性）")
    print(show.to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    print("\n[stats] 各方法相对 B0 的电费节约率与 95% CI")
    bci = E.bill_ci_table(runs)
    bci.to_csv(C.RESULTS_DIR / "e3_bill_ci_vs_B0.csv", index=False)
    print(bci.pivot(index="method", columns="window", values="rel_diff_pct")
          .reindex(C.METHODS).round(2).to_string())

    # ---------------------------------------------------------- E3
    print("\n[E3] 用户电费（代理负荷）与深度对照")
    lsens = E.e3_load_sensitivity(panel)
    lsens.to_csv(C.RESULTS_DIR / "e3_load_sensitivity.csv", index=False)
    print("  负荷形状稳健性（M1 相对 B0）：")
    print(lsens[lsens.method == "M1_NP_DP"][["load_mode", "window", "bill_delta_pct", "coverage"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))

    ov3 = E.e3_overlap(panel)
    ov3.to_csv(C.RESULTS_DIR / "e3_overlap.csv", index=False)
    print(f"  M1 最低价段与 B0 深谷 Jaccard={ov3.jaccard_m1_b0.mean():.3f}；"
          f"B5={ov3.jaccard_m1_b5.mean():.3f}；B3(2018净负荷)={ov3.jaccard_m1_b3.mean():.3f}；"
          f"B3b(2025净负荷)={ov3.jaccard_m1_b3b.mean():.3f}")

    het = E.e3_heterogeneity(panel)
    het.to_csv(C.RESULTS_DIR / "e3_heterogeneity.csv", index=False)

    print("  ε × τ 情景（收支中性 + 原始乘子）")
    scen = E.e3_scenarios(panel)
    scen.to_csv(C.RESULTS_DIR / "e3_scenarios.csv", index=False)
    pv = (scen[(scen.revenue_neutral) & (scen.tau == C.TAU_MAIN)]
          .pivot_table(index="method", columns="elasticity", values="bill_delta_pct"))
    print(pv.reindex(C.METHODS).round(2).to_string())

    # ---------------------------------------------------------- E4
    print("\n[E4a] λ 消融（含验证集选择标记）")
    abl = E.e4_lambda_ablation(panel, "W1")
    abl.to_csv(C.RESULTS_DIR / "e4_ablation_lambda.csv", index=False)
    print(abl.to_string(index=False, float_format=lambda v: f"{v:.4g}"))

    print("\n[E4d] 负对照（日内打乱负价权重）")
    n_rep = 20 if args.quick else 200
    lam_star = runs["W1"]["lambda"]
    nc = pd.concat([E.e4_negative_control(panel, "W1", lambda_=lm, n_rep=n_rep)
                    for lm in sorted({lam_star, 5.0})], ignore_index=True)
    nc.to_csv(C.RESULTS_DIR / "e4_negative_control.csv", index=False)
    for lm, sub in nc.groupby("lambda"):
        act = float(sub[sub.type == "actual"]["coverage"].iloc[0])
        sh = sub[sub.type == "shuffled"]["coverage"]
        print(f"  λ={lm:g}: 真实设计 {act*100:.1f}%；打乱后 中位 {sh.median()*100:.1f}%，"
              f"95% 区间 [{sh.quantile(.025)*100:.1f}, {sh.quantile(.975)*100:.1f}]；"
              f"P(打乱≥真实)={(sh >= act).mean():.3f}")

    print("\n[E4f] 敏感性（K / L_min / 阈值）")
    sens = E.e4_sensitivity(panel, "W1")
    sens.to_csv(C.RESULTS_DIR / "e4_robustness.csv", index=False)
    print(f"  共 {len(sens)} 组设置；覆盖率范围 {sens.coverage.min()*100:.1f}%–{sens.coverage.max()*100:.1f}%")

    # ---------------------------------------------------------- 图
    print("\n[fig] 生成图表")
    F.fig_price_overview(panel, e1["monthly"])
    F.fig_neg_heatmap(e1["profile"])
    F.fig_neg_structure(e1["profile"], e1["events"])
    F.fig_b0_coverage(e1["coverage_b0"])
    F.fig_boundaries(runs, panel)
    F.fig_coverage_by_method(main)
    F.fig_tradeoff(main)
    F.fig_lambda(abl)
    F.fig_negative_control(nc)
    F.fig_sensitivity(sens)
    F.fig_load_profile(panel)
    F.fig_bill_delta(bci)
    F.fig_bill_decomp(main)
    F.fig_elasticity(scen)

    # ---------------------------------------------------------- 摘要
    summary = {
        "run_at": datetime.now().isoformat(timespec="seconds"),
        "python": platform.python_version(),
        "data": {"price": C.RAW_PRICE_FILE.name, "load": C.LOAD_FILE.name,
                 "netload": C.NETLOAD_FILE.name},
        "n_days": qa["n_days"], "n_hours": qa["n_hours"],
        "n_neg": qa["n_neg"], "neg_share": qa["neg_share"],
        "n_events": e1["n_events"],
        "median_duration": float(e1["events"].median()),
        "max_duration": int(e1["events"].max()),
        "b0_deep_coverage": float(deep), "b0_deep_low_coverage": float(deep_low),
        "lambda_selected": {w: runs[w]["lambda"] for w in C.WINDOWS},
        "stability": stab.to_dict(orient="records"),
        "main": main.to_dict(orient="records"),
        "runtime_s": round(time.perf_counter() - t_start, 2),
    }
    with open(C.RESULTS_DIR / "run_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=str)

    print("\n" + "=" * 78)
    print(f"完成，用时 {summary['runtime_s']} s。结果：{C.RESULTS_DIR}")
    print(f"日志：{log_path}")
    print("=" * 78)
    sys.stdout = tee.stdout
    tee.f.close()


if __name__ == "__main__":
    main()
