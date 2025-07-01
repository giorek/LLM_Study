import pandas as pd
import os

# 构建 Excel 文件路径
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'data', 'policy_data.xlsx')

try:
    df = pd.read_excel(file_path)
    print("\n===== 数据集基本信息 =====")
    print(f"行数: {df.shape[0]}, 列数: {df.shape[1]}")
    print("列名和类型:")
    print(df.dtypes)

    print("\n===== 前10行数据预览 =====")
    print(df.head(10))

    print("\n===== 缺失值统计 =====")
    print(df.isnull().sum())

    print("\n===== 数值型特征描述性统计 =====")
    print(df.describe())

    print("\n===== 类别型特征唯一值统计 =====")
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        print(f"\n{col} 唯一值:")
        print(df[col].value_counts())

except FileNotFoundError:
    print(f'文件未找到: {file_path}')
except Exception as e:
    print(f'读取或分析文件时发生错误: {e}') 