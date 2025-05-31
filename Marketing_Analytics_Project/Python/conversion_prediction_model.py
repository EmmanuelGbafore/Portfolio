# conversion_prediction_model.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Define base path for all your CSV files
BASE_PATH = "C:/Data Analyst Project/"

# Load data with full paths
customers_df = pd.read_csv(BASE_PATH + "dim_customers.csv")
reviews_df = pd.read_csv(BASE_PATH + "fact_customer_reviews_with_sentiment.csv")

# Merge customer info with their reviews on CustomerID
df = pd.merge(reviews_df, customers_df, on='CustomerID', how='left')

# Target variable: Define high rating (e.g. 4 or 5 stars) as 1, else 0
df['HighRating'] = (df['Rating'] >= 4).astype(int)

# Select features for the model
# Use SentimentScore (numeric), SentimentCategory (categorical), SentimentBucket (categorical), Gender (categorical), AgeGroup (categorical)
features = ['SentimentScore', 'SentimentCategory', 'SentimentBucket', 'Gender', 'AgeGroup']

# Drop rows with missing values in those columns
df = df.dropna(subset=features + ['HighRating'])

# Encode categorical features
label_encoders = {}
for col in ['SentimentCategory', 'SentimentBucket', 'Gender', 'AgeGroup']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df[features]
y = df['HighRating']

# Split into train/test sets (80/20)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Initialize and train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluate model
print("=== Accuracy Score ===")
print(accuracy_score(y_test, y_pred))

print("\n=== Classification Report ===")
print(classification_report(y_test, y_pred))

print("\n=== Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred))

# Feature importance
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values(by='Importance', ascending=False)

print("\n=== Feature Importances ===")
print(importance_df)

# Predict conversion probability on all data
df['ConversionProbability'] = model.predict_proba(X)[:, 1]

# Show top 10 customers most likely to give high rating
top_customers = df[['CustomerID', 'ConversionProbability', 'Rating', 'SentimentScore', 'SentimentCategory']].sort_values(by='ConversionProbability', ascending=False).head(10)

print("\n=== Top 10 Customers Most Likely to Give High Rating ===")
print(top_customers)

# === Client Recommendations ===
print("\n=== Client Recommendations ===\n")

# From the letters you received from Marketing Manager and Customer Experience Manager,
# these recommendations directly address their concerns about engagement, conversion, and feedback.

if importance_df.loc[importance_df['Feature'] == 'SentimentCategory', 'Importance'].values[0] > 0.5:
    print("- Customer sentiment category is the strongest predictor of conversion. We recommend focusing on improving customer sentiment by enhancing product quality, customer support, and post-purchase engagement.")

if importance_df.loc[importance_df['Feature'] == 'SentimentScore', 'Importance'].values[0] > 0.1:
    print("- Sentiment scores extracted from customer reviews should be monitored regularly. Negative sentiment trends can be early signals for campaign or product issues.")

if importance_df.loc[importance_df['Feature'] == 'AgeGroup', 'Importance'].values[0] < 0.01 and \
   importance_df.loc[importance_df['Feature'] == 'Gender', 'Importance'].values[0] < 0.01:
    print("- Demographic factors like age group and gender have minimal impact on conversion rates, so marketing efforts should be optimized around sentiment and feedback rather than demographic segmentation.")

print("\nBased on this predictive analysis, we advise ShopEasy to:\n"
      "1. Prioritize campaigns and customer experience improvements targeting sentiment uplift.\n"
      "2. Utilize sentiment analysis as a continuous feedback loop to detect and address issues early.\n"
      "3. Focus marketing spend on messaging that improves customer sentiment to reverse declining engagement and conversion rates.\n"
      "4. Use the model predictions to identify at-risk customers and personalize retention strategies.\n")

print("Please feel free to reach out for further support or more customized insights.\n")
print("Best regards,\nYour Data Analyst")

