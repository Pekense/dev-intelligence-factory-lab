import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")

DASHBOARD_REFRESH_INTERVAL_SECONDS = int(
    os.getenv("DASHBOARD_REFRESH_INTERVAL_SECONDS", "60")
)
