from flask import Flask, jsonify, render_template
import pandas as pd
import os

app = Flask(__name__)

# 定义列名映射 - *** 请根据你的Excel文件实际情况修改这里的列名 ***
COLUMN_MAPPING = {
    'date': '报告日期',      # 你的日期列名
    'district': '地区名称',  # 你的地区列名
    'cases': '新增确诊'    # 你的确诊数列名
}

# 构建一个基于 app.py 文件位置的绝对路径
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_PATH = os.path.join(APP_ROOT, 'static', 'data', '香港各区疫情数据_20250322.xlsx')

def get_excel_columns():
    """一个临时的调试函数，用于获取Excel的列名"""
    try:
        df = pd.read_excel(DATA_FILE_PATH)
        return {"columns": df.columns.tolist()}
    except FileNotFoundError:
        return {"error": f"数据文件未找到: {DATA_FILE_PATH}"}
    except Exception as e:
        return {"error": f"读取文件时发生未知错误: {e}"}

def process_data():
    """读取并处理Excel数据"""
    try:
        df = pd.read_excel(DATA_FILE_PATH)
        # 使用映射重命名列
        df.rename(columns={v: k for k, v in COLUMN_MAPPING.items()}, inplace=True)
        
        df['date'] = pd.to_datetime(df['date'])

        # 1. 数据概览
        daily_sum = df.groupby('date')['cases'].sum().sort_index()
        total_cases = int(daily_sum.cumsum().iloc[-1])
        latest_new_cases = int(daily_sum.iloc[-1])
        yesterday_cumulative = int(daily_sum.cumsum().iloc[-2])
        latest_growth_rate = f"{(latest_new_cases / yesterday_cumulative) * 100:.2f}%" if yesterday_cumulative else "N/A"
        overview = {
            "total_cases": total_cases,
            "latest_new_cases": latest_new_cases,
            "latest_growth_rate": latest_growth_rate
        }

        # 2. 趋势图
        trend = {
            'dates': daily_sum.index.strftime('%Y-%m-%d').tolist(),
            'new': daily_sum.tolist(),
            'cumulative': daily_sum.cumsum().tolist()
        }
        
        # 3. 区域分布饼图 & 排名
        district_sum = df.groupby('district')['cases'].sum()
        pie_data = [{"name": idx, "value": int(val)} for idx, val in district_sum.items()]
        
        rank_data_sorted = district_sum.sort_values(ascending=True)
        rank = {
            'districts': rank_data_sorted.index.tolist(),
            'values': rank_data_sorted.values.astype(int).tolist()
        }
        
        # 4. 增长率柱状图
        cumulative_cases = daily_sum.cumsum()
        growth_rate_series = (daily_sum / cumulative_cases.shift(1).fillna(0)) * 100
        growth_rate_chart = {
            'dates': growth_rate_series.index.strftime('%Y-%m-%d').tolist(),
            'rates': [f"{val:.2f}" for val in growth_rate_series.values]
        }

        return {
            'overview': overview,
            'trend': trend,
            'pie': pie_data,
            'rank': rank,
            'growth_rate_chart': growth_rate_chart
        }
        
    except FileNotFoundError:
        return {"error": f"数据文件未找到: {DATA_FILE_PATH}"}
    except KeyError as e:
        return {"error": f"Excel文件中缺少必需的列: {e}。请检查 COLUMN_MAPPING 是否正确。"}
    except Exception as e:
        return {"error": f"处理数据时发生未知错误: {e}"}

@app.route('/')
def index():
    """渲染主页面"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """提供JSON数据接口"""
    data = process_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5001) 