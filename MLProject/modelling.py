# Import library yang digunakan
import pandas as pd
import mlflow
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Set experiment MLflow
mlflow.set_experiment("Banknote Experiment")

# Load dataset
df = pd.read_csv("banknote_preprocessing.csv")
X = df.drop(columns="class")
y = df["class"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# GridSearch untuk tuning SVM
param_grid = {
    "C": [0.1, 1, 10],
    "kernel": ["linear", "rbf"],
    "gamma": ["scale", "auto"]
}

grid = GridSearchCV(SVC(), param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid.fit(X_train, y_train)

# Evaluasi model
best_model = grid.best_estimator_
y_pred = best_model.predict(X_test)

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred)
rec = recall_score(y_test, y_pred)

with mlflow.start_run():
    mlflow.log_param("best_C", grid.best_params_["C"])
    mlflow.log_param("kernel", grid.best_params_["kernel"])
    mlflow.log_param("gamma", grid.best_params_["gamma"])

    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("precision", prec)
    mlflow.log_metric("recall", rec)