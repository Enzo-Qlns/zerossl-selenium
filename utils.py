from config import settings


def get_env() -> str:
    """
    Get the current environment
    :return: str
    """
    return settings.APP_ENV


def is_dev() -> bool:
    """
    Check if the current environment is development
    :return: bool
    """
    return get_env() == 'dev'


def get_api_url() -> str:
    """
    Get the API URL based on the current environment
    :return: str
    """
    return "http://localhost:8000" if get_env() == 'dev' else "https://api.enzoquelenis.fr"
