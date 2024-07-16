from dotenv import load_dotenv
from pathlib import Path
import os
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

def get_env(key):
	return os.environ.get(key)
