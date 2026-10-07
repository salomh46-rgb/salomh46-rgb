"""
Zero-Dependency Schema Validator
Author: Javohirbek Asqarov (Jasper) & Autonomous AI Engine
"""

from typing import Dict, Any, List

class ValidationError(Exception):
    def __init__(self, errors: List[str]):
        super().__init__("; ".join(errors))
        self.errors = errors

class SchemaValidator:
    """
    Declarative rule validation engine for configuration dictionaries and API requests.
    """
    @staticmethod
    def validate(data: Dict[str, Any], schema: Dict[str, Dict[str, Any]]) -> bool:
        errors = []
        for field, rules in schema.items():
            required = rules.get("required", False)
            if field not in data or data[field] is None:
                if required:
                    errors.append(f"Field '{field}' is required")
                continue

            val = data[field]
            expected_type = rules.get("type")
            if expected_type and not isinstance(val, expected_type):
                errors.append(f"Field '{field}' must be of type {expected_type.__name__}, got {type(val).__name__}")
                continue

            if isinstance(val, (int, float)):
                if "min" in rules and val < rules["min"]:
                    errors.append(f"Field '{field}' cannot be less than {rules['min']}")
                if "max" in rules and val > rules["max"]:
                    errors.append(f"Field '{field}' cannot be greater than {rules['max']}")

            if isinstance(val, str) and "min_len" in rules and len(val) < rules["min_len"]:
                errors.append(f"Field '{field}' must be at least {rules['min_len']} chars long")

        if errors:
            raise ValidationError(errors)
        return True
