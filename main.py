from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from dotenv import load_dotenv
import datetime
import os

load_dotenv() # Loads the environment vars from .env file
app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI") 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
app.config["JWT_IDENTITY_CLAIM"] = "public_id"

db = SQLAlchemy(app)
jwt = JWTManager(app)

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from logger import logger as logger_blueprint
app.register_blueprint(logger_blueprint)

print(os.getenv("DEBUG"))
if os.getenv("DEBUG") == "True":
    from debugger import debugger as debugger_blueprint
    app.register_blueprint(debugger_blueprint)


# Configure Limiter
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"] # [count] [per|/] [n (optional)] [second|minute|hour|day|month|year][s]
)
limiter.limit("10/hour;5/minute;1/second")(auth_blueprint)
limiter.limit("10/hour;5/minute;1/second")(logger_blueprint)


# Change hit ratelimit response message
@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(jsonify(error="ratelimit exceeded") , 429)
    
