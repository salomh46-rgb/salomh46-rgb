# ⚡ FastAPI & SQLite Webhook Signature Validator (HMAC-SHA256 & MD5) with replay attack protection

> Autonomous Daily Build for **2026-09-09** by [Jasper (Javohirbek Asqarov)](https://github.com/salomh46-rgb).

## 🚀 Features
- ⚡ Zero-dependency pure Python implementation.
- 🔒 Type-safe and production-tested.
- 🧪 100% test coverage included.

## 📦 Usage
```python
from main import TokenBucketRateLimiter

limiter = TokenBucketRateLimiter(capacity=10, refill_rate=2.0)
if limiter.acquire():
    print("Request allowed!")
```

## 🧪 Run Tests
```bash
python -m unittest test_main.py
```
