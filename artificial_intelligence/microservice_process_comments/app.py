from dotenv import load_dotenv
from helpers.variable_environments import validate_env_vars
from Model import CommentsProcessor
# Load environment variables
load_dotenv()

# Validate environment variables
there_are_env_vars = validate_env_vars()
if not there_are_env_vars:
    print("You have to stablished environment variables")
    print("1. POSTGRES_URL -> postgres url for database eg. postgresql://username:password@host:port/database")
    raise ImportError("Environment variables are needed.")

# Create a model object
model = CommentsProcessor()

# Start the Model for this microservice
try:
    model.process_comments()
except Exception as e:
    model.get_logger().critical(f"Error with the Model: {e.__str__()}")