from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv
from os.path import join, dirname
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from bson import ObjectId, json_util
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.client_routes import client_bp
from routes.api_routes import api_bp



# ************************* Variable & Key *****************************
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


# * config flask
app = Flask(__name__, template_folder='templates')
csrf = CSRFProtect(app)

app.config.from_mapping(
    SECRET_KEY=os.environ.get("SECRET_KEY"),
    TEMPLATE_AUTO_RELOAD=True,
    UPLOAD_FOLDER=["./static/assets/img/news",
                   "./static/assets/img/projects", "./static/assets/img/users"],
)

# * Connect database

app.register_blueprint(auth_bp)
app.register_blueprint(client_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(api_bp)



# *********************************************** Error Page *********************************************
# Handler untuk kesalahan server internal (500)
@app.errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html'), 500
# Handler untuk kesalahan server internal (404)
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error/404.html'), 404



if __name__ == '__main__':
    app.run(debug=True)
