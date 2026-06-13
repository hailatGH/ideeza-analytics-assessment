import os

# Set a default settings module
env = os.getenv("DJANGO_ENV", "development")

if env == "production":
    from .prd import *  # noqa: F401, F403
elif env == "staging":
    from .stg import *  # noqa: F401, F403
else:
    from .dev import *  # noqa: F401, F403
