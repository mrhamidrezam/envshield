# 🛡️ EnvShield

> **Zero-dependency environment configuration validator & secret exposure sanitizer for Python.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

EnvShield prevents bad configurations from crashing your production applications and protects sensitive credentials from accidental leakage into logs or dashboards.

---

## ✨ Features

- **Schema Validation**: Define types, required fields, and custom validators for environment variables.
- **Secret Masking & Sanitization**: Automatically mask sensitive keys (API tokens, passwords, credentials) in nested dictionaries before logging.
- **Pattern Detection**: Detects common high-entropy credentials (GitHub PATs, JWTs, AWS Keys, etc.).
- **Zero Dependencies**: Pure Python standard library with fast startup and no external bloat.

---

## 🚀 Quickstart

### 1. Schema Validation

```python
import os
from envshield import EnvSchema, Field, ValidationError

schema = EnvSchema({
    "PORT": Field(field_type=int, default=8000),
    "DEBUG": Field(field_type=bool, default=False),
    "DATABASE_URL": Field(
        field_type=str,
        required=True,
        validator=lambda s: s.startswith("postgresql://")
    ),
})

try:
    config = schema.validate(os.environ)
    print(f"Server configured on port {config['PORT']}")
except ValidationError as e:
    print(e)
```

### 2. Sanitize Dictionaries & Logs

```python
from envshield import sanitize_dict

raw_request = {
    "user_id": 42,
    "api_key": "sk-1234567890abcdef1234567890abcdef",
    "meta": {"password": "supersecretpassword"}
}

safe_request = sanitize_dict(raw_request)
# safe_request['api_key'] is masked: 'sk...ef'
# safe_request['meta']['password'] is masked: 'su...rd'
```

---

## 🧪 Running Tests

```bash
python -m pytest
```

---

## 📄 License

MIT License. Copyright (c) Hamidreza.
