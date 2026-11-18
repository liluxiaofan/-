# FIGURE_TABLE_PLAN
## NP-TOU 项目 · 论文图表计划（Visualization Agent）

> **日期**：2026-11-18
> **输入**：`METHOD_PLAN.md`、`EXPERIMENT_PLAN.md`、`w1-5成果/DATA_AUDIT.md`、`w1-5成果/EXPERIMENT_RESULTS.md`、`w1-5成果/main_results.csv`
> **真实结果**：`main_results.csv`（24 行 = 3 窗口 × 8 方法；17 列）
> **原则**：图表只从真实 CSV/审计表生成；不编造数值；不截断坐标轴；不把“覆盖率”写成“用户电费改善”。
> **质控**：[`QC_REPORT.md`](QC_REPORT.md)；[`FIGURE_TABLE_CATALOG.md`](FIGURE_TABLE_CATALOG.md)

---

## 0. 先说明数据可用性

| 项目 | 状态 |
|---|---|
| 真实结果表 `main_results.csv` | **可用**（已复制到 `data/main_results.csv`） |
| 数据审计 `DATA_AUDIT.md` | **可用**（已复制到 `data/`） |
| 实验摘要 `EXPERIMENT_RESULTS.md` | **可用**（已复制到 `data/`） |
| 逐日 CI 表 / λ 表 / 负对照表 / 稳健性表 | **未随结果文件夹提供**（`EXPERIMENT_RESULTS.md` 引用了 `results/*.csv`，但文件夹只有 `main_results.csv`） |
| 原始小时价格/负荷 xlsx | **桌面“原始数据集”只有 `._` AppleDouble 元数据（约 176 字节），没有实际 xlsx**；因此不能从原始数据重画时间序列 |
| 现有 `fig05_boundaries.png` | 有，但缺少可复现脚本；本计划不直接复用，改为从 `cuts` 重新生成稳定性图 |

**因此**：
- 7 张图全部来自 `main_results.csv` 或由 `cuts` 计算；
- 2 张统计/消融表来自 `EXPERIMENT_RESULTS.md`，在表中明确标注“reported, not recomputed”；
- 不生成“价格时间序列/负价热力图/事件时长直方图”，因为原始 xlsx 不在手，避免用摘要数字伪造图形。

---

## 1. Figure Plan

| ID | 文件名 | 回答的问题 | 数据 | 图形 | 关键信息 | 状态 |
|---|---|---|---|---|---|---|
| **Fig 1** | `fig01_coverage_b0_vs_m1.png` | 现行政策看见负价了吗？NP 设计是否把边界推向负价小时？ | `main_results.csv`: `coverage` for B0/M1 | 分组柱状图 | B0 34.5/0.0/47.9%；M1 76.7/73.2/84.5% | 已生成 |
| **Fig 2** | `fig02_coverage_heatmap.png` | 不同方法在各窗口的负价覆盖率如何？ | `main_results.csv`: `coverage` | 热力图（方法×窗口） | M1 最高，B3 2018 最低；B0 W2=0 | 已生成 |
| **Fig 3** | `fig03_coverage_regret.png` | 覆盖率是否以价格拟合为代价？ | `coverage`, `regret` | 散点图（方法颜色、窗口形状） | 覆盖率↑ 通常 regret↑；B0 高 regret 低覆盖 | 已生成 |
| **Fig 4** | `fig04_bill_delta.png` | 样本外用户电费是否达到 ≥2% 改善？M1 相对 B4 的增量多大？ | `bill_delta_pct` | 分组柱 + 增量柱 | M1−B4 = −0.44/+0.14/+0.00 pp；均 <2% | 已生成 |
| **Fig 5** | `fig05_boundary_stability.png` | 覆盖率提升是否以边界频繁变动为代价？ | `cuts` 计算 `S` | 柱状图 | M1 S=0.50 最低；B3=1.00 | 已生成 |
| **Fig 6** | `fig06_bill_decomposition.png` | 账单变化有多少是“平均乘子/转移支付”，多少是收入中性后的设计效应？ | `bill_delta_raw_pct` vs `bill_delta_pct` | 哑铃图 | M1 W1 raw −16.8% vs neutral −4.4%；B4 W1 raw +14.8% vs neutral −4.0% | 已生成 |
| **Fig 7** | `fig07_coverage_vs_bill.png` | 高覆盖率是否等于低账单？ | `coverage`, `bill_delta_pct` | 散点图 | 覆盖率 80%+ 仍可能账单 +3%；无单调关系 | 已生成 |

### 不生成的图（及原因）

| 建议图 | 为什么没有生成 |
|---|---|
| 2026 年价格时间序列 / 负价小时热力图 | 原始 xlsx 不在桌面文件夹（只有 `._` 元数据） |
| 负价事件时长直方图 | 同上；`DATA_AUDIT` 只有汇总值（4.79/4/20 h） |
| λ 敏感性曲线 | `e2_lambda_selection.csv` 未提供；只有摘要表 |
| 负对照分布 / 置换检验图 | `e4_negative_control.csv` 未提供 |
| CI forest plot | `ci_table.csv` 未提供；表 4 只转录摘要 |
| 边界 24h 图 | 现有 `fig05_boundaries.png` 无可复现脚本；`lowest_hours` 跨月，单日 24h 图会误导 |

> 如果团队后续提供 `results/` 下的 `ci_table.csv`、`e2_lambda_selection.csv`、`e4_negative_control.csv`、`e4_robustness.csv`，可以补 3–4 张图；当前不补。

---

## 2. Table Plan

| ID | 文件名 | 内容 | 数据来源 | 用途 |
|---|---|---|---|---|
| **Table 1** | `table01_dataset_description` | 数据样本、价格类型、负价、B0、代理负荷、窗口、口径 caveat | `DATA_AUDIT.md` §2–§9；`EXPERIMENT_RESULTS.md` §1.1 | 数据与方法节 |
| **Table 2** | `table02_baseline_performance` | 24 行：窗口×方法；覆盖率、regret、unit bill、Δbill vs B0、Jaccard、cuts | `main_results.csv`（逐行） | 主结果/基线对比 |
| **Table 3** | `table03_hypothesis_summary` | H1/H2/H3 的判定与关键证据 | `EXPERIMENT_RESULTS.md` §2/§3.2/§5/§7 | 结果讨论 |
| **Table 4** | `table04_statistical_results` | M1 vs B0/B4/B5/B3b 的 paired 估计与 95% CI | `EXPERIMENT_RESULTS.md` §3.2/§4.2（reported） | 统计结果 |
| **Table 5** | `table05_lambda_ablation` | λ 网格、切点、验证/测试覆盖率、SSE | `EXPERIMENT_RESULTS.md` §5.2（reported） | 消融 |
| **Table 6** | `table06_data_audit_checks` | 文档旧值 vs 复算值（303→299 等） | `DATA_AUDIT.md` §8 | 数据质量/附录 |

> Table 4/5 的原始 `ci_table.csv`/`e2_lambda_selection.csv` 未随结果文件夹提供；表中每个数字在 `source`/`note` 标注“reported, not recomputed”。**不能把它们说成“从 CSV 重新计算”。**

---

## 3. 绘图规范

1. **坐标轴**：覆盖率 0–100%；账单变化不截断（−10.5% 到 +6.2%），零线可见；稳定性 0–1。
2. **颜色**：M1 蓝、B4 红、B0 深灰、B5 紫红、B3b 绿；全图一致。
3. **窗口**：W1 圆、W2 方、W3 三角；图例说明。
4. **标注**：只标关键点（M1/B0/B4/B5），避免遮挡；精确值放表 2/4。
5. **不做的**：不截断 y 轴制造差异；不把“覆盖率”当“电费”；不把“raw multiplier”当“设计效应”；不删除不利窗口。
6. **可追溯**：每张图脚本只读 `data/main_results.csv`；不手写任何实验数值（标签/顺序除外）。

---

## 4. 论文中的推荐用法

| 论文位置 | 用哪张图/表 | 一句话结论 |
|---|---|---|
| Results §1：现行政策是否看见负价 | Fig 1 + Table 2（B0 行） | B0 覆盖率 34.5/0/47.9%，W2 完全看不见 |
| Results §2：方法对比 | Fig 2 + Table 2 | M1 覆盖率最高，但价格拟合 regret 不是最低 |
| Results §3：覆盖率代价 | Fig 3 + Fig 5 | 覆盖率↑ 伴随 regret↑、边界稳定性↓ |
| Results §4：用户电费 | Fig 4 + Table 4 | M1−B4 三窗口均 <2%，H2 不支持 |
| Results §5：账单分解 | Fig 6 | 原始乘子与收入中性差异大，不能读成用户节约 |
| Discussion：覆盖率≠福利 | Fig 7 | 高覆盖不等于低账单 |
| Appendix：数据质量 | Table 1 + Table 6 | 299 天/7176 h、实时价、严格区间口径 |

---

## 5. 质量检查清单（生成后逐项打勾）

- [ ] Fig 1–7 的数值与 `main_results.csv` 一致（脚本读取，非手写）。
- [ ] Table 2 的 24 行与 CSV 逐行一致。
- [ ] Fig 4 的 M1−B4 与 Table 4 的差异已标注（aggregate vs paired）。
- [ ] 坐标轴未截断；零线可见；单位完整。
- [ ] 没有把“覆盖率提升”写成“用户电费改善”。
- [ ] 没有把 Table 4/5 的 reported 值说成“从 CSV 复算”。
- [ ] 每张图有数据来源、脚本、生成日期（见 `FIGURE_TABLE_CATALOG.md`）。
