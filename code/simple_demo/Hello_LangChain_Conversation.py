import os
from langchain.agents import load_tools
from langchain_community.llms import Tongyi 
from langchain import ConversationChain

llm = Tongyi(model="qwen-plus", api_key=os.getenv("DASHSCOPE_API_KEY"))

"""
ConversationChain 是 LangChain 中的一个类，用于构建对话系统。它提供了一个简单的接口，可以方便地构建对话模型，并支持对话历史的管理。
ConversationChain 的主要功能包括：
1. 管理对话历史：ConversationChain 会自动管理对话历史，包括对话的上下文、对话的参与者、对话的时间戳等。
2. 支持对话的生成：ConversationChain 可以生成对话的回复，并支持对话的生成。
3. 支持对话的评估：ConversationChain 可以评估对话的质量，并支持对话的评估。
4. 支持对话的优化：ConversationChain 可以优化对话的质量，并支持对话的优化。
5. 支持对话的存储：ConversationChain 可以存储对话的历史，并支持对话的存储。

ConversationChain 的参数包括：
llm：用于生成对话的模型。
verbose：是否打印对话的详细信息。

ConversationChain 的属性包括：
history：对话历史。
input_key：输入的键。
output_key：输出的键。


"""
conversation = ConversationChain(llm=llm, verbose=True)


if __name__ == "__main__":
    while True:
        user_input = input("请输入：")
        if user_input == "exit":
            break
        response = conversation.invoke({"input": user_input})
        print(response["response"])