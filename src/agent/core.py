import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def normalize_message(msg: Dict[str, Any]) -> str:
    return str(msg.get("content", ""))
