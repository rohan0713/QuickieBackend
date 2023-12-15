from dotenv import load_dotenv, find_dotenv
import os
import urllib.parse
from pymongo import MongoClient

load_dotenv(find_dotenv())

username = urllib.parse.quote_plus(os.environ.get('MONGODB_USER'))
password = urllib.parse.quote_plus(os.environ.get('MONGODB_PWD'))
URL = os.environ.get('MONGODB_URL')

CONNECTION_STRING = URL % (username, password)
client = MongoClient(CONNECTION_STRING)