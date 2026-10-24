"""
Shannon Entropy Secret & Token Strength Analyzer
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import math
from typing import Dict, Any

class ShannonEntropyAnalyzer:
    """
    Computes Shannon entropy (H = -sum(p * log2(p))) and assesses password / token complexity.
    """
    @staticmethod
    def calculate_entropy(secret: str) -> float:
        if not secret:
            return 0.0

        length = len(secret)
        freq: Dict[str, int] = {}
        for char in secret:
            freq[char] = freq.get(char, 0) + 1

        entropy = 0.0
        for count in freq.values():
            p = count / length
            entropy -= p * math.log2(p)

        return round(entropy * length, 2)  # Total information entropy in bits

    @classmethod
    def evaluate_strength(cls, secret: str) -> Dict[str, Any]:
        bits = cls.calculate_entropy(secret)
        if bits < 40:
            rating = "VERY_WEAK"
        elif bits < 60:
            rating = "WEAK"
        elif bits < 80:
            rating = "MODERATE"
        elif bits < 100:
            rating = "STRONG"
        else:
            rating = "CRYPTOGRAPHIC_GRADE"

        return {
            "entropy_bits": bits,
            "rating": rating,
            "length": len(secret),
            "is_secure": bits >= 80
        }
