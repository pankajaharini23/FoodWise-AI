# 🍽️ FoodWise AI

## AI-Powered Food Demand Prediction and Smart College Mess Management System

FoodWise AI is an intelligent web-based application designed to help college mess management predict food demand and reduce food wastage.

The system uses a Machine Learning model to predict the number of food servings required based on factors such as the day, meal type, menu, expected student count, holidays, special events, semester status, and previous food demand.

FoodWise AI also provides food waste analysis, analytics, AI-powered recommendations, smart alerts, prediction history, and user account management.

---

# 🚀 Features

## 🔐 User Authentication

- User Registration
- Secure User Login
- Password Hashing
- Session Management
- User Logout
- User Profile Management
- Update Profile Name
- Change Password

---

## 🤖 AI Food Demand Prediction

The system predicts food demand using Machine Learning based on:

- Day of the Week
- Meal Type
- Menu
- Expected Number of Students
- Holiday Status
- Special Event Status
- Semester Status
- Previous Food Demand

The prediction system also provides:

- Predicted Food Demand
- Safety Buffer
- Buffer Percentage
- Recommended Food Preparation Quantity

---

## ♻️ Food Waste Analysis

FoodWise AI helps analyze food wastage using:

- Food Prepared
- Students Served
- Food Wasted
- Wastage Percentage

Based on the results, the system provides smart recommendations for reducing food wastage.

---

## 📊 Analytics Dashboard

The analytics section provides:

- Food Demand Trends
- Expected Students vs Predicted Demand
- Food Waste Trends
- Wastage Percentage Analysis

---

## 🧠 AI Recommendations

The application generates intelligent recommendations based on:

- Latest Food Demand Prediction
- Expected Student Count
- Food Waste Records
- Historical Consumption Patterns

---

## 🔔 Smart Alerts

FoodWise AI provides alerts for:

- High Food Demand
- Low Food Demand
- Normal Food Demand
- High Food Wastage
- Moderate Food Wastage
- Low Food Wastage

---

## 📋 Prediction History

Users can:

- View Previous Predictions
- Search Prediction Records
- Monitor Historical Demand
- Clear Prediction History

---

## 🗂️ Waste History

Users can:

- View Food Waste Records
- Search Waste Records
- Monitor Wastage Trends
- Analyze Historical Food Waste

---

# 🛠️ Technologies Used

## Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 Templates

## Backend

- Python
- Flask

## Database

- SQLite

## Machine Learning

- Scikit-learn
- Pandas
- Joblib

---

# 📁 Project Structure

```text
Food-Demand-Prediction/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── database.py
│   └── foodwise.db
│
├── model/
│   └── food_demand_model.pkl
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── base.html
    ├── login.html
    ├── register.html
    ├── index.html
    ├── analytics.html
    ├── recommendations.html
    ├── alerts.html
    ├── history.html
    ├── waste_analysis.html
    ├── waste_history.html
    ├── profile.html
    ├── about.html
    └── model_performance.html