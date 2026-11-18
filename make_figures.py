"""生成 Figure 1–7（严格按 FIGURE_TABLE_PLAN.md §1）。

数据来源：data/main_results.csv（24 行 = 3 窗口 × 8 方法）
         data/designs_boundaries.csv（仅用于 Fig 5 的边界稳定性 S 复算）

原则：脚本只读取 CSV，不硬编码任何实验数值；
      方法顺序、颜色、标记、标签是代码常量（非数据）。
运行：python3 plotting_scripts/make_figures.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

import style  # noqa: E402

style.apply_style()

METHOD_ORDER = style.METHOD_ORDER
METHOD_LABEL = style.METHOD_LABEL
METHOD_COLOR = style.METHOD_COLOR
WINDOW_ORDER = style.WINDOW_ORDER
WINDOW_LABEL = style.WINDOW_LABEL
WINDOW_MARKER = style.WINDOW_MARKER
ACCENT = style.ACCENT


def get(df: pd.DataFrame, window: str, method: str, col: str) -> float:
    """从主表取一个值；不存在或多条则报错（不静默填 0）。"""
    sub = df[(df["window"] == window) & (df["method"].astype(str) == method)]
    if len(sub) != 1:
        raise KeyError(f"main_results.csv 缺少 {window}/{method} 的唯一记录")
    return float(sub.iloc[0][col])


def col_major(items, ncol: int):
    """把按行排列的图例项重排为 matplotlib 的列优先填充顺序。"""
    n = len(items)
    nrow = -(-n // ncol)
    out = [None] * n
    for i, item in enumerate(items):
        r, c = divmod(i, ncol)
        out[r + c * nrow] = item
    return out


def method_legend_handles(methods, markers: bool = False):
    return [
        Line2D(
            [], [], color=METHOD_COLOR[m], marker="o" if not markers else "s",
            linestyle="", markersize=5.5, label=METHOD_LABEL[m],
        )
        for m in methods
    ]


# --------------------------------------------------------------------------
# Fig 1 覆盖率：B0 vs M1（分组柱）
# --------------------------------------------------------------------------
def fig01(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    x = np.arange(len(WINDOW_ORDER))
    width = 0.34

    for method, off in [("B0_policy", -width / 2), ("M1_NP_DP", width / 2)]:
        vals = [get(df, w, method, "coverage") * 100 for w in WINDOW_ORDER]
        bars = ax.bar(
            x + off, vals, width,
            color=METHOD_COLOR[method], edgecolor="white", linewidth=0.7,
            label=METHOD_LABEL[method], zorder=3,
        )
        for bar, v, w in zip(bars, vals, WINDOW_ORDER):
            ax.annotate(
                style.pct(v),
                xy=(bar.get_x() + bar.get_width() / 2, v),
                xytext=(0, 3), textcoords="offset points",
                ha="center", va="bottom", fontsize=8, color="#1A1A1A",
            )
            style.record("fig01", **{f"coverage|{method}|{w}": v / 100})

    ax.set_xticks(x)
    ax.set_xticklabels([WINDOW_LABEL[w] for w in WINDOW_ORDER])
    ax.set_ylabel("负价小时覆盖率 (%)")
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_locator(plt.MultipleLocator(20))
    ax.set_xlim(-0.55, len(WINDOW_ORDER) - 0.45)
    ax.grid(axis="x", visible=False)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2,
              frameon=False, handlelength=1.4, columnspacing=2.0)
    return fig, ["fig01_coverage_b0_vs_m1"]


# --------------------------------------------------------------------------
# Fig 2 覆盖率热力图（方法 × 窗口）
# --------------------------------------------------------------------------
def fig02(df: pd.DataFrame):
    mat = np.array(
        [[get(df, w, m, "coverage") * 100 for w in WINDOW_ORDER] for m in METHOD_ORDER]
    )
    fig, ax = plt.subplots(figsize=(5.2, 4.2))
    im = ax.imshow(mat, cmap="Blues", vmin=0, vmax=100, aspect="auto")

    ax.set_xticks(np.arange(len(WINDOW_ORDER)))
    ax.set_xticklabels([WINDOW_LABEL[w] for w in WINDOW_ORDER], fontsize=8.5)
    ax.set_yticks(np.arange(len(METHOD_ORDER)))
    ax.set_yticklabels([METHOD_LABEL[m] for m in METHOD_ORDER])
    ax.tick_params(length=0)

    ax.set_xticks(np.arange(-0.5, len(WINDOW_ORDER), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(METHOD_ORDER), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.4)
    ax.grid(which="major", visible=False)
    ax.tick_params(which="minor", length=0)

    for i, m in enumerate(METHOD_ORDER):
        for j, w in enumerate(WINDOW_ORDER):
            v = mat[i, j]
            ax.text(
                j, i, style.pct(v),
                ha="center", va="center", fontsize=8,
                color="white" if v > 55 else "#1A1A1A",
            )
            style.record("fig02", **{f"coverage|{m}|{w}": v / 100})

    cbar = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cbar.set_label("负价小时覆盖率 (%)")
    cbar.outline.set_linewidth(0.6)
    cbar.ax.tick_params(width=0.6, labelsize=8)
    return fig, ["fig02_coverage_heatmap"]


# --------------------------------------------------------------------------
# Fig 3 覆盖率 vs 价格拟合遗憾（散点）
# --------------------------------------------------------------------------
def fig03(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(6.2, 4.0))

    for m in METHOD_ORDER:
        for w in WINDOW_ORDER:
            ax.scatter(
                get(df, w, m, "coverage") * 100,
                get(df, w, m, "regret") * 100,
                s=46, c=METHOD_COLOR[m], marker=WINDOW_MARKER[w],
                edgecolors="white", linewidths=0.6, zorder=3,
            )
            style.record(
                "fig03",
                **{
                    f"coverage|{m}|{w}": get(df, w, m, "coverage"),
                    f"regret|{m}|{w}": get(df, w, m, "regret"),
                },
            )

    for m, w, off, ha in [
        ("M1_NP_DP", "W1", (8, 2), "left"),
        ("B0_policy", "W1", (8, 2), "left"),
        ("B1_quantile", "W3", (-8, -2), "right"),
    ]:
        ax.annotate(
            f"{METHOD_LABEL[m].split()[0]} {w}",
            xy=(get(df, w, m, "coverage") * 100, get(df, w, m, "regret") * 100),
            xytext=off, textcoords="offset points",
            fontsize=7.5, color=METHOD_COLOR[m], ha=ha, va="center",
        )

    ax.set_xlabel("负价小时覆盖率 (%)")
    ax.set_ylabel("价格拟合遗憾 R (%)")
    ax.set_xlim(0, 95)
    ax.set_ylim(0, 43)
    ax.xaxis.set_major_locator(plt.MultipleLocator(20))
    ax.yaxis.set_major_locator(plt.MultipleLocator(10))

    method_h = method_legend_handles(col_major(METHOD_ORDER, 4))
    window_h = [
        Line2D([], [], color="#666666", marker=WINDOW_MARKER[w], linestyle="",
               markersize=5.5, label=WINDOW_LABEL[w])
        for w in WINDOW_ORDER
    ]
    leg1 = fig.legend(
        handles=method_h, loc="upper center", bbox_to_anchor=(0.5, -0.175),
        bbox_transform=ax.transAxes,
        ncol=4, frameon=False, columnspacing=1.0, handletextpad=0.5,
    )
    fig.add_artist(leg1)
    fig.legend(
        handles=window_h, loc="upper center", bbox_to_anchor=(0.5, -0.315),
        bbox_transform=ax.transAxes,
        ncol=3, frameon=False, columnspacing=1.2, handletextpad=0.5,
        title="标记形状＝窗口", title_fontsize=7.6,
    )
    fig.subplots_adjust(bottom=0.30)
    return fig, ["fig03_coverage_regret"]


# --------------------------------------------------------------------------
# Fig 4 用户电费变化（分组柱 + M1−B4 增量柱）
# --------------------------------------------------------------------------
def fig04(df: pd.DataFrame):
    methods = [m for m in METHOD_ORDER if m != "B0_policy"]  # B0 为参照，Δ≡0
    fig, axes = plt.subplots(
        1, 2, figsize=(7.4, 3.5), gridspec_kw={"width_ratios": [1.55, 1]}
    )
    ax = axes[0]
    x = np.arange(len(WINDOW_ORDER))
    width = 0.8 / len(methods)

    for i, m in enumerate(methods):
        vals = [get(df, w, m, "bill_delta_pct") for w in WINDOW_ORDER]
        ax.bar(
            x + (i - (len(methods) - 1) / 2) * width, vals, width * 0.9,
            color=METHOD_COLOR[m], edgecolor="white", linewidth=0.5,
            label=METHOD_LABEL[m], zorder=3,
        )
        style.record("fig04", **{f"bill_delta|{m}|{w}": v for w, v in zip(WINDOW_ORDER, vals)})

    ax.axhline(0, color="#1A1A1A", linewidth=0.9, zorder=4)
    ax.set_xticks(x)
    ax.set_xticklabels([WINDOW_LABEL[w] for w in WINDOW_ORDER])
    ax.set_xlim(-0.55, len(WINDOW_ORDER) - 0.45)
    ax.set_ylabel("单位电费变化 vs B0 (%, 收支中性)")
    ax.set_ylim(-10.6, 6.2)
    ax.yaxis.set_major_locator(plt.MultipleLocator(4))
    ax.grid(axis="x", visible=False)
    ax.text(0.985, 0.03, "B0 为参照组（Δ≡0），未绘制",
            transform=ax.transAxes, fontsize=7, color="#666666", ha="right")
    ax.text(0.012, 0.97, "(a) 各方法 / 各窗口", transform=ax.transAxes,
            fontsize=8.5, va="top", ha="left")

    # ---- 右栏：M1 − B4（聚合口径，pp） ----
    ax2 = axes[1]
    diffs = []
    for w in WINDOW_ORDER:
        d = get(df, w, "M1_NP_DP", "bill_delta_pct") - get(df, w, "B4_DP_lambda0", "bill_delta_pct")
        diffs.append(d)
        style.record("fig04", **{f"m1_minus_b4|{w}": d})

    xi = np.arange(len(WINDOW_ORDER))
    colors = ["#1F4E79" if d < 0 else "#C0392B" for d in diffs]
    bars = ax2.bar(xi, diffs, 0.46, color=colors, edgecolor="white",
                   linewidth=0.7, zorder=3)
    for bar, v in zip(bars, diffs):
        ax2.annotate(
            f"{v:+.2f} pp",
            xy=(bar.get_x() + bar.get_width() / 2, v),
            xytext=(0, 6 if v >= 0 else -14), textcoords="offset points",
            ha="center", fontsize=8,
        )
    ax2.axhline(0, color="#1A1A1A", linewidth=0.9, zorder=4)
    for yv in (2, -2):
        ax2.axhline(yv, color=ACCENT, linestyle="--", linewidth=0.9, zorder=2)
    ax2.text(2.42, 1.60, "+2% 预注册阈值", ha="right", va="top",
             fontsize=7, color=ACCENT)
    ax2.text(2.42, -1.60, "−2% 预注册阈值", ha="right", va="bottom",
             fontsize=7, color=ACCENT)
    ax2.set_xticks(xi)
    ax2.set_xticklabels(WINDOW_ORDER)
    ax2.set_xlim(-0.6, 2.6)
    ax2.set_ylabel("M1 − B4 (百分点)")
    ax2.set_ylim(-2.4, 2.4)
    ax2.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax2.grid(axis="x", visible=False)
    ax2.text(0.03, 0.97, "(b) M1 − B4 增量", transform=ax2.transAxes,
             fontsize=8.5, va="top", ha="left")

    handles = method_legend_handles(col_major(methods, 4), markers=True)
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.34, -0.185),
               bbox_transform=ax.transAxes, ncol=4, frameon=False,
               columnspacing=1.0, handletextpad=0.4, fontsize=7.6)
    fig.subplots_adjust(wspace=0.33, bottom=0.28)
    return fig, ["fig04_bill_delta"]


# --------------------------------------------------------------------------
# Fig 5 边界稳定性 S（柱状）
# --------------------------------------------------------------------------
def compute_stability(designs: pd.DataFrame) -> pd.DataFrame:
    """由 designs_boundaries.csv 的 cuts 复算 S。

    S = 1 − 相邻窗口切点位置变化数 / ((K−1) × (窗口数−1))
    仅对 partition 类型设计有定义；tier 设计（B0/B5）无切点，不参与。
    """
    rows = []
    part = designs[designs["kind"] == "partition"]
    for method, sub in part.groupby("method"):
        sub = sub.set_index("window").reindex(WINDOW_ORDER)
        cut_lists = [str(sub.loc[w, "cuts"]).split("|") for w in WINDOW_ORDER]
        K = len(cut_lists[0]) + 1
        if any(len(c) + 1 != K for c in cut_lists):
            raise ValueError(f"{method} 各窗口段数不一致")
        changes = sum(
            1 for a, b in zip(cut_lists[:-1], cut_lists[1:]) for i, j in zip(a, b) if i != j
        )
        rows.append(
            {
                "method": method,
                "K": K,
                "n_changes": changes,
                "S": 1 - changes / ((K - 1) * (len(WINDOW_ORDER) - 1)),
            }
        )
    out = pd.DataFrame(rows)
    out["method"] = pd.Categorical(out["method"], METHOD_ORDER, ordered=True)
    return out.sort_values("method").reset_index(drop=True)


def fig05(df: pd.DataFrame, designs: pd.DataFrame):
    stab = compute_stability(designs)
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    x = np.arange(len(stab))
    vals = stab["S"].to_numpy()
    bars = ax.bar(
        x, vals, 0.55,
        color=[METHOD_COLOR[m] for m in stab["method"].astype(str)],
        edgecolor="white", linewidth=0.7, zorder=3,
    )
    for bar, v, m in zip(bars, vals, stab["method"].astype(str)):
        ax.annotate(
            f"{v:.3f}",
            xy=(bar.get_x() + bar.get_width() / 2, v),
            xytext=(0, 3), textcoords="offset points",
            ha="center", fontsize=8,
        )
        style.record("fig05", **{f"stability|{m}": v})

    ax.set_xticks(x)
    ax.set_xticklabels([METHOD_LABEL[m] for m in stab["method"].astype(str)],
                       fontsize=8, rotation=14, ha="right", rotation_mode="anchor")
    ax.set_ylabel("边界稳定性 S")
    ax.set_ylim(0, 1.16)
    ax.yaxis.set_major_locator(plt.MultipleLocator(0.2))
    ax.grid(axis="x", visible=False)
    ax.text(-0.45, 1.05, "S = 1：三窗口切点完全不变；S 越低表示时段表越不稳定", fontsize=7,
            color="#666666", va="bottom", ha="left")
    return fig, ["fig05_boundary_stability"], stab


# --------------------------------------------------------------------------
# Fig 6 账单分解：原始乘子 vs 收支中性（哑铃图）
# --------------------------------------------------------------------------
def fig06(df: pd.DataFrame):
    fig, axes = plt.subplots(1, 3, figsize=(7.4, 3.5), sharey=True)
    methods = list(METHOD_ORDER)
    y = np.arange(len(methods))[::-1]

    for ax, w in zip(axes, WINDOW_ORDER):
        raw = [get(df, w, m, "bill_delta_raw_pct") for m in methods]
        neu = [get(df, w, m, "bill_delta_pct") for m in methods]
        for yi, r, n in zip(y, raw, neu):
            ax.plot([n, r], [yi, yi], color="#B0B0B0", linewidth=1.6,
                    solid_capstyle="round", zorder=2)
        ax.scatter(neu, y, s=40, marker="s", facecolor="#1F4E79",
                   edgecolor="white", linewidth=0.7, zorder=3)
        ax.scatter(raw, y, s=40, marker="o", facecolor="#C0392B",
                   edgecolor="white", linewidth=0.7, zorder=3)
        for m, r, n in zip(methods, raw, neu):
            style.record("fig06", **{f"raw|{m}|{w}": r, f"neutral|{m}|{w}": n})
        ax.axvline(0, color="#1A1A1A", linewidth=0.9, zorder=1)
        ax.set_xlim(-27, 19)
        ax.set_title(WINDOW_LABEL[w], fontsize=9, pad=4)
        ax.xaxis.set_major_locator(plt.MultipleLocator(10))
        ax.grid(axis="y", visible=False)

    axes[0].set_yticks(y)
    axes[0].set_yticklabels([METHOD_LABEL[m] for m in methods], fontsize=8)
    axes[1].set_xlabel("单位电费变化 vs B0 (%)", fontsize=9)

    handles = [
        Line2D([], [], marker="s", color="none", markerfacecolor="#1F4E79",
               markeredgecolor="white", markersize=6, label="收支中性（κ 校正）"),
        Line2D([], [], marker="o", color="none", markerfacecolor="#C0392B",
               markeredgecolor="white", markersize=6, label="原始乘子（未校正）"),
        Line2D([], [], color="#B0B0B0", linewidth=1.6, label="两者之差＝转移成分"),
    ]
    fig.legend(handles=handles, loc="upper center", ncol=3, frameon=False,
               bbox_to_anchor=(0.5, -0.225), bbox_transform=axes[1].transAxes,
               handlelength=1.4, columnspacing=1.6)
    fig.subplots_adjust(wspace=0.12, bottom=0.28)
    return fig, ["fig06_bill_decomposition"]


# --------------------------------------------------------------------------
# Fig 7 覆盖率 vs 账单变化（散点）
# --------------------------------------------------------------------------
def fig07(df: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(5.9, 4.0))
    for m in METHOD_ORDER:
        for w in WINDOW_ORDER:
            ax.scatter(
                get(df, w, m, "coverage") * 100, get(df, w, m, "bill_delta_pct"),
                s=46, c=METHOD_COLOR[m], marker=WINDOW_MARKER[w],
                edgecolors="white", linewidths=0.6, zorder=3,
            )
            style.record(
                "fig07",
                **{
                    f"coverage|{m}|{w}": get(df, w, m, "coverage"),
                    f"bill_delta|{m}|{w}": get(df, w, m, "bill_delta_pct"),
                },
            )

    ax.axhline(0, color="#1A1A1A", linewidth=0.9, zorder=1)
    ax.axvline(80, color="#999999", linestyle=":", linewidth=0.9, zorder=1)
    ax.text(80.7, -10.15, "覆盖率 80%", fontsize=7, color="#666666", va="bottom")

    for m, w, txt, off, ha, va in [
        ("B5_deep_valley", "W3", "B5 W3：74.6%，\n+3.43%", (-12, 12), "right", "bottom"),
        ("M1_NP_DP", "W3", "M1 W3：84.5%，\n+2.18%", (0, 10), "center", "bottom"),
        ("B1_quantile", "W2", "B1 W2：74.4%，\n−7.13%", (14, -6), "left", "center"),
    ]:
        ax.annotate(
            txt,
            xy=(get(df, w, m, "coverage") * 100, get(df, w, m, "bill_delta_pct")),
            xytext=off, textcoords="offset points", fontsize=7,
            color=METHOD_COLOR[m], ha=ha, va=va, linespacing=1.25,
            arrowprops=dict(arrowstyle="-", color=METHOD_COLOR[m],
                            linewidth=0.6, shrinkA=2, shrinkB=4,
                            relpos=(0.5, 0.0) if m == "M1_NP_DP" else (1.0, 0.3)),
        )

    ax.set_xlabel("负价小时覆盖率 (%)")
    ax.set_ylabel("单位电费变化 vs B0 (%, 收支中性)")
    ax.set_xlim(0, 97)
    ax.set_ylim(-10.4, 6.4)
    ax.xaxis.set_major_locator(plt.MultipleLocator(20))
    ax.yaxis.set_major_locator(plt.MultipleLocator(4))

    handles = method_legend_handles(col_major(METHOD_ORDER, 4))
    fig.legend(handles=handles, loc="upper center", bbox_to_anchor=(0.5, -0.175),
               bbox_transform=ax.transAxes, ncol=4, frameon=False,
               columnspacing=0.9, handletextpad=0.4, fontsize=7.4)
    fig.subplots_adjust(bottom=0.27)
    return fig, ["fig07_coverage_vs_bill"]


# --------------------------------------------------------------------------
def main() -> None:
    df = style.load_main()
    designs = style.load_designs()

    made: list[Path] = []
    for builder in (fig01, fig02, fig03, fig04):
        fig, names = builder(df)
        made += style.save(fig, names[0])

    fig5, names, stab = fig05(df, designs)
    made += style.save(fig5, names[0])
    stab.to_csv(style.TABLE_DIR / "aux_boundary_stability_S.csv",
                index=False, encoding="utf-8-sig")

    for builder in (fig06, fig07):
        fig, names = builder(df)
        made += style.save(fig, names[0])

    made.append(style.dump_plotted_values())
    for p in made:
        print(f"  ✓ {p.relative_to(style.ROOT)}")
    print(f"\n共 {len(made)} 个文件；中文字体：{style.FONT}")


if __name__ == "__main__":
    main()
