import pandas as pd
import os

# 构建 Excel 文件路径
base_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(base_dir, 'data', 'policy_data.xlsx')

# 读取前10行数据
try:
    df = pd.read_excel(file_path)
    print(df.head(10))
except FileNotFoundError:
    print(f'文件未找到: {file_path}')
except Exception as e:
    print(f'读取文件时发生错误: {e}') 