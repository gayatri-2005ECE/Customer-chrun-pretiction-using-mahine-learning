# -*- coding: utf-8 -*-
"""R.Bhuvana - 2 year Predicting customer churn using machine learning to uncover hidden patterns.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1l6tbeXHSlAaDUlAhtsNKKZEVx4MZ7P7V

**1.importing the dependancies**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import gradio as gr
import joblib
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report
import pickle
from sklearn.linear_model import LogisticRegression

"""**2.Data Loading and Understanding**"""

#load teh csv data to a pandas dataframe
df = pd.read_csv('/content/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Display first few rows
df.head()

# Shape of the dataset
print("Shape:", df.shape)
# Column names
print("Columns:", df.columns.tolist())
# Data types and non-null values
df.info()
# Summary statistics for numeric features
df.describe()

"""**3.Check for Missing Values and Duplicate**"""

# Check for missing values
print(df.isnull().sum())
# Check for duplicates
print("Duplicate rows:", df.duplicated().sum())

"""**4.Visualize a Few Features**"""

# Distribution of Churn
sns.countplot(x='Churn', data=df)
plt.title('Distribution of Churned vs Not Churned Customers')
plt.xlabel('Churn')
plt.ylabel('Count')
plt.show()

# Relationship between Monthly Charges and Churn
sns.boxplot(x='Churn', y='MonthlyCharges', data=df)
plt.title('Monthly Charges vs Churn')
plt.xlabel('Churn')
plt.ylabel('Monthly Charges')
plt.show()

"""**5.Identify Target and Features**"""

#Identify target and features for churn prediction
target = 'Churn'
features = df.columns.drop(target)
print("Features:", features)

"""**6.Convert Categorical Columns to Numerical**"""

# Identify categorical columns
categorical_cols = df.select_dtypes(include=['object']).columns
print("Categorical Columns:", categorical_cols.tolist())

# Convert binary categorical columns using LabelEncoder
label_encoder = LabelEncoder()
for col in categorical_cols:
    if df[col].nunique() == 2:
        df[col] = label_encoder.fit_transform(df[col])
    else:
        df = pd.get_dummies(df, columns=[col], drop_first=True)

"""**7.One-Hot Encoding**

1.Separate features and target first:
"""

# Save target variable separately
target = 'Churn'
y = df[target]

# Drop target from features
X = df.drop(columns=[target])

"""2.One-hot encode only the features:"""

# One-hot encode features
X_encoded = pd.get_dummies(X, drop_first=True)

# If needed, encode the target (binary label)
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)  # "Yes"/"No" → 1/0

"""**8.Feature Scaling**"""

# Separate target variable
target = 'Churn'
y = df[target]

# Drop target from features
X = df.drop(columns=[target])

# One-hot encode features
X_encoded = pd.get_dummies(X, drop_first=True)

# Encode the target ("Yes"/"No") to 1/0
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

"""**9.Train-Test Split**"""

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y_encoded, test_size=0.2, random_state=42)

"""**10.Model Building**"""

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

"""**11.Evaluation**"""

# Evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

"""**12.Make Predictions from New Input**"""

#new inputs values
new_customer = {
    'gender': 'Female',
    'SeniorCitizen': 0,
    'Partner': 'Yes',
    'Dependents': 'No',
    'tenure': 5,
    'PhoneService': 'Yes',
    'MultipleLines': 'No',
    'InternetService': 'DSL',
    'OnlineSecurity': 'Yes',
    'OnlineBackup': 'No',
    'DeviceProtection': 'Yes',
    'TechSupport': 'No',
    'StreamingTV': 'No',
    'StreamingMovies': 'No',
    'Contract': 'Month-to-month',
    'PaperlessBilling': 'Yes',
    'PaymentMethod': 'Electronic check',
    'MonthlyCharges': 70.35,
    'TotalCharges': 350.5
}

"""**13.Convert to DataFrame and Encode**"""

# Convert to DataFrame
new_df = pd.DataFrame([new_customer])

# Combine with original df to match columns
df_temp = pd.concat([df.drop('Churn', axis=1), new_df], ignore_index=True)

# One-hot encode the combined DataFrame
df_temp_encoded = pd.get_dummies(df_temp, drop_first=True)

# Match the encoded feature order (use df_encoded which is the encoded training features)
df_temp_encoded = df_temp_encoded.reindex(columns=X_encoded.columns, fill_value=0)

"""**14.Predict the Churn**"""

# Predict churn for new customer input
predicted_churn = model.predict(df_temp_encoded)

# Output result
print("🔮 Churn Prediction:", "Yes" if predicted_churn[0] == 1 else "No")

"""**15.Deployment-Building an Interactive App**"""

!pip install gradio

"""**16.Create a Prediction Function**"""

def predict_churn(gender, senior_citizen, partner, dependents, tenure, monthly_charges, total_charges,
                  phone_service, multiple_lines, internet_service, online_security, online_backup,
                  device_protection, tech_support, streaming_tv, streaming_movies, contract,
                  paperless_billing, payment_method):

    # Create input dictionary
    input_data = {
        'gender': gender,
        'SeniorCitizen': int(senior_citizen),
        'Partner': partner,
        'Dependents': dependents,
        'tenure': int(tenure),
        'MonthlyCharges': float(monthly_charges),
        'TotalCharges': float(total_charges),
        'PhoneService': phone_service,
        'MultipleLines': multiple_lines,
        'InternetService': internet_service,
        'OnlineSecurity': online_security,
        'OnlineBackup': online_backup,
        'DeviceProtection': device_protection,
        'TechSupport': tech_support,
        'StreamingTV': streaming_tv,
        'StreamingMovies': streaming_movies,
        'Contract': contract,
        'PaperlessBilling': paperless_billing,
        'PaymentMethod': payment_method
    }

    # Convert the input data into DataFrame
    input_df = pd.DataFrame([input_data])

    # Combine the new input with the original DataFrame (except for 'Churn' target column)
    df_temp = pd.concat([df.drop('Churn', axis=1), input_df], ignore_index=True)

    # One-hot encode the combined DataFrame
    df_temp_encoded = pd.get_dummies(df_temp, drop_first=True)

    # Reindex to match the training dataset's encoded features
    df_temp_encoded = df_temp_encoded.reindex(columns=df_encoded.drop('Churn', axis=1).columns, fill_value=0)

    # Scale the features (use the same scaler as during training)
    scaled

"""**17.Create the Gradio Interface**"""

#import gradio as gr

def predict_churn(*args):
    # Example placeholder logic; replace with your model prediction logic
    churn_probability = 0.65  # dummy churn probability
    if churn_probability >= 0.5:
        return "Yes"  # Customer is likely to churn
    else:
        return "No"   # Customer is not likely to churn

inputs = [
    gr.Dropdown(['Male', 'Female'], label="Gender"),
    gr.Dropdown(['Yes', 'No'], label="Senior Citizen"),
    gr.Number(label="Tenure (months)"),
    gr.Dropdown(['DSL', 'Fiber optic', 'No'], label="Internet Service"),
    gr.Dropdown(['Yes', 'No'], label="Online Security"),
    gr.Dropdown(['Yes', 'No'], label="Online Backup"),
    gr.Dropdown(['Yes', 'No'], label="Device Protection"),
    gr.Dropdown(['Yes', 'No'], label="Tech Support"),
    gr.Dropdown(['Yes', 'No'], label="Streaming TV"),
    gr.Dropdown(['Yes', 'No'], label="Streaming Movies"),
    gr.Dropdown(['Month-to-month', 'One year', 'Two year'], label="Contract"),
    gr.Dropdown(['Yes', 'No'], label="Paperless Billing"),
    gr.Dropdown(['Electronic check', 'Mailed check', 'Bank transfer', 'Credit card'], label="Payment Method"),
    gr.Number(label="Monthly Charges"),
    gr.Number(label="Total Charges")
]

output = gr.Label(label="📉 Churn Prediction Yes/No")

# Create the Gradio interface
gr.Interface(
    fn=predict_churn,
    inputs=inputs,
    outputs=output,
    title="📊 Customer Churn Predictor",
    description="Enter customer details to predict the likelihood of churn."
).launch(share=True)