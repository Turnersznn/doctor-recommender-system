import pandas as pd
from surprise import Dataset, Reader, SVD, accuracy
from surprise.model_selection import train_test_split
import joblib

# === STEP 1: Load and Preprocess the Data ===

df = pd.read_csv("user_doctor_ratings.csv")
print("Loaded ratings data:")
print(df.head())

# Check for missing values
print("\nMissing values:\n", df.isnull().sum())

# === STEP 2: Prepare Data for Surprise ===
reader = Reader(rating_scale=(df.rating.min(), df.rating.max()))
data = Dataset.load_from_df(df[["user_id", "doctor_id", "rating"]], reader)

# === STEP 3: Train-Test Split ===
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# === STEP 4: Build and Train the Model ===
model = SVD()
model.fit(trainset)

# === STEP 5: Evaluate the Model ===
predictions = model.test(testset)
print("\nModel evaluation:")
accuracy.rmse(predictions)

# === STEP 6: Save the Model ===
joblib.dump(model, "collaborative_model.pkl")
print("\n✅ Trained collaborative filtering model saved as 'collaborative_model.pkl'")

# === STEP 7: Function to Recommend Doctors for a User ===
def recommend_doctors(user_id, doctor_ids, n=5):
    # Predict ratings for all doctors for the given user
    preds = [
        (doctor_id, model.predict(user_id, doctor_id).est)
        for doctor_id in doctor_ids
    ]
    # Sort by predicted rating, descending
    preds.sort(key=lambda x: x[1], reverse=True)
    return preds[:n]

# Example usage:
unique_doctors = df['doctor_id'].unique()
user_to_recommend = df['user_id'].iloc[0]
recommendations = recommend_doctors(user_to_recommend, unique_doctors)
print(f"\nTop recommendations for user {user_to_recommend}:")
for doc_id, pred_rating in recommendations:
    print(f"Doctor {doc_id}: predicted rating {pred_rating:.2f}") 