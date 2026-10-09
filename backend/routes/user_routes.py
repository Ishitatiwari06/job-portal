from flask import Blueprint, request, jsonify
from bson import ObjectId
from db import users_collection

user_routes = Blueprint("user_routes", __name__)


# CREATE USER
@user_routes.route("/api/users", methods=["POST"])
def create_user():
    try:
        data = request.json

        # Check whether email already exists
        existing_user = users_collection.find_one({
            "email": data.get("email")
        })

        if existing_user:
            return jsonify({
                "message": "Email already registered"
            }), 400

        result = users_collection.insert_one(data)

        return jsonify({
            "message": "User created successfully",
            "user_id": str(result.inserted_id)
        }), 201

    except Exception as error:
        return jsonify({
            "message": "Failed to create user",
            "error": str(error)
        }), 400


# GET ALL USERS
@user_routes.route("/api/users", methods=["GET"])
def get_users():
    try:
        users = list(users_collection.find())

        for user in users:
            user["_id"] = str(user["_id"])

        return jsonify(users), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch users",
            "error": str(error)
        }), 500


# GET USER BY ID
@user_routes.route("/api/users/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = users_collection.find_one({
            "_id": ObjectId(user_id)
        })

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        user["_id"] = str(user["_id"])

        return jsonify(user), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch user",
            "error": str(error)
        }), 400


# DELETE USER
@user_routes.route("/api/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        result = users_collection.delete_one({
            "_id": ObjectId(user_id)
        })

        if result.deleted_count == 0:
            return jsonify({
                "message": "User not found"
            }), 404

        return jsonify({
            "message": "User deleted successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to delete user",
            "error": str(error)
        }), 400