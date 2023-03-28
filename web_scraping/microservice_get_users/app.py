from dotenv import load_dotenv
from Scraper import Scraper

load_dotenv()
scraper = Scraper()

scraper.getUsersFromInstagram()