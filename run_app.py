import subprocess
import sys

def run_weatherstats():
    print("Running WeatherStats (main.py)...")
    result = subprocess.run([sys.executable, "main.py"])

    if result.returncode != 0:
        print("WeatherStats failed. Exiting.")
        sys.exit(1)

def run_webapp():
    print("Starting Flask app...")
    subprocess.run([sys.executable, "web_app.py"])


if __name__ == "__main__":
    run_weatherstats()
    run_webapp()