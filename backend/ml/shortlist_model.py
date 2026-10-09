import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

from db import applications_collection


# Get applications from MongoDB
applications = list(applications_collection.find())


if len(applications) < 10:
    print("Not enough data to train the model.")
    print("Please add at least 10 applications.")
    exit()


# Convert MongoDB data to DataFrame
df = pd.DataFrame(applications)


# Convert status into numerical target
df["target"] = df["status"].apply(
    lambda x: 1 if x == "Shortlisted" else 0
)


# Features
X = df[
    [
        "experience",
        "skills_match"
    ]
]


# Target
y = df["target"]


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Create model
model = LogisticRegression()


# Train
model.fit(X_train, y_train)


# Predict
y_pred = model.predict(X_test)


# Evaluation
accuracy = accuracy_score(y_test, y_pred)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)


print("\n===== Logistic Regression Results =====")

print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1 Score :", f1)