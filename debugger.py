from flask import Blueprint, jsonify
from tabulate import tabulate
from Models.user import User
from Models.log import Log 

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from main import db

debugger = Blueprint('debugger', __name__)


@debugger.route("/getLogs", methods=["GET", "POST"])
def getLogs():
    """gets all logs in the system for debugging purpose"""

    logs = Log.query.all()
    logs_table = []

    for log in logs:
        logs_table.append([log.id, log.username, log.unlocking_method, log.date_time])

    return "<pre>" + tabulate(logs_table, headers=["ID","Username", "Unlocking Method", "Unlocking Date/Time"])  + "</pre>"


@debugger.route("/getUsers", methods=["GET", "POST"])
def getUsers():
    """gets all users in the system for debugging purpose"""

    users = User.query.all()
    users_table = []

    for user in users:
        users_table.append([user.id, user.public_id, user.username, user.password, user.phone, user.address])

    return "<pre>" + tabulate(users_table, headers=["ID", "Public ID", "Username", "Password", "Phone", "Address"]) + "</pre>"