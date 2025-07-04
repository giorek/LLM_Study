"""
基于 Assistant 实现的文本计数智能助手

该模块提供了一个文本计数助手，可以：
1. 通过自然语言进行文本计数服务查询
2. 支持多种交互方式（GUI、TUI、测试模式）
3. 支持文本计数、文件统计等功能
"""

import os
from typing import Optional
from qwen_agent.agents import Assistant
from qwen_agent.gui import WebUI

# 定义资源文件根目录
ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')

def init_agent_service():
    """初始化文本计数助手服务
    
    配置说明：
    - 使用 qwen-max 作为底层语言模型
    - 设置系统角色为文本计数助手
    - 配置本地 text_countercopy.py 作为 MCP 工具
    
    Returns:
        Assistant: 配置好的助手实例
    """
    # LLM 模型配置
    llm_cfg = {
        'model': 'qwen-max',
        'timeout': 30,
        'retry_count': 3,
    }
    # 系统角色设定
    system = (
        '你扮演一个文本计数助手，你可以统计文本的字符数、词数等。'
        '你可以帮助用户分析文本长度、内容等。'
        '你应该充分利用本地计数工具来提供专业的统计服务。'
    )
    # MCP 工具配置
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tools = [{
        "mcpServers": {
            "txt-counter": {
                "command": "python",
                "args": [os.path.join(current_dir, "text_countercopy.py")],
                "port": 6274
            }
        }
    }]
    try:
        bot = Assistant(
            llm=llm_cfg,
            name='文本计数助手',
            description='文本计数/文件统计',
            system_message=system,
            function_list=tools,
        )
        print("助手初始化成功！")
        return bot
    except Exception as e:
        print(f"助手初始化失败: {str(e)}")
        raise

def test(query='统计这段文本的字符数', file: Optional[str] = None):
    """测试模式
    用于快速测试单个查询
    """
    try:
        bot = init_agent_service()
        messages = []
        if not file:
            messages.append({'role': 'user', 'content': query})
        else:
            messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})
        print("正在处理您的请求...")
        for response in bot.run(messages):
            print('bot response:', response)
    except Exception as e:
        print(f"处理请求时出错: {str(e)}")

def app_tui():
    """终端交互模式
    提供命令行交互界面，支持连续对话和文件输入
    """
    try:
        bot = init_agent_service()
        messages = []
        while True:
            try:
                query = input('user question: ')
                file = input('file url (press enter if no file): ').strip()
                if not query:
                    print('user question cannot be empty！')
                    continue
                if not file:
                    messages.append({'role': 'user', 'content': query})
                else:
                    messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})
                print("正在处理您的请求...")
                response = []
                for response in bot.run(messages):
                    print('bot response:', response)
                messages.extend(response)
            except Exception as e:
                print(f"处理请求时出错: {str(e)}")
                print("请重试或输入新的问题")
    except Exception as e:
        print(f"启动终端模式失败: {str(e)}")

def app_gui():
    """图形界面模式
    提供 Web 图形界面，特点：
    - 友好的用户界面
    - 预设查询建议
    - 智能文本计数
    """
    try:
        print("正在启动 Web 界面...")
        bot = init_agent_service()
        chatbot_config = {
            'prompt.suggestions': [
                '统计"你好，世界！"的字符数',
                '统计一段英文文本的单词数',
                '分析文件的内容长度',
                '统计一段文本的词频'
            ]
        }
        print("Web 界面准备就绪，正在启动服务...")
        WebUI(
            bot,
            chatbot_config=chatbot_config
        ).run()
    except Exception as e:
        print(f"启动 Web 界面失败: {str(e)}")
        print("请检查 MCP 工具和端口配置")

if __name__ == '__main__':
    # 运行模式选择
    # test()           # 测试模式
    # app_tui()        # 终端交互模式
    app_gui()          # 图形界面模式（默认） 