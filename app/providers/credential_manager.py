import logging
import threading
from typing import List, Optional

logger = logging.getLogger(__name__)

class CredentialManager:
    def __init__(self, credentials: List[str]):
        if not credentials:
            raise ValueError("凭证列表不能为空。请在 .env 文件中配置 GPTOMNI_CREDENTIALS。")
        
        self.credentials = credentials
        self.num_credentials = len(credentials)
        self.current_index = 0
        self.lock = threading.Lock()
        logger.info(f"凭证管理器已启动，共加载了 {self.num_credentials} 个凭证。")

    def get_credential(self) -> str:
        with self.lock:
            credential = self.credentials[self.current_index]
            self.current_index = (self.current_index + 1) % self.num_credentials
            return credential

credential_manager: Optional[CredentialManager] = None

def initialize_credential_manager(credentials: List[str]):
    global credential_manager
    if not credential_manager:
        credential_manager = CredentialManager(credentials)

def get_credential_manager() -> CredentialManager:
    if credential_manager is None:
        raise RuntimeError("凭证管理器尚未初始化。")
    return credential_manager
