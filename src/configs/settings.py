import os

from dotenv import load_dotenv

load_dotenv()

# Centralized environment variables
BFL_API_KEY = os.getenv("BFL_API_KEY")
FITROOM_API_KEY = os.getenv("FITROOM_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ARIZE_API_KEY = os.getenv("ARIZE_API_KEY")

# Optional: Raise error if key is missing
if not BFL_API_KEY:
    raise RuntimeError("Missing BFL_API_KEY in environment variables.")

# Optional: Raise error if key is missing
if not FITROOM_API_KEY:
    raise RuntimeError("Missing FITROOM_API_KEY in environment variables.")

# Optional: Raise error if key is missing
if not GOOGLE_API_KEY:
    raise RuntimeError("Missing GOOGLE_API_KEY in environment variables.")

# Optional: Raise error if key is missing
if not ARIZE_API_KEY:
    raise RuntimeError("Missing ARIZE_API_KEY in environment variables.")