"""
Consistent Hashing Ring with Virtual Nodes
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import hashlib
import bisect
from typing import Dict, List, Optional

class ConsistentHashRing:
    """
    Consistent Hash Ring for distributed partitioning and load balancing.
    """
    def __init__(self, replicas: int = 100):
        self.replicas = replicas
        self.ring: List[int] = []
        self.ring_map: Dict[int, str] = {}

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        for i in range(self.replicas):
            vnode_key = f"{node}#vnode{i}"
            h = self._hash(vnode_key)
            bisect.insort(self.ring, h)
            self.ring_map[h] = node

    def remove_node(self, node: str) -> None:
        for i in range(self.replicas):
            vnode_key = f"{node}#vnode{i}"
            h = self._hash(vnode_key)
            idx = bisect.bisect_left(self.ring, h)
            if idx < len(self.ring) and self.ring[idx] == h:
                del self.ring[idx]
                self.ring_map.pop(h, None)

    def get_node(self, key: str) -> Optional[str]:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        return self.ring_map[self.ring[idx]]
