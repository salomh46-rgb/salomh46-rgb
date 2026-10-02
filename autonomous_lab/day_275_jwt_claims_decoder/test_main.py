import unittest
import json
import base64
import time
from main import JWTClaimsDecoder, JWTDecodeError

class TestJWTClaimsDecoder(unittest.TestCase):
    def make_jwt(self, header: dict, payload: dict) -> str:
        h = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
        p = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
        return f"{h}.{p}.fake_signature"

    def test_valid_token_decode(self):
        token = self.make_jwt({"alg": "HS256"}, {"sub": "user_42", "role": "admin"})
        data = JWTClaimsDecoder.decode_unverified(token)
        self.assertEqual(data["header"]["alg"], "HS256")
        self.assertEqual(data["payload"]["sub"], "user_42")

    def test_expiration_detection(self):
        expired_token = self.make_jwt({"alg": "HS256"}, {"exp": time.time() - 100})
        self.assertTrue(JWTClaimsDecoder.is_expired(expired_token))
        
        active_token = self.make_jwt({"alg": "HS256"}, {"exp": time.time() + 1000})
        self.assertFalse(JWTClaimsDecoder.is_expired(active_token))

    def test_malformed_token(self):
        with self.assertRaises(JWTDecodeError):
            JWTClaimsDecoder.decode_unverified("invalid.token")

if __name__ == "__main__":
    unittest.main()
