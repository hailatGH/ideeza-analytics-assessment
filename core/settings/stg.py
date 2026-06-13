from .common import *

DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",") if os.getenv("ALLOWED_HOSTS") else []