from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from Models.user import User
import uuid

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from main import db

auth = Blueprint('auth', __name__)


def verify_user_data(data, keys_to_verify):
    """verifies that a list of keys exist in the JSON data and :returns a list of missing keys"""
    missing_kays = []

    # verify JSON data
    for key in keys_to_verify:
        try:
            data[key]
        except KeyError:
            missing_kays.append(key)

    return missing_kays


def check_password_strength(password):
    """:returns False if the password doesn't follow the password policy, True otherwise."""
    # Policy:
    # Minimum length of 8 characters
    if len(list(password)) < 8:
        return False
    return True


@auth.route("/register", methods=["GET", "POST"])
def signup_user():
    """handles the user registration process"""
    # get JSON data from request
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"msg": "Invalid JSON format"}), 400

    # verify JSON data
    missing_data = verify_user_data(data, keys_to_verify=["username", "password", "email", "phone", "address"])
    if len(missing_data) > 0:
        return jsonify({
            "msg": "Missing " + ", ".join(missing_data)
        }), 400

    # check if user exists
    if User.query.filter_by(username=data["username"]).first() is not None:
        return jsonify({
            "msg": "User already exists"
        }), 400

    # check password strength
    if not check_password_strength(data["password"]):
        return jsonify({
            "msg": "Weak password"
        }), 400

    # hash the password
    hashed_password = generate_password_hash(data["password"], method="sha256")

    # add user to the database
    new_user = User(
        public_id=str(uuid.uuid4()),
        username=data["username"], 
        password=hashed_password,
        email=data["email"],
        phone=data["phone"],
        address=data["address"]
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User registered successfully"})


@auth.route("/login", methods=["GET", "POST"])
def login_user():
    """handles the user authentication process"""
    # get JSON data from request
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"msg": "Invalid JSON format"}), 400
        
    # verify JSON data
    missing_data = verify_user_data(data, keys_to_verify=["username", "password"])
    if len(missing_data) > 0:
        return jsonify({
            "msg": "Missing " + ", ".join(missing_data)
        }), 400

    user = User.query.filter_by(username=data["username"]).first()
    # user doesn't exist
    if user is None:
        return jsonify({"msg": "Invalid username or password"}), 401
    # return access token if logged in successfully
    if check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.public_id)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Invalid username or password"}), 401

