"""Syntax check for all generated files."""
import ast
import sys

files = [
    "src/analyzer/base.py",
    "src/analyzer/ocr_analyzer.py",
    "src/analyzer/amount_extractor.py",
    "src/analyzer/payment_detector.py",
    "src/analyzer/__init__.py",
    "tests/test_analyzer/test_ocr_analyzer.py",
    "tests/test_analyzer/test_amount_extractor.py",
    "tests/test_analyzer/test_payment_detector.py",
]

errors = []
for f in files:
    try:
        with open(f, encoding="utf-8") as fh:
            ast.parse(fh.read())
        print(f"OK: {f}")
    except SyntaxError as e:
        errors.append(f"SYNTAX ERROR in {f}: {e}")
        print(f"FAIL: {f} - {e}")

if errors:
    print(f"\n{len(errors)} file(s) have syntax errors")
    sys.exit(1)
else:
    print(f"\nAll {len(files)} files syntax OK")
