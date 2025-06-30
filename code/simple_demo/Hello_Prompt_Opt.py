import dashscope
import os



"""
Hello_Prompt_Opt.py

本脚本演示了如何利用大模型（如 Qwen-max）来优化和创建更有效的提示词（Prompt）。
这种方法被称为"元提示词"（Meta Prompting），即用一个提示词去指导模型生成或改进另一个提示词。

功能简介：
- 将用户的原始需求和一套优化指令结合，构成一个"元提示词"。
- 调用 DashScope 的 `qwen-max` 模型，处理这个元提示词。
- 模型会返回一个优化后的提示词、具体的改进建议以及用于澄清需求的问题。

主要依赖：
- dashscope
- 需要设置环境变量 DASHSCOPE_API_KEY 以访问 DashScope 服务。

主要函数：
- get_completion(prompt): 接收一个提示词，调用 DashScope API 并返回模型的生成结果。

用法：
1. 配置好 DASHSCOPE_API_KEY 环境变量。
2. 在 `user_input` 变量中定义你的原始需求。
3. 在 `instruction` 变量中定义你希望模型如何优化提示词。
4. 运行本脚本，查看模型生成的优化版提示词和建议。
"""
def get_completion(prompt)->str:
    messages = [{"role":"user","content":prompt}]
    completion = dashscope.Generation.call(
        model="qwen-max",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        messages=messages
    )
    return completion


#用户输入
user_input="""
做一个手机流量套餐的客服代表，叫小瓜。可以帮助用户 选择最合适的流量套餐产品。
可以选择的套餐包括: 
经济套餐，月费50元，10G流量; 
畅游套餐，月费180元，100G流量; 
无限套餐，月费300元，1000G流量; 
校园套餐，月费150元，200G流量，仅限在校生。
"""

#指令
instruction="""
你是一名专业的提示词创作者。你的目标是帮助我根据需
求打造更好的提示词。
你将生成以下部分: 
提示词:{根据我的需求提供更好的提示词} 
优化建议:{用简练段落分析如何改进提示词，需给出严格批判性建议} 
问题示例:{提出最多3个问题，以用于和用户更好 的交流}
"""

prompt=f"""
#指令
{instruction}

#用户输入
{user_input}

"""



if __name__ == "__main__":
    result = get_completion(prompt)
    print(result)