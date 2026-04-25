import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


def train_model(csv_path):
    df = pd.read_csv(csv_path)

    features = [
        "MinTemp",
        "MaxTemp",
        "Rainfall",
        "Humidity3pm",
        "Pressure3pm"
    ]

    df = df[features + ["RainTomorrow"]]

    # Ensure numeric features
    df[features] = df[features].apply(pd.to_numeric, errors="coerce")

    df = df.dropna(subset=["RainTomorrow"])

    # Fill missing feature values
    df[features] = df[features].fillna(df[features].mean())

    if len(df) == 0:
        raise ValueError("Dataset is empty after preprocessing")

    X = df[features]
    y = df["RainTomorrow"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2
    )

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    return model, features


def predict(model, features, input_data):
    df = pd.DataFrame([input_data], columns=features)
    prediction = model.predict(df)[0]
    return "Rain" if prediction == 1 else "No Rain"