import os

from dotenv import load_dotenv

root_path = os.path.abspath(os.path.dirname(__file__)).split('applications')[0]
# dot_env_path = os.path.join(root_path, '.env')
flask_env_path = os.path.join(root_path, '.flaskenv')

# if os.path.exists(dot_env_path):
#     load_dotenv(dot_env_path)


def init_dotenv():
    if os.path.exists(flask_env_path):
        load_dotenv(flask_env_path)
