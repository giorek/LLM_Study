"""
Hello.py

本脚本用于演示如何通过阿里云通义千问（Qwen）大模型进行产品口碑的正负向舆情分析。

功能简介：
- 通过 OpenAI 兼容接口或 DashScope SDK 调用 Qwen 模型，对输入的产品评论进行情感分析，判断其为"正向"或"负向"。
- 适用于中文产品评论的自动化情感判别。

主要依赖：
- openai
- dashscope
- 需要设置环境变量 DASHSCOPE_API_KEY 以访问 DashScope 服务。

主要函数：
- hello_openai(): 通过 OpenAI 兼容接口调用 Qwen 模型。
- hello_dashscope(): 通过 DashScope 官方 SDK 调用 Qwen 模型。

用法：
1. 配置好 DASHSCOPE_API_KEY 环境变量。
2. 运行本脚本，默认调用 hello_openai()，如需调用 hello_dashscope()，请取消 main 函数中的注释。

参考文档：
https://help.aliyun.com/zh/model-studio/developer-reference/error-code
"""

import os
import openai
import dashscope

review = ''
messages=[
    {"role":"system","content":"你是一名舆情分析师，帮我判 断产品口碑的正负向，回复请用一个词语:正向 或者 负向"},
    {"role":"user","content":review}
]

"""
通过openai兼容接口进行获取
"""
def hello_openai():
    try:
        client = openai.OpenAI(
            base_url='https://dashscope.aliyuncs.com/compatible-mode/v1',
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            timeout=30
        )
        completion = client.chat.completions.create(
            model='qwen-plus',
            messages=messages
        )
        # print(completion)
        print(f"cotent:{completion.choices[0].message.content}")

    except Exception as e:
        print(f"错误信息：{e}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")


"""
通过dashcope sdk调用
"""
def hello_dashscope():
    response = dashscope.Generation.call(
        model='deepseek-v3',
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        messages=messages,
    )
    if response.status_code == 200:
        # print(response)
        print(f"status_code:{response.status_code}")
        print(f"结果:{response.output.choices[0].message.content}")
        
    else:
        print(f"HTTP返回码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
        print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        




if __name__ == "__main__":
    # hello_dashscope()
    review = '这款音效特别好 给你意想不到的音质。'
    hello_openai()
    review="我不喜欢这个产品"
    messages=[
        {"role":"system","content":"你是一名舆情分析师，帮我判 断产品口碑的正负向，回复请用一个词语:正向 或者 负向"},
        {"role":"user","content":review}
    ]
    hello_dashscope()
    # hello_openai()