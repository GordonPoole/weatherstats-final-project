# WeatherStats Final Project

Username: admin
Password: wrongpassword

## Overview

WeatherStats is a Python web application designed to analyze and visualize Australian weather data through an interactive browser dashboard. The system allows authenticated users to securely log in, upload CSV weather datasets, and explore city level insights using live charts, dynamic filtering, and real time weather metrics.

This project was developed to demonstrate advanced Python programming, modular software architecture, interactive web development, secure authentication, data analytics, and iterative software refinement over multiple weeks.

---

## Purpose of the Application

WeatherStats transforms raw CSV weather data into clear visual insights through an easy-to-use dashboard.

Users can explore:

- Temperature behavior
- Rainfall patterns
- Extreme weather conditions
- City level comparisons
- Real time metrics

---

## Core Features

- Secure login system
- Protected routes
- CSV upload support
- Interactive dashboard
- Dynamic city filtering
- Live chart generation
- Real time metrics table
- Machine learning extension

---

## System Architecture

### Frontend

HTML, CSS, JavaScript, Jinja Templates

### Backend

Flask handles routing, authentication, sessions, uploads, APIs, and templates.

### Data Processing

Pandas reads CSV files, filters cities, and calculates metrics.

### Visualization

Matplotlib dynamically creates charts.

### Database

SQLite stores internal records and history.

---

## Folder Structure
WeatherStats_Final/

- web_app.py
- run_app.py
- db.py
- requirements.txt
- README.md
- templates/
- weatherstats/
- tests/
- data_sets/

---

## Dashboard Flow

1. Login
2. Upload CSV
3. Dashboard loads cities
4. Select category
5. Select city
6. Charts and metrics update live

---

## CSV Upload and Processing

1. CSV uploaded through Flask
2. Saved locally
3. Loaded with Pandas
4. Cities extracted from `Location`
5. Numeric columns cleaned
6. Metrics calculated
7. Charts generated

---

## Interactive Behavior

### Buttons

- Temperature Patterns
- Rainfall Distribution
- Weather Extremes

### Dropdown

Changing cities updates:

- Charts
- Titles
- Insights table

---

## Development Phases

1. Command line analytics tool
2. Flask web conversion
3. Added login system
4. Added CSV upload
5. Built live dashboard
6. Improved charts
7. Added insights table
8. Final deployment prep

---

## Challenges and Improvements

### Matplotlib MacOS Backend Error

Resolved with:

```python
matplotlib.use("Agg")
```

### Early Chart Quality

Improved labels, units, smoothing, and styling.

### Dashboard UX

Rebuilt with JavaScript fetch requests.

---

## Testing

Tests cover:

- CSV loading
- City filtering
- Calculations
- Chart generation
- Route security

Located in `tests/`

---

## Technologies Used

- Python
- Flask
- Pandas
- Matplotlib
- SQLite
- HTML
- CSS
- JavaScript
- Scikit-learn

---

## How to Run

Username: admin
Password: wrongpassword

```bash
pip install -r requirements.txt
python3 web_app.py
```

Open:

`http://127.0.0.1:5000`

---

## Final Reflection

This project helped me understand how to build and structure a full stack Python application by separating backend logic with Flask, data processing with Pandas, visualization with Matplotlib, and frontend interaction using HTML templates and JavaScript. I learned how these components work together to create a functional interactive dashboard and gained experience handling CSV uploads, session management, and dynamic updates without full page reloads. Deploying the application to a cloud environment also taught me how production systems differ from local development, especially around port configuration, dependencies, and startup behavior. Overall, the project strengthened my ability to debug issues, interpret logs, and build a complete end to end data driven web application.

**Live Deployment:**
https://weatherstats-final-project.onrender.com

username: admin
password: wrongpassword

**GitHub Repository:** 
https://github.com/GordonPoole/weatherstats-final-project

