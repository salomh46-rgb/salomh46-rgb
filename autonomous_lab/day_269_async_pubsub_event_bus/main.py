"""
Decoupled Async Pub-Sub Event Bus
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import fnmatch
from typing import Callable, Dict, List, Any

class AsyncEventBus:
    """
    Decoupled publish-subscribe event routing engine supporting wildcard patterns.
    """
    def __init__(self):
        self._listeners: Dict[str, List[Callable[[str, Any], None]]] = {}

    def subscribe(self, topic_pattern: str, handler: Callable[[str, Any], None]) -> None:
        if topic_pattern not in self._listeners:
            self._listeners[topic_pattern] = []
        self._listeners[topic_pattern].append(handler)

    def publish(self, topic: str, payload: Any) -> int:
        dispatched_count = 0
        for pattern, handlers in self._listeners.items():
            if fnmatch.fnmatch(topic, pattern):
                for handler in handlers:
                    try:
                        handler(topic, payload)
                        dispatched_count += 1
                    except Exception as err:
                        print(f"Handler error on topic {topic}: {err}")
        return dispatched_count
