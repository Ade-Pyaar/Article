from flask import Flask
from decouple import config
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


app.config["SECRET_KEY"] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)




from article_query import routes