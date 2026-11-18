# WORKBUDDY_FIX_PROMPTS
## NP-TOU 项目 · 可直接交给 WorkBuddy 的修复指令

> **配套**：[`FIGURE_TABLE_AUDIT.md`](FIGURE_TABLE_AUDIT.md)、[`FIGURE_TABLE_FIX_LIST.md`](FIGURE_TABLE_FIX_LIST.md)
> **使用方式**：按 P0 → P1 → P2 顺序，把每个 Prompt 整段复制给 WorkBuddy；一次只执行一个 Prompt。
> **总原则**：不得修改原始数据来迎合图表；不得编造缺失值；任何无法找到的原始文件，必须停下来报告，不得合成。

---

## 通用规则（每个 Prompt 都适用）

```text
项目根目录：C:\Users\lenovo\Desktop\科研大脑
主图：figures/（7 张，PDF+PNG）
补充图：RESULTS_FIGURES/（14 个文件 / 15 个图号）
表：tables/（CSV+MD+XLSX）
绘图代码：plotting_scripts/（主图）、code/np_tou/figures.py（补充图）
结果：results/（派生 CSV）
原始数据：C:\Users\lenovo\Desktop\相关数据（价格 xlsx）；C:\Users\lenovo\Desktop\原始数据集（负荷只有 ._ 元数据）

硬性要求：
1. 先备份要改的文件（复制为 *.bak_YYYYMMDD）。
2. 不得手改 results/*.csv 的数值；只能通过 run_all.py 重算，或只改图表/表格的呈现。
3. 不得用插值、合成、随机数补原始负荷。
4. 不得为了让图“好看”而截断/拉伸坐标轴（除非 Prompt 明确要求 zoom 并加注）。
5. 每步结束后运行对应 QC；失败则停止并报告。
```

---

## WB-01（P0）｜恢复原始负荷/净负荷，重建 E3 可追溯性

```text
角色：数据工程修复员。
任务：找到并恢复 NP-TOU 的原始负荷/净负荷工作簿，使 E3（用户电费）可从原始数据重跑。

背景：
- code/np_tou/config.py 的 LOAD_FILE = 原始数据集/山东省用户小时负荷.xlsx
- NETLOAD_FILE = 原始数据集/山东省净负荷.xlsx
- 现在 C:\Users\lenovo\Desktop\原始数据集 里这两个文件只有 ._ 元数据（约 163 字节），没有实际 xlsx。
- data/MANIFEST.csv 没有 load/netload 行。
- 因此 figures/fig04、fig06、fig07 与 RESULTS_FIGURES/fig11–fig14、tables/table02 的账单列、table04 的账单行无法回溯原始数据。

步骤：
1. 在 C:\Users\lenovo\Desktop、C:\Users\lenovo\OneDrive、C:\Users\lenovo\Downloads、以及项目相关目录中搜索：
   - 山东省用户小时负荷.xlsx
   - 山东省净负荷.xlsx
   也搜索同名但不同后缀/副本（*.xls、*负荷*.xlsx、*净负荷*.xlsx）。
2. 找到后，用 pandas 验证：
   - 用户负荷工作簿含 sheet "2018逐小时"，行数 8760，列含 年/月/日/时/负荷(MW)；
   - 净负荷工作簿含 sheet "2018逐小时" 与 "2025典型日"；
   - 2018 负荷与净负荷的负荷列最大绝对差 <1e-6。
3. 把文件放到 C:\Users\lenovo\Desktop\原始数据集\（保留原文件名）。
4. 在 data/MANIFEST.csv 增加两行：file,source,rows,cols,sha256_16。
5. 设置环境变量：
   set NPTOU_DATA_DIR=C:\Users\lenovo\Desktop\原始数据集
6. 重跑：
   cd C:\Users\lenovo\Desktop\科研大脑\code
   python run_all.py
7. 重跑绘图/表格/QC：
   cd C:\Users\lenovo\Desktop\科研大脑
   python plotting_scripts\make_figures.py
   python plotting_scripts\make_tables.py
   python plotting_scripts\verify_outputs.py
8. 比较新旧 results/main_results.csv、e3_scenarios.csv、e3_bill_ci_vs_B0.csv；如数值变化，更新所有下游图表/表。

停止条件：
- 如果 10 分钟内找不到两个 xlsx：停止，写 DATA_GAP_REPORT.md，列出已搜索路径、缺少的文件、受影响的图表；不要把任何图标记为“已验证”。
- 如果找到但行数/列名不符：停止并报告，不要强行改列名。

验收：
[ ] data/MANIFEST.csv 含 load/netload。
[ ] python -c "from np_tou.load_data import read_2018_load, read_2025_typical; print(len(read_2018_load()), len(read_2025_typical()))" 输出 8760 和 48。
[ ] run_all.py 无错误。
[ ] fig11_load_profile 可从原始 xlsx 重画。
[ ] fig04/06/07、fig12/13/14 与重跑结果一致。
[ ] 若未找到：DATA_GAP_REPORT.md 明确标记“E3 不可核验”。
```

---

## WB-02（P0）｜修正 Table 3 的 H3 Jaccard 与“单调”错误

```text
角色：统计表格校对员。
任务：修正 tables/table03_hypothesis_summary.csv/.md 中 H3 行的硬性错误。

证据：
- results/e3_overlap.csv：J(M1,B5)=0.857143（85.7%）；J(M1,B3b)=0.714286（71.4%）。
- 现表写“J(M1,B3b)=0.714（均 >80%）” → 71.4% 不满足 >80%，错误。
- results/e3_heterogeneity.csv（W1，M1−B4）：
  0h: -0.3799；1–5h: -0.3563；≥6h: -0.5304 → 不是单调扩大。
- 现表写“分层 M1−B4 = -0.38 / -0.36 / -0.53 pp”可以保留数值，但不能写“单调扩大/方向正确”。

修改：
1. 打开 tables/table03_hypothesis_summary.csv（UTF-8）。
2. 将 H3 行的“实际结果”改为：
   “J(M1,B5)=0.857（85.7%，>80%）；J(M1,B3b)=0.714（71.4%，<80%，未过门槛）；分层 M1−B4=-0.38/-0.36/-0.53 pp，无单调梯度（先变浅再变深）。”
3. 将 H3 的“判定”改为：
   “混合/不支持：预注册的‘与深谷/净负荷重合度 <80%’未同时满足（B5 85.7%>80%）；负对照 P=0.075 边缘。”
4. 将 H3 的“证据”列更新为：
   “Fig 5、Fig 6、results/e3_overlap.csv、results/e3_heterogeneity.csv、results/e4_negative_control.csv”。
5. 同步 tables/table03_hypothesis_summary.md、tables/all_tables.xlsx（如果手工维护）、EXPERIMENT_RESULTS.md §7。
6. 不要改 H1/H2 的数值。

验收：
[ ] 全文 grep “均 >80%” 无结果。
[ ] 全文 grep “单调扩大” 无结果。
[ ] H3 的 J 值与 e3_overlap.csv 一致。
[ ] H3 判定与预注册标准一致（B3b 未过 80% 门槛）。
[ ] 重新运行 `python plotting_scripts\make_tables.py` 不报错。
```

---

## WB-03（P0）｜拆分图1/图2，统一 15 个图号与文件

```text
角色：科研绘图重构员。
任务：把 RESULTS_FIGURES/fig01_price_overview.png 拆成两个图，并把后续文件整体后移一位，使 15 个图号对应 15 个文件。

现状：
- fig01_price_overview.png 内含“图1”（价格走势）和“图2”（月度负价占比）。
- 现有 14 个文件对应图1–图15；没有独立 fig02_neg_monthly。
- code/np_tou/figures.py::fig_price_overview 目前用 2×1 子图，两个 title 分别“图1”“图2”。

目标文件映射（文件名 → 图号）：
fig01_price_overview.png → 图1（只保留上半价格走势）
fig02_neg_monthly.png → 图2（新增；只保留月度负价占比）
fig03_neg_heatmap.png → 图3（原 fig02_neg_heatmap）
fig04_neg_structure.png → 图4a/4b（原 fig03_neg_structure）
fig05_b0_coverage.png → 图5a/5b（原 fig04_b0_coverage）
fig06_boundaries.png → 图6（原 fig05_boundaries）
fig07_coverage_by_method.png → 图7（原 fig06_coverage_by_method）
fig08_tradeoff.png → 图8（原 fig07_tradeoff）
fig09_lambda_ablation.png → 图9a/9b（原 fig08_lambda_ablation）
fig10_negative_control.png → 图10（原 fig09_negative_control）
fig11_sensitivity.png → 图11（原 fig10_sensitivity）
fig12_load_profile.png → 图12a/12b（原 fig11_load_profile）
fig13_bill_delta.png → 图13（原 fig12_bill_delta）
fig14_bill_decomp.png → 图14（原 fig13_bill_decomp）
fig15_elasticity.png → 图15（原 fig14_elasticity）

步骤：
1. 修改 code/np_tou/figures.py：
   - 新增 `fig_neg_monthly(monthly)`，只画月度负价占比，title “图2 …”。
   - 修改 `fig_price_overview(panel, monthly)`：只保留上半价格走势，title “图1 …”。
   - 修改 `_save` 的目标文件名，按上表重命名。
   - 所有内部 `fig.suptitle/ax.set_title` 的“图N”与上表一致。
2. 修改 code/run_all.py 的调用：`F.fig_price_overview(panel, monthly)` 后增加 `F.fig_neg_monthly(monthly)`；其余调用名按新函数名调整。
3. 删除/重命名旧文件（先备份到 `RESULTS_FIGURES/_bak_YYYYMMDD/`）。
4. 更新 EXPERIMENT_RESULTS.md §6 的表格：15 行，文件/图号一一对应，不再写“图1–2”。
5. 更新 FIGURE_TABLE_CATALOG.md：增加 Supplementary S1–S15 表（见 WB-09）。
6. 重跑：
   cd C:\Users\lenovo\Desktop\科研大脑\code
   python run_all.py
7. 检查 RESULTS_FIGURES 有 15 个 PNG（若同时输出 PDF 则 15 个 PDF）。

验收：
[ ] Get-ChildItem RESULTS_FIGURES\*.png 计数 = 15。
[ ] 每个 PNG 内标题的图号与文件名一致。
[ ] 全文无“图1–2”。
[ ] EXPERIMENT_RESULTS §6 与文件一一对应。
[ ] run_all.py 无错误。
```

---

## WB-04（P0）｜修正 S15 弹性图标题

```text
角色：科研绘图 + 结论校对员。
任务：修正 RESULTS_FIGURES/fig14_elasticity.png（拆分后 fig15_elasticity）的标题，使其与 ε=0 数据一致。

证据：
- results/e3_scenarios.csv，τ=1、revenue_neutral=True：
  ε=0：M1 W1 -4.43%、W2 -7.02%、W3 +2.18%。
- 现标题：“图15 只有负荷真正转移（ε<0）时才出现电费节约；ε=0 时差异来自会计口径与负荷形状”。
  问题：ε=0 已经出现负值，读者会把“会计差异”读成“需求响应节约”；标题自相矛盾。

修改：
1. 打开 code/np_tou/figures.py::fig_elasticity。
2. 将 suptitle 改为：
   “图15  ε=0 仍存在会计差异；ε<0 只改变差异幅度；不能把 ε=0 的负值读作需求响应节约”
3. 如需更短：
   “图15  会计差异 vs 需求响应：ε=0 的负值不是节约”
4. 图注补充：
   “收支中性、τ=1；ε=0 的差异来自设计/测试窗口负荷形状与平均乘子；ε<0 才是行为情景。”
5. 同步 EXPERIMENT_RESULTS §4.6 与 FIGURE_TABLE_CATALOG 的 caption。
6. 重生成 S15。

验收：
[ ] 标题不再出现“只有……才”。
[ ] 图注明确 ε=0 的负值不是需求响应节约。
[ ] 与 EXPERIMENT_RESULTS §1.4/§4.6 一致。
```

---

## WB-05（P1）｜修正 S9 λ 图：0–100 轴 + 图例 + SSE 注

```text
角色：科研绘图员。
任务：修正 RESULTS_FIGURES/fig08_lambda_ablation.png（拆分后 fig09_lambda_ablation）的截断轴与缺失图例。

现状：
- 左图 y 轴约 45–85，覆盖率 46.7–84.9；0 未显示。
- 左图有测试/验证两条线，但代码只设 label，没有 ax.legend()。
- 右图 SSE 50.4–51.6，属于 zoom，但无说明。

修改：
1. 左图：ax.set_ylim(0, 100)；加 ax.legend(frameon=False, loc="lower right")。
2. 右图：
   方案 A：ax.set_ylim(0, 55)；
   方案 B：保留 zoom，但在图注写“纵轴放大；绝对差 <1.2×10⁶”。
   建议 B（否则差异不可见），但必须在图上/图注标注。
3. 保留“验证集选中 λ=5”的虚线/注记。
4. 重生成 S9。

验收：
[ ] 左图 0 和 100 刻度可见。
[ ] 图例能区分测试/验证。
[ ] 右图有“zoom”说明或 0 起点。
[ ] 与 e4_ablation_lambda.csv 数值一致。
```

---

## WB-06（P1）｜修正 S6 边界图的标题、代表月、净负荷映射

```text
角色：方法图校对员 + 绘图员。
任务：修正 RESULTS_FIGURES/fig05_boundaries.png（拆分后 fig06_boundaries）与实际方法不一致的标题。

问题：
- 标题“按电价排名映射到政策档位”不适用于：
  * B3/B3b：baselines.py 的 b3_netload/b3_netload_typical 用净负荷段均值，rank_by=netload；
  * B0/B5：tier 设计，直接用政策档位，不排名。
- fig_boundaries 用 m_ref = median(test months) 只画一个代表月，但图注未说明。

修改：
1. 标题改为：
   “图6  各方法在 24h 上的档位归属（只改边界、不改浮动比例；partition 按段均值，B3/B3b 按净负荷均值，B0/B5 用政策档位）”
2. 图注加：
   “条带为代表测试月中位月（m_ref），不是整个窗口逐月政策表；B0/B5 的档位随月份可能不同。”
3. 如觉得 B3/B3b 的净负荷映射不适合放在同一图，可把 B3/B3b 拆到单独图；但不要改数据。
4. 重生成 S6。

验收：
[ ] 标题不再泛化“按电价排名”。
[ ] 图注说明代表月与 B3/B3b 净负荷排名。
[ ] 与 billing.py::coef_vector、baselines.py 的 rank_by 一致。
```

---

## WB-07（P1）｜统一主图/补充图的方法颜色

```text
角色：视觉规范员。
任务：让 figures/ 与 RESULTS_FIGURES/ 使用同一套方法颜色。

唯一 palette（plotting_scripts/style.py::METHOD_COLOR）：
M1_NP_DP #1F4E79
B0_policy #2B2B2B
B4_DP_lambda0 #C0392B
B5_deep_valley #8E44AD
B1_quantile #E69F00
B2_kmeans #56B4E9
B3_netload_2025 #2E8B57
B3_netload #8C8C8C

步骤：
1. 修改 code/np_tou/figures.py 的 METHOD_COLORS 为上表。
2. 检查 fig_tradeoff/fig_bill_decomp/fig_elasticity/fig_bill_delta 等使用 METHOD_COLORS 的地方。
3. 重生成 S1–S15。
4. 抽查：M1 在 F1、S7、S9、S13、S15 中均为深蓝；B4 均为砖红；B5 均为紫。

验收：
[ ] 任一方法在所有图中颜色一致。
[ ] 图例颜色与数据点颜色一致。
[ ] 不改变任何数值。
```

---

## WB-08（P1）｜修正 Table 4：效应量、2% 门槛、基线口径

```text
角色：统计表格校对员。
任务：让 tables/table04_statistical_results.csv/.md 不再误导读者。

问题：
- 效应量 d 出现 B5 W3 -56.15、B0 W3 17.02、B5 W2 16.32；绝对值只有 -1.21%/+2.18%/+1.60%；d 由日间方差极小产生，不能解释为“巨大效应”。
- “估计值”未说明是 M1 − 基线；B0/B4/B5/B3b 易与 T2 的“vs B0”混淆。
- 覆盖率天数 45/20/15（负价日）与账单天数 61/62/26（测试日）混在“天数”。
- 没有“是否达到 2%”列；W1 B4 -0.46% 虽 BH 显著，但远低于 2%。

修改：
1. 表头：“估计值” → “估计值（M1 − 基线）”。
2. 加列“是否达到 ≥2% 改善?”：
   - B4 W1 -0.46 → 否；W2 +0.15 → 否；W3 +0.00 → 否。
   - 其余基线也按“改善 ≥2%”判定；负值才可能是改善。
3. 把“天数”拆成“覆盖天数（负价日）”和“账单天数（测试日）”，或加表注。
4. 删除“效应量 d”列，或保留但加脚注：
   “d 由日间方差计算；B5 W3 d=-56.15 等为方差极小的数学产物，不作效应大小解释。”
5. 重生成 table04_statistical_results.csv/.md、all_tables.xlsx。
6. 同步 FIGURE_TABLE_CATALOG / EXPERIMENT_RESULTS 的 Table 4 说明。

验收：
[ ] 读者不会把 BH 显著误读为 H2 支持。
[ ] 表头明确 M1 − 基线。
[ ] 覆盖率/账单天数分开。
[ ] d 不再被当作“巨大效应”。
[ ] 数值与 ci_table.csv 一致（显示精度内）。
```

---

## WB-09（P1）｜补全目录、修正 Fig3 caption、更新计划

```text
角色：文档/图表目录维护员。
任务：让 FIGURE_TABLE_CATALOG.md、FIGURE_TABLE_PLAN.md、EXPERIMENT_RESULTS §6 与实际文件一致。

步骤：
1. 在 FIGURE_TABLE_CATALOG.md 增加“Supplementary S1–S15”表：
   列：ID、文件、图号、类型、RQ/H、数据、代码、caption、核验状态。
   S1/S2 按 WB-03 拆分后的文件写；S3–S15 按新文件名写。
2. 把“7 图 6 表”改为“7 主图 + 15 补充图 + 6 表”。
3. 修正 Fig 3 caption：
   原文“B0 在 W1 覆盖率最低但 R 最高” → 
   “B0 在 W1 覆盖率为 34.5%，低于 M1（76.7%），但高于 B3（5.2%）；B0 的 R 最高（38.7%）。”
4. 更新 FIGURE_TABLE_PLAN §0：
   把“CI/λ/负对照未提供”改为“results/ 已提供全部 17 表”；Table4/5 改为“由 ci_table/e4_ablation_lambda 生成”。
5. 更新 EXPERIMENT_RESULTS §6 为 15 行（与 WB-03 的文件名一致）。
6. 检查全目录无“图1–2”“7 图”残留。

验收：
[ ] 每个图文件都能在 catalog 找到数据/代码/caption。
[ ] 文件数/图号数一致（15）。
[ ] 目录/计划/实验报告三处一致。
[ ] Fig 3 caption 与 main_results 一致。
```

---

## WB-10（P1）｜F4/F6/F7 加 CI/口径注；S14 改“转移”措辞

```text
角色：科研绘图 + 写作校对员。
任务：避免读者把聚合点估计当作精确值，避免把会计差额说成可观测转移。

A. F4/F6/F7：
1. 在 figures/fig04、fig06、fig07 的图注（或图内注）加：
   “图中为聚合值；逐日配对 95% CI 见 Table 4；CI 只含日间变异，不含设计选择不确定性。”
2. 如时间允许，F4 加 errorbar（用 Table 4 的 CI）；否则至少加注。
3. 重生成 F4/F6/F7。

B. S14（fig13_bill_decomp）：
1. 标题“红蓝两柱之差 = 平均乘子改变带来的转移，蓝柱才是结构效应”改为：
   “红蓝两柱之差 = 平均乘子/收支中性带来的会计差额；不是可观测的转移支付。”
2. 图注加：“差额是会计分解，不是因果效应。”
3. 重生成 S14。

验收：
[ ] 图注明确 aggregate vs paired CI。
[ ] F4 的 H2 结论与 Table 4 一致。
[ ] S14 不再用“转移支付”作为因果词。
```

---

## WB-11（P2）｜可读性小修

```text
角色：排版/绘图员。
任务：按需修以下 Minor 项，不改变任何数值。

1. S7（fig06_coverage_by_method）：标签保留 1 位小数（76.7 而非 77），或图注写“四舍五入到整数”。
2. S10（fig09_negative_control）：x 轴改 30–80，或图注写“数据范围 35–77”。
3. S12（fig11_load_profile）：图注写“纵轴起点 50”；不要让人以为从 0 开始。
4. S1（fig01_price_overview）：零线加图例“0 元/MWh”。
5. S1–S15：输出 PDF（字体嵌入）；统一字体/字号；图内标题去掉“图N”或与 caption 一致。
6. 主图/补充图文件名加 `main_`/`supp_` 前缀，避免 `fig01` 冲突（可选，但推荐）。

验收：
[ ] 不改变数值。
[ ] 图注/轴标签能独立读懂。
[ ] 主图与补充图字体/线宽一致。
```

---

## 建议执行顺序

```text
1. WB-01（原始负荷）——决定 E3 能不能救
2. WB-02（Table 3 H3）——修正结论
3. WB-03（图1/2 拆分 + 15 图号）
4. WB-04（S15 标题）
5. WB-05（S9 轴/图例）
6. WB-06（S6 标题/代表月）
7. WB-07（颜色统一）
8. WB-08（Table 4）
9. WB-09（目录/计划/Fig3 caption）
10. WB-10（F4/F6/F7 CI 注 + S14 措辞）
11. WB-11（Minor）
```

> **停止条件**：WB-01 找不到原始负荷时，停止后续“用户电费”图的“已验证”表述；所有 E3 图改为“情景/派生”，并在论文摘要/局限中写明“未能从原始负荷复算”。
