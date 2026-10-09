
import sys
import os

# Allow Python to find backend/db.py
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

from db import jobs_collection


# Fetch jobs from MongoDB
jobs = list(jobs_collection.find())

if len(jobs) < 5:
    print("Not enough jobs to train the model.")
    print("Please add at least 5 jobs.")
    sys.exit()


# Prepare the dataset
records = []

for job in jobs:
    salary = job.get("salary", {})

    if isinstance(salary, dict) and "min" in salary and "max" in salary:
        experience = job.get("experience", {})

        if isinstance(experience, dict):
            min_exp = experience.get("min", 0)
            max_exp = experience.get("max", 0)

            records.append({
                "experience": (min_exp + max_exp) / 2,
                "skills_count": len(job.get("skills", [])),
                "salary": (salary["min"] + salary["max"]) / 2
            })


df = pd.DataFrame(records)

if len(df) < 5:
    print("Not enough jobs with valid salary and experience data.")
    sys.exit()


X = df[["experience", "skills_count"]]
y = df["salary"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

r2 = r2_score(y_test, predictions)
mae = mean_absolute_error(y_test, predictions)


print("\n===== Linear Regression Results =====")
print("R² Score:", round(r2, 3))
print("MAE:", round(mae, 2))


# Example salary prediction
sample = pd.DataFrame([{
    "experience": 2,
    "skills_count": 4
}])

predicted_salary = model.predict(sample)[0]

print("\nExample Salary Prediction")
print("Experience: 2 years")
print("Skills: 4")
print("Predicted Salary: ₹", round(predicted_salary, 2))
