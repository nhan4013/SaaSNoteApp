import os
from dotenv import load_dotenv


load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

print("here my key ",os.getenv("SECRET_KEY"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM","HS256")

SQLALCHEMY_DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URL",
    "postgresql://postgres:123@localhost:5433/note_db"
)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
NOTES_CHANNEL = os.getenv("NOTES_CHANNEL", "notes_channel")
TAGS_CHANNEL = os.getenv("TAGS_CHANNEL", "tags_channel")

