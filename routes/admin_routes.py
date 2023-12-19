from pymongo import MongoClient
import jwt
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv
from os.path import join, dirname
import os
from flask import Flask, render_template, jsonify, request, redirect, url_for,Blueprint
from flask_wtf.csrf import CSRFProtect, generate_csrf, validate_csrf
from validation.forms import Newsform,UpdateProjectsform, UpdateNewsform,Projectsform,UpdateUsersForm
from werkzeug.utils import secure_filename
from bson import ObjectId, json_util


admin_bp = Blueprint('admin', __name__)
SECRET_KEY=os.environ.get("SECRET_KEY")
MONGODB_URI=os.environ.get("MONGODB_URI")
DB_NAME=os.environ.get("DB_NAME")
TOKEN_KEY=os.environ.get("TOKEN_KEY")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]


# * Function Helper
def decode_token(payload):
    token = jwt.decode(payload, SECRET_KEY, algorithms=["HS256"])
    return token


def encode_token(payload):
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def save_image(file, file_type):
    time_now = datetime.now()
    time_str = time_now.strftime("%Y-%m-%d-%H-%M-%S")

    extention = file.filename.split(".")[-1]
    filename = f"assets/img/{file_type}/post-{time_str}.{extention}"
    file.save("./static/" +filename)

    return filename



# *************************************** Admin *****************************************


@admin_bp.route('/dashboard/admin')
def dashboard():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})

        if user_info and "role" in user_info and user_info["role"] == "admin":
            # Jika role adalah admin, kembalikan True
            return render_template('admin/index.html', user_info=user_info)
        else:
            # Jika role bukan admin, kembalikan False atau lakukan penanganan lainnya
            return redirect(url_for("client.index"))
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@admin_bp.route('/dashboard/admin/users')
def users_admin():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        
        return render_template('admin/table-users.html', user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@admin_bp.route('/dashboard/admin/news')
def news_admin():
    token_receive = request.cookies.get(TOKEN_KEY)
    form = Newsform()
    updateform = UpdateNewsform()
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        return render_template('admin/table-news.html', user_info=user_info, form=form, updateform=updateform)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@admin_bp.route('/dashboard/admin/project')
def project_admin():
    token_receive = request.cookies.get(TOKEN_KEY)
    form = Projectsform()
    updateform = UpdateProjectsform()
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        
        return render_template('admin/table-project.html',user_info=user_info,form=form,updateform=updateform)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@admin_bp.route('/dashboard/admin/donate')
def donate_admin():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        
        return render_template('admin/table-donate.html',user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@admin_bp.route('/dashboard/admin/profile')
def profile_admin():
    token_receive = request.cookies.get(TOKEN_KEY)
    form = UpdateUsersForm()
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        # Konversi ObjectId menjadi string
        user_info["_id"] = str(user_info["_id"])
        
        return render_template('admin/pages-profile.html',user_info=user_info, form=form)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))


@admin_bp.route('/dashboard/admin/mail')
def mail_admin():
    token_receive = request.cookies.get(TOKEN_KEY)
    try:
        payload = decode_token(token_receive)
        user_info = db.users.find_one({"username": payload.get("username")})
        # Konversi ObjectId menjadi string
        user_info["_id"] = str(user_info["_id"])
        
        return render_template('admin/mail.html',user_info=user_info)
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("client.index"))
