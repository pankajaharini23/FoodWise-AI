import csv
import random
from datetime import datetime, timedelta


# ==========================================
# FOODWISE AI - DATASET GENERATOR
# ==========================================


# Number of historical records to generate
NUM_RECORDS = 1000


# Starting date for the historical dataset
START_DATE = datetime(2024, 1, 1)


# ------------------------------------------
# AVAILABLE MEALS
# ------------------------------------------

MEALS = [
    "Breakfast",
    "Lunch",
    "Dinner"
]


# ------------------------------------------
# AVAILABLE MENU ITEMS
# ------------------------------------------

MENUS = {
    "Breakfast": [
        "Idli",
        "Dosa",
        "Pongal",
        "Poori",
        "Upma"
    ],

    "Lunch": [
        "South Indian Meals",
        "Biryani",
        "Variety Rice",
        "Chapati",
        "Special Meals"
    ],

    "Dinner": [
        "Chapati",
        "Dosa",
        "Idli",
        "Variety Rice",
        "Parotta"
    ]
}


# ------------------------------------------
# DAY EFFECT
# ------------------------------------------

DAY_EFFECT = {
    "Monday": 20,
    "Tuesday": 10,
    "Wednesday": 0,
    "Thursday": 15,
    "Friday": 30,
    "Saturday": -70,
    "Sunday": -150
}


# ------------------------------------------
# MEAL EFFECT
# ------------------------------------------

MEAL_EFFECT = {
    "Breakfast": -60,
    "Lunch": 50,
    "Dinner": -20
}


# ------------------------------------------
# MENU EFFECT
# ------------------------------------------

MENU_EFFECT = {

    "Biryani": 60,
    "Special Meals": 40,
    "Dosa": 20,
    "Poori": 15,
    "Parotta": 25,

    "South Indian Meals": 10,
    "Variety Rice": 5,
    "Chapati": 0,
    "Idli": -10,
    "Pongal": -15,
    "Upma": -20
}


# ------------------------------------------
# SEMESTER STATUS
# ------------------------------------------

SEMESTER_STATUS = [
    "Regular",
    "Exam Period",
    "Semester Holiday"
]


# ==========================================
# FUNCTION: DETERMINE SEMESTER STATUS
# ==========================================

def get_semester_status(date):

    month = date.month

    # Summer holidays
    if month in [5, 6]:
        return "Semester Holiday"

    # Example exam months
    elif month in [4, 11]:
        return "Exam Period"

    else:
        return "Regular"


# ==========================================
# FUNCTION: CHECK HOLIDAY
# ==========================================

def is_holiday(date):

    # Sunday is considered a holiday
    if date.weekday() == 6:
        return 1

    # Random festival / public holidays
    random_holiday = random.random()

    if random_holiday < 0.03:
        return 1

    return 0


# ==========================================
# FUNCTION: SPECIAL EVENT
# ==========================================

def has_special_event():

    # Around 8% of records can have events
    if random.random() < 0.08:
        return 1

    return 0


# ==========================================
# FUNCTION: GENERATE EXPECTED STUDENTS
# ==========================================

def generate_expected_students(day, holiday, semester_status):

    # Semester holiday
    if semester_status == "Semester Holiday":
        students = random.randint(80, 200)

    # Exam period
    elif semester_status == "Exam Period":
        students = random.randint(250, 450)

    # Weekend
    elif day == "Saturday":
        students = random.randint(250, 400)

    elif day == "Sunday":
        students = random.randint(80, 200)

    # Normal working days
    else:
        students = random.randint(400, 600)

    # Holiday reduces student attendance
    if holiday == 1:
        students = int(students * random.uniform(0.5, 0.8))

    return students


# ==========================================
# FUNCTION: CALCULATE ACTUAL DEMAND
# ==========================================

def calculate_actual_demand(
        day,
        meal,
        menu,
        expected_students,
        holiday,
        special_event,
        semester_status,
        previous_demand):

    # --------------------------------------
    # BASE DEMAND
    # --------------------------------------

    # Demand starts as a percentage of
    # expected students instead of a fixed value

    base_demand = expected_students * random.uniform(0.65, 0.85)


    # --------------------------------------
    # DAY EFFECT
    # --------------------------------------

    demand = base_demand + DAY_EFFECT[day]


    # --------------------------------------
    # MEAL EFFECT
    # --------------------------------------

    demand += MEAL_EFFECT[meal]


    # --------------------------------------
    # MENU EFFECT
    # --------------------------------------

    demand += MENU_EFFECT[menu]


    # --------------------------------------
    # HOLIDAY EFFECT
    # --------------------------------------

    if holiday == 1:
        demand *= random.uniform(0.75, 0.9)


    # --------------------------------------
    # SPECIAL EVENT EFFECT
    # --------------------------------------

    if special_event == 1:

        # Events can bring additional students
        demand += random.randint(20, 60)


    # --------------------------------------
    # SEMESTER STATUS EFFECT
    # --------------------------------------

    if semester_status == "Exam Period":

        # Slightly lower demand during exams
        demand *= random.uniform(0.85, 0.95)


    elif semester_status == "Semester Holiday":

        # Much lower demand during holidays
        demand *= random.uniform(0.70, 0.90)


    # --------------------------------------
    # PREVIOUS DEMAND EFFECT
    # --------------------------------------

    # Add a small influence from previous demand
    # This prevents previous demand from
    # completely controlling the result

    demand = (demand * 0.85) + (previous_demand * 0.15)


    # --------------------------------------
    # RANDOM REAL-WORLD VARIATION
    # --------------------------------------

    random_variation = random.randint(-20, 20)

    demand += random_variation


    # --------------------------------------
    # FINAL LIMITS
    # --------------------------------------

    # Demand should not be negative
    demand = max(demand, 0)

    # Normally demand should not exceed expected students
    demand = min(demand, expected_students)

    return round(demand)


# ==========================================
# GENERATE DATASET
# ==========================================


def generate_dataset():

    # CSV file name
    filename = "food_data.csv"


    # Previous demand for the first record
    previous_demand = random.randint(250, 400)


    # Start from starting date
    current_date = START_DATE


    # Open CSV file
    with open(filename, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)


        # ----------------------------------
        # CSV COLUMN HEADERS
        # ----------------------------------

        writer.writerow([
            "date",
            "day",
            "meal",
            "menu",
            "expected_students",
            "holiday",
            "special_event",
            "semester_status",
            "previous_demand",
            "actual_demand"
        ])


        # ----------------------------------
        # CREATE RECORDS
        # ----------------------------------

        for i in range(NUM_RECORDS):


            # Get day name
            day = current_date.strftime("%A")


            # Determine semester status
            semester_status = get_semester_status(current_date)


            # Check holiday
            holiday = is_holiday(current_date)


            # Check special event
            special_event = has_special_event()


            # Randomly select meal
            meal = random.choice(MEALS)


            # Select menu based on meal
            menu = random.choice(MENUS[meal])


            # Generate expected student count
            expected_students = generate_expected_students(
                day,
                holiday,
                semester_status
            )


            # Calculate actual demand
            actual_demand = calculate_actual_demand(
                day,
                meal,
                menu,
                expected_students,
                holiday,
                special_event,
                semester_status,
                previous_demand
            )


            # ----------------------------------
            # WRITE RECORD TO CSV
            # ----------------------------------

            writer.writerow([
                current_date.strftime("%Y-%m-%d"),
                day,
                meal,
                menu,
                expected_students,
                holiday,
                special_event,
                semester_status,
                previous_demand,
                actual_demand
            ])


            # ----------------------------------
            # UPDATE PREVIOUS DEMAND
            # ----------------------------------

            previous_demand = actual_demand


            # ----------------------------------
            # MOVE TO NEXT DATE
            # ----------------------------------

            current_date += timedelta(days=1)


    print("Dataset generated successfully!")
    print("Total records generated:", NUM_RECORDS)
    print("File created:", filename)


# ==========================================
# RUN THE PROGRAM
# ==========================================

if __name__ == "__main__":
    generate_dataset()