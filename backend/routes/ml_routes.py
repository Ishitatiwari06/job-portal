
from flask import Blueprint, request, jsonify
import sys
import os
import pandas as pd

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from db import jobs_collection
from sklearn.linear_model import LinearRegression

ml_routes = Blueprint("ml_routes", __name__)


def train_salary_model():
    jobs = list(jobs_collection.find())
    records = []

    for job in jobs:
        salary = job.get("salary", {})
        experience = job.get("experience", {})
        skills = job.get("skills", [])

        if (
            isinstance(salary, dict)
            and "min" in salary
            and "max" in salary
            and isinstance(experience, dict)
        ):
            records.append({
                "experience": (
                    float(experience.get("min", 0))
                    + float(experience.get("max", 0))
                ) / 2,
                "skills_count": len(skills),
                "salary": (
                    float(salary["min"])
                    + float(salary["max"])
                ) / 2
            })

    if len(records) < 5:
        return None

    df = pd.DataFrame(records)

    X = df[["experience", "skills_count"]]
    y = df["salary"]

    model = LinearRegression()
    model.fit(X, y)

    return model


@ml_routes.route("/api/predict-salary", methods=["POST"])
def predict_salary():
    try:
        data = request.get_json()

        experience = float(data["experience"])
        skills_count = int(data["skills_count"])

        if experience < 0 or skills_count < 0:
            return jsonify({
                "error": "Experience and skills count must be non-negative."
            }), 400

        model = train_salary_model()

        if model is None:
            return jsonify({
                "error": "Add at least 5 jobs with valid salary and experience data."
            }), 400

        sample = pd.DataFrame([{
            "experience": experience,
            "skills_count": skills_count
        }])

        prediction = model.predict(sample)[0]

        return jsonify({
            "predicted_salary": round(float(prediction), 2),
            "currency": "INR",
            "message": "Salary predicted successfully"
        }), 200

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Provide numeric experience and skills_count."
        }), 400

    except Exception as error:
        return jsonify({
            "error": str(error)
        }), 500
