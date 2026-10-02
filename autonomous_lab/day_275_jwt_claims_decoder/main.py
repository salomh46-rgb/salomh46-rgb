"""
Zero-Dependency JWT Claims Decoder
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

import json
import base64
import time
from typing import Dict, Any, Optional

class JWTDecodeError(Exception):
    pass

class JWTClaimsDecoder:
    """
    Extracts headers and claims from standard JWT tokens without bulky external libraries.
    """
    @staticmethod
    def _b64_decode(data: str) -> str:
        padded = data + "=" * ((4 - len(data) % 4) % 4)
        try:
            return base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8")
        except Exception as e:
            raise JWTDecodeError(f"Invalid Base64URL string: {e}")

    @classmethod
    def decode_unverified(cls, token: str) -> Dict[str, Any]:
        parts = token.split(".")
        if len(parts) != 3:
            raise JWTDecodeError(f"JWT must contain exactly 3 segments separated by dots, got {len(parts)}")
        
        header_raw = cls._b64_decode(parts[0])
        payload_raw = cls._b64_decode(parts[1])
        
        try:
            header = json.loads(header_raw)
            payload = json.loads(payload_raw)
        except json.JSONDecodeError as e:
            raise JWTDecodeError(f"Malformed JSON in token segments: {e}")
            
        return {"header": header, "payload": payload, "signature": parts[2]}

    @classmethod
    def is_expired(cls, token: str, leeway_seconds: float = 0.0) -> bool:
        claims = cls.decode_unverified(token)["payload"]
        exp = claims.get("exp")
        if exp is None:
            return False
        return (time.time() - leeway_seconds) > float(exp)
