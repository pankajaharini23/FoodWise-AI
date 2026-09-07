import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# ==========================================
# FOODWISE AI - MACHINE LEARNING MODEL
# ==========================================


# ------------------------------------------
# STEP 1: GET PROJECT PATH
# ------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "food_data.csv"
)


# ------------------------------------------
# STEP 2: LOAD DATASET
# ------------------------------------------

print("Loading dataset...")

data = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Dataset Shape:", data.shape)


# ------------------------------------------
# STEP 3: SELECT INPUT FEATURES
# ------------------------------------------

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


# ------------------------------------------
# STEP 4: SELECT TARGET
# ------------------------------------------

y = data["actual_demand"]


# ------------------------------------------
# STEP 5: DEFINE CATEGORICAL COLUMNS
# ------------------------------------------

CATEGORICAL_FEATURES = [
    "day",
    "meal",
    "menu",
    "semester_status"
]


NUMERICAL_FEATURES = [
    "expected_students",
    "holiday",
    "special_event",
    "previous_demand"
]


# ------------------------------------------
# STEP 6: CREATE DATA PREPROCESSOR
# ------------------------------------------

preprocessor = ColumnTransformer(

    transformers=[

        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            CATEGORICAL_FEATURES
        ),

        (
            "numerical",
            "passthrough",
            NUMERICAL_FEATURES
        )

    ]

)


# ------------------------------------------
# STEP 7: CREATE RANDOM FOREST MODEL
# ------------------------------------------

model = RandomForestRegressor(

    n_estimators=200,
    random_state=42
)


# ------------------------------------------
# STEP 8: CREATE MACHINE LEARNING PIPELINE
# ------------------------------------------

pipeline = Pipeline(

    steps=[

        (
            "preprocessor",
            preprocessor
        ),

        (
            "model",
            model
        )

    ]

)


# ------------------------------------------
# STEP 9: SPLIT DATA
# ------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)


print("\nTraining Records:", len(X_train))
print("Testing Records:", len(X_test))


# ------------------------------------------
# STEP 10: TRAIN MODEL
# ------------------------------------------

print("\nTraining the Machine Learning Model...")

pipeline.fit(

    X_train,
    y_train
)


print("Model training completed successfully!")


# ------------------------------------------
# STEP 11: MAKE PREDICTIONS
# ------------------------------------------

predictions = pipeline.predict(X_test)


# ------------------------------------------
# STEP 12: EVALUATE MODEL
# ------------------------------------------

mae = mean_absolute_error(

    y_test,
    predictions
)

mse = mean_squared_error(

    y_test,
    predictions
)

r2 = r2_score(

    y_test,
    predictions
)


print("\n========== MODEL PERFORMANCE ==========")

print("Mean Absolute Error (MAE):", round(mae, 2))

print("Mean Squared Error (MSE):", round(mse, 2))

print("R² Score:", round(r2, 4))


# ------------------------------------------
# STEP 13: SAVE TRAINED MODEL
# ------------------------------------------

MODEL_PATH = os.path.join(

    BASE_DIR,
    "model",
    "food_demand_model.pkl"
)


joblib.dump(

    pipeline,
    MODEL_PATH
)


print("\n======================================")

print("Model saved successfully!")

print("Model Location:")

print(MODEL_PATH)

print("======================================")