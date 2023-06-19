from dotenv import load_dotenv
from Scraper import Scraper
from helpers.variable_environments import validate_env_vars
# Load environment variables
load_dotenv()

# Validate environment variables
there_are_env_vars = validate_env_vars()
if not there_are_env_vars:
    print("You have to stablished environment variables")
    print("1. IG_USERNAME  -> Instagram username for login")
    print("2. IG_PASSWORD  -> Instagram password for login")
    print("3. POSTGRES_URL -> postgres url for database eg. postgresql://username:password@host:port/database")
    raise ImportError("Environment variables are needed.")

# Create a scraper object
scraper = Scraper()

# Start the scraper
try:
    scraper.get_users()
except Exception as e:
    scraper.get_logger().critical(f"Error with the Scraper {e.__str__()}")    