import pandas as pd

# Load the data
df = pd.read_excel('Specialist_perfect.xlsx')

print("Dataset shape:", df.shape)
print("\nAll columns:")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

# Find the target column (likely the last one or one with 'specialist' in name)
print("\nLooking for target column...")
target_col = None
for col in df.columns:
    if 'specialist' in col.lower():
        target_col = col
        break

if target_col:
    print(f"\nTarget column found: {target_col}")
    print(f"Unique values: {df[target_col].unique()}")
    print(f"Value counts:")
    print(df[target_col].value_counts().head(10))
else:
    print("\nNo specialist column found. Last column might be target:")
    last_col = df.columns[-1]
    print(f"Last column: {last_col}")
    print(f"Unique values: {df[last_col].unique()}")
    print(f"Value counts:")
    print(df[last_col].value_counts().head(10)) 