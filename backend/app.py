from flask import Flask, jsonify
from db import client
from routes.job_routes import job_routes

app = Flask(__name__)

app.register_blueprint(job_routes)


@app.route("/")
def home():
    return jsonify({
        "message": "Job Portal Backend is running"
    })


@app.route("/test-db")
def test_db():
    try:
        client.admin.command("ping")

        return jsonify({
            "message": "MongoDB connection successful"
        })

    except Exception as error:
        return jsonify({
            "message": "MongoDB connection failed",
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)