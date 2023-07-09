from dotenv import load_dotenv
from Scraper import Scraper

# Load environment variables
load_dotenv()

# Create a scraper object
scraper = Scraper()

# Start the scraper
try:  
  scraper.follow_new_people()
except Exception as e:
  scraper.get_logger().critical(f"Error with the Scraper {e.__str__()}")