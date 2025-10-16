from abc import ABC, abstractmethod
from typing import Dict, Any, Union
from fastapi.responses import StreamingResponse, JSONResponse

class BaseProvider(ABC):
    @abstractmethod
    async def chat_completion(
        self,
        request_data: Dict[str, Any]
    ) -> Union[StreamingResponse, JSONResponse]:
        """处理聊天补全请求的核心方法。"""
        pass

    @abstractmethod
    async def get_models(self) -> JSONResponse:
        """返回可用模型列表的方法。"""
        pass
