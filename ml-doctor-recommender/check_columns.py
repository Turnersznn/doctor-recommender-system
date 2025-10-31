import pandas as pd

# Load the data and check columns
df = pd.read_excel("Specialist.xlsx")
print("Columns in Specialist.xlsx:")
for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

print(f"\nTotal columns: {len(df.columns)}")
print(f"Sample data shape: {df.shape}") 