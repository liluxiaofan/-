# FIGURE_TABLE_CATALOG
## NP-TOU 项目 · 论文图表目录、图注与数据溯源

> **生成日期**：2026-11-18
> **依据**：[`FIGURE_TABLE_PLAN.md`](FIGURE_TABLE_PLAN.md)（Fig 1–7、Table 1–6，未增删图号）
> **生成脚本**：`plotting_scripts/make_figures.py`、`make_tables.py`、`verify_outputs.py`（统一样式 `style.py`）
> **质量报告**：[`plotting_scripts/QC_REPORT.md`](plotting_scripts/QC_REPORT.md)（62 项检查，0 失败）
> **数据快照**：`data/*.csv`（15 个文件，来源与 SHA-256 见 `data/MANIFEST.csv`）
> **主数据**：`data/main_results.csv` — 24 行（3 窗口 × 8 方法）× 17 列

---

## 0. 数据可用性（与计划书的一处出入）

`FIGURE_TABLE_PLAN.md` §0 记录“逐日 CI 表 / λ 表 / 负对照表未随结果文件夹提供”。**本次核对发现 `results/` 已包含全部 17 张表**，因此本版对计划做了两处**加强**（内容与图号不变）：

| 计划原定 | 本版实际 | 影响 |
|---|---|---|
| Table 4 用 `EXPERIMENT_RESULTS.md` 的 reported 值，标注“reported, not recomputed” | 直接由 `results/ci_table.csv`（84 行）生成，并与摘要逐项比对一致 | 表格可复算，不再是转抄 |
| Table 5 用摘要表 | 直接由 `results/e4_ablation_lambda.csv`（5 行）生成 | 同上 |

**仍然无法生成**的，只有依赖**原始 xlsx** 的图（§5 列出）：桌面“原始数据集”只有 `._` AppleDouble 元数据（约 176 字节），没有实际价格/负荷工作簿。因此**没有**任何价格时间序列图、负价热力图、事件时长直方图——这些若用 `DATA_AUDIT.md` 的汇总值硬画，等于伪造分布形状。

---

## 1. 图片目录

所有图同时提供 `.pdf`（矢量，TrueType 内嵌）与 `.png`（300 dpi）。

| ID | 文件 | 回答的问题 | 图形 | 数据字段 | 关键数值 |
|---|---|---|---|---|---|
| **Fig 1** | `figures/fig01_coverage_b0_vs_m1.{pdf,png}` | 现行政策看见负价了吗？ | 分组柱 | `coverage`（B0、M1） | B0 34.5 / 0.0 / 47.9%；M1 76.7 / 73.2 / 84.5% |
| **Fig 2** | `figures/fig02_coverage_heatmap.{pdf,png}` | 8 方法 × 3 窗口的覆盖率格局 | 热力图 | `coverage` | 最高 B1 W3 85.9%；最低 B3 W2 2.4%；B0 W2 = 0.0% |
| **Fig 3** | `figures/fig03_coverage_regret.{pdf,png}` | 覆盖率是否以价格拟合为代价？ | 散点 | `coverage`, `regret` | M1 W1 76.7%/15.6%；B0 W1 34.5%/38.7%；B1 W3 85.9%/27.2% |
| **Fig 4** | `figures/fig04_bill_delta.{pdf,png}` | 是否达到 ≥2% 预注册改善？M1−B4 多大？ | 分组柱 + 增量柱 | `bill_delta_pct` | M1−B4 = −0.44 / +0.14 / +0.00 pp（聚合口径） |
| **Fig 5** | `figures/fig05_boundary_stability.{pdf,png}` | 覆盖率提升是否以边界频繁变动为代价？ | 柱状 | `designs_boundaries.csv` 的 `cuts` | S：M1 0.500、B1 0.625、B4 0.750、B2 0.875、B3/B3b 1.000 |
| **Fig 6** | `figures/fig06_bill_decomposition.{pdf,png}` | 账单变化里多少是转移支付、多少是结构效应？ | 哑铃图 | `bill_delta_raw_pct` vs `bill_delta_pct` | M1 W1：−16.76% → −4.43%；B4 W1：+14.80% → −3.99% |
| **Fig 7** | `figures/fig07_coverage_vs_bill.{pdf,png}` | 高覆盖率等于低账单吗？ | 散点 | `coverage`, `bill_delta_pct` | B5 W3 74.6%/+3.43%；M1 W3 84.5%/+2.18%；B1 W2 74.4%/−7.13% |

### 图注（可直接用于论文，中文）

**图 1** 现行政策（B0）与负价感知设计（M1）对负价小时的覆盖率。覆盖率为 pooled 口径，分母为各测试窗口内全部负价小时；W1 为 5–6 月、W2 为 7–8 月、W3 为 10 月 1–26 日。W2 的 B0 覆盖率为 0，原因是 7–8 月代理购电价格表不含深谷档，最低价档退化为凌晨 1–6 时，而负价集中在午间。数据：`main_results.csv`。

**图 2** 8 种时段划分方法在三个测试窗口的负价覆盖率（%）。行按“主方法—政策参照—关键对照—其他基线”排列，单元格内为 pooled 覆盖率。

**图 3** 负价覆盖率与价格拟合遗憾 R 的权衡。R =(SSE − oracle SSE)/oracle SSE，衡量时段划分对日内价格形状的拟合程度，**不是**用户电费。颜色表示方法，形状表示窗口。覆盖率与 R 之间没有单调关系：B0 在 W1 覆盖率最低但 R 最高（38.7%），B2/B3b 以较低覆盖率取得更低 R。

**图 4** 单位电费变化（收支中性口径，负值＝更便宜）。(a) 各方法相对现行政策 B0 的变化；B0 为参照组，Δ≡0，未绘制。(b) M1 与 B4（同方法 λ=0）之差，虚线为预注册的 ±2% 判据；三个窗口的差异分别为 −0.44、+0.14、+0.00 个百分点，均远低于阈值。注意 (b) 为**聚合口径**（由两行 CSV 相减），与表 4 的**逐日配对**口径有 0.01–0.02 pp 的舍入差。

**图 5** 时段表边界稳定性 S。S = 1 − 相邻窗口切点位置变化数 / ((K−1)×(窗口数−1))，K=5、窗口数=3，分母为 8；S=1 表示三个窗口切点完全不变。M1 的 S 最低（0.500），即覆盖率提升的代价是时段表随窗口变动。B0、B5 为政策档位设计，无切点，不参与计算。

**图 6** 单位电费变化的两种口径分解。方块为收支中性（κ 校正）后的变化，圆点为未校正的原始乘子口径，灰线长度即“转移成分”。M1 在 W1 的原始乘子口径为 −16.76%，校正后仅 −4.43%；B4 反之（+14.80% → −3.99%）。**原始乘子列不能读作用户节约。**

**图 7** 覆盖率与单位电费变化的关系。竖虚线为 80% 覆盖率参考线。覆盖率达到 80% 以上的设计仍可能使电费上升（M1 W3：84.5%/+2.18%），而覆盖率 74% 的设计也可能下降（B1 W2：74.4%/−7.13%），说明覆盖率不是福利指标。

### 统一绘图规范（`style.py` 强制执行）

- 字体 Arial Unicode MS（PDF 内嵌 FontFile2）；刻度 8.5 pt、轴标签 9.5 pt、图例 8 pt、注记 7–7.5 pt。
- 方法色固定：M1 `#1F4E79`、B0 `#2B2B2B`、B4 `#C0392B`、B5 `#8E44AD`、B1 `#E69F00`、B2 `#56B4E9`、B3b `#2E8B57`、B3 `#8C8C8C`；窗口标记 W1 圆、W2 方、W3 三角。
- 覆盖率轴 0–100%；电费轴不截断（−10.6 ~ +6.2，或按数据范围留边）；S 轴 0–1.16；零线始终可见。
- 图内不写结论式标题，图题由本文件的 caption 提供。

---

## 2. 表格目录

| ID | 文件 | 行数 | 数据来源 | 用途 |
|---|---|---|---|---|
| **Table 1** | `tables/table01_dataset_description.{csv,md}` | 18 | `data/price_clean.csv`（7 176 行）复算 + `DATA_AUDIT.md` 口径 | 数据与方法节 |
| **Table 2** | `tables/table02_baseline_performance.{csv,md}` | 24 | `data/main_results.csv` 逐行 | 主结果 |
| **Table 3** | `tables/table03_hypothesis_summary.{csv,md}` | 3 | `EXPERIMENT_PLAN.md` 判据 + 由 CSV 复算的证据 | 结果讨论 |
| **Table 4** | `tables/table04_statistical_results.{csv,md}` | 24 | `data/ci_table.csv`（metric = bill / cov） | 统计检验 |
| **Table 5** | `tables/table05_lambda_ablation.{csv,md}` | 5 | `data/e4_ablation_lambda.csv` | 消融 |
| **Table 6** | `tables/table06_data_audit_checks.{csv,md}` | 10 | `DATA_AUDIT.md` §8 | 附录：数据质量 |
| — | `tables/all_tables.xlsx` | 6 sheet | 上述 6 表 | 投稿/共享 |
| — | `tables/aux_boundary_stability_S.csv` | 6 | Fig 5 的 S 复算中间表 | 复核用 |

**Table 1** 的 18 项中有 11 项直接由 `price_clean.csv` 复算（299 天、7 176 h、1 130 负价小时＝15.75%、236 次事件、4.79/4/20 h、−80 地板价 742 h、负价落在深谷/低谷/平段/高峰/尖峰 = 29.7/26.8/39.8/2.6/1.1%），其余为口径说明并逐行标注来源。

**Table 4** 每行给估计值、95% CI、BH 校正 p 值、效应量与匹配天数。覆盖率行（cov）的配对天数少于电费行（bill），因为只有含负价小时的日子才有覆盖率可比；这一点已在表中以“天数”列显式区分。

---

## 3. 质量检查结果

完整逐项记录见 [`plotting_scripts/QC_REPORT.md`](plotting_scripts/QC_REPORT.md)：**62 项检查全部通过**。

| 检查 | 方法 | 结果 |
|---|---|---|
| 图内 198 个数据点 | 绘图时登记 `plotted_values.json`，再由 `verify_outputs.py` **独立**从 CSV 复算比对（不 import 绘图脚本） | 最大相对偏差 1.3×10⁻¹⁶（浮点噪声） |
| Fig 5 的 S | 由 `cuts` 复算 → 与 `boundary_stability.csv` 对照 | 5/5 一致；B3b 复算 1.000 |
| Table 2 的 168 个数值 | 逐单元格对照 `main_results.csv`，按显示精度设容差（覆盖率 0.005、电费 0.005、Jaccard 5×10⁻⁴） | 0 超差 |
| Table 4 的 72 个数值 | 对照 `ci_table.csv` | 0 超差 |
| Table 5 的 5 行 | 对照 `e4_ablation_lambda.csv` | 0 超差 |
| 文件完整性 | 7 图 × (PDF + PNG)、6 表 × (CSV + MD)、1 个 Excel | PNG 全部 300 dpi；PDF 全部 FontFile2 内嵌 |

---

## 4. 已知的口径差异（**不是**数据错误，但同一段落不要混用）

| # | 现象 | 原因 | 处理 |
|---|---|---|---|
| 1 | Fig 1 的 B0→M1 差距 42.2 / 73.2 / 36.6 pp，而 Table 4 的 paired 估计为 +45.0 / +69.5 / +29.3 pp | Fig 1 用 **pooled**（窗口内全部负价小时为分母）；Table 4 用**逐日配对**（先算每日覆盖率再平均） | 图注写“pooled”；表 4 用“配对”；两者不可互相替代 |
| 2 | Fig 4(b) 的 M1−B4 = −0.44 / +0.14 / +0.00，而 Table 4 为 −0.46 / +0.15 / +0.005 | 聚合相减 vs 逐日配对 + 两位小数舍入 | Fig 4 标“aggregate”；引用阈值判定时用 Table 4 |
| 3 | M1 相对 B5 的 W1 电费差：`main_results` 相减得 −1.730，`ci_table` 配对得 −1.778 | 同 #2 | 正文引用 B5 时统一用 Table 4 的 −1.78 |
| 4 | Table 6 中 303 天/7 272 h/15.5%/237 次/19 h/74.2%/46.7%/33.6% 等旧值 | 旧分母与“标签含端点”口径 | 论文一律用“复算值”列：299 天/7 176 h/15.75%/236 次/20 h/63.54%/35.66%/43.45% |
| 5 | Fig 5 含 B3b，但 `boundary_stability.csv` 只有 5 个方法 | 官方表未收录新增基线 | B3b 的 S 由 `designs_boundaries.csv` 复算（7-10-15-18 三窗口相同 → 1.000），已在 QC 中单列 |

### 需要更正的旧表述

旧版目录曾写“**M1 覆盖率最高**”，与数据不符：M1 仅在 W1 最高（76.7% vs B1 68.6%），在 W2、W3 均略低于 B1（73.2% vs 74.4%；84.5% vs 85.9%）。正文应写“M1 的覆盖率显著高于 B0 与 B4，但与 B1 同量级”。

---

## 5. 未生成的图（及原因）

| 建议图 | 为什么没有 |
|---|---|
| 2026 年价格时间序列、负价小时×月份热力图 | 原始 xlsx 不在手（桌面“原始数据集”仅 `._` 元数据）；`DATA_AUDIT.md` 只有汇总值，硬画会伪造分布 |
| 负价事件时长直方图 | 同上；仅有 4.79/4/20 h 三个汇总量 |
| 24 小时档位归属图（boundary map） | 旧 `fig05_boundaries.png` 无脚本；`lowest_hours` 跨月，单日 24 h 图会误导；如需可另做“三窗口×24h”热力图（数据在 `designs_boundaries.csv` 的 `labels_24h`，可补） |
| λ 敏感性曲线 | 计划未列；数据 `e2_lambda_selection.csv` 已在手，若审稿要求可补 1 张（λ 仅 5 点，且 0–2 完全重合，曲线意义有限） |
| 负对照分布图 | 计划未列；`e4_negative_control.csv`（200 次）已在手，可补 |
| CI forest plot | 计划未列；`ci_table.csv` 已有全部 CI，可补 |

**当前严格按计划出 7 图 6 表**；上述 3–4 张为可选补充，未纳入本轮交付。

---

## 6. 论文中的推荐用法

| 位置 | 图/表 | 一句话结论 |
|---|---|---|
| Results 1：现行政策是否看见负价 | Fig 1 + Table 2（B0 行） | B0 覆盖率 34.5 / 0.0 / 47.9%，W2 完全看不见负价 |
| Results 2：方法对比 | Fig 2 + Table 2 | M1 覆盖率显著高于 B0/B4，但与 B1 同量级；其 R 不是最低 |
| Results 3：覆盖率的代价 | Fig 3 + Fig 5 | 覆盖率提升伴随 R 上升与边界不稳定（M1 的 S=0.500 最低） |
| Results 4：用户电费 | Fig 4 + Table 4 | M1−B4 三窗口 −0.46/+0.15/+0.005%，均未达 2% 阈值；H2 不支持 |
| Results 5：账单分解 | Fig 6 | 原始乘子 −16.8% 与收入中性 −4.4% 的差额主要是转移支付 |
| Discussion：覆盖率≠福利 | Fig 7 | 覆盖率 80%+ 仍可能涨价；覆盖率不是福利指标 |
| Appendix：数据质量 | Table 1 + Table 6 | 299 天/7 176 h、实时价、严格区间口径；旧文档数字已修正 |

### 禁止写法

- ❌ “负价感知设计使用户电费下降 10.36%”——那是 A11 的净负荷成本，不是本文口径。
- ❌ “M1 显著优于 B0”——账单方向在 W3 反转（+2.18%）；覆盖率显著 ≠ 账单显著。
- ❌ “M1 覆盖率最高”——W2/W3 低于 B1，见 §4。
- ❌ “原始乘子口径的 −16.8% 是用户节约”——那是零售商少收钱（转移支付）。
- ❌ “CI 很小所以方法稳定”——CI 只含日间变异，不含设计选择不确定性。

---

## 7. 复现

```bash
cd /Users/liuxiaofan/Desktop/科研大脑
python3 plotting_scripts/make_figures.py     # Fig 1–7（PDF + 300dpi PNG）
python3 plotting_scripts/make_tables.py      # Table 1–6（CSV + MD + XLSX）
python3 plotting_scripts/verify_outputs.py   # 数值核对 → QC_REPORT.md
```

依赖：`pandas`、`numpy`、`matplotlib`、`openpyxl`；中文字体 `Arial Unicode MS`（缺失时自动回退 PingFang SC / Songti SC）。

---

## 8. 一句话

> 这 7 图 6 表支持的结论是：**负价信息把时段表推向午间，覆盖率从 34.5%/0%/47.9% 提到 76.7%/73.2%/84.5%，但用户电费没有达到预注册的 2% 改善（M1−B4 仅 −0.46/+0.15/+0.005%），且覆盖率提升以价格拟合遗憾与边界不稳定为代价；高覆盖率不等于低账单。** 这是一个“部分支持 + 阴性结果”的图表集，不是“方法更优”的宣传图。
