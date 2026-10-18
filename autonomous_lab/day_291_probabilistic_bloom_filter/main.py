"""
Probabilistic Bloom Filter
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import math
import hashlib
from typing import List

class BloomFilter:
    """
    Space-efficient probabilistic structure for fast element membership testing.
    """
    def __init__(self, expected_elements: int = 1000, false_positive_rate: float = 0.01):
        if expected_elements <= 0 or not (0 < false_positive_rate < 1):
            raise ValueError("Invalid parameters for BloomFilter")
            
        self.size = int(- (expected_elements * math.log(false_positive_rate)) / (math.log(2) ** 2))
        self.hash_count = int((self.size / expected_elements) * math.log(2))
        self.bit_array = bytearray((self.size + 7) // 8)

    def _hashes(self, item: str) -> List[int]:
        item_bytes = item.encode("utf-8")
        h1 = int(hashlib.md5(item_bytes).hexdigest(), 16)
        h2 = int(hashlib.sha1(item_bytes).hexdigest(), 16)
        return [(h1 + i * h2) % self.size for i in range(self.hash_count)]

    def add(self, item: str) -> None:
        for bit_index in self._hashes(item):
            byte_idx = bit_index // 8
            bit_idx = bit_index % 8
            self.bit_array[byte_idx] |= (1 << bit_idx)

    def contains(self, item: str) -> bool:
        for bit_index in self._hashes(item):
            byte_idx = bit_index // 8
            bit_idx = bit_index % 8
            if not (self.bit_array[byte_idx] & (1 << bit_idx)):
                return False
        return True
