import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import pandas as pd
import os
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']  # 支持中文
plt.rcParams['axes.unicode_minus'] = False  # 负号正常显示
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# 构建 Excel 文件路径
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'data', 'policy_data.xlsx')

# 读取数据
df = pd.read_excel(file_path)

# 检查 renewal 字段
if 'renewal' not in df.columns:
    raise ValueError('数据中未找到 renewal 字段')

# 1. 特征与标签
y = df['renewal']
X = df.drop(columns=['renewal'])

# 删除所有 datetime 类型的列
X = X.drop(columns=X.select_dtypes(include=['datetime', 'datetime64[ns]', 'timedelta']).columns)

# 2. 处理类别特征（自动 one-hot 编码）
X = pd.get_dummies(X, drop_first=True)

# 3. 拆分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 训练逻辑回归模型
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# 5. 评估准确率
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"测试集准确率: {acc:.4f}")

# 6. 系数可视化
coefs = model.coef_[0]
features = X.columns
coef_df = pd.DataFrame({'feature': features, 'coef': coefs})
coef_df = coef_df.sort_values('coef', key=abs, ascending=False)

# 只取绝对值最大的Top20特征
coef_df_top20 = coef_df.head(20)

plt.figure(figsize=(12, 8))
colors = coef_df_top20['coef'].apply(lambda x: 'red' if x < 0 else 'green')
plt.barh(coef_df_top20['feature'], coef_df_top20['coef'], color=colors)  # 横向条形图
plt.axvline(0, color='black', linewidth=0.8)
plt.yticks(fontsize=10)
plt.title('Logistic回归系数Top20（正负区分）')
plt.xlabel('系数值')
plt.tight_layout()
plt.show()

# 保存Top20特征及其系数，便于解释
coef_df_top20.to_csv('logistic_coef_top20.csv', index=False, encoding='utf-8-sig') 