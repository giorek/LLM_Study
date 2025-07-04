# txt_countercopy.py
# 该脚本用于统计输入文本的字符数或词数，可作为MCP工具集成使用。
# 
# 使用说明：
# 1. 如何注册函数给MCP：
#    - 按照MCP工具开发规范，将你的主处理函数（如 count_text）注册到 MCP 工具管理器中。
#    - 例如：
#        from mcp import tool
#        @tool()
#        def count_text():
#                text =''
#            return len(text)
# 2. 推荐启动方式：
#    - 使用 MCP 官方命令行工具启动开发服务：
#        mcp dev txt_counter copy.py
#    - 这样可以自动加载和热重载本地MCP工具，便于开发调试。
#    - 或在 assistant_mcp_txt_bot.py 的 mcpServers 配置中指定本脚本路径。
# 3. 输入输出说明：
#    - 输入：通过标准输入或参数传入待统计的文本。
#    - 输出：返回文本的字符数或词数，可根据实际需求修改处理逻辑。
#

import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from typing import Optional

# 创建 MCP Server
mcp = FastMCP("桌面 TXT 文件统计器")

@mcp.tool()
def count_desktop_txt_files() -> int:
    """统计桌面上 .txt 文件的数量"""
    # 获取桌面路径
    desktop_path = Path(os.path.expanduser("~/Desktop"))

    # 统计 .txt 文件
    txt_files = list(desktop_path.glob("*.txt"))
    return len(txt_files)

@mcp.tool()
def list_desktop_txt_files() -> str:
    """获取桌面上所有 .txt 文件的列表"""
    # 获取桌面路径
    desktop_path = Path(os.path.expanduser("~/Desktop"))

    # 获取所有 .txt 文件
    txt_files = list(desktop_path.glob("*.txt"))

    # 返回文件名列表
    if not txt_files:
        return "桌面上没有找到 .txt 文件。"

    # 格式化文件名列表
    file_list = "\n".join([f"- {file.name}" for file in txt_files])
    return f"在桌面上找到 {len(txt_files)} 个 .txt 文件：\n{file_list}"

@mcp.tool()
def read_txt_file(filename: str) -> str:
    """读取指定txt文件的内容
    
    Args:
        filename: txt文件的名称（例如：test.txt）
        
    Returns:
        文件内容，如果文件不存在则返回错误信息
    """
    # 获取桌面路径
    desktop_path = Path(os.path.expanduser("~/Desktop"))
    file_path = desktop_path / filename
    
    # 检查文件是否存在
    if not file_path.exists():
        return f"错误：文件 '{filename}' 不存在于桌面上。"
    
    # 检查文件是否是txt文件
    if file_path.suffix.lower() != '.txt':
        return f"错误：文件 '{filename}' 不是txt文件。"
    
    try:
        # 读取文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return f"文件 '{filename}' 的内容：\n\n{content}"
    except Exception as e:
        return f"读取文件时发生错误：{str(e)}"

if __name__ == "__main__":
    # 初始化并运行服务器
    mcp.run()