from dotenv import load_dotenv
from Scraper import Scraper

# Load environment variables
load_dotenv()

# Create a scraper object
scraper = Scraper()

# Start the scraper
scraper.getUsersFromInstagram()