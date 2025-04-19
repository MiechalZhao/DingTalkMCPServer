"""
Service for processing and storing Lark messages
"""
import json
import os

from datetime import datetime
import logging
from app.config.settings import settings
from app.core.llm_service import LLMService
from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport

class MessageService:
    """Service for processing and storing messages"""
    
    def __init__(self, logger : logging.Logger = None):
        self.llm_service = LLMService()
        if logger:
            self.logger = logger
        self.mcp_transport = PythonStdioTransport("app/core/mcp_server.py", env={"PATHEXT": os.environ.get("PATHEXT", "")})
        self.system_message = {"role": "system", "content": "你是一个很有帮助的助手。当用户提问需要调用工具时，请使用 tools 中定义的函数。"}

    def process_message(self, method: object) -> dict[str, str]:
        """Process a message"""
        message_result = {
            'name': '张三',
            'date': '2025年期间',
            'text': '主要工作职责为海量数据处理',
            'team_info': '属于平台研发部门'
        }
        return message_result
    # You can instead the above function process_message to provide mcp service
    async def process_message_with_llm(self, method: object, content):
        """Process a message"""
        await self._handle_function_call(self, method, content)

    async def _handle_function_call(self, method: object, content):
        self.logger.info("处理来自用户请求")
        query = content.strip()[len(settings.FUNCTION_TRIGGER_FLAG):].strip()
        messages = [
            self.system_message,
            {"role": "user", "content": query}
        ]
        tools = []
        resp = self.llm_service.chat_completion(messages, tools)
        msg = resp.choices[0].message
        if msg.tool_calls:
            call = msg.tool_calls[0]
            fn_name = call.function.name
            args = json.loads(call.function.arguments)
            summary = self.llm_service.chat_completion(messages)
            response = summary.choices[0].message.content
        else:
            response = msg.content

        return response
