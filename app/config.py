import os
from dotenv import load_dotenv
import sentry_sdk

load_dotenv()

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Sentry Configuration
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    # Add data like request headers and IP for users,
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
    # Enable sending logs to Sentry
    enable_logs=True,
    # Capture 100% of transactions for tracing
    traces_sample_rate=1.0,
    # Set profile_session_sample_rate to 1.0 to profile 100% of profile sessions.
    profile_session_sample_rate=1.0,
    # Set environment
    environment=os.getenv("ENVIRONMENT", "development")
)