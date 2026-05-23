# Weeks 12-16 Revised Outline

## Status
- document_type: revised_course_outline
- scope: weeks_12_to_16
- replaces: original late-semester outline for weeks 12-16
- current_week_when_revised: 12
- audience_priority: AI_first_human_readable_second
- language: zh-CN with English technical terms

## Purpose
本文件用于定义新的 `12~16` 周课程大纲。

压缩重排的原因：
- 课程已经进入第 12 周；
- 原计划中第 9~11 周及后续若干主题尚未完整覆盖；
- 需要在仅剩的 `12~16` 周内，保留核心知识主线，并减少分散主题。

## Non-Negotiable Coverage
以下内容必须在新的 `12~16` 周中明确出现：

1. `bias-variance trade-off`
2. `loss function extension + penalty`
   - losses: `RMSE`, `MAE`
   - penalties: `Ridge (L2)`, `Lasso (L1)`, `Elastic Net (L1 + L2)`
   - emphasis: 不同损失函数与不同惩罚项的组合如何体现各自特点
3. `generalized linear models (GLM)`
   - mandatory: `Logistic Regression`
   - optional_extension: `count process / Poisson Regression`
4. `dimensionality reduction`
   - required: `PCA`, `PCR`
5. `variable selection`
   - 必须显式出现，不能只隐含在 Lasso 中一笔带过

## Explicitly Deprioritized / Removed
以下内容不再作为新的 `12~16` 周主线：
- deployment
- FastAPI
- Docker
- 将原第 16 周的工程部署主题移出本轮压缩大纲

## Curriculum Design Logic
新的压缩主线按如下逻辑组织：

1. 先解释：为什么原始 OLS 不够用
   - 泛化误差
   - 偏差-方差权衡
   - 不同损失函数的差异
2. 再解释：如何在原变量空间中改造线性模型
   - Ridge
   - Lasso
   - Elastic Net
   - variable selection
3. 再解释：面对高维与共线性时，除了加惩罚，还可以做降维
   - PCA
   - PCR
4. 再解释：如果目标变量类型变了，线性模型如何广义化
   - Logistic Regression
   - optional: Poisson Regression
5. 最后一周不再引入大块新理论，而做综合案例整合与模型路线选择

## Recommended Module Title
`模块四：线性模型的扩展、泛化与广义化（第12-16周）`

---

# Week-by-Week Outline

## Week 12
### theme
`泛化误差、偏差-方差权衡与损失函数`

### theory_2h
- 训练误差、测试误差与泛化误差
- `Bias-Variance Tradeoff` 的核心思想与直观图像
- 模型复杂度与欠拟合 / 过拟合
- 从经验风险最小化理解回归建模
- 常见损失函数对比：
  - 平方损失 / `RMSE`
  - 绝对损失 / `MAE`
- `RMSE` 与 `MAE` 在以下方面的差异：
  - 对异常值的敏感性
  - 优化目标的几何特性
  - 业务解释口径

### practice_and_discussion_1h
- 使用模拟数据或多项式回归演示：
  - 欠拟合
  - 过拟合
  - 测试误差随模型复杂度的变化
- 比较 `RMSE` 与 `MAE` 在含异常值数据上的表现差异
- 讨论问题：什么时候应接受“更有偏但更稳定”的模型？

### learning_objectives
- 学生能够解释为什么“训练误差更低”不等于“模型更好”
- 学生能够说明 `bias-variance trade-off` 与模型选择的关系
- 学生能够比较 `RMSE` 和 `MAE` 的适用场景

### keywords
- `generalization`
- `bias`
- `variance`
- `underfitting`
- `overfitting`
- `RMSE`
- `MAE`

---

## Week 13
### theme
`正则化回归与变量筛选：Ridge、Lasso、Elastic Net`

### theory_2h
- 统一框架：
  - `objective = loss + penalty`
- `Ridge (L2)`：
  - 参数收缩
  - 抗共线性
  - 提升稳定性
- `Lasso (L1)`：
  - 稀疏解
  - 自动变量筛选
- `Elastic Net (L1 + L2)`：
  - 在相关特征存在时兼顾筛选与稳定
- `variable selection` 的定位：
  - 经典子集选择思想（概念性介绍）
  - `Lasso` 作为现代变量筛选工具
  - 变量被选中 ≠ 因果解释自动成立
- 不同 `loss + penalty` 组合的特点：
  - 平方损失 + `L2`：平滑、稳定、抗共线性
  - 平方损失 + `L1`：稀疏、可筛选
  - 平方损失 + `Elastic Net`：相关变量下更稳健
  - 绝对损失 + 惩罚项：更稳健，但优化与解释方式会变化

### practice_and_discussion_1h
- 绘制 `Ridge` / `Lasso` 的 regularization path
- 使用 `Pipeline + GridSearchCV` 搜索最优 `alpha`
- 代码互审重点：
  - scaling 是否发生在 CV 之外
  - 是否存在 data leakage
- 观察不同 `alpha` 下被保留变量集合的变化

### learning_objectives
- 学生能够用统一目标函数理解正则化回归
- 学生能够区分 `Ridge`、`Lasso`、`Elastic Net` 的主要用途
- 学生能够解释“变量筛选”和“模型解释”之间的区别

### keywords
- `regularization`
- `Ridge`
- `Lasso`
- `Elastic Net`
- `variable selection`
- `regularization path`
- `data leakage`

---

## Week 14
### theme
`高维问题、共线性与降维回归：PCA / PCR`

### theory_2h
- `P > N` 问题与高维建模困难
- 多重共线性如何破坏 OLS 的稳定性与解释性
- `PCA` 复习：
  - 主成分
  - 最大方差方向
  - 线性组合表示
- `PCR (Principal Component Regression)` 的流程：
  - 先做 `PCA`
  - 再在主成分空间中回归
- `PCR` 与正则化方法的对比：
  - `Ridge`: 在原变量空间中收缩
  - `Lasso`: 在原变量空间中筛选
  - `PCR`: 先投影到低维空间再回归
- 核心问题：
  - 什么时候更需要 `variable selection`？
  - 什么时候更需要 `information compression`？

### practice_and_discussion_1h
- 比较 `Lasso vs PCR`
- 在高维或强相关数据上比较以下维度：
  - prediction performance
  - stability
  - interpretability
- 场景讨论：
  - 基因数据
  - 文本回归
  - 传感器数据
  在这些任务中，筛选与降维各自的优缺点是什么？

### learning_objectives
- 学生能够解释为什么高维和共线性会导致 OLS 不稳定
- 学生能够说清 `PCA` 与 `PCR` 的基本区别和联系
- 学生能够比较 `Lasso` 和 `PCR` 在高维问题中的不同取向

### keywords
- `high-dimensional regression`
- `multicollinearity`
- `PCA`
- `PCR`
- `projection`
- `compression`

---

## Week 15
### theme
`广义线性模型（GLM）核心：逻辑回归`

### theory_2h
- 为什么分类问题也可以放入“回归框架”
- `Bernoulli` 分布、`Sigmoid` 函数与极大似然估计 (`MLE`)
- `log-odds`（对数几率）的推导与解释
- 逻辑回归系数的统计解释与业务解释
- 正则化逻辑回归：
  - `L1`
  - `L2`
  - 用于高维分类与特征筛选
- 为 GLM 扩展埋伏笔：
  - 逻辑回归不是唯一的 GLM
  - 不同响应变量类型会对应不同分布与 link function

### practice_and_discussion_1h
- 二分类案例实战：
  - 可选示例：信用评分、违约预测、用户流失
- 比较以下分类指标的关注点：
  - accuracy
  - recall
  - ROC-AUC
  - log loss
- 讨论问题：为什么逻辑回归在工业界长期不过时？

### learning_objectives
- 学生能够解释逻辑回归为什么不是“普通线性回归直接套 sigmoid”
- 学生能够解释 `log-odds` 和概率输出之间的关系
- 学生能够区分分类任务中不同评价指标的含义

### keywords
- `GLM`
- `Logistic Regression`
- `Sigmoid`
- `MLE`
- `log-odds`
- `classification metrics`

---

## Week 16
### theme
`综合案例整合：模型路线选择、GLM扩展与期末导向`

### theory_and_discussion_2h
- 回顾完整建模路线：
  - 什么时候先看 `bias-variance`
  - 什么时候换 `loss`
  - 什么时候加 `penalty`
  - 什么时候做 `variable selection`
  - 什么时候做 `PCA / PCR`
  - 什么时候切换到 `Logistic Regression`
- `GLM` 扩展简介（选讲，不作为主线重心）：
  - `Poisson Regression` 处理计数数据
  - `overdispersion` 的概念
  - `Negative Binomial Regression` 的概念性引入
- 面向综合项目的模型决策框架：
  - prediction-first vs interpretation-first
  - sparsity vs stability
  - original variables vs principal components
  - continuous target vs binary target

### practice_and_discussion_1h
- 综合案例讨论 / mini project proposal
- 要求学生对给定问题说明：
  - 使用什么损失函数
  - 是否需要正则化
  - 是否需要变量筛选
  - 是否需要 `PCA / PCR`
  - 是否需要转向逻辑回归
- 小组互评重点：
  - 是否存在 data leakage
  - 模型选择是否匹配数据结构
  - 指标选择是否匹配任务目标

### learning_objectives
- 学生能够把 12~15 周内容串成完整的模型选择框架
- 学生能够针对数据结构和任务类型给出合理建模路线
- 学生知道计数过程属于 GLM 扩展方向，但本轮不作为核心主线

### keywords
- `model selection`
- `workflow integration`
- `Poisson Regression`
- `overdispersion`
- `Negative Binomial`
- `capstone orientation`

---

# Compact Summary Table

| week | core_theme | must_have_topics | practical_focus |
|---|---|---|---|
| 12 | bias-variance + loss | generalization, RMSE, MAE | underfit/overfit demo, loss comparison |
| 13 | regularization + variable selection | Ridge, Lasso, Elastic Net, selection | regularization path, GridSearch, leakage check |
| 14 | dimensionality reduction | PCA, PCR, collinearity, high-dimensional regression | Lasso vs PCR comparison |
| 15 | GLM core | Logistic Regression, MLE, log-odds | binary classification case |
| 16 | integration + optional GLM extension | model-routing, optional Poisson, capstone framing | mini project / integrated decision-making |

# Final Notes
- 本版大纲的目标不是“保留所有原内容”，而是“保留最关键的统计学习主线”。
- 变量筛选已被显式纳入 `Week 13`，并在 `Week 14` 中通过 `Lasso vs PCR` 再次强化。
- `Poisson / count process` 被保留为 `Week 16` 的选讲扩展，而不是主线周。
- 原第 16 周的 deployment / FastAPI / Docker 已移出本压缩大纲。
