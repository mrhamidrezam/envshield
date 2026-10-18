"""
Schema definition and environment variable validation.
"""

from typing import Any, Callable, Dict, List, Optional, Type


class ValidationError(Exception):
    """Raised when environment variables fail schema validation."""

    def __init__(self, errors: Dict[str, str]):
        self.errors = errors
        message = "Environment validation failed:\n" + "\n".join(
            f"  - {key}: {err}" for key, err in errors.items()
        )
        super().__init__(message)


class Field:
    """Represents a validated environment variable field."""

    def __init__(
        self,
        field_type: Type = str,
        required: bool = True,
        default: Any = None,
        validator: Optional[Callable[[Any], bool]] = None,
        description: str = "",
    ):
        self.field_type = field_type
        self.required = required
        self.default = default
        self.validator = validator
        self.description = description

    def cast(self, raw_value: Optional[str]) -> Any:
        if raw_value is None or raw_value == "":
            if self.required and self.default is None:
                raise ValueError("Value is required but not provided")
            return self.default

        if self.field_type is bool:
            lowered = raw_value.strip().lower()
            if lowered in {"1", "true", "yes", "on"}:
                return True
            if lowered in {"0", "false", "no", "off"}:
                return False
            raise ValueError(f"Cannot cast '{raw_value}' to boolean")

        try:
            casted = self.field_type(raw_value)
        except Exception as e:
            raise ValueError(f"Cannot cast '{raw_value}' to {self.field_type.__name__}: {e}")

        if self.validator is not None and not self.validator(casted):
            raise ValueError(f"Value '{casted}' failed custom validation")

        return casted


class EnvSchema:
    """Defines and validates an environment configuration schema."""

    def __init__(self, fields: Dict[str, Field]):
        self.fields = fields

    def validate(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input environment dictionary against schema."""
        errors: Dict[str, str] = {}
        validated: Dict[str, Any] = {}

        for key, field in self.fields.items():
            raw_val = source.get(key)
            try:
                validated[key] = field.cast(raw_val)
            except ValueError as e:
                errors[key] = str(e)

        if errors:
            raise ValidationError(errors)

        return validated
