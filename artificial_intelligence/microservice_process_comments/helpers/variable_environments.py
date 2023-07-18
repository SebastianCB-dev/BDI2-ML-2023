import os

def validate_env_vars():
    """
    Validates the existence of required environment variables.
    
    Returns:
        bool: True if all required environment variables are set, False otherwise.
    """
    required_vars = ["POSTGRES_URL"]
    for var in required_vars:
        if not os.getenv(var):
            return False

    return True