import unittest
from main import SchemaValidator, ValidationError

class TestSchemaValidator(unittest.TestCase):
    def setUp(self):
        self.user_schema = {
            "username": {"type": str, "required": True, "min_len": 3},
            "age": {"type": int, "required": True, "min": 18, "max": 120},
            "email": {"type": str, "required": False}
        }

    def test_valid_data(self):
        data = {"username": "jasper", "age": 25}
        self.assertTrue(SchemaValidator.validate(data, self.user_schema))

    def test_missing_required_field(self):
        data = {"age": 20}
        with self.assertRaises(ValidationError) as ctx:
            SchemaValidator.validate(data, self.user_schema)
        self.assertIn("username", str(ctx.exception))

    def test_type_and_range_mismatch(self):
        data = {"username": "al", "age": 15}
        with self.assertRaises(ValidationError) as ctx:
            SchemaValidator.validate(data, self.user_schema)
        self.assertIn("at least 3 chars", str(ctx.exception))
        self.assertIn("cannot be less than 18", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
