from flask import Flask
from flaskConfig import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from dashboard import routes