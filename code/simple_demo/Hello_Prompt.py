import dashscope
import os

"""
Hello_Prompt.py

本脚本旨在演示如何通过构建一个结构化、详细的提示词（Prompt）来引导大模型（如 Qwen-max）完成特定任务。

功能简介：
- 将一个复杂的任务分解为多个元素（如指令、用户输入、上下文、输出格式等）。
- 将这些元素组合成一个结构化的提示词，以精确控制模型的行为。
- 本示例中，模型被要求识别用户对手机流量套餐的需求，并以 JSON 格式输出识别结果。

主要依赖：
- dashscope
- 需要设置环境变量 DASHSCOPE_API_KEY 以访问 DashScope 服务。

主要函数：
- get_completion(prompt): 接收一个提示词，调用 DashScope API 并返回模型的生成结果。

用法：
1. 配置好 DASHSCOPE_API_KEY 环境变量。
2. 根据你的需求，修改 `instruction`、`input_text`、`output_format` 等变量。
3. 运行本脚本，查看模型根据结构化提示词生成的输出。
"""

"""
调用大模型，构建的提示词工程只是作为向大模型传递的user信息部分
"""
def get_completion(prompt)->str:
    messages = [{"role":"user","content":prompt}]
    completion = dashscope.Generation.call(
        model="qwen-max",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        messages=messages
    )
    return completion

###############定义提示词中的相关元素################
"""
#任务/指令
#用户输入
#上下文
#示例
#输出格式
#角色
#语气
#思维链 例如请一步步输出
#这些内容一起构成了像大模型传递的user数据信息
"""
# 任务描述
instruction = """
 你的任务是识别用户对手机流量套餐产品的选择条件。 
 每种流量套餐产品包含三个属性:名称，月费价格，月流量。 
 根据用户输入，识别用户在上述三种属性上的需求是什么。 
 """
# 用户输入
input_text = """
办个100G的套餐。
"""

#上下文
contxt=''

#示例
example=''

# 输出格式 
output_format = """
 以 JSON 格式输出 
 """

#角色
role=''

#语气
tone=''

#cot
cot='一步步输出'

#构建完整的提示词
prompt = f"""
# 目标
{instruction}

# 用户输入
{input_text}

#上下文
{contxt}

#示例
{example}

#输出格式
{output_format}

#角色
{role}

#语气
{tone}

#cot
{cot}

"""


if __name__ == "__main__":
    result = get_completion(prompt)
    print(result)