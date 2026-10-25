"""
Priority Task Queue with Dynamic Aging
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import time
import heapq
import threading
from typing import Any, Optional, Tuple

class PriorityTaskQueue:
    """
    Thread-safe priority queue with aging heuristics to prevent priority starvation.
    """
    def __init__(self, aging_rate: float = 0.5):
        self.aging_rate = aging_rate
        self._heap: list = []
        self._counter = 0
        self._lock = threading.Lock()

    def push(self, task_name: str, payload: Any, base_priority: int = 10) -> None:
        """Lower priority numbers represent higher scheduling priority."""
        with self._lock:
            self._counter += 1
            entry = [base_priority, time.monotonic(), self._counter, task_name, payload]
            heapq.heappush(self._heap, entry)

    def pop(self) -> Optional[Tuple[str, Any]]:
        with self._lock:
            if not self._heap:
                return None
            now = time.monotonic()
            # Apply dynamic aging to all items in heap
            for item in self._heap:
                wait_time = now - item[1]
                effective_prio = item[0] - (wait_time * self.aging_rate)
                item[0] = effective_prio
            heapq.heapify(self._heap)

            item = heapq.heappop(self._heap)
            return (item[3], item[4])

    def size(self) -> int:
        with self._lock:
            return len(self._heap)
