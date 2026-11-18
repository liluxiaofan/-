"""统一绘图样式与公共工具（NP-TOU 项目）。

所有图形脚本只通过本模块设置样式、颜色、标记与保存方式，
以保证 Figure 1–7 的字体、字号、图例、坐标轴风格完全一致。

设计约定
--------
* 字体：Arial Unicode MS（TrueType，含完整 CJK，可随 PDF 嵌入）
* 字号：正文刻度 8.5 pt，轴标签 9.5 pt，图例 8 pt，注记 7.5 pt
* 颜色：按方法固定（语义色，全图复用），见 METHOD_COLOR
* 标记：W1 圆、W2 方、W3 三角
* 输出：<stem>.pdf（矢量，TrueType 嵌入）+ <stem>.png（300 dpi）
* 不在图内写结论式标题：图题统一放在 FIGURE_TABLE_CATALOG.md 的 caption 中
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ticker import MultipleLocator  # noqa: F401  (供各图按需导入使用)

# --------------------------------------------------------------------------
# 路径
# --------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / "figures"
TABLE_DIR = ROOT / "tables"
for _d in (FIG_DIR, TABLE_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------
# 方法 / 窗口元数据（顺序、标签、颜色、标记）
# --------------------------------------------------------------------------
METHOD_ORDER = [
    "M1_NP_DP",
    "B0_policy",
    "B4_DP_lambda0",
    "B5_deep_valley",
    "B1_quantile",
    "B2_kmeans",
    "B3_netload_2025",
    "B3_netload",
]

METHOD_LABEL = {
    "M1_NP_DP": "M1 负价感知DP",
    "B0_policy": "B0 现行政策",
    "B4_DP_lambda0": "B4 同法 λ=0",
    "B5_deep_valley": "B5 深谷扩展",
    "B1_quantile": "B1 分位切段",
    "B2_kmeans": "B2 K-means",
    "B3_netload_2025": "B3b 净负荷(2025)",
    "B3_netload": "B3 净负荷(2018)",
}

# 语义色：主方法深蓝、关键对照砖红、现行政策近黑，其余为 Okabe–Ito 系
METHOD_COLOR = {
    "M1_NP_DP": "#1F4E79",
    "B0_policy": "#2B2B2B",
    "B4_DP_lambda0": "#C0392B",
    "B5_deep_valley": "#8E44AD",
    "B1_quantile": "#E69F00",
    "B2_kmeans": "#56B4E9",
    "B3_netload_2025": "#2E8B57",
    "B3_netload": "#8C8C8C",
}

WINDOW_ORDER = ["W1", "W2", "W3"]
WINDOW_LABEL = {"W1": "W1 (5–6月)", "W2": "W2 (7–8月)", "W3": "W3 (10月)"}
WINDOW_MARKER = {"W1": "o", "W2": "s", "W3": "^"}

GRID_COLOR = "#D9D9D9"
ACCENT = "#C0392B"

# --------------------------------------------------------------------------
# 字体探测
# --------------------------------------------------------------------------
_FONT_CANDIDATES = [
    "Arial Unicode MS",   # TrueType + 完整 CJK，PDF 嵌入最稳
    "PingFang SC",
    "Songti SC",
    "Heiti SC",
    "Hiragino Sans GB",
    "DejaVu Sans",
]


def pick_font() -> str:
    """返回本机可用的第一个 CJK 字体名。"""
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in _FONT_CANDIDATES:
        if name in available:
            return name
    raise RuntimeError(
        "未找到可用的中文字体，请安装 Arial Unicode MS 或 PingFang SC。"
    )


FONT = pick_font()

# --------------------------------------------------------------------------
# 全局 rcParams
# --------------------------------------------------------------------------
BASE_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": [FONT, "DejaVu Sans"],
    "axes.unicode_minus": False,
    "font.size": 8.5,
    "axes.titlesize": 10,
    "axes.labelsize": 9.5,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
    "legend.fontsize": 8,
    "legend.title_fontsize": 8,
    "legend.frameon": True,
    "legend.framealpha": 0.92,
    "legend.edgecolor": "#CCCCCC",
    "legend.fancybox": False,
    "legend.borderpad": 0.5,
    "legend.labelspacing": 0.35,
    "legend.handlelength": 1.6,
    "axes.linewidth": 0.8,
    "axes.edgecolor": "#333333",
    "axes.labelcolor": "#1A1A1A",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.axisbelow": True,
    "axes.grid": True,
    "grid.color": GRID_COLOR,
    "grid.linewidth": 0.6,
    "grid.linestyle": "-",
    "grid.alpha": 0.9,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
    "xtick.major.size": 3.2,
    "ytick.major.size": 3.2,
    "xtick.color": "#333333",
    "ytick.color": "#333333",
    "lines.linewidth": 1.2,
    "lines.markersize": 5.5,
    "lines.markeredgewidth": 0.7,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "pdf.compression": 6,
    "figure.constrained_layout.use": False,
}


def apply_style() -> None:
    """应用全局样式（幂等）。"""
    plt.rcParams.update(BASE_RC)


# --------------------------------------------------------------------------
# 保存
# --------------------------------------------------------------------------
PLOTTED_VALUES: dict[str, dict[str, float]] = {}


def record(fig_id: str, **values: float) -> None:
    """记录图中实际绘制的数值，供 verify_outputs.py 与 CSV 逐项核对。"""
    PLOTTED_VALUES.setdefault(fig_id, {}).update(
        {k: float(v) for k, v in values.items()}
    )


def save(fig, stem) -> list[Path]:
    """同时保存矢量 PDF 与 300 dpi PNG，返回路径列表。

    stem 允许传入单元素列表（配合 ``fig_xx() -> (fig, [name])`` 的返回约定）。
    """
    if isinstance(stem, (list, tuple)):
        stem = stem[0]
    pdf_path = FIG_DIR / f"{stem}.pdf"
    png_path = FIG_DIR / f"{stem}.png"
    meta = {
        "Title": stem,
        "Subject": "NP-TOU paper figure",
        "Creator": "matplotlib (make_figures.py)",
        "CreationDate": None,
        "ModDate": None,
    }
    fig.savefig(pdf_path, format="pdf", metadata=meta)
    fig.savefig(png_path, format="png", dpi=300)
    plt.close(fig)
    return [pdf_path, png_path]


def dump_plotted_values(path: Path | None = None) -> Path:
    """把记录到的绘图数值写到 figures/plotted_values.json。"""
    path = path or (FIG_DIR / "plotted_values.json")
    path.write_text(
        json.dumps(PLOTTED_VALUES, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def pct(x: float, nd: int = 1) -> str:
    """百分比标签（统一小数位）。"""
    return f"{x:.{nd}f}%"


def load_main():
    """读取主结果表，并附加方法与窗口标签。"""
    import pandas as pd

    df = pd.read_csv(DATA_DIR / "main_results.csv")
    df["method"] = pd.Categorical(df["method"], METHOD_ORDER, ordered=True)
    df = df.sort_values(["window", "method"]).reset_index(drop=True)
    df["method_label"] = df["method"].astype(str).map(METHOD_LABEL)
    return df


def load_designs():
    """读取 24 小时档位表（用于边界稳定性 S 的复算）。"""
    import pandas as pd

    return pd.read_csv(DATA_DIR / "designs_boundaries.csv")
