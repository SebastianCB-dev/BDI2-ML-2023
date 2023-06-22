import platform


def get_platform():
    # This function gets the platform of the system (Windows, Linux, Mac)
    return platform.system()


def is_darwin_arm_validator():
    """
    Validates if the current platform is Darwin and ARM architecture.

    Returns:
        bool: True if the platform is Darwin and ARM, False otherwise.
    """
    return platform.machine().startswith('arm')
