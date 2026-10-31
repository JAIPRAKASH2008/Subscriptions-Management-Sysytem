#!/usr/bin/env python
"""
Brightloop Entrypoint Runner
Execute: python run.py
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.app import app
from backend.config import Config

if __name__ == '__main__':
    print("=" * 70)
    print(" Brightloop Subscription Management System starting...")
    print(f" URL: http://127.0.0.1:{Config.PORT}")
    print("=" * 70)
    app.run(host='0.0.0.0', port=Config.PORT, debug=Config.DEBUG)

