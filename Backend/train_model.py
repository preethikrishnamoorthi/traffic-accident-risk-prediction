
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib


# --------------------------------------------------
# Load the accident dataset
# --------------------------------------------------

data = pd.read_csv("../UK_Accident.csv")
data = data.sample(n=200000, random_state=42)
data = data.reset_index(drop=True)

print("Dataset loaded successfully!")
print("Rows:", len(data))
print("Columns:", len(data.columns))


print("\nFirst 5 rows:")
print(data.head())


print("\nColumn names:")
print(data.columns.tolist())


# --------------------------------------------------
# Accident Severity
# --------------------------------------------------

print("\nAccident Severity:")
print(data["Accident_Severity"].value_counts())


# --------------------------------------------------
# Missing values
# --------------------------------------------------

print("\nMissing values:")
print(data.isnull().sum())


# --------------------------------------------------
# Remove unnecessary columns
# --------------------------------------------------

data = data.drop(columns=[
    "Unnamed: 0",
    "Accident_Index",
    "Special_Conditions_at_Site",
    "Carriageway_Hazards",
    "LSOA_of_Accident_Location"
])


print("\nColumns after cleaning:")
print(data.columns.tolist())


# --------------------------------------------------
# Fill missing values
# --------------------------------------------------

for column in data.columns:

    if data[column].isnull().any():

        data[column] = data[column].fillna(
            data[column].mode()[0]
        )


print("\nMissing values after cleaning:")
print(data.isnull().sum().sum())


# --------------------------------------------------
# Convert Time into Hour
# --------------------------------------------------

data["Hour"] = pd.to_datetime(
    data["Time"],
    format="%H:%M",
    errors="coerce"
).dt.hour


data["Hour"] = data["Hour"].fillna(
    data["Hour"].mode()[0]
)


data = data.drop(columns=["Time"])


print("\nTime converted to Hour successfully!")
print(data[["Hour"]].head())


# --------------------------------------------------
# Select features
# --------------------------------------------------

features = [
    "Number_of_Vehicles",
    "Number_of_Casualties",
    "Day_of_Week",
    "Hour",
    "Road_Type",
    "Speed_limit",
    "Junction_Control",
    "Light_Conditions",
    "Weather_Conditions",
    "Road_Surface_Conditions",
    "Urban_or_Rural_Area",
    "Latitude",
    "Longitude",
    "Year"
]


X = data[features]

y = data["Accident_Severity"]


print("\nFeatures selected:")
print(X.columns.tolist())


print("\nTarget:")
print(y.name)


# --------------------------------------------------
# Numeric features
# --------------------------------------------------

numeric_features = [
    "Number_of_Vehicles",
    "Number_of_Casualties",
    "Day_of_Week",
    "Hour",
    "Speed_limit",
    "Latitude",
    "Longitude",
    "Year"
]


# --------------------------------------------------
# Categorical features
# --------------------------------------------------

categorical_features = [
    "Road_Type",
    "Junction_Control",
    "Light_Conditions",
    "Weather_Conditions",
    "Road_Surface_Conditions",
    "Urban_or_Rural_Area"
]


print("\nNumeric features:")
print(numeric_features)


print("\nCategorical features:")
print(categorical_features)


# --------------------------------------------------
# Encode categorical features
# --------------------------------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OrdinalEncoder(
                handle_unknown="use_encoded_value",
                unknown_value=-1
            ),
            categorical_features
        )
    ],
    remainder="passthrough"
)


print("\nCategorical encoding prepared successfully!")


# --------------------------------------------------
# Create Random Forest model
# --------------------------------------------------

model = Pipeline([
    (
        "preprocessor",
        preprocessor
    ),

    (
        "random_forest",
        RandomForestClassifier(
        n_estimators=20,
        max_depth=15,
        random_state=42,
        n_jobs=-1,
        class_weight={1: 4, 2: 2, 3: 1}
        )
    )
])


print("\nRandom Forest model created successfully!")


# --------------------------------------------------
# Split data
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("\nData split successfully!")

print("Training rows:", len(X_train))

print("Testing rows:", len(X_test))


# --------------------------------------------------
# Train Random Forest
# --------------------------------------------------

print("\nTraining Random Forest model...")


model.fit(
    X_train,
    y_train
)


print(
    "Random Forest training completed successfully!"
)


# --------------------------------------------------
# Evaluate model
# --------------------------------------------------

y_pred = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    y_pred
)


print("\nModel Accuracy:")

print(accuracy)


print("\nAccuracy Percentage:")

print(
    accuracy * 100,
    "%"
)


print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)


# --------------------------------------------------
# Save model
# --------------------------------------------------

joblib.dump(
    model,
    "accident_model.pkl"
)


print("\nModel saved successfully!")

print(
    "File: accident_model.pkl"
)