import json
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    APP_NAME: str = "gptomni-2api"
    APP_VERSION: str = "1.0.0"
    DESCRIPTION: str = "一个将 gptomni.ai 转换为兼容 OpenAI 格式 API 的高性能代理。"

    API_MASTER_KEY: Optional[str] = None
    
    # 直接从 .env 文件读取 GPTOMNI_CREDENTIALS 变量
    GPTOMNI_CREDENTIALS: str = '[]'

    @property
    def parsed_credentials(self) -> List[str]:
        """将 JSON 字符串凭证解析为 Python 列表。"""
        try:
            creds = json.loads(self.GPTOMNI_CREDENTIALS)
            if isinstance(creds, list):
                return creds
            return []
        except (json.JSONDecodeError, TypeError):
            return []

    API_REQUEST_TIMEOUT: int = 10
    NGINX_PORT: int = 8088

    DEFAULT_MODEL: str = "gptomni"
    KNOWN_MODELS: List[str] = ["gptomni"]

settings = Settings()
