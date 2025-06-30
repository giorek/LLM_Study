"""
Hello_FileCount.py

本脚本演示如何结合 DashScope 大模型的 Function Calling 能力与本地 Python 函数，实现智能助手自动调用本地工具函数查询当前工程目录下的文件数量。

功能简介：
- 通过 DashScope 的 Function Calling 机制，模型可根据用户问题自动决定是否调用本地函数。
- 本示例内置 get_file_count 函数，可统计当前工作目录下的文件数量。
- 支持自动解析模型返回的 function_call 字段并执行对应本地函数。

主要依赖：
- dashscope
- 需要设置环境变量 DASHSCOPE_API_KEY 以访问 DashScope 服务。

主要函数：
- get_file_count(): 返回当前工作目录下的文件数量。
- hello_dashscope(): 负责与 DashScope 交互，并根据模型返回自动调用本地函数。

用法：
1. 配置好 DASHSCOPE_API_KEY 环境变量。
2. 运行本脚本，输入与文件数量相关的问题，模型会自动调用本地函数获取答案。

参考文档：
https://help.aliyun.com/zh/model-studio/developer-reference/function-calling
"""
from datetime import datetime
import os
import dashscope

# 查询当前工程目录下文件数量的工具

def get_file_count():
    print("调用本地函数-----")
    # 获取当前工作目录
    cwd = os.getcwd()
    # 统计文件数量（不包括子目录下的文件）
    file_count = len([f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))])
    return f"当前目录（{cwd}）下的文件数量为：{file_count}。"

functions = [
    {
        "name": "get_file_count",
        "description": "查询当前工程目录下的文件数量",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
]

query = "当前目录有多少个文件？"
messages=[
    {"role":"system","content":"""
    你是一个有用的专业助手，当我向你提问的时候，你根据提问信息选择正确的回答方式
    """},
    {"role":"user","content":query}
]

"""
通过dashscope sdk调用
"""
def hello_dashscope():
    response = dashscope.Generation.call(
        model='qwen-max',
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        messages=messages,
        functions=functions
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
                if func_name == "get_file_count":
                    # 执行本地函数
                    result = get_file_count()
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