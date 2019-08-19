from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

SERVER_IP = os.environ.get("FMCSERVER_IP")
USERNAME = os.environ.get("FMCUSERNAME")
PASSWORD = os.environ.get("FMCPASSWORD")
GDOMAIN = os.environ.get("GlobalDOMAIN")
