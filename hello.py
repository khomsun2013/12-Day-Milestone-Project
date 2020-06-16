import os
from flask import Flask

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def hello():
	logging.debug("saying Hello")
    return 'Hello Heroku'