from config import settings


def get_env() -> str:
    """
    Get the current environment
    :return:
    """
    return settings.APP_ENV


def is_dev() -> bool:
    """
    Check if the current environment is development
    :return:
    """
    return get_env() == 'dev'
