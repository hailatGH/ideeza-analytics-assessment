import os

# Set a default settings module
env = os.getenv("DJANGO_ENV", "development")

if env == "production":
    from .prd import *
elif env == "staging":
    from .stg import *
else:
    from .dev import *
