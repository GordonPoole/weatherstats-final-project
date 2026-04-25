from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session, jsonify
from pathlib import Path
import json
import pandas as pd

from weatherstats import DatasetPaths, WeatherApp
from weatherstats.ml_model import train_model, predict
from weatherstats.dashboard_visualization import (
    make_temperature_chart,
    make_rainfall_chart,
    make_extreme_chart
)
from db import db, SearchHistory

app = Flask(__name__)
app.secret_key = "change_this_weather_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)

with app.app_context():
    db.create_all()

ROOT = Path(__file__).resolve().parent
TRAIN = ROOT / "data_sets" / "Weather Training Data.csv"
TEST = ROOT / "data_sets" / "Weather Test Data.csv"

CHART_FOLDER = ROOT / "outputs" / "charts"

print("Training ML model...")
MODEL, FEATURES = train_model(TRAIN)
print("Model ready!")


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "wrongpassword":
            session["user"] = username
            return redirect(url_for("upload"))
        else:
            error = "Invalid username or password"

    return render_template("login.html", error=error)


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if "user" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        file = request.files["file"]

        if file:
            upload_path = ROOT / "uploaded_weather.csv"
            file.save(upload_path)
            session["uploaded_file"] = str(upload_path)

            return redirect(url_for("dashboard"))

    return render_template("upload.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    if "uploaded_file" in session:
        active_file = Path(session["uploaded_file"])
    else:
        active_file = TRAIN

    cities = []

    try:
        df = pd.read_csv(active_file)

        if "Location" in df.columns:
            cities = sorted(df["Location"].dropna().unique().tolist())

    except Exception:
        cities = []

    return render_template("index.html", cities=cities)


@app.route("/city_insights")
def city_insights():
    if "user" not in session:
        return jsonify({})

    if "uploaded_file" in session:
        active_file = Path(session["uploaded_file"])
    else:
        active_file = TRAIN

    city = request.args.get("city", "")

    df = pd.read_csv(active_file)
    city_df = df[df["Location"] == city].copy()

    numeric_cols = [
        "MinTemp",
        "MaxTemp",
        "Rainfall",
        "Humidity3pm"
    ]

    for col in numeric_cols:
        city_df[col] = pd.to_numeric(city_df[col], errors="coerce")

    city_df = city_df.dropna(subset=numeric_cols)

    data = {
        "observations": int(len(city_df)),
        "avg_min_temp": float(round(city_df["MinTemp"].mean(), 1)),
        "avg_max_temp": float(round(city_df["MaxTemp"].mean(), 1)),
        "max_temp": float(round(city_df["MaxTemp"].max(), 1)),
        "min_temp": float(round(city_df["MinTemp"].min(), 1)),
        "avg_rainfall": float(round(city_df["Rainfall"].mean(), 1)),
        "max_rainfall": float(round(city_df["Rainfall"].max(), 1)),
        "avg_humidity": float(round(city_df["Humidity3pm"].mean(), 1))
    }

    return jsonify(data)


@app.route("/generate_chart/<chart_type>")
def generate_chart(chart_type):
    if "user" not in session:
        return redirect(url_for("login"))

    if "uploaded_file" in session:
        active_file = Path(session["uploaded_file"])
    else:
        active_file = TRAIN

    city = request.args.get("city", "")

    df = pd.read_csv(active_file)

    outpath = CHART_FOLDER / "live_chart.png"

    if chart_type == "temp":
        make_temperature_chart(df, city, outpath)

    elif chart_type == "rain":
        make_rainfall_chart(df, city, outpath)

    elif chart_type == "extreme":
        make_extreme_chart(df, city, outpath)

    return send_from_directory(CHART_FOLDER, "live_chart.png")


@app.route("/summary")
def summary():
    if "user" not in session:
        return redirect(url_for("login"))

    if "uploaded_file" in session:
        active_file = Path(session["uploaded_file"])
    else:
        active_file = TRAIN

    app_logic = WeatherApp(
        datasets=DatasetPaths(train=active_file, test=TEST),
        outdir=ROOT / "outputs"
    )

    app_logic.run(preview_rows=10)

    summary_file = ROOT / "outputs" / "summary_preview.json"

    data = {}
    if summary_file.exists():
        with open(summary_file, "r", encoding="utf-8") as f:
            data = json.load(f)

    entry = SearchHistory(action="Viewed Summary")
    db.session.add(entry)
    db.session.commit()

    return render_template("summary.html", data=data)


@app.route("/history")
def history():
    if "user" not in session:
        return redirect(url_for("login"))

    records = (
        SearchHistory.query
        .order_by(SearchHistory.timestamp.desc())
        .limit(20)
        .all()
    )

    return render_template("history.html", records=records)


@app.route("/charts")
def charts():
    if "user" not in session:
        return redirect(url_for("login"))

    if "uploaded_file" in session:
        active_file = Path(session["uploaded_file"])
    else:
        active_file = TRAIN

    app_logic = WeatherApp(
        datasets=DatasetPaths(train=active_file, test=TEST),
        outdir=ROOT / "outputs"
    )

    app_logic.run(preview_rows=10)

    images = [f.name for f in CHART_FOLDER.glob("*.png")]

    return render_template("charts.html", images=images)


@app.route("/charts/<filename>")
def chart_file(filename):
    if "user" not in session:
        return redirect(url_for("login"))

    return send_from_directory(CHART_FOLDER, filename)


@app.route("/predict", methods=["GET", "POST"])
def predict_route():
    if "user" not in session:
        return redirect(url_for("login"))

    result = None

    if request.method == "POST":
        try:
            data = [
                float(request.form["MinTemp"]),
                float(request.form["MaxTemp"]),
                float(request.form["Rainfall"]),
                float(request.form["Humidity3pm"]),
                float(request.form["Pressure3pm"]),
            ]

            result = predict(MODEL, FEATURES, data)

        except Exception as e:
            result = f"Error: {e}"

    return render_template("predict.html", result=result)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=False)