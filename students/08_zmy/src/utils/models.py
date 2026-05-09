import numpy as np
from scipy import stats

class AnalyticalOLS:
    """解析解 OLS，支持截距选项"""
    def __init__(self, fit_intercept=True):
        self.fit_intercept = fit_intercept# 是否自动添加截距项，默认 True
        self.coef_ = None # 拟合后，存储模型系数
        self._is_fitted = False

    def _add_intercept(self, X): # 若需要截距，在特征矩阵最左侧添加一列 1。
        if self.fit_intercept:
            return np.column_stack([np.ones(X.shape[0]), X])
        return X

    def fit(self, X, y):
        X_design = self._add_intercept(X)
        self.coef_ = np.linalg.lstsq(X_design, y, rcond=None)[0]
        self._is_fitted = True
        return self

    def predict(self, X):
        if not self._is_fitted:
            raise RuntimeError("Model not fitted.")
        X_design = self._add_intercept(X) # 对输入的x
        return X_design @ self.coef_

    def score(self, X, y): # 计算r2决定系数
        y_pred = self.predict(X)
        sse = np.sum((y - y_pred)**2)
        sst = np.sum((y - np.mean(y))**2)
        return 1 - sse/sst if sst != 0 else 0.0


class GradientDescentOLS:
    """梯度下降 OLS，支持 full_batch 和 mini_batch，记录 loss 历史"""
    def __init__(self, learning_rate=0.01, tol=1e-5, max_iter=1000,
                 gd_type="full_batch", batch_fraction=0.1, fit_intercept=True):
        self.learning_rate = learning_rate# 学习率，控制每次更新的步长
        self.tol = tol # 收敛阈值，当连续两次迭代的 loss 变化小于 tol 时停止训练
        self.max_iter = max_iter # 最大迭代次数，防止无限循环
        self.gd_type = gd_type # 梯度下降类型，支持 "full_batch" 和 "mini_batch"
        self.batch_fraction = batch_fraction # mini_batch 时每次使用的样本比例，范围 (0, 1]
        self.fit_intercept = fit_intercept # 是同解析解，否自动添加截距项，默认 True
        self.coef_ = None
        self.loss_history_ = [] # 每轮全量 MSE 记录
        self._is_fitted = False

    def _add_intercept(self, X):
        if self.fit_intercept:
            return np.column_stack([np.ones(X.shape[0]), X])
        return X

    def fit(self, X, y, seed=42):
        X_design = self._add_intercept(X) # 设计矩阵，得到得到 (n, p) 矩阵。
        n, p = X_design.shape
        self.coef_ = np.zeros(p) # 初始化系数
        self.loss_history_ = []
        rng = np.random.default_rng(seed)

        if self.gd_type == "full_batch": # 确定批量大小
            batch_size = n
        elif self.gd_type == "mini_batch":
            batch_size = max(1, int(n * self.batch_fraction))
        else:
            raise ValueError("gd_type must be 'full_batch' or 'mini_batch'")

        for epoch in range(self.max_iter): # 迭代优化
            if self.gd_type == "mini_batch":
                idx = rng.choice(n, size=batch_size, replace=False)
                X_batch = X_design[idx]
                y_batch = y[idx]
            else:
                X_batch = X_design
                y_batch = y

            y_pred_batch = X_batch @ self.coef_
            error = y_pred_batch - y_batch # 误差
            gradient = (2 / len(X_batch)) * (X_batch.T @ error) # 梯度
            self.coef_ -= self.learning_rate * gradient # 参数更新

            # 全量 loss 用于监控，尽管 batch 可能使用子集，但 loss 始终基于全部训练数据计算，保证梯度下降过程的可比性和正确停止条件。
            y_pred_full = X_design @ self.coef_
            mse = np.mean((y - y_pred_full)**2)
            self.loss_history_.append(mse)

            if epoch > 0 and abs(self.loss_history_[-1] - self.loss_history_[-2]) < self.tol:
                break # 早停机制

        self._is_fitted = True
        return self

    def predict(self, X):
        if not self._is_fitted:
            raise RuntimeError("Model not fitted.")
        X_design = self._add_intercept(X)
        return X_design @ self.coef_

    def score(self, X, y):
        y_pred = self.predict(X)
        sse = np.sum((y - y_pred)**2)
        sst = np.sum((y - np.mean(y))**2)
        return 1 - sse/sst if sst != 0 else 0.0