import pandas as pd
import random

# Simulate 50 users and 20 doctors
num_users = 50
num_doctors = 20

# Doctor IDs from 101 to 120
doctor_ids = list(range(101, 101 + num_doctors))

# Generate interaction data
interactions = []

for user_id in range(1, num_users + 1):
    sampled_doctors = random.sample(doctor_ids, random.randint(3, 7))
    for doctor_id in sampled_doctors:
        rating = random.randint(3, 5)  # 3 = normal, 5 = highly engaged
        interactions.append({
            'user_id': user_id,
            'doctor_id': doctor_id,
            'rating': rating
        })

# Save as CSV
df = pd.DataFrame(interactions)
df.to_csv("user_doctor_ratings.csv", index=False)

print("✅ Interaction data generated and saved as 'user_doctor_ratings.csv'")
