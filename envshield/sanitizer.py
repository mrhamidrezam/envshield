"""
Secret pattern detection and dictionary/logging sanitization.
"""

import re
from typing import Any, Dict, List, Set

SENSITIVE_KEY_PATTERNS = [
    r"api[_-]?key",
    r"secret",
    r"password",
    r"token",
    r"auth",
    r"credential",
    r"private[_-]?key",
    r"jwt",
    r"bearer",
]

SECRET_VALUE_PATTERNS = [
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),  # GitHub Personal Access Token
    re.compile(r"ey[A-Za-z0-9_-]{10,}\.[A-Za-z0-9._-]{10,}"),  # JWT Token
    re.compile(r"sk-[a-zA-Z0-9]{32,}"),  # Common API key prefix
    re.compile(r"AKIA[0-9A-Z]{16}"),  # AWS Access Key ID
]

KEY_REGEX = re.compile("|".join(SENSITIVE_KEY_PATTERNS), re.IGNORECASE)


def mask_secret(value: str, visible_chars: int = 4) -> str:
    """Masks secret value showing only the leading and trailing characters."""
    if not isinstance(value, str):
        return "***"
    n = len(value)
    if n <= visible_chars:
        return "*" * n
    return f"{value[:2]}...{value[-2:]}" if n > 6 else "*" * n


def detect_secrets(text: str) -> List[str]:
    """Detect potential leaked secrets matching known high-entropy token patterns."""
    found: List[str] = []
    for pattern in SECRET_VALUE_PATTERNS:
        matches = pattern.findall(text)
        found.extend(matches)
    return found


def sanitize_dict(data: Dict[str, Any], mask_known_keys: bool = True) -> Dict[str, Any]:
    """Recursively sanitizes sensitive values from configuration or log dictionaries."""
    sanitized: Dict[str, Any] = {}
    for k, v in data.items():
        is_sensitive = bool(mask_known_keys and KEY_REGEX.search(k))

        if isinstance(v, dict):
            sanitized[k] = sanitize_dict(v, mask_known_keys=mask_known_keys)
        elif is_sensitive:
            sanitized[k] = mask_secret(str(v))
        elif isinstance(v, str):
            # Check if value itself matches high confidence secret pattern
            detected = detect_secrets(v)
            if detected:
                masked_val = v
                for secret in detected:
                    masked_val = masked_val.replace(secret, mask_secret(secret))
                sanitized[k] = masked_val
            else:
                sanitized[k] = v
        else:
            sanitized[k] = v
    return sanitized
