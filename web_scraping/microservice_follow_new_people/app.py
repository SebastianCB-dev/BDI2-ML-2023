from dotenv import load_dotenv
from Scraper import Scraper

# Load environment variables
load_dotenv()

# Create a scraper object
scraper = Scraper()

# Start the scraper
try:  
  scraper.getUsersFromInstagram()
except Exception as e:
  scraper.getLogger().critical(f"Error with the Scraper {e.__str__()}")