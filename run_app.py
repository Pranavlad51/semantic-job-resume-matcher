#!/usr/bin/env python3
"""
run_app.py
Simple script to run the Streamlit app

Usage:
    python run_app.py
"""

import subprocess
import sys

if __name__ == "__main__":
    # Run streamlit app
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
