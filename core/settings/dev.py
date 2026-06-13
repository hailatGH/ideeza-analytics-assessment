from .common import *

# For development, we default to DEBUG=True if not specified in .env
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "0.0.0.0,localhost,127.0.0.1").split(",")