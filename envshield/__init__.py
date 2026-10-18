"""
EnvShield: Environment Configuration Validator & Secret Sanitization Toolkit.
"""

from .validator import EnvSchema, Field, ValidationError
from .sanitizer import sanitize_dict, mask_secret, detect_secrets

__version__ = "0.1.0"
__all__ = [
    "EnvSchema",
    "Field",
    "ValidationError",
    "sanitize_dict",
    "mask_secret",
    "detect_secrets",
]
