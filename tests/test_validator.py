import unittest
from envshield.validator import EnvSchema, Field, ValidationError


class TestEnvValidator(unittest.TestCase):
    def setUp(self):
        self.schema = EnvSchema(
            {
                "PORT": Field(field_type=int, default=8000),
                "DEBUG": Field(field_type=bool, default=False),
                "DATABASE_URL": Field(
                    field_type=str,
                    required=True,
                    validator=lambda s: s.startswith("postgresql://"),
                ),
                "API_TIMEOUT": Field(field_type=float, default=5.0),
            }
        )

    def test_valid_environment(self):
        env = {
            "PORT": "3000",
            "DEBUG": "true",
            "DATABASE_URL": "postgresql://localhost:5432/db",
        }
        res = self.schema.validate(env)
        self.assertEqual(res["PORT"], 3000)
        self.assertTrue(res["DEBUG"])
        self.assertEqual(res["DATABASE_URL"], "postgresql://localhost:5432/db")
        self.assertEqual(res["API_TIMEOUT"], 5.0)

    def test_missing_required_field(self):
        env = {"PORT": "8080"}
        with self.assertRaises(ValidationError) as ctx:
            self.schema.validate(env)
        self.assertIn("DATABASE_URL", ctx.exception.errors)

    def test_invalid_type_conversion(self):
        env = {
            "PORT": "invalid-port",
            "DATABASE_URL": "postgresql://localhost:5432/db",
        }
        with self.assertRaises(ValidationError) as ctx:
            self.schema.validate(env)
        self.assertIn("PORT", ctx.exception.errors)

    def test_failed_custom_validator(self):
        env = {
            "DATABASE_URL": "mysql://localhost:3306/db",
        }
        with self.assertRaises(ValidationError) as ctx:
            self.schema.validate(env)
        self.assertIn("DATABASE_URL", ctx.exception.errors)


if __name__ == "__main__":
    unittest.main()
