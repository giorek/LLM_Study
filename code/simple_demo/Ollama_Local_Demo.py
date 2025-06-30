"""
Ollama_Local_Demo.py

本脚本演示如何通过 OpenAI 兼容接口调用本地 Ollama 部署的大模型，实现简单的对话或文本生成。

依赖:
- openai
- 本地已启动 Ollama 服务（默认 http://localhost:11434）

用法:
1. 启动 Ollama 并拉取你需要的模型（如 llama3）。
2. 运行本脚本，体验本地大模型推理。

参考:
https://github.com/ollama/ollama/blob/main/docs/openai.md
"""

import openai

# 配置本地 Ollama OpenAI 兼容接口
client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama 默认不校验 API Key，但 openai 库需要一个字符串
)

"""
如果使用ollama部署本地大模型，可以使用如下方式进行调用
model可以选择本地安装的模型
"""
#def chat_with_ollama(prompt, model="llama3"):
def chat_with_ollama(prompt, model="deepseek-r1:1.5b"):
    messages = [
        {"role": "system", "content": "你是一个本地大模型助手。"},
        {"role": "user", "content": prompt}
    ]
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    while True:
        user_input = input("请输入你的问题：")
        result = chat_with_ollama(user_input)
        print("Ollama 回复：", result) 