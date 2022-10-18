import sys
from os import path
from dotenv import load_dotenv


def build_env(cur_path: str):
    root_path = path.abspath(path.join(cur_path, '../..'))
    sys.path.append(root_path)
    load_dotenv(dotenv_path=path.join(root_path, '.env'))
    load_dotenv(dotenv_path=path.join(root_path, '.env.prod'))
