"""
Command-line interface for EnvShield secret auditing.
"""

import argparse
import os
import sys
from .sanitizer import detect_secrets


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="envshield",
        description="Audit files and environment definitions for accidental secret exposure.",
    )
    parser.add_argument("path", help="Path to file or directory to scan for secrets", default=".")
    args = parser.parse_args()

    target = args.path
    if not os.path.exists(target):
        print(f"Error: Path '{target}' does not exist.", file=sys.stderr)
        return 1

    findings = 0
    if os.path.isfile(target):
        files_to_scan = [target]
    else:
        files_to_scan = []
        for root, _, files in os.walk(target):
            if ".git" in root:
                continue
            for f in files:
                files_to_scan.append(os.path.join(root, f))

    print(f"EnvShield scanning {len(files_to_scan)} file(s)...")
    for file_path in files_to_scan:
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                secrets = detect_secrets(content)
                if secrets:
                    findings += len(secrets)
                    print(f"⚠️  Detected {len(secrets)} potential secret(s) in {file_path}")
        except Exception as e:
            print(f"Could not read {file_path}: {e}", file=sys.stderr)

    if findings > 0:
        print(f"\n❌ Scan failed: {findings} sensitive item(s) found.")
        return 1

    print("\n✅ Clean! No leaked secrets detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
