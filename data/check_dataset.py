import pandas as pd


# Load the dataset
data = pd.read_csv("food_data.csv")


# Display first 10 rows
print("\nFIRST 10 RECORDS:")
print(data.head(10))


# Display dataset information
print("\nDATASET INFORMATION:")
print(data.info())


# Check dataset shape
print("\nDATASET SIZE:")
print("Rows:", data.shape[0])
print("Columns:", data.shape[1])


# Check missing values
print("\nMISSING VALUES:")
print(data.isnull().sum())


# Display statistics
print("\nNUMERICAL STATISTICS:")
print(data.describe())