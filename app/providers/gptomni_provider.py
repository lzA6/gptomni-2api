import httpx
import json
import time
import logging
import uuid
import cloudscraper
from typing import Dict, Any, AsyncGenerator

from fastapi import HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from aiolimiter import AsyncLimiter

from app.core.config import settings
from app.providers.base_provider import BaseProvider
from app.providers.credential_manager import get_credential_manager
from app.utils.sse_utils import create_sse_data, create_chat_completion_chunk, DONE_CHUNK

logger = logging.getLogger(__name__)

class GptOmniProvider(BaseProvider):
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.api_url = "https://gptomni.ai/api/chatWithText"
        self.limiter = AsyncLimiter(2, 60)

    async def chat_completion(self, request_data: Dict[str, Any]) -> StreamingResponse:
        
        async def stream_generator() -> AsyncGenerator[bytes, None]:
            request_id = f"chatcmpl-{uuid.uuid4()}"
            try:
                async with self.limiter:
                    logger.info("速率限制器已授权，准备向上游发送请求。")
                    
                    payload = self._prepare_payload(request_data)
                    headers = self._prepare_headers()

                    response = self.scraper.post(
                        self.api_url, 
                        headers=headers, 
                        data=json.dumps(payload),
                        stream=True,
                        timeout=settings.API_REQUEST_TIMEOUT
                    )
                    response.raise_for_status()

                    # --- 忠诚代理逻辑 (Faithful Proxy Logic) ---
                    # 使用 iter_content() 替代 iter_lines() 来保留所有原始格式，包括换行符。
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            delta_content = chunk.decode('utf-8', errors='ignore')
                            sse_chunk = create_chat_completion_chunk(request_id, settings.DEFAULT_MODEL, delta_content)
                            yield create_sse_data(sse_chunk)

                # 流结束后发送终止块
                final_chunk = create_chat_completion_chunk(request_id, settings.DEFAULT_MODEL, "", "stop")
                yield create_sse_data(final_chunk)
                yield DONE_CHUNK

            except httpx.TimeoutException:
                logger.error("请求上游 API 超时。")
                error_message = "上游服务超时 (10秒)，请稍后再试。"
                error_chunk = create_chat_completion_chunk(request_id, settings.DEFAULT_MODEL, error_message, "stop")
                yield create_sse_data(error_chunk)
                yield DONE_CHUNK
            except Exception as e:
                logger.error(f"处理流时发生错误: {e}", exc_info=True)
                error_message = f"内部服务器错误: {str(e)}"
                error_chunk = create_chat_completion_chunk(request_id, settings.DEFAULT_MODEL, error_message, "stop")
                yield create_sse_data(error_chunk)
                yield DONE_CHUNK

        return StreamingResponse(stream_generator(), media_type="text/event-stream")

    def _prepare_headers(self) -> Dict[str, str]:
        cred_manager = get_credential_manager()
        cookie = cred_manager.get_credential()
        
        return {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Content-Type": "text/plain;charset=UTF-8",
            "Origin": "https://gptomni.ai",
            "Referer": "https://gptomni.ai/zh",
            "Cookie": cookie
        }

    def _prepare_payload(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        messages = request_data.get("messages", [])
        last_user_message = next((m['content'] for m in reversed(messages) if m['role'] == 'user'), "")
        
        return {"prompt": last_user_message}

    async def get_models(self) -> JSONResponse:
        model_data = {
            "object": "list",
            "data": [
                {"id": name, "object": "model", "created": int(time.time()), "owned_by": "lzA6"}
                for name in settings.KNOWN_MODELS
            ]
        }
        return JSONResponse(content=model_data)
