
import os
from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'Act-shortener Swagger API',
    'uiversion': 3
}
swagger = Swagger(app)
app.config.from_object('shortener.config')
app.url_map.strict_slashes = False

from shortener.views import *
