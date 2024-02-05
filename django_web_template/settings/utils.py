import os

import environ


# Build paths inside the project like this: BASE_DIR / 'subdir'.
def get_env():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    env = environ.Env()
    environ.Env.read_env()
    return env
