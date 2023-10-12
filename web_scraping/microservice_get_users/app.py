from dotenv import load_dotenv
from Scraper import ScraperGetUsers
from helpers.variable_environments import validate_env_vars
# Load environment variables
load_dotenv()

# Validate environment variables
there_are_env_vars = validate_env_vars()
if not there_are_env_vars:
    print("You have to stablish environment variables")
    print("1. IG_USERNAME  -> Instagram username for login")
    print("2. IG_PASSWORD  -> Instagram password for login")
    print("3. POSTGRES_URL -> postgres url for database eg. postgresql://username:password@host:port/database")
    raise ImportError("Environment variables are needed.")

# Create a scraper object
scraper = ScraperGetUsers()
try:
    # Start the scraper
    scraper.get_users()
except Exception as e:
    scraper.get_logger().critical("""
        There is a problem with scraping.
        It could be:
        1. The Instagram credentials are wrong.
        2. The database is down.
        3. The internet is down.
        4. The scraper is not working.
        5. The Web Drives is not working due it is not updated. (The versions between the Google Chrome and the Web Driver have to be the same)
        For the 4 problem you can try to fix it by following the steps below:
            * Check if the tag elements are being taken correctly.
        If you have any questions, please contact me.
        Email: carrillobaronj@gmail.com
    """)
    scraper.get_logger().critical(e)    