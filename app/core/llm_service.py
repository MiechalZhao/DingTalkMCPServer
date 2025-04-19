"""
Service for Large Language Model operations
"""
import json
import logging

from app.utils.logger import setup_logger
from openai import OpenAI
# from qwenai import QwenAI
from app.config.settings import settings

class LLMService:
    """Service for handling LLM API calls"""
    
    def __init__(self):
        api_key = None
        ai_llm = None
        self.api_key = api_key
        self.ai_llm = ai_llm
        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(
                api_key=api_key,
                base_url=settings.OPENAI_API_BASE_URL,
            )
            ai_llm = settings.OPEN_AI
        else:
            api_key = settings.QWEN_API_KEY
            if api_key:
                self.ai_llm = settings.QWEN_AI
            else:
                setup_logger(logging.WARN).warning("未在配置中设置 OPENAI_API_KEY")

    def chat_completion(self, messages, tools=None, model=None):
        if self.ai_llm is None:
            return None
        if self.ai_llm == settings.OPEN_AI:
            return self.open_ai_handler(messages, tools, model)
        else:
            return self.qwen_ai_handler(messages, tools, model)

    def open_ai_handler(self, messages, tools=None, model=None):
        """
        发送请求到OpenAI并返回回复
        
        Args:
            messages: 消息列表 
            tools: 工具列表
            model: 模型名称，默认使用settings中的配置
            
        Returns:
            OpenAI API的响应对象
        """
        if not self.openai_client:
            raise ValueError("OpenAI client is not initialized")
        model = model or settings.OPENAI_API_MODEL
        if tools:
            return self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools
            )
        else:
            return self.openai_client.chat.completions.create(
                model=model,
                messages=messages
            )

    def qwen_ai_handler(self, messages, tools=None, model=None):
        # TO BE ADD
        return

    def is_available(self):
        """检查API是否可用"""
        return self.openai_client is not None
