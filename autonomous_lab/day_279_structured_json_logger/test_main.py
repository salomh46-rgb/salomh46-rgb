import unittest
import json
from main import StructuredJSONLogger

class TestStructuredLogger(unittest.TestCase):
    def test_log_output(self):
        logger = StructuredJSONLogger("payment-service", min_level="INFO")
        out = logger.log("INFO", "Transaction initiated", tx_id="TX_1001", amount=75000)
        data = json.loads(out)
        self.assertEqual(data["service"], "payment-service")
        self.assertEqual(data["level"], "INFO")
        self.assertEqual(data["context"]["tx_id"], "TX_1001")

    def test_min_level_filtering(self):
        logger = StructuredJSONLogger("auth-service", min_level="WARNING")
        self.assertEqual(logger.log("DEBUG", "debug msg"), "")
        self.assertEqual(logger.log("INFO", "info msg"), "")
        self.assertNotEqual(logger.log("ERROR", "error msg"), "")

if __name__ == "__main__":
    unittest.main()
