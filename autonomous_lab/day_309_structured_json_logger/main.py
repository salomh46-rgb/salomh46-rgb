"""
High-Throughput Structured JSON Logger
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import json
import sys
import datetime
from typing import Dict, Any, Optional

class StructuredJSONLogger:
    """
    Standard-compliant JSON logger for microservices and observability pipelines.
    """
    LEVELS = {"DEBUG": 10, "INFO": 20, "WARNING": 30, "ERROR": 40, "CRITICAL": 50}

    def __init__(self, service_name: str, min_level: str = "INFO"):
        self.service_name = service_name
        self.min_level_value = self.LEVELS.get(min_level.upper(), 20)

    def log(self, level: str, message: str, **context) -> str:
        level_upper = level.upper()
        if self.LEVELS.get(level_upper, 0) < self.min_level_value:
            return ""

        payload: Dict[str, Any] = {
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "service": self.service_name,
            "level": level_upper,
            "message": message,
        }
        if context:
            payload["context"] = context

        return json.dumps(payload, ensure_ascii=False)
