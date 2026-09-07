# ==========================================
# FOODWISE AI
# MODEL PERFORMANCE EVALUATION
# ==========================================

import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ==========================================
# STEP 1: GET PROJECT PATH
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================
# STEP 2: DATASET PATH
# ==========================================

DATA_PATH = os.path.join(

    BASE_DIR,

    "data",

    "food_data.csv"

)


# ==========================================
# STEP 3: MODEL PATH
# ==========================================

MODEL_PATH = os.path.join(

    BASE_DIR,

    "model",

    "food_demand_model.pkl"

)


# ==========================================
# STEP 4: LOAD DATASET
# ==========================================

print("\nLoading dataset...")

data = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")

print("Total Records:", len(data))


# ==========================================
# STEP 5: SELECT FEATURES
# ==========================================

FEATURES = [

    "day",

    "meal",

    "menu",

    "expected_students",

    "holiday",

    "special_event",

    "semester_status",

    "previous_demand"

]


X = data[FEATURES]


# ==========================================
# STEP 6: SELECT TARGET
# ==========================================

y = data["actual_demand"]


# ==========================================
# STEP 7: CREATE SAME TRAIN/TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.2,

    random_state=42

)


print("\nTraining Records:", len(X_train))

print("Testing Records:", len(X_test))


# ==========================================
# STEP 8: LOAD TRAINED MODEL
# ==========================================

print("\nLoading trained Machine Learning model...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")


# ==========================================
# STEP 9: MAKE PREDICTIONS
# ==========================================

print("\nMaking predictions...")

predictions = model.predict(X_test)


# ==========================================
# STEP 10: CALCULATE MAE
# ==========================================

mae = mean_absolute_error(

    y_test,

    predictions

)


# ==========================================
# STEP 11: CALCULATE MSE
# ==========================================

mse = mean_squared_error(

    y_test,

    predictions

)


# ==========================================
# STEP 12: CALCULATE RMSE
# ==========================================

rmse = mse ** 0.5


# ==========================================
# STEP 13: CALCULATE R² SCORE
# ==========================================

r2 = r2_score(

    y_test,

    predictions

)


# ==========================================
# STEP 14: DISPLAY RESULTS
# ==========================================

print("\n")

print("======================================")

print("      FOODWISE AI MODEL PERFORMANCE")

print("======================================")

print()

print("Mean Absolute Error (MAE):")

print(round(mae, 2))

print()

print("Mean Squared Error (MSE):")

print(round(mse, 2))

print()

print("Root Mean Squared Error (RMSE):")

print(round(rmse, 2))

print()

print("R² Score:")

print(round(r2, 4))

print()

print("======================================")