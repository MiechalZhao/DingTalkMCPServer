# -*- coding: utf-8 -*-
import os
import sys
import random
import datetime

from fastmcp import FastMCP

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from app.core.llm_service import LLMService

mcp = FastMCP("DINGTALK_MCP_SERVER")
registered_tools = []
llm_service = LLMService()

def register_tool(name: str, description: str):
    def decorator(func):
        mcp.tool(name=name, description=description)(func)
        registered_tools.append((name, description))
        return func
    return decorator

@register_tool(name="list_tools", description="List all available tools and their descriptions")
def list_tools() -> str:
    result = "🛠️ 当前可用功能列表：\n"
    for name, desc in registered_tools:
        result += f"- `{name}`：{desc}\n"
    return result

@register_tool(name="extra_order_from_content", description="提取文字中的订单信息，包括订单号、商品名称、数量等，以json格式返回")
def extra_order_from_content(content: str) -> str:
    """
    提取订单信息
    :param content: 消息内容
    :return: 提取的订单信息
    """
    res = llm_service.chat_completion(
        messages=[
            {"role": "user", "content": content},
            {"role": "system", "content": "请提取订单信息，包括订单号、商品名称、数量等，以json格式返回"},
        ],
        tools=None,
        model="qwen-plus"
    )
    if res and res.choices:
        content = res.choices[0].message.content
        if content:
            return content
    return "未能提取到订单信息，请检查消息内容是否包含有效的订单信息。"


@register_tool(name="tell_joke", description="Tell a random joke")
def tell_joke() -> str:
    jokes = [
        "为什么程序员都喜欢黑色？因为他们不喜欢 bug 光。",
        "Python 和蛇有什么共同点？一旦缠上你就放不下了。",
        "为什么 Java 开发者很少被邀去派对？因为他们总是抛出异常。",
    ]
    return random.choice(jokes)


@register_tool(name="get_time", description="Get the current time")
def get_time() -> str:
    now = datetime.datetime.now()
    return f"当前时间是 {now.strftime('%Y-%m-%d %H:%M:%S')}"


@register_tool(name="fortune", description="Draw a random fortune")
def fortune() -> str:
    fortunes = [
        "大吉：今天适合尝试新事物！✨",
        "中吉：平稳的一天，保持专注。",
        "小吉：会有小惊喜出现～",
        "凶：注意不要过度疲劳。",
        "大凶：小心电子设备出问题 🧯"
    ]
    return random.choice(fortunes)

if __name__ == "__main__":
    print(get_weather("China"))
    mcp.run(transport="stdio")