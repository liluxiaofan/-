# NP-TOU · 负价感知的分时电价时段设计

科研创新挑战赛中期仓库。研究问题：在零售侧负价不传导、浮动比例受政策锁定的条件下，以负价事件经验分布用于时段边界设计，能否在样本外降低用户电费、缩小与事后最优时段的差距，以及该结论的成立边界。

## 仓库结构

| 路径 | 内容 |
|---|---|
| `code/` | 可复跑实验代码（`run_all.py` + `np_tou/` 10 个模块），一键运行约 7 秒 |
| `data/` | 清洗后的价格序列、政策时段表、负荷代理数据 |
| `results/` | 17 个 CSV 结果表、`run_summary.json`、审计产物 |
| `RESULTS_FIGURES/` | 14 张 300 dpi 结果图（图1–图15，图12 含双面板） |
| `tables/` / `figures/` | 中期报告用表与图 |
| `plotting_scripts/` | 独立复算与校验脚本 |
| `*.md` | 研究宪章、文献核查、方法/实验计划、数据审计、结果说明等全套文档 |

## 快速复跑

```bash
cd code
python3 -m pip install -r requirements.txt
python3 run_all.py
```

依赖仅 `pandas`、`numpy`、`matplotlib`、`openpyxl`。默认数据路径为 `/Users/liuxiaofan/Desktop/原始数据集`，可通过环境变量覆盖：

```bash
NPTOU_DATA_DIR="/path/to/原始数据集" python3 run_all.py
```

详见 [`code/README.md`](code/README.md)。

## 关键文档

- [`PROJECT_OVERVIEW.md`](PROJECT_OVERVIEW.md) — 项目总览与研究现状
- [`DATA_AUDIT.md`](DATA_AUDIT.md) — 数据审计与口径核验
- [`METHOD_PLAN.md`](METHOD_PLAN.md) / [`EXPERIMENT_PLAN.md`](EXPERIMENT_PLAN.md) — 方法与实验设计
- [`EXPERIMENT_RESULTS.md`](EXPERIMENT_RESULTS.md) — 三窗口实验结果与假设判定
- [`FIGURE_TABLE_AUDIT.md`](FIGURE_TABLE_AUDIT.md) — 图表独立复算审计

## 结果摘要

现行政策时段（B0）的负价覆盖率约 34.49% / 0% / 47.89%（三个滚动窗口），负价感知方法（M1）为 76.66% / 73.17% / 84.51%。电费指标上 M1 相对 B0 为 −0.46% / +0.15% / +0.005%，未超过"扩深谷"基线（B4）。原始用户负荷缺失，电费部分为负荷形状迁移代理下的**情景结果**，不作因果宣称。

> AI（WorkBuddy Agent）辅助完成代码实现、审计复算、图表生成与质量审查；研究设计与结论由作者负责。
