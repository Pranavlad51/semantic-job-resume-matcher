#!/usr/bin/env python3
"""
run_tests.py
Script to run all tests

Usage:
    python run_tests.py
"""

import pytest
import sys

if __name__ == "__main__":
    # Run pytest with verbose output
    exit_code = pytest.main([
        "tests/",
        "-v",
        "--tb=short",
        "--color=yes"
    ])
    sys.exit(exit_code)
