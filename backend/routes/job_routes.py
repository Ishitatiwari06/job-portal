from flask import Blueprint, request, jsonify
from bson import ObjectId
from db import jobs_collection

job_routes = Blueprint("job_routes", __name__)


# CREATE JOB
@job_routes.route("/api/jobs", methods=["POST"])
def create_job():
    try:
        data = request.json

        result = jobs_collection.insert_one(data)

        return jsonify({
            "message": "Job created successfully",
            "job_id": str(result.inserted_id)
        }), 201

    except Exception as error:
        return jsonify({
            "message": "Failed to create job",
            "error": str(error)
        }), 400


# GET ALL JOBS
@job_routes.route("/api/jobs", methods=["GET"])
def get_jobs():
    try:
        jobs = list(jobs_collection.find())

        for job in jobs:
            job["_id"] = str(job["_id"])

        return jsonify(jobs), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch jobs",
            "error": str(error)
        }), 500


# GET JOB BY ID
@job_routes.route("/api/jobs/<job_id>", methods=["GET"])
def get_job(job_id):
    try:
        job = jobs_collection.find_one({
            "_id": ObjectId(job_id)
        })

        if not job:
            return jsonify({
                "message": "Job not found"
            }), 404

        job["_id"] = str(job["_id"])

        return jsonify(job), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to fetch job",
            "error": str(error)
        }), 400


# UPDATE JOB
@job_routes.route("/api/jobs/<job_id>", methods=["PUT"])
def update_job(job_id):
    try:
        data = request.json

        result = jobs_collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": data}
        )

        if result.matched_count == 0:
            return jsonify({
                "message": "Job not found"
            }), 404

        return jsonify({
            "message": "Job updated successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to update job",
            "error": str(error)
        }), 400


# DELETE JOB
@job_routes.route("/api/jobs/<job_id>", methods=["DELETE"])
def delete_job(job_id):
    try:
        result = jobs_collection.delete_one({
            "_id": ObjectId(job_id)
        })

        if result.deleted_count == 0:
            return jsonify({
                "message": "Job not found"
            }), 404

        return jsonify({
            "message": "Job deleted successfully"
        }), 200

    except Exception as error:
        return jsonify({
            "message": "Failed to delete job",
            "error": str(error)
        }), 400