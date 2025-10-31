import pandas as pd

# Check training data feature columns
train_df = pd.read_excel("Specialist_clean_clinical.xlsx")
train_features = [col for col in train_df.columns if col != 'Specialist']
print(f"Training data has {len(train_features)} features")
print("First 10 training features:", train_features[:10])

# Check if 'itching' and 'headache' are in training features
print(f"\n'itching' in training features: {'itching' in train_features}")
print(f"'headache' in training features: {'headache' in train_features}")

# Check the actual column names (case sensitivity, spaces, etc.)
itching_cols = [col for col in train_features if 'itch' in col.lower()]
headache_cols = [col for col in train_features if 'head' in col.lower()]
print(f"\nColumns containing 'itch': {itching_cols}")
print(f"Columns containing 'head': {headache_cols}") 