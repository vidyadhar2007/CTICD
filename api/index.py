import os
import sys

# Ensure root directory is accessible by Python on Vercel
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

# Vercel WSGI entrypoint
app = app
