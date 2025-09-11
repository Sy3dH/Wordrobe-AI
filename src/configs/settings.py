import os

from dotenv import load_dotenv

load_dotenv()

# Centralized environment variables
BFL_API_KEY = os.getenv("BFL_API_KEY")
FITROOM_API_KEY = os.getenv("FITROOM_API_KEY")

# Optional: Raise error if key is missing
if not BFL_API_KEY:
    raise RuntimeError("Missing BFL_API_KEY in environment variables.")

if not FITROOM_API_KEY:
    raise RuntimeError("Missing FITROOM_API_KEY in environment variables.")
