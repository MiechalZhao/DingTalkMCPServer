import os

class Settings:
    """Application settings"""

    CLIENT_ID = 'app_key or suite_key from https://open-dev.digntalk.com'
    CLIENT_SECRET = 'app_secret or suite_secret from https://open-dev.digntalk.com'
    FUNCTION_TRIGGER_FLAG = os.getenv("FUNCTION_TRIGGER_FLAG", "/run")
    OPENAI_API_KEY = 'openai api key for llm'
    OPEN_AI = "OPEN_AI"
    QWEN_API_KEY = 'qwen api key for llm'
    QWEN_AI = "QWEN_AI"

settings = Settings()

