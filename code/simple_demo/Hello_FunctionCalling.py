"""
Hello_FunctionCalling.py

本脚本演示如何结合 DashScope 大模型的 Function Calling 能力与本地 Python 函数，实现智能助手自动调用本地工具函数。

功能简介：
- 通过 DashScope 的 Function Calling 机制，模型可根据用户问题自动决定是否调用本地函数。
- 本示例内置 get_current_time 函数，可查询本地当前时间。
- 支持自动解析模型返回的 function_call 字段并执行对应本地函数。

主要依赖：
- dashscope
- 需要设置环境变量 DASHSCOPE_API_KEY 以访问 DashScope 服务。

主要函数：
- get_current_time(): 返回本地当前时间字符串。
- hello_dashscope(): 负责与 DashScope 交互，并根据模型返回自动调用本地函数。

用法：
1. 配置好 DASHSCOPE_API_KEY 环境变量。
2. 运行本脚本，输入与时间相关的问题，模型会自动调用本地函数获取答案。

参考文档：
https://help.aliyun.com/zh/model-studio/developer-reference/function-calling
"""
from datetime import datetime
import os
import dashscope

# 查询当前时间的工具。返回结果示例："当前时间：2024-04-15 17:15:18。"
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"


functions = [
    {
        "name": "get_current_time",
        "description": "获取本地的机器的当前时间",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

query = "现在几点"
messages=[
    {"role":"system","content":"你是一个有用的专业助手。如果用户的问题涉及当前时间，请调用 get_current_time 工具函数。"},
    {"role":"user","content":f"{query}"}
]

"""
通过dashcope sdk调用
"""
def hello_dashscope():
    response = dashscope.Generation.call(
        model='qwen-max',
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        messages=messages,
        functions = functions
    )
    print(response)
    if response.status_code == 200:
        output = response.output
        # 检查是否有 function_call
        if hasattr(output, "choices") and output.choices:
            choice = output.choices[0]
            message = choice.get("message", {})
            function_call = message.get("function_call")
            if function_call:
                func_name = function_call.get("name")
                arguments = function_call.get("arguments", "{}")
                if func_name == "get_current_time":
                    # 执行本地函数
                    result = get_current_time()
                    print(f"本地函数执行结果: {result}")
                else:
                    print(f"未知函数调用: {func_name}")
            else:
                print("无 function_call 字段")
        elif hasattr(output, "text"):
            print(f"结果:{output.text}")
        else:
            print(f"未知返回结构: {output}")
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        




if __name__ == "__main__":
    hello_dashscope()