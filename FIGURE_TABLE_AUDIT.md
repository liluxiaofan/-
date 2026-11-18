# FIGURE_TABLE_AUDIT
## NP-TOU 项目 · 论文图表与统计表审查报告（Scientific Visualization Review）

> **审查日期**：2026-11-18
> **审查对象**：`C:\Users\lenovo\Desktop\科研大脑\` 下的 `figures/`（7 张主图）、`RESULTS_FIGURES/`（14 个文件 / 15 个图号）、`tables/`（6 张表）、`plotting_scripts/`、`code/np_tou/figures.py`、`results/`
> **原始数据**：`C:\Users\lenovo\Desktop\相关数据\`（价格 xlsx 可用）；`C:\Users\lenovo\Desktop\原始数据集\`（只有 `._` AppleDouble 元数据）；`科研大脑/data/`（派生 CSV）
> **原则**：只判断可追溯性与科学表达，不修改数据、不伪造数值。缺少原始数据或绘图代码的图表，明确标为 **“无法完成数值核验”**。

---

## 0. 结论先行

| 结论 | 判定 |
|---|---|
| 7 张主图（`figures/fig01–07`） | **可保留，但需修 3 处**：Fig 4/6/7 的负荷来源与不确定性说明、Fig 3 的目录 caption 错误、Fig 4 与 Table 4 的口径标注 |
| 14 个 `RESULTS_FIGURES/` 文件（15 个图号） | **不能按现状作为论文图**：图号/文件名不一致，且未进入 `FIGURE_TABLE_CATALOG`；其中 4 张依赖缺失的原始负荷 |
| 6 张表 | **Table 1/2/5/6 基本可用**；**Table 3 有硬性数值错误（Critical）**；**Table 4 需补口径与效应量说明** |
| 原始负荷数据 | **缺失**：`山东省用户小时负荷.xlsx` / `山东省净负荷.xlsx` 只有 `._` 元数据；`data/MANIFEST.csv` 没有 load/netload；所有用户电费图/表**无法从原始数据独立复算** |
| 总体是否达到论文初稿要求 | **未达到**。Critical 问题解决前，不能把“用户电费”相关图作为已验证结果提交 |

**一句话**：价格侧图表基本可追溯；“用户电费”侧图表只有派生 CSV，没有原始负荷，且 Figure 8/14、Table 3 存在会误导读者的刻度/标题/数值问题。**当前是“可修复的内部稿”，不是“可投稿稿”。**

---

## 1. 图表清单（Inventory）

### 1.1 主图（`figures/`，7 张，论文正文候选）

| ID | 标题/内容 | 文件 | 类型 | 对应 RQ/H | 数据 | 代码 | 准备支持的主张 | 状态 |
|---|---|---|---|---|---|---|---|---|
| **F1** | 现行政策 vs M1 的负价覆盖率 | `fig01_coverage_b0_vs_m1.{png,pdf}` | 分组柱 | SQ1 / H1 | `data/main_results.csv` `coverage` | `plotting_scripts/make_figures.py::fig01` | B0 覆盖不足，M1 提高覆盖率 | 可保留；无 CI（描述性） |
| **F2** | 8 方法 × 3 窗口覆盖率热力图 | `fig02_coverage_heatmap.{png,pdf}` | 热力图 | SQ1/SQ2 / H1 | 同上 | `make_figures.py::fig02` | 方法间覆盖率格局 | 可保留 |
| **F3** | 覆盖率 vs 价格拟合遗憾 | `fig03_coverage_regret.{png,pdf}` | 散点 | SQ3 / H3 | `coverage`, `regret` | `make_figures.py::fig03` | 覆盖率有代价 | 可保留；目录 caption 有错（M8） |
| **F4** | 收入中性账单变化 + M1−B4 增量 | `fig04_bill_delta.{png,pdf}` | 分组柱 + 增量柱 | SQ2 / H2 | `bill_delta_pct`（派生） | `make_figures.py::fig04` | 未达到 2% 改善 | **依赖缺失负荷；无 CI** |
| **F5** | 边界稳定性 S | `fig05_boundary_stability.{png,pdf}` | 柱状 | SQ3/稳健性 | `designs_boundaries.csv`, `boundary_stability.csv` | `make_figures.py::fig05` | M1 边界最不稳定 | 可保留 |
| **F6** | 原始乘子 vs 收支中性 | `fig06_bill_decomposition.{png,pdf}` | 哑铃图 | SQ2/会计口径 | `bill_delta_raw_pct` vs `bill_delta_pct`（派生） | `make_figures.py::fig06` | 原始乘子不能读作节约 | **依赖缺失负荷；措辞需改** |
| **F7** | 覆盖率 vs 账单变化 | `fig07_coverage_vs_bill.{png,pdf}` | 散点 | SQ2/SQ3 | `coverage`, `bill_delta_pct`（派生） | `make_figures.py::fig07` | 高覆盖 ≠ 低账单 | **依赖缺失负荷** |

### 1.2 结果图（`RESULTS_FIGURES/`，14 个文件 / 15 个图号）

> **注意**：`fig01_price_overview.png` 内同时有“图1”和“图2”；其余文件与内部图号存在 +1 偏移。**文件数 14，图号 15**。

| ID | 内部图号/标题 | 文件 | 类型 | 对应 RQ/H | 数据 | 代码 | 状态 |
|---|---|---|---|---|---|---|---|
| **S1** | 图1 2026 价格走势（日均 + 日内 min–max） | `fig01_price_overview.png`（上半） | 线 + 区间 | SQ1 | `data/price_clean.csv` | `code/np_tou/figures.py::fig_price_overview` | 数值可复算；**与 S2 同文件，图号错误（C3）** |
| **S2** | 图2 月度负价小时占比 | `fig01_price_overview.png`（下半） | 柱状 | SQ1 | `e1_neg_monthly.csv` / `price_clean` | 同上 | 数值可复算；**无独立文件（C3）** |
| **S3** | 图3 负价“月份×钟点”热力图 | `fig02_neg_heatmap.png` | 热力图 | SQ1 | `e1_neg_profile_by_month_hour.csv` | `fig_neg_heatmap` | 可复算；色标 0–90 |
| **S4** | 图4a/4b 事件时长 + 钟点分布 | `fig03_neg_structure.png` | 直方图/柱 | SQ1 | `price_clean.csv` | `fig_neg_structure` | 可复算（n=236，中位 4 h） |
| **S5** | 图5a/5b B0 档位占比 + 逐月覆盖 | `fig04_b0_coverage.png` | 柱 + 线 | SQ1/H1 | `e1_coverage_b0.csv` | `fig_b0_coverage` | 可复算；H1 >90% 线 |
| **S6** | 图6 24h 档位归属（三窗口） | `fig05_boundaries.png` | 线 + 条带 | SQ3/方法 | `designs_boundaries.csv` + price/netload | `fig_boundaries` | **标题“按电价排名”不适用于 B3/B3b；代表月未注明（M2）** |
| **S7** | 图7 各方法样本外覆盖率 | `fig06_coverage_by_method.png` | 分组柱 | SQ2/H1 | `main_results.csv` | `fig_coverage_by_method` | 可复算；标签取整 |
| **S8** | 图8 覆盖率×regret | `fig07_tradeoff.png` | 散点 | SQ3 | `main_results.csv` | `fig_tradeoff` | 与 F3 重复；颜色与 F3 不一致（M4） |
| **S9** | 图9a/9b λ 消融 | `fig08_lambda_ablation.png` | 折线 | SQ3/消融 | `e4_ablation_lambda.csv` | `fig_lambda` | **左轴 45–85 截断；无图例（M1）** |
| **S10** | 图10 负对照 CDF | `fig09_negative_control.png` | 阶梯 CDF | 稳健性 | `e4_negative_control.csv` | `fig_negative_control` | p=0.075；x 轴截断 35–77（N2） |
| **S11** | 图11 K×L_min 敏感性 | `fig10_sensitivity.png` | 热力图 | 稳健性 | `e4_robustness.csv` | `fig_sensitivity` | 可复算 |
| **S12** | 图12a/12b 代理负荷/鸭子曲线 | `fig11_load_profile.png` | 折线/面积 | 数据描述 | 2018/2025 load（**缺失**） | `fig_load_profile` | **无法从原始负荷复算（C1）** |
| **S13** | 图13 账单变化 + 95% CI | `fig12_bill_delta.png` | 柱 + 误差棒 | SQ2/H2 | `e3_bill_ci_vs_B0.csv`（派生） | `fig_bill_delta` | **依赖缺失负荷（C1）** |
| **S14** | 图14 账单“转移/结构”分解 | `fig13_bill_decomp.png` | 分组柱 | SQ2/会计 | `main_results.csv`（派生） | `fig_bill_decomp` | **依赖缺失负荷；“转移”措辞（M11）** |
| **S15** | 图15 弹性情景 | `fig14_elasticity.png` | 折线 | SQ2/H3 | `e3_scenarios.csv`（派生） | `fig_elasticity` | **依赖缺失负荷；标题与数据矛盾（C4）** |

### 1.3 表格（`tables/`，6 张）

| ID | 标题 | 文件 | 数据 | 代码 | 主要主张 | 状态 |
|---|---|---|---|---|---|---|
| **T1** | 数据集描述 | `table01_dataset_description.csv/.md` | `DATA_AUDIT` + `price_clean` | `make_tables.py` | 299 天/7176 h、负价 15.75%、代理负荷 | **负荷部分无法原始核验**；H1 措辞需改（M7） |
| **T2** | 基线性能（24 行） | `table02_baseline_performance.csv/.md` | `main_results.csv` | `make_tables.py` | 覆盖率/regret/账单 | 价格列可复算；账单列依赖缺失负荷 |
| **T3** | 假设判定 | `table03_hypothesis_summary.csv/.md` | `EXPERIMENT_RESULTS` + `e3_*` | `make_tables.py` | H1 支持/H2 不支持/H3 混合 | **H3 有硬性错误（C2）** |
| **T4** | 统计结果（24 行） | `table04_statistical_results.csv/.md` | `ci_table.csv` | `make_tables.py` | 配对估计/CI/p/BH | 数值与 CI 表一致；**效应量 d 需删/注（M5）**；基线口径需注（M6） |
| **T5** | λ 消融（5 行，W1） | `table05_lambda_ablation.csv/.md` | `e4_ablation_lambda.csv` | `make_tables.py` | λ 高阈值才变切点 | 数值一致；**仅 W1 需注明** |
| **T6** | 数据审计修正 | `table06_data_audit_checks.csv/.md` | `DATA_AUDIT` §8 | `make_tables.py` | 303→299 等 | 数值与审计一致 |

### 1.4 概念/方法图

| 图 | 类型 | 与 METHOD_PLAN 的一致性 | 结论 |
|---|---|---|---|
| **S6 / 图6** (`fig05_boundaries.png`) | 24h 档位条带 + 设计窗口均价 | 方法集合 M1/B0/B1/B2/B3/B3b/B4/B5 与 METHOD_PLAN 一致；但标题“按电价排名”不适用于 B3/B3b（净负荷排名）与 B0/B5（政策档位） | **逻辑需修正**（M2），无虚构模块 |
| 其他 | 数据图，不是流程图 | 无算法流程图/架构图 | 不适用“模块/箭头”核验 |

---

## 2. 数据可用性与核验范围（先看这一节）

| 数据 | 位置 | 状态 | 能否复算 |
|---|---|---|---|
| 2026 小时价格 | `相关数据/2026年现货电价-截至10月26日.xlsx`；`data/price_clean.csv`（7176 行） | **可用** | **能**：299 天/7176 h、负价 1130、事件 236、月度占比均可复算 |
| 2025 月均价格 | `相关数据/2025年现货电价-*.xlsx` | 可用（月均，不能日度） | 能核对月均，不能用于日度 OOS |
| 用户小时负荷 2018 | `原始数据集/山东省用户小时负荷.xlsx` | **只有 `._`（163 字节），无实际 xlsx** | **不能** |
| 净负荷 2018/2025 典型日 | `原始数据集/山东省净负荷.xlsx` | **只有 `._`（163 字节），无实际 xlsx** | **不能** |
| 派生结果表 | `科研大脑/results/*.csv`、`data/*.csv` | 可用 | 能核对“图/表 ↔ 派生 CSV”，**不能核对“派生 CSV ↔ 原始负荷”** |
| 绘图代码 | `plotting_scripts/`、`code/np_tou/figures.py` | 可用 | 能重画（价格侧） |

**关键判断**：
- **F1/F2/F3/F5、S1–S11** 主要依赖价格/设计，**可从 `price_clean.csv` 与 `results` 复算**（其中 S6 的 B3/B3b 条带依赖缺失净负荷）。
- **F4/F6/F7、S12–S15、T2 的账单列、T4 的账单行、T3 的 H2/H3** 依赖 2018/2025 负荷；**原始负荷缺失，无法完成数值核验**。
- `data/MANIFEST.csv` 只有 15 个派生文件，**没有 load/netload**；`config.py` 的 `LOAD_FILE`/`NETLOAD_FILE` 指向不存在的文件。
- `相关数据/` 有价格 xlsx，但**没有** `山东省用户小时负荷.xlsx`/`山东省净负荷.xlsx`。`FIGURE_TABLE_CATALOG` §0 说“原始数据集只有 `._`”只对 `原始数据集` 成立；**不能据此说价格原始数据缺失**（价格在 `相关数据`）。

---

## 3. 主图逐图审查（F1–F7）

### F1 `fig01_coverage_b0_vs_m1`
- **问题/主张**：B0 负价覆盖率 34.5/0/47.9%，M1 76.7/73.2/84.5%；W2 B0=0。
- **数据/代码**：`main_results.csv`；`make_figures.py::fig01`；`plotted_values.json` 6 点；QC 通过。
- **检查**：坐标 0–100%；零线；单位清晰；无截断；无误差线（描述性 pooled，可接受，但 caption 必须写 pooled）。
- **结论**：**可保留**。Caption 需注明“pooled；W3 仅 10 月 1–26 日”。

### F2 `fig02_coverage_heatmap`
- **检查**：8×3 单元格与 T2 一致；色标 0–100；无截断；行序符合“主方法—政策—关键对照—基线”。
- **结论**：**可保留**。

### F3 `fig03_coverage_regret`
- **检查**：x 0–95、y 0–43；B0 W1（34.5, 38.7）、M1 W1（76.7, 15.6）与 CSV 一致。
- **问题**：`FIGURE_TABLE_CATALOG` caption 写“**B0 在 W1 覆盖率最低**但 R 最高”；实际 B3 W1 覆盖率 5.23%，低于 B0 34.49%。**Caption 事实错误（M8）**。
- **结论**：图本身可保留；caption 必须改。

### F4 `fig04_bill_delta`
- **检查**：左图 7 方法 × 3 窗口；右图 M1−B4 −0.44/+0.14/+0.00 pp；与 T4 的 −0.46/+0.15/+0.005 有 0.01–0.02 pp 口径差（已由 catalog 注明）。
- **问题**：
  - **原始负荷缺失**：`main_results` 的 `bill_delta_pct` 依赖 2018/2025 代理负荷；无法从原始数据复算（C1）。
  - **无 CI/误差线**：图只给聚合值；T4 有 paired CI。读者可能把“−0.44”当作精确值；caption 必须写“aggregate；paired CI 见 Table 4”（M10）。
- **结论**：**可保留但需加口径注/CI**；在原始负荷补齐前不能作为“已核验”主结果。

### F5 `fig05_boundary_stability`
- **检查**：S M1 0.500、B4 0.750、B1 0.625、B2 0.875、B3/B3b 1.000；与 `boundary_stability.csv`/复算一致；y 0–1.16。
- **结论**：**可保留**。

### F6 `fig06_bill_decomposition`
- **检查**：M1 W1 raw −16.76→neutral −4.43；B4 W1 +14.80→−3.99；与 CSV 一致。
- **问题**：依赖缺失负荷（C1）；“转移成分”是会计差额，不是可观测转移（M11）；无 CI。
- **结论**：**需补原始负荷/措辞**；图本身保留。

### F7 `fig07_coverage_vs_bill`
- **检查**：B5 W3 74.6/+3.43、M1 W3 84.5/+2.18、B1 W2 74.4/−7.13；与 CSV 一致；x 0–97、y −10.4~6.4。
- **问题**：依赖缺失负荷（C1）；无 CI。
- **结论**：**可保留但需注 C1**。

---

## 4. 结果图逐图审查（S1–S15）

### S1/S2 `fig01_price_overview`（图1 + 图2）
- **数据/代码**：`price_clean.csv` + `e1_neg_monthly.csv`；`figures.py::fig_price_overview`；299 天/7176 h；月度负价 19.0/31.2/14.9/25.7/24.2/14.9/7.4/3.6/6.0/11.4%，与复算一致。
- **Critical（C3）**：一个 PNG 内出现“图1”和“图2”，而 `EXPERIMENT_RESULTS §6` 也写“图1–2”；文件只有 14 个，图号 15 个。正文如果引用“图2”，没有独立文件；如果引用“图1–2”，又不是规范图号。
- **建议**：拆成两个文件（`fig01_price_overview`=图1，`fig02_neg_monthly`=图2），后续 13 个文件整体后移一位；或明确合并为“图1a/1b”并只保留一个图号。
- **结论**：**必须重绘/重命名**。

### S3 `fig02_neg_heatmap`（图3）
- **数据/代码**：`e1_neg_profile_by_month_hour.csv`；`fig_neg_heatmap`；色标 0–90。
- **检查**：月份×小时；x 轴标签 1–23（偶数小时无标签，但单元格完整）；标题说明“负价天数占比”。
- **结论**：可保留；建议补“24 时”标签/色标上限说明（Minor）。

### S4 `fig03_neg_structure`（图4a/4b）
- **数据/代码**：`price_clean.csv`；事件 236、中位 4 h、均值 4.79、最长 20 h；与复算一致。
- **检查**：左图时长分布；右图钟点分布；x 轴 0–20；单位清晰。
- **结论**：可保留；图号与文件名差 1（C3 的一部分）。

### S5 `fig04_b0_coverage`（图5a/5b）
- **数据/代码**：`e1_coverage_b0.csv`；`fig_b0_coverage`；负价档位 29.7/26.8/39.8/2.6/1.1%；逐月覆盖。
- **检查**：y 0–40 / 0–105；H1 >90% 线；7–8 月 0；与 T1/复算一致。
- **结论**：可保留；图号差 1（C3）。

### S6 `fig05_boundaries`（图6）
- **数据/代码**：`designs_boundaries.csv` + `price_clean`/netload；`fig_boundaries`。
- **逻辑问题（M2）**：
  - 标题写“**按电价排名映射到政策档位**”，但 `billing.py` 的 `coef_vector` 对 partition 设计使用 `design.meta['means']`；`baselines.py` 的 B3/B3b `means` 是**净负荷段均值**（`rank_by: netload`），B0/B5 直接是政策档位。因此该标题对 B3/B3b/B0/B5 都不准确。
  - `m_ref = median(test months)`：条带只代表一个“中位测试月”，但图题/图注没有说；B0 逐月变化，读者会以为是整个窗口的政策表。
- **结论**：**必须改标题/注“代表月”，并说明 B3/B3b 按净负荷排名**；否则概念图与实际方法不一致。

### S7 `fig06_coverage_by_method`（图7）
- **检查**：值 77/73/85 等来自 `main_results`；与 T2 一致（取整）；y 0–104。
- **结论**：可保留；但建议保留 1 位小数（N1），避免 76.7→77 的“整数精度”错觉。

### S8 `fig07_tradeoff`（图8）
- **检查**：与 F3 同一数据（coverage×regret），只是配色/图例不同；x 0–40、y auto；M1/B0/B4/B5 色与 F3 不一致（M3/M4）。
- **结论**：**与 F3 重复**；保留一张即可，另一张移补充或删；若要保留，统一颜色。

### S9 `fig08_lambda_ablation`（图9a/9b）
- **数据/代码**：`e4_ablation_lambda.csv`；λ 0/0.5/1/2/5；test coverage 46.7→76.7；SSE 51.54→50.38。
- **问题（M1，Major）**：
  - 左图 y 轴 45–85，**截断**（0 未显示），把 46.7→76.7 的差异视觉放大；覆盖率的自然轴是 0–100。
  - 左图有两条线（测试/验证），但代码只设 `label=`，**没有 `ax.legend()`**；读者无法分辨红/蓝。
  - 右图 SSE 50.4–51.6 也是截断；至少应标注“zoom / 绝对差 <1.2×10⁶”。
- **结论**：**必须重绘**（轴、图例、注）。

### S10 `fig09_negative_control`（图10）
- **数据/代码**：`e4_negative_control.csv`；200 次打乱；p=0.075（图显示 0.07）；真实 76.7%。
- **检查**：CDF 正确；x 轴 35–77（截断），但 CDF 只在数据范围画；y 0–105。
- **结论**：可保留；建议 x 轴 30–80 或不截断并注“数据范围”（N2）。

### S11 `fig10_sensitivity`（图11）
- **数据/代码**：`e4_robustness.csv`；K=3–6 × L_min=1–3；λ=0/5；色标 0–100。
- **检查**：值合理；无截断；无误差线（确定性）。
- **结论**：可保留。

### S12 `fig11_load_profile`（图12a/12b）
- **数据/代码**：2018 load + 2025 typical；`fig_load_profile`；左 y 50–148，右 auto。
- **Critical（C1）**：原始 `山东省用户小时负荷.xlsx` / `山东省净负荷.xlsx` 缺失；**无法从原始数据复算**。图只是派生/历史运行的产物。
- **其他**：左 y 轴 50 起（数据 min ~59），虽未裁剪但截断；图注必须写“代理负荷/不同年”。
- **结论**：**在原始负荷补齐前不可作为已验证图**；可保留为“情景/数据描述”并明确标注。

### S13 `fig12_bill_delta`（图13）
- **数据/代码**：`e3_bill_ci_vs_B0.csv`；`fig_bill_delta`；95% CI；y −10~10；值 −8.5~+3.4。
- **Critical（C1）**：依赖缺失负荷；派生 CSV 无法回溯原始。
- **检查**：误差棒、零线、−2% 线；B0 未画（参照）。
- **结论**：**原始负荷补齐前只能作“情景图”**；不要称“用户账单”。

### S14 `fig13_bill_decomp`（图14）
- **数据/代码**：`main_results`；`fig_bill_decomp`；raw/neutral。
- **Critical（C1）**：依赖缺失负荷。
- **问题（M11）**：标题“红蓝两柱之差 = 平均乘子改变带来的转移，蓝柱才是结构效应”把会计残差称为“转移”；应改为“会计差额/平均乘子效应”，不能说成可观测的转移支付。
- **结论**：需改标题/注；补负荷后再作为结果图。

### S15 `fig14_elasticity`（图15）
- **数据/代码**：`e3_scenarios.csv`；`fig_elasticity`；τ=1、revenue_neutral；ε=0/−0.05/−0.10/−0.20。
- **Critical（C4）**：标题“**只有负荷真正转移（ε<0）时才出现电费节约**”与数据矛盾：`ε=0` 时 M1 W1 已是 −4.43%、W2 −7.02%（名义“节约”），W3 +2.18%。图注自己说“ε=0 差异来自会计口径与负荷形状”，但标题仍写“only when ε<0”。读者会把 ε=0 的负值误读为需求响应节约。
- **结论**：**必须改标题/图注**（“ε=0 已存在会计差异；ε<0 只改变幅度；不能把 ε=0 读作需求响应节约”），并依赖缺失负荷（C1）。

---

## 5. 表格逐表审查（T1–T6）

### T1 `table01_dataset_description`
- **可复算**：299 天/7176 h、负价 1130/15.75%、事件 236、−80 742 h、月度/档位 shares；与 `price_clean`/审计一致。
- **无法核验**：2018 负荷 8760 h、2025 典型日（原始 xlsx 缺失）。
- **问题（M7）**：第 13 行“平段近四成 → 零售侧拿不到负价信号（H1 的直接证据）”把 **H1（覆盖不足）** 与 **零售传导** 混在一起；H1 的证据是 B0 覆盖率，不是“平段 39.8%”。应改为“描述性证据：平段占负价 39.8%，说明现行档位没有把负价单独识别；是否传导需另验”。
- **结论**：可保留但需改措辞；负荷行标“代理/无法原始核验”。

### T2 `table02_baseline_performance`
- **可复算**：24 行；coverage/regret/unit bill/Δbill/Jaccard 与 `main_results` 的差异 ≤0.005（显示精度）；`cuts` 无竖线；`n_neg` 287/82/71 正确。
- **无法核验**：`单位电费`/`Δ电费` 列依赖缺失负荷（C1）。
- **问题**：无 CI/标准差；作为描述表可以，但必须注“账单列为派生/情景”。
- **结论**：价格/设计列可保留；账单列在负荷补齐前只能作情景。

### T3 `table03_hypothesis_summary`
- **H1**：B0 34.5/0/47.9；M1 76.7/73.2/84.5；+45.0/+69.5/+29.3 pp（paired）；与 T4 一致。
- **H2**：M1−B4 −0.46/+0.15/+0.005%；<1%；H2 不支持；与 T4 一致。
- **H3（Critical，C2）**：
  - 表中写“J(M1,B3b)=0.714（均 >80%）”；实际 **0.714 = 71.4% < 80%**，`J(M1,B5)=0.857=85.7%`；**“均 >80%”是错误**。
  - 表中写“分层 M1−B4 = −0.38/−0.36/−0.53 pp”；实际从低到高密度为 **−0.3799/−0.3563/−0.5304**，**不是单调扩大**（先变浅再变深）。
  - 影响：H3 的“方向正确、强度不足”表述不成立；应按预注册标准判“混合/不支持”，并明确 B3b 未过 80% 重合门槛。
- **结论**：**必须重新计算/重写**。

### T4 `table04_statistical_results`
- **可复算**：24 行与 `ci_table.csv` 的估计/CI 在 0.02 内一致；p/BH/天数/效应量列存在。
- **问题（M5）**：效应量 d 出现 **B5 W3 −56.15、B0 W3 17.02、B5 W2 16.32**；这是日间方差极小时的数学产物，绝对值只有 −1.21%/+2.18%/+1.60%。**不能把 d 当“巨大效应”**；应删除或加醒目注“d 不稳定，不作解释”。
- **问题（M6）**：
  - 表头“估计值”没有说明是 **M1 − 基线**；`基线` 列 B0/B4/B5/B3b 容易与 T2 的“vs B0”混淆。
  - 覆盖率天数 45/20/15（负价日），账单天数 61/62/26（全部测试日）；表头只写“天数”，需分开注。
  - 没有“是否达到预注册 2%”列；W1 B4 −0.46% 虽 p<0.001，但远低于 2%；读者可能把“BH 显著”误读为 H2 支持。
- **结论**：数值基本正确，但**统计表达不合格**；需补列/注，重生成表与 XLSX。

### T5 `table05_lambda_ablation`
- **可复算**：5 行 W1，λ 0/0.5/1/2/5；切点 9-11-15-16（λ≤2）、9-16-17-22（λ=5）；验证覆盖 49.7/84.9；测试 46.7/76.7；SSE 25.37/25.93、51.54/50.38；与 `e4_ablation_lambda.csv` 一致。
- **问题**：只覆盖 W1；表名/图注需写“W1 only”；不能外推三窗口。
- **结论**：可保留 + 注。

### T6 `table06_data_audit_checks`
- **可复算**：303→299、7272→7176、15.5→15.75、237→236、19→20 h、74.2→63.54、46.7→35.66、33.6→43.45；与 `price_clean` 复算一致。
- **结论**：可保留。

---

## 6. 概念/方法图核验（S6 / 图6）

| 检查项 | 结果 |
|---|---|
| 节点/模块是否来自 METHOD_PLAN | 方法集合 M1/B0/B1/B2/B3/B3b/B4/B5 与计划一致；无虚构方法 |
| 箭头/数据流 | 无流程图；条带表示“设计→档位”，逻辑基本成立 |
| 变量/公式/术语 | “按电价排名映射”与实际 B3/B3b 的净负荷排名不一致；B0/B5 是政策档位，不是排名 |
| 代表月 | `m_ref = median(test months)`；未注明，读者会误以为是整个窗口 |
| 文字清晰度 | 三列×8 行，字号偏小；但可读 |
| 结论 | **逻辑需修正（M2）**；不改数据，只改标题/注和代表月说明 |

---

## 7. 问题分级与证据

### Critical（必须解决，否则不能投稿）

| ID | 位置 | 问题 | 证据 | 影响 | 修改建议 | 需重算/重绘 |
|---|---|---|---|---|---|---|
| **C1** | F4/F6/F7、S12–S15、T2 账单列、T4 账单行、T3 H2/H3 | 原始负荷/净负荷缺失；用户电费图/表只能追到派生 CSV，不能追到原始 xlsx | `data/MANIFEST.csv` 无 load/netload；`原始数据集` 只有 `._`；`config.py` `LOAD_FILE`/`NETLOAD_FILE` 指向不存在文件；`相关数据` 无这两个 xlsx | 论文核心“用户电费”不可复现；审稿人可质疑数据真实性 | 恢复 `山东省用户小时负荷.xlsx`/`山东省净负荷.xlsx`，加入 `data/MANIFEST`，重跑 `run_all.py`；若无法恢复，把所有电费结论降级为“派生情景/未核验”，不得称已验证 | 是 |
| **C2** | T3 H3 行 | “J(M1,B3b)=0.714（均 >80%）”错误；分层 −0.38/−0.36/−0.53 不是单调 | `e3_overlap.csv`：0.857/0.714；`e3_heterogeneity.csv`：−0.3799/−0.3563/−0.5304 | H3 证据被错误表述；可能改变 H3 判定 | 改为“B5 85.7%>80%；B3b 71.4%<80%，未过门槛”；删除“单调”，改为“无单调梯度/方向不一致”；按预注册判“混合/不支持” | 重算表，不需重画 |
| **C3** | S1/S2 + `EXPERIMENT_RESULTS §6` | `fig01_price_overview.png` 内含“图1+图2”；14 个文件对应 15 个图号；无独立图2文件 | `figures.py:34–64` 两个 title；`EXPERIMENT_RESULTS §6` 写“图1–2”；目录 14 个 PNG | 正文图号引用会错；图2无法单独插入 | 拆成 `fig01_price_overview`（图1）+ `fig02_neg_monthly`（图2），后续文件整体后移一位；更新 `run_all.py`/`EXPERIMENT_RESULTS §6`/目录 | 重绘 + 重命名 |
| **C4** | S15 `fig14_elasticity` | 标题“只有 ε<0 才出现电费节约”与 ε=0 数据矛盾 | `e3_scenarios.csv` ε=0：M1 W1 −4.43%、W2 −7.02%、W3 +2.18% | 读者会把会计差异误读为需求响应节约；结论被夸大 | 改为“ε=0 已存在会计差异；ε<0 只改变幅度；不能把 ε=0 读作需求响应节约”；图注说明 | 重绘 |
| **C5** | `FIGURE_TABLE_CATALOG` | 只列 7 张主图；14 个 `RESULTS_FIGURES`/15 个图号未入目录，无数据/代码/caption | catalog 1–167 行；`RESULTS_FIGURES` 14 文件；`EXPERIMENT_RESULTS §6` 15 图号 | 论文图表无完整 provenance；审稿人无法核对 | 新增“Supplementary S1–S15”表：文件、图号、数据、代码、caption、核验状态；明确主图/补充图 | 文档 + 可能重命名 |

### Major（影响可读性/统计表达/一致性，需修）

| ID | 位置 | 问题 | 证据 | 影响 | 修改建议 |
|---|---|---|---|---|---|
| **M1** | S9 `fig08_lambda_ablation` | 左图 y 45–85 截断；无图例；右图 SSE 50.4–51.6 截断 | `figures.py:266–286`：无 `set_ylim(0,100)`、无 `ax.legend()`；`set_ylim(min−0.1,max+0.1)` | 放大 λ 效果；红/蓝线不可辨；SSE 差异被放大 | 左轴 0–100；加图例（测试/验证）；右轴注明“zoom，绝对差 <1.2×10⁶”或画 ΔSSE |
| **M2** | S6 `fig05_boundaries` | 标题“按电价排名”不适用于 B3/B3b（净负荷排名）与 B0/B5（政策档位）；`m_ref` 代表月未注明 | `billing.py:58–63` 用 `means`；`baselines.py:104–106` B3b `rank_by: netload`；`figures.py:162` `m_ref=median` | 概念图与实际方法不符；读者误解档位来源 | 标题改“partition 按段均值；B3/B3b 按净负荷均值；B0/B5 用政策档位”；图注写“代表测试月中位月” |
| **M3** | F1–F7 vs S1–S15 | 同一方法颜色不一致：M1 主图蓝、结果图红；B4 主图红、结果图紫；B5 主图紫、结果图橙 | `style.py:65–74` vs `figures.py:13–22` | 读者无法跨图追踪方法 | 以 `style.METHOD_COLOR` 为唯一 palette；`figures.py` 改为导入/复制同一映射；重生成 14 图 |
| **M4** | F3/F4/F6 vs S8/S13/S14；F2 vs S7 | 两套图重复同一数据（coverage-regret、bill、bill decomposition、coverage）；文件前缀相同 | 文件列表；`main_results` 共用 | 论文结构重复；易插错图 | 明确“主图 7 张 + 补充 S1–S15”；重复图只保留一套，另一套移补充/删除 |
| **M5** | T4 `效应量 d` | d=−56.15/17.02/16.32 等由日间方差极小产生；绝对值只有 −1.21/+2.18/+1.60% | `ci_table.csv` `cohens_d`；`table04` | 读者误以为“巨大效应”；审稿人会质疑 | 删除 d 或加脚注“d 不稳定，不作解释”；主报相对效应+CI |
| **M6** | T4 表头/口径 | “估计值”未说明 M1−基线；覆盖率天数（45/20/15）与账单天数（61/62/26）混在“天数”；无 2% 门槛列 | `table04` 列；`ci_table` n_days | 读者把 BH 显著误读为 H2 支持；口径混淆 | 加“对比=M1−基线”“覆盖率为负价日/账单为测试日”；加“≥2%? 是/否”列 |
| **M7** | T1 第 13 行 | “平段近四成 → 零售侧拿不到负价信号（H1 直接证据）”把 H1 与传导混为一谈 | T1 行；`price_clean` 平段 450/1130=39.8% | H1 证据被错误归因；概念不严谨 | 改为“描述性证据：平段占负价 39.8%，说明现行档位未单独识别负价；传导需另验” |
| **M8** | `FIGURE_TABLE_CATALOG` Fig3 caption | 写“B0 在 W1 覆盖率最低但 R 最高”；实际 B3 W1 5.23% < B0 34.49% | `main_results` B0/B3 W1；catalog 行 46 | Caption 事实错误；审稿人可查 | 改为“B0 W1 覆盖率 34.5%，低于 M1 但高于 B3；B0 R 最高（38.7%）” |
| **M9** | `FIGURE_TABLE_PLAN` §0 | 仍写“CI/λ/负对照未提供”；实际 `results/` 已有全部 17 表 | plan 行 19；`results` 文件列表；catalog 行 15 | 与目录矛盾；修复者会误判 | 更新为“已提供”；Table4/5 改为可复算 |
| **M10** | F4/F6/F7 | 无 CI/误差线；F4 仅聚合值 | `make_figures.py:207–279` 无 errorbar；T4 有 CI | 读者把点估计当精确值 | 加 errorbar（用 T4 CI）或 caption 明确“aggregate；paired CI 见 Table 4” |
| **M11** | F6/S14 | “转移成分”把会计残差说成可观测转移 | `billing.py` κ 定义；`fig13` 标题 | 概念过度解释 | 改“会计差额/平均乘子效应”；避免“转移支付”因果词 |
| **M12** | S1–S15 | 只有 PNG，无 PDF；主图有 PDF；字体/风格两套 | `RESULTS_FIGURES` 文件列表；`style.py` vs `config.py` | 期刊排版/字体不一致 | 统一输出 PDF+PNG；统一字体、字号、线宽 |

### Minor（格式/可读性）

| ID | 位置 | 问题 | 建议 |
|---|---|---|---|
| **N1** | S7 图7 | 覆盖率取整（77/73/85），与 T2 的 76.7/73.2/84.5 不完全一致 | 保留 1 位小数或图注“四舍五入” |
| **N2** | S10 图10 | x 轴 35–77 截断；CDF 仅数据范围 | 改 30–80 或注“数据范围” |
| **N3** | S12 图12a | y 轴 50–148，tick 60–120；数据 min ~59 | 注“纵轴起点 50”或不截断 |
| **N4** | S1–S15 | 图内标题带“图N”，与文件名/目录不一致 | 统一图号或在图内去掉编号，只留 caption |
| **N5** | S1–S15 | 无 PDF 矢量版 | 输出 PDF，字体嵌入 |
| **N6** | 全部 | 主图/结果图字体不同（Arial Unicode MS vs PingFang/SimHei） | 统一字体与字号 |
| **N7** | S1 图1 | 零线红色虚线无图例 | 加“0 元/MWh”图例 |
| **N8** | 文件名 | 主图/结果图都用 `fig01…` 前缀，易混 | 加 `main_`/`supp_` 前缀或分目录 |

---

## 8. 逐图/逐表“保留/重绘/补数据”结论

| 图表 | 保留 | 重绘 | 补数据/统计 | 说明 |
|---|---|---|---|---|
| F1 | ✅ | — | — | 加 pooled/W3 注 |
| F2 | ✅ | — | — | 加色标说明（可选） |
| F3 | ✅ | — | — | 改 catalog caption（M8） |
| F4 | ⚠️ | 建议 | **C1 负荷** | 加 CI/口径注 |
| F5 | ✅ | — | — | — |
| F6 | ⚠️ | 建议 | **C1 负荷** | 改“转移”措辞 |
| F7 | ⚠️ | 建议 | **C1 负荷** | 加 CI/口径注 |
| S1/S2 | ❌ | ✅ 拆分 | — | C3 |
| S3 | ✅ | — | — | — |
| S4 | ✅ | — | — | — |
| S5 | ✅ | — | — | — |
| S6 | ⚠️ | ✅ 标题/注 | 净负荷原始数据 | M2 |
| S7 | ✅ | — | — | 取整注 |
| S8 | ⚠️ | 可删/合并 | — | 与 F3 重复 |
| S9 | ❌ | ✅ 轴/图例 | — | M1 |
| S10 | ✅ | — | — | x 轴注 |
| S11 | ✅ | — | — | — |
| S12 | ❌ | 保留为情景 | **C1 负荷** | 不可核验 |
| S13 | ⚠️ | 保留为情景 | **C1 负荷** | 不可核验 |
| S14 | ⚠️ | 改标题 | **C1 负荷** | M11 |
| S15 | ❌ | ✅ 标题 | **C1 负荷** | C4 |
| T1 | ✅ | — | 负荷行注 | M7 |
| T2 | ✅（价格列） | — | 负荷行注 | C1 |
| T3 | ❌ | 重算 H3 | — | C2 |
| T4 | ⚠️ | 加列/注 | 负荷原始数据 | M5/M6 |
| T5 | ✅ | — | — | 注 W1 |
| T6 | ✅ | — | — | — |

---

## 9. 最终回答

### 9.1 哪些图表可以保留？
- **可直接保留**：F1、F2、F3（改 caption）、F5；S3、S4、S5、S7、S10、S11；T5、T6。
- **保留但必须加注/补 CI**：F4、F6、F7、S13、S14；T1、T2（价格列）。
- **不能按现状保留**：S1/S2（图号拆分）、S6（标题/代表月）、S9（轴/图例）、S12（原始负荷）、S15（标题）；T3（H3）。

### 9.2 哪些必须重新绘制？
- **S1/S2**：拆分图1/图2，后续 13 个文件重命名。
- **S9**：λ 图 0–100% 轴 + 图例 + SSE zoom 注。
- **S15**：弹性图标题/注。
- **S6**：标题/代表月注；若保留 B3/B3b 条带。
- **F4/F6/F7**：至少加 CI/口径注；若加 errorbar，需重绘。
- **S14**：改“转移”措辞。
- **T3**：重算表（非图）。

### 9.3 哪些需要补充数据或统计分析？
- **最高优先**：原始 `山东省用户小时负荷.xlsx`、`山东省净负荷.xlsx`；加入 `data/MANIFEST`；重跑 E3；否则所有“用户电费”图表只能标“派生/未核验”。
- **Table 4**：补“≥2% 实践门槛”列、基线定义、覆盖率/账单天数说明；删除或标注 d。
- **Table 3**：重算 H3 的 Jaccard/梯度；按预注册标准重写判定。
- **T5**：注明仅 W1；如需三窗口，补 λ 表。
- **S13**：确认 CI 是逐日配对；误差棒定义。

### 9.4 是否存在图表与论文主张不一致？
**是，至少 4 处：**
1. **S15 图15** 标题说“只有 ε<0 才节约”，但 ε=0 已有 −4.43/−7.02%（W1/W2）——**直接矛盾**。
2. **T3 H3** 说“J(M1,B3b)=0.714 且均>80%”——**71.4% < 80%**；且 −0.38/−0.36/−0.53 非单调。
3. **`FIGURE_TABLE_CATALOG` Fig3 caption** 说“B0 在 W1 覆盖率最低”——实际 B3 W1 5.23% 更低。
4. **`FIGURE_TABLE_CATALOG` 只列 7 图**，但 `EXPERIMENT_RESULTS §6` 有 15 个图号——**图表清单与正文不一致**。

### 9.5 当前图表是否达到论文初稿使用要求？
**未达到。**
- 价格侧（F1/F2/F3/F5、S3–S11）基本达到“可核验的描述性图表”；
- 用户电费侧（F4/F6/F7、S12–S15、T2/T3/T4）**未达到**：原始负荷缺失 + 统计表达/标题/数值问题；
- Critical 问题 C1–C5 未解决前，不建议把“用户电费改善/不改善”作为论文主结论提交；可以把“覆盖率提升但账单未达 2%”写成**情景性、待核验**的结果。

---

## 10. 审查证据索引

- 主图代码：`plotting_scripts/make_figures.py`；`style.py`；`figures/plotted_values.json`
- 结果图代码：`code/np_tou/figures.py`（`fig01` 行 34–64；`fig05` 行 140–194；`fig08` 行 263–293；`fig14` 行 460–483）
- 负荷读取：`code/np_tou/load_data.py` 行 37–72；`config.py` 行 14–20
- 数据清单：`data/MANIFEST.csv`（无 load/netload）
- 统计：`results/ci_table.csv`；`results/e3_overlap.csv`；`results/e3_heterogeneity.csv`；`results/e4_ablation_lambda.csv`
- 表格：`tables/table03_hypothesis_summary.csv`、`table04_statistical_results.csv`
- 目录：`FIGURE_TABLE_CATALOG.md` 行 46；`FIGURE_TABLE_PLAN.md` 行 19；`EXPERIMENT_RESULTS.md` §6 行 314–331
- 质控：`plotting_scripts/verify_outputs.py` 行 54–97 只覆盖 `fig01–fig07`；`QC_REPORT.md` 未覆盖 `RESULTS_FIGURES`
