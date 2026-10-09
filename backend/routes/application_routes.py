from flask import Blueprint, request, jsonify
from bson import ObjectId
from db import applications_collection, jobs_collection, users_collection

application_routes = Blueprint("application_routes", __name__)


# CREATE APPLICATION
@application_routes.route("/api/applications", methods=["POST"])
def create_application():
    try:
        data = request.json

        # Check user
        user = users_collection.find_one({
            "_id": ObjectId(data["user_id"])
        })

        if not user:
            return jsonify({
                "message": "User not found"
            }), 404

        # Check job
        job = jobs_collection.find_one({
            "_id": ObjectId(data["job_id"])
        })

        if not job:
            return jsonify({
                "message": "Job not found"
            }), 404

        # Prevent duplicate application
        existing = applications_collection.find_one({
            "user_id": data["user_id"],
            "job_id": data["job_id"]
        })

        if existing:
            return jsonify({
                "message": "You have already applied for this job"
            }), 400

        application = {
            "user_id": data["user_id"],
            "job_id": data["job_id"],
            "experience": data.get("experience", 0),
            "education": data.get("education", ""),
            "skills_match": data.get("skills_match", 0),
            "status": "Applied"
        }

        result = applications_collection.insert_one(application)

        return jsonify({
            "message": "Application submitted successfully",
            "application_id": str(result.inserted_id)
        }), 201

    except Exception as error:
        return jsonify({
            "message": "Failed to submit application",
            "error": str(error)
        }), 400


# GET ALL APPLICATIONS
@application_routes.route("/api/applications", methods=["GET"])
def get_applications():
    try:
        applications = list(applications_collection.find())

        for application in applications:
            application["_id"] = str(application["_id"])

        return jsonify(applications), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch applications",
            "error": str(error)
        }), 500


# GET APPLICATIONS FOR A PARTICULAR JOB
@application_routes.route("/api/applications/job/<job_id>", methods=["GET"])
def get_job_applications(job_id):
    try:
        applications = list(
            applications_collection.find({
                "job_id": job_id
            })
        )

        for application in applications:
            application["_id"] = str(application["_id"])

        return jsonify(applications), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch applications",
            "error": str(error)
        }), 500


# UPDATE APPLICATION STATUS
@application_routes.route("/api/applications/<application_id>", methods=["PUT"])
def update_application(application_id):
    try:
        data = request.json

        result = applications_collection.update_one(
            {
                "_id": ObjectId(application_id)
            },
            {
                "$set": {
                    "status": data["status"]
                }
            }
        )

        if result.matched_count == 0:
            return jsonify({
                "message": "Application not found"
            }), 404

        return jsonify({
            "message": "Application status updated successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to update application",
            "error": str(error)
        }), 400