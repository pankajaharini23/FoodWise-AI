# ==========================================
# FOODWISE AI
# FOOD DEMAND PREDICTION FOR COLLEGE MESS
# COMPLETE FLASK APPLICATION
# ==========================================


from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from functools import wraps

import pandas as pd
import joblib
import os
import sys


# ==========================================
# PROJECT BASE DIRECTORY
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================
# DATABASE IMPORT
# ==========================================

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

sys.path.append(
    DATABASE_DIR
)


from database import (

    create_database,

    save_prediction,

    get_predictions,

    get_recent_predictions,

    save_waste_record,

    get_waste_records,

    get_recent_waste_records,

    get_latest_waste_record,

    get_prediction_count,

    get_waste_record_count,

    get_latest_prediction,

    clear_predictions,
    
    delete_prediction,
    
    delete_waste_record,

    create_user,

    get_user_by_email,

    get_user_by_id,
    
    update_user_name,
    
    update_user_password,
    
    delete_prediction,
    
    delete_waste_record
    

)


# ==========================================
# CREATE FLASK APPLICATION
# ==========================================

app = Flask(__name__)


# ==========================================
# SECRET KEY FOR USER SESSIONS
# ==========================================

app.secret_key = "foodwise_ai_secret_key_2026"


# ==========================================
# CREATE DATABASE
# ==========================================

create_database()


# ==========================================
# LOGIN REQUIRED DECORATOR
# ==========================================

def login_required(view):

    @wraps(view)

    def wrapped_view(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login to access FoodWise AI.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        return view(*args, **kwargs)

    return wrapped_view


# ==========================================
# MACHINE LEARNING MODEL PATH
# ==========================================

MODEL_PATH = os.path.join(

    BASE_DIR,

    "model",

    "food_demand_model.pkl"

)


# ==========================================
# LOAD MACHINE LEARNING MODEL
# ==========================================

try:

    model = joblib.load(
        MODEL_PATH
    )

    print(
        "Machine Learning Model Loaded Successfully!"
    )


except Exception as e:

    print(
        "Error loading Machine Learning Model:",
        e
    )

    model = None


# ==========================================
# USER REGISTRATION
# ==========================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    # --------------------------------------
    # IF USER IS ALREADY LOGGED IN
    # --------------------------------------

    if "user_id" in session:

        return redirect(
            url_for("home")
        )


    # --------------------------------------
    # HANDLE REGISTRATION FORM
    # --------------------------------------

    if request.method == "POST":

        name = request.form.get(
            "name"
        )

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )


        # ----------------------------------
        # REMOVE EXTRA SPACES
        # ----------------------------------

        if name:

            name = name.strip()


        if email:

            email = email.strip().lower()


        # ----------------------------------
        # VALIDATION
        # ----------------------------------

        if not name or not email or not password or not confirm_password:

            flash(
                "Please fill in all fields.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        # ----------------------------------
        # PASSWORD MATCH CHECK
        # ----------------------------------

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        # ----------------------------------
        # PASSWORD LENGTH
        # ----------------------------------

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


        # ----------------------------------
        # HASH PASSWORD
        # ----------------------------------

        hashed_password = generate_password_hash(
            password
        )


        # ----------------------------------
        # CREATE USER
        # ----------------------------------

        user_created = create_user(

            name,

            email,

            hashed_password

        )


        # ----------------------------------
        # SUCCESS
        # ----------------------------------

        if user_created:

            flash(
                "Registration successful! Please login.",
                "success"
            )

            return redirect(
                url_for("login")
            )


        # ----------------------------------
        # EMAIL ALREADY EXISTS
        # ----------------------------------

        else:

            flash(
                "This email is already registered.",
                "danger"
            )

            return redirect(
                url_for("register")
            )


    # --------------------------------------
    # DISPLAY REGISTRATION PAGE
    # --------------------------------------

    return render_template(
        "register.html"
    )


# ==========================================
# USER LOGIN
# ==========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # --------------------------------------
    # IF USER IS ALREADY LOGGED IN
    # --------------------------------------

    if "user_id" in session:

        return redirect(
            url_for("home")
        )


    # --------------------------------------
    # HANDLE LOGIN FORM
    # --------------------------------------

    if request.method == "POST":

        email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )


        # ----------------------------------
        # CLEAN EMAIL
        # ----------------------------------

        if email:

            email = email.strip().lower()


        # ----------------------------------
        # VALIDATION
        # ----------------------------------

        if not email or not password:

            flash(
                "Please enter your email and password.",
                "danger"
            )

            return redirect(
                url_for("login")
            )


        # ----------------------------------
        # GET USER
        # ----------------------------------

        user = get_user_by_email(
            email
        )


        # ----------------------------------
        # CHECK USER AND PASSWORD
        # ----------------------------------

        if user:

            stored_password = user[3]


            if check_password_hash(

                stored_password,

                password

            ):

                # --------------------------
                # CREATE USER SESSION
                # --------------------------

                session["user_id"] = user[0]

                session["user_name"] = user[1]

                session["user_email"] = user[2]

                session["user_role"] = user[4]


                flash(

                    f"Welcome back, {user[1]}!",

                    "success"

                )


                return redirect(

                    url_for("home")

                )


        # ----------------------------------
        # INVALID LOGIN
        # ----------------------------------

        flash(

            "Invalid email or password.",

            "danger"

        )


        return redirect(

            url_for("login")

        )


    # --------------------------------------
    # DISPLAY LOGIN PAGE
    # --------------------------------------

    return render_template(

        "login.html"

    )


# ==========================================
# USER LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()


    flash(

        "You have been logged out successfully.",

        "success"

    )


    return redirect(

        url_for("login")

    )


# ==========================================
# HOME / DASHBOARD PAGE
# ==========================================

@app.route("/")
@login_required
def home():

    # --------------------------------------
    # GET DASHBOARD STATISTICS
    # --------------------------------------

    total_predictions = get_prediction_count()

    total_waste_records = get_waste_record_count()

    latest_prediction = get_latest_prediction()

    latest_waste = get_latest_waste_record()


    # --------------------------------------
    # LATEST PREDICTED DEMAND
    # --------------------------------------

    latest_predicted_demand = 0


    if latest_prediction:

        latest_predicted_demand = latest_prediction[9]


    # --------------------------------------
    # LATEST FOOD WASTED
    # --------------------------------------

    latest_food_wasted = 0


    if latest_waste:

        latest_food_wasted = latest_waste[3]


    return render_template(

        "index.html",

        total_predictions=total_predictions,

        total_waste_records=total_waste_records,

        latest_predicted_demand=latest_predicted_demand,

        latest_food_wasted=latest_food_wasted

    )


# ==========================================
# FOOD DEMAND PREDICTION
# ==========================================

@app.route(
    "/predict",
    methods=["POST"]
)
@login_required
def predict():

    try:


        # ==================================
        # CHECK MACHINE LEARNING MODEL
        # ==================================

        if model is None:

            return jsonify({

                "success": False,

                "error":

                    "Machine Learning model could not be loaded."

            })


        # ==================================
        # GET FORM DATA
        # ==================================

        day = request.form.get(
            "day"
        )


        meal = request.form.get(
            "meal"
        )


        menu = request.form.get(
            "menu"
        )


        expected_students = int(

            request.form.get(
                "expected_students"
            )

        )


        holiday = int(

            request.form.get(
                "holiday"
            )

        )


        special_event = int(

            request.form.get(
                "special_event"
            )

        )


        semester_status = request.form.get(

            "semester_status"

        )


        previous_demand = int(

            request.form.get(

                "previous_demand"

            )

        )


        # ==================================
        # CREATE MODEL INPUT DATAFRAME
        # ==================================

        input_data = pd.DataFrame({

            "day":

                [day],


            "meal":

                [meal],


            "menu":

                [menu],


            "expected_students":

                [expected_students],


            "holiday":

                [holiday],


            "special_event":

                [special_event],


            "semester_status":

                [semester_status],


            "previous_demand":

                [previous_demand]

        })


        # ==================================
        # MACHINE LEARNING PREDICTION
        # ==================================

        prediction = model.predict(

            input_data

        )[0]


        predicted_demand = round(

            float(prediction)

        )


        # ==================================
        # PREVENT NEGATIVE VALUES
        # ==================================

        if predicted_demand < 0:

            predicted_demand = 0


        # ==================================
        # CALCULATE SAFETY BUFFER
        # ==================================

        if predicted_demand < 200:

            buffer_percentage = 5


        elif predicted_demand <= 400:

            buffer_percentage = 4


        else:

            buffer_percentage = 3


        safety_buffer = round(

            predicted_demand

            *

            buffer_percentage

            /

            100

        )


        # ==================================
        # RECOMMENDED PREPARATION
        # ==================================

        recommended_preparation = (

            predicted_demand

            +

            safety_buffer

        )


        # ==================================
        # SAVE PREDICTION
        # ==================================

        save_prediction(

            day,

            meal,

            menu,

            expected_students,

            holiday,

            special_event,

            semester_status,

            previous_demand,

            predicted_demand

        )


        # ==================================
        # RETURN RESULT
        # ==================================

        return jsonify({

            "success":

                True,


            "predicted_demand":

                predicted_demand,


            "safety_buffer":

                safety_buffer,


            "buffer_percentage":

                buffer_percentage,


            "recommended_preparation":

                recommended_preparation

        })


    except Exception as e:


        print(

            "Prediction Error:",

            e

        )


        return jsonify({

            "success":

                False,


            "error":

                str(e)

        })


# ==========================================
# PREDICTION HISTORY PAGE
# ==========================================

@app.route("/history")
@login_required
def history():

    predictions = get_predictions()


    return render_template(

        "history.html",

        predictions=predictions

    )
# ==========================================
# DELETE SINGLE PREDICTION
# ==========================================

@app.route(
    "/delete-prediction/<int:prediction_id>",
    methods=["POST"]
)
@login_required
def delete_prediction_record(prediction_id):

    delete_prediction(
        prediction_id
    )

    flash(
        "Prediction record deleted successfully!",
        "success"
    )

    return redirect(
        url_for("history")
    )

# ==========================================
# CLEAR PREDICTION HISTORY
# ==========================================

@app.route(
    "/clear-history",
    methods=["POST"]
)
@login_required
def clear_history():

    clear_predictions()


    return render_template(

        "history.html",

        predictions=get_predictions()

    )


# ==========================================
# ANALYTICS PAGE
# ==========================================

@app.route("/analytics")
@login_required
def analytics():

    predictions = get_recent_predictions()

    waste_records = get_recent_waste_records()


    # ======================================
    # PREDICTION DATA
    # ======================================

    labels = []

    predicted_demands = []

    expected_students = []


    # Reverse records so charts display
    # oldest → newest

    predictions = predictions[::-1]


    for prediction in predictions:


        labels.append(

            str(prediction[1])

            +

            " - "

            +

            str(prediction[2])

        )


        expected_students.append(

            int(prediction[4])

        )


        predicted_demands.append(

            int(prediction[9])

        )


    # ======================================
    # WASTE DATA
    # ======================================

    waste_labels = []

    food_wasted = []

    wastage_percentages = []


    waste_records = waste_records[::-1]


    for record in waste_records:


        waste_labels.append(

            "Record "

            +

            str(record[0])

        )


        food_wasted.append(

            int(record[3])

        )


        wastage_percentages.append(

            float(record[4])

        )


    # ======================================
    # RENDER ANALYTICS PAGE
    # ======================================

    return render_template(

        "analytics.html",

        labels=labels,

        predicted_demands=predicted_demands,

        expected_students=expected_students,

        waste_labels=waste_labels,

        food_wasted=food_wasted,

        wastage_percentages=wastage_percentages

    )


# ==========================================
# AI RECOMMENDATIONS PAGE
# ==========================================

@app.route("/recommendations")
@login_required
def recommendations():

    latest_prediction = get_latest_prediction()

    latest_waste = get_latest_waste_record()


    recommendations_list = []


    # ======================================
    # FOOD DEMAND RECOMMENDATION
    # ======================================

    if latest_prediction:


        predicted_demand = int(

            latest_prediction[9]

        )


        expected_students = int(

            latest_prediction[4]

        )


        recommendations_list.append({

            "title":

                "Food Preparation Strategy",


            "icon":

                "🍽️",


            "message":

                f"Prepare approximately {predicted_demand} servings "
                f"based on the latest AI prediction."

        })


        if predicted_demand > expected_students:


            difference = (

                predicted_demand

                -

                expected_students

            )


            recommendations_list.append({

                "title":

                    "Demand Buffer",


                "icon":

                    "📈",


                "message":

                    f"The predicted demand is {difference} servings "
                    f"higher than the expected student count. "
                    f"Monitor attendance before preparing extra food."

            })


    else:


        recommendations_list.append({

            "title":

                "Start Predicting",


            "icon":

                "🤖",


            "message":

                "Create a food demand prediction to receive "
                "personalized AI recommendations."

        })


    # ======================================
    # WASTE RECOMMENDATION
    # ======================================

    if latest_waste:


        wastage_percentage = float(

            latest_waste[4]

        )


        if wastage_percentage < 5:


            waste_message = (

                "Excellent! Food wastage is currently low. "
                "Continue following the current preparation strategy."

            )


        elif wastage_percentage < 15:


            waste_message = (

                "Moderate food wastage detected. "
                "Consider reducing food preparation slightly."

            )


        else:


            waste_message = (

                "High food wastage detected. "
                "Review historical consumption patterns and "
                "reduce future food preparation."

            )


        recommendations_list.append({

            "title":

                "Waste Management",


            "icon":

                "♻️",


            "message":

                waste_message

        })


    else:


        recommendations_list.append({

            "title":

                "Track Food Waste",


            "icon":

                "♻️",


            "message":

                "Add food waste records to receive "
                "smart waste reduction recommendations."

        })


    # ======================================
    # GENERAL RECOMMENDATION
    # ======================================

    recommendations_list.append({

        "title":

            "Smart Planning",


        "icon":

            "💡",


        "message":

            "Use historical predictions, student attendance, "
            "and food consumption trends to improve future "
            "mess planning."

    })


    return render_template(

        "recommendations.html",

        recommendations=recommendations_list

    )


# ==========================================
# WASTE ANALYSIS PAGE
# ==========================================

@app.route("/waste-analysis")
@login_required
def waste_analysis():

    return render_template(

        "waste_analysis.html"

    )


# ==========================================
# ANALYZE FOOD WASTE
# ==========================================

@app.route(

    "/analyze-waste",

    methods=["POST"]

)
@login_required
def analyze_waste():

    try:


        # ==================================
        # GET JSON DATA
        # ==================================

        data = request.get_json()


        if not data:

            return jsonify({

                "success":

                    False,


                "error":

                    "No data received."

            })


        # ==================================
        # CONVERT VALUES
        # ==================================

        food_prepared = int(

            data.get(

                "food_prepared",

                0

            )

        )


        students_served = int(

            data.get(

                "students_served",

                0

            )

        )


        # ==================================
        # VALIDATION
        # ==================================

        if food_prepared <= 0:


            return jsonify({

                "success":

                    False,


                "error":

                    "Food prepared must be greater than 0."

            })


        if students_served < 0:


            return jsonify({

                "success":

                    False,


                "error":

                    "Students served cannot be negative."

            })


        # ==================================
        # CALCULATE FOOD WASTE
        # ==================================

        food_wasted = (

            food_prepared

            -

            students_served

        )


        if food_wasted < 0:

            food_wasted = 0


        # ==================================
        # CALCULATE WASTAGE PERCENTAGE
        # ==================================

        wastage_percentage = round(

            (

                food_wasted

                /

                food_prepared

            )

            *

            100,

            2

        )


        # ==================================
        # AI RECOMMENDATION
        # ==================================

        if wastage_percentage < 5:


            recommendation = (

                "Excellent food management! "
                "Food wastage is very low. Continue "
                "following the current preparation strategy."

            )


        elif wastage_percentage < 10:


            recommendation = (

                "Good food management. "
                "A small reduction in food preparation "
                "may further reduce wastage."

            )


        elif wastage_percentage < 20:


            recommendation = (

                "Moderate food wastage detected. "
                "Review previous demand patterns before "
                "planning the next meal."

            )


        else:


            recommendation = (

                "High food wastage detected. "
                "Consider significantly reducing future "
                "food preparation and analyzing student attendance."

            )


        # ==================================
        # SAVE WASTE RECORD
        # ==================================

        save_waste_record(

            food_prepared,

            students_served,

            food_wasted,

            wastage_percentage

        )


        # ==================================
        # RETURN RESULT
        # ==================================

        return jsonify({

            "success":

                True,


            "food_prepared":

                food_prepared,


            "students_served":

                students_served,


            "food_wasted":

                food_wasted,


            "wastage_percentage":

                wastage_percentage,


            "recommendation":

                recommendation

        })


    except Exception as e:


        print(

            "Waste Analysis Error:",

            e

        )


        return jsonify({

            "success":

                False,


            "error":

                str(e)

        })


# ==========================================
# WASTE HISTORY PAGE
# ==========================================

@app.route("/waste-history")
@login_required
def waste_history():

    records = get_waste_records()


    return render_template(

        "waste_history.html",

        records=records

    )
# ==========================================
# DELETE SINGLE WASTE RECORD
# ==========================================

@app.route(
    "/delete-waste-record/<int:record_id>",
    methods=["POST"]
)
@login_required
def delete_waste_record_route(record_id):

    delete_waste_record(
        record_id
    )

    flash(
        "Waste record deleted successfully!",
        "success"
    )

    return redirect(
        url_for("waste_history")
    )

# ==========================================
# ABOUT PROJECT PAGE
# ==========================================

@app.route("/about")
@login_required
def about():

    return render_template(

        "about.html"

    )


# ==========================================
# MODEL PERFORMANCE PAGE
# ==========================================

@app.route("/model-performance")
@login_required
def model_performance():

    # These values are from your model results

    mae = 20.53

    mse = 745.88

    rmse = 27.31

    r2_score_value = 0.9649


    return render_template(

        "model_performance.html",

        mae=mae,

        mse=mse,

        rmse=rmse,

        r2_score_value=r2_score_value

    )

# ==========================================
# USER PROFILE PAGE
# ==========================================

@app.route("/profile")
@login_required
def profile():

    # --------------------------------------
    # GET LOGGED-IN USER ID
    # --------------------------------------

    user_id = session.get(
        "user_id"
    )


    # --------------------------------------
    # GET USER DETAILS FROM DATABASE
    # --------------------------------------

    user = get_user_by_id(
        user_id
    )


    # --------------------------------------
    # SAFETY CHECK
    # --------------------------------------

    if not user:

        session.clear()

        flash(
            "User account not found. Please login again.",
            "danger"
        )

        return redirect(
            url_for("login")
        )


    # --------------------------------------
    # RENDER PROFILE PAGE
    # --------------------------------------

    return render_template(

        "profile.html",

        user=user

    )
# ==========================================
# UPDATE USER PROFILE
# ==========================================

@app.route(
    "/update-profile",
    methods=["POST"]
)
@login_required
def update_profile():

    name = request.form.get(
        "name"
    )


    # --------------------------------------
    # CLEAN NAME
    # --------------------------------------

    if name:

        name = name.strip()


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if not name:

        flash(

            "Name cannot be empty.",

            "danger"

        )

        return redirect(

            url_for("profile")

        )


    # --------------------------------------
    # UPDATE DATABASE
    # --------------------------------------

    update_user_name(

        session["user_id"],

        name

    )


    # --------------------------------------
    # UPDATE SESSION NAME
    # --------------------------------------

    session["user_name"] = name


    flash(

        "Profile updated successfully!",

        "success"

    )


    return redirect(

        url_for("profile")

    )
# ==========================================
# CHANGE USER PASSWORD
# ==========================================

@app.route(
    "/change-password",
    methods=["POST"]
)
@login_required
def change_password():

    current_password = request.form.get(
        "current_password"
    )

    new_password = request.form.get(
        "new_password"
    )

    confirm_password = request.form.get(
        "confirm_password"
    )


    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if (

        not current_password

        or

        not new_password

        or

        not confirm_password

    ):

        flash(

            "Please fill in all password fields.",

            "danger"

        )

        return redirect(

            url_for("profile")

        )


    # --------------------------------------
    # NEW PASSWORD MATCH CHECK
    # --------------------------------------

    if new_password != confirm_password:

        flash(

            "New passwords do not match.",

            "danger"

        )

        return redirect(

            url_for("profile")

        )


    # --------------------------------------
    # PASSWORD LENGTH CHECK
    # --------------------------------------

    if len(new_password) < 6:

        flash(

            "New password must contain at least 6 characters.",

            "danger"

        )

        return redirect(

            url_for("profile")

        )


    # --------------------------------------
    # GET CURRENT USER
    # --------------------------------------

    user = get_user_by_id(

        session["user_id"]

    )


    # --------------------------------------
    # VERIFY CURRENT PASSWORD
    # --------------------------------------

    if not user or not check_password_hash(

        user[3],

        current_password

    ):

        flash(

            "Current password is incorrect.",

            "danger"

        )

        return redirect(

            url_for("profile")

        )


    # --------------------------------------
    # HASH NEW PASSWORD
    # --------------------------------------

    hashed_password = generate_password_hash(

        new_password

    )


    # --------------------------------------
    # UPDATE PASSWORD
    # --------------------------------------

    update_user_password(

        session["user_id"],

        hashed_password

    )


    flash(

        "Password changed successfully!",

        "success"

    )


    return redirect(

        url_for("profile")

    )
# ==========================================
# SMART ALERTS PAGE
# ==========================================

@app.route("/alerts")
@login_required
def alerts():

    alerts_list = []


    # ======================================
    # GET LATEST DATA
    # ======================================

    latest_prediction = get_latest_prediction()

    latest_waste = get_latest_waste_record()


    # ======================================
    # FOOD DEMAND ALERTS
    # ======================================

    if latest_prediction:

        expected_students = int(
            latest_prediction[4]
        )

        predicted_demand = int(
            latest_prediction[9]
        )


        difference = (
            predicted_demand
            -
            expected_students
        )


        # HIGH DEMAND ALERT

        if difference > 50:

            alerts_list.append({

                "type": "warning",

                "icon": "📈",

                "title": "High Food Demand Expected",

                "message":

                    f"Predicted demand is {difference} servings "
                    f"higher than the expected student count. "
                    f"Plan additional food preparation carefully."

            })


        # LOW DEMAND ALERT

        elif difference < -50:

            alerts_list.append({

                "type": "info",

                "icon": "📉",

                "title": "Lower Food Demand Expected",

                "message":

                    f"Predicted demand is {abs(difference)} servings "
                    f"lower than the expected student count. "
                    f"Consider reducing food preparation."

            })


        # NORMAL DEMAND

        else:

            alerts_list.append({

                "type": "success",

                "icon": "✅",

                "title": "Food Demand Looks Stable",

                "message":

                    "The latest AI prediction is close to the "
                    "expected student count."

            })


    else:

        alerts_list.append({

            "type": "info",

            "icon": "🤖",

            "title": "No Prediction Available",

            "message":

                "Create a food demand prediction to receive "
                "smart demand alerts."

        })


    # ======================================
    # FOOD WASTE ALERTS
    # ======================================

    if latest_waste:

        wastage_percentage = float(
            latest_waste[4]
        )


        # HIGH WASTE

        if wastage_percentage >= 20:

            alerts_list.append({

                "type": "danger",

                "icon": "🚨",

                "title": "High Food Waste Detected",

                "message":

                    f"Food wastage is currently "
                    f"{wastage_percentage}%. "
                    f"Review food preparation quantities immediately."

            })


        # MODERATE WASTE

        elif wastage_percentage >= 10:

            alerts_list.append({

                "type": "warning",

                "icon": "⚠️",

                "title": "Moderate Food Waste Detected",

                "message":

                    f"Current food wastage is "
                    f"{wastage_percentage}%. "
                    f"Consider reducing preparation quantity."

            })


        # LOW WASTE

        else:

            alerts_list.append({

                "type": "success",

                "icon": "♻️",

                "title": "Food Waste Is Under Control",

                "message":

                    f"Excellent! Current food wastage is only "
                    f"{wastage_percentage}%."

            })


    else:

        alerts_list.append({

            "type": "info",

            "icon": "♻️",

            "title": "No Waste Data Available",

            "message":

                "Add food waste records to receive "
                "waste management alerts."

        })


    # ======================================
    # GENERAL SMART ALERT
    # ======================================

    alerts_list.append({

        "type": "info",

        "icon": "💡",

        "title": "Smart Planning Tip",

        "message":

            "Use predictions and food waste analysis together "
            "to continuously improve food preparation planning."

    })


    return render_template(

        "alerts.html",

        alerts=alerts_list

    )
# ==========================================
# RUN FLASK APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(

        debug=True

    )
    