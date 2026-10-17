
from flask import Blueprint, request, jsonify
import sys
import os
import pandas as pd

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from db import jobs_collection
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from db import applications_collection

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

@ml_routes.route("/api/predict-shortlist", methods=["POST"])
def predict_shortlist():
    try:
        data = request.get_json()

        experience = float(data["experience"])
        skills_match = float(data["skills_match"])

        if experience < 0 or not 0 <= skills_match <= 100:
            return jsonify({
                "error": "Experience must be non-negative and skills match must be between 0 and 100."
            }), 400

        records = list(applications_collection.find({
            "experience": {"$exists": True},
            "skills_match": {"$exists": True},
            "status": {"$exists": True}
        }))

        X = []
        y = []

        for record in records:
            try:
                exp = float(record["experience"])
                match = float(record["skills_match"])
                status = str(record["status"]).strip().lower()

                X.append([exp, match])
                y.append(1 if status == "shortlisted" else 0)
            except (ValueError, TypeError):
                continue

        if len(X) < 4 or len(set(y)) < 2:
            return jsonify({
                "error": "Not enough valid application data. Add applications with both Shortlisted and non-Shortlisted statuses."
            }), 400

        model = LogisticRegression()
        model.fit(X, y)

        sample = pd.DataFrame([{
            "experience": experience,
            "skills_match": skills_match
        }])

        prediction = int(model.predict(sample)[0])
        probability = float(model.predict_proba(sample)[0][1])

        return jsonify({
            "prediction": (
                "Shortlisted" if prediction == 1
                else "Not Shortlisted"
            ),
            "shortlist_probability": round(probability * 100, 2),
            "message": "Prediction generated successfully"
        })

    except (KeyError, TypeError, ValueError):
        return jsonify({
            "error": "Please provide valid experience and skills_match values."
        }), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500