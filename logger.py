from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from data_verifier import verify_user_data
from Models.user import User
from Models.log import Log 

import sys, os
sys.path.append(os.path.abspath(os.path.join('..')))
from main import db

logger = Blueprint('logger', __name__)


@logger.route("/logUnlocking", methods=["POST"])
@jwt_required()
def logUnlocking():
    """Logs unlocking process done by one of the clients"""

    # get JSON data from request
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"msg": "Invalid JSON format"}), 400

    # verify JSON data
    missing_data = verify_user_data(data, keys_to_verify=["unlocking-method"])
    if len(missing_data) > 0:
        return jsonify({
            "msg": "Missing " + ", ".join(missing_data)
        }), 400
    
    # get username from the jwt token
    public_id = get_jwt_identity()
    user = User.query.filter_by(public_id=public_id).first()
    if user is None:
        return jsonify({
            "msg": "There is an error with this token"
        }), 400

    # add log to the database
    new_log = Log(
        username=user.username, 
        unlocking_method=data["unlocking-method"],
    )
    db.session.add(new_log)
    db.session.commit()

    return jsonify({"msg": "Unlocking process logged successfully"})

