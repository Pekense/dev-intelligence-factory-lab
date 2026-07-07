import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", "DEV")

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://dev_user:dev_password@localhost:5432/logistics_dev"
)

DASHBOARD_REFRESH_INTERVAL_SECONDS = int(
    os.getenv("DASHBOARD_REFRESH_INTERVAL_SECONDS", "60")
)
