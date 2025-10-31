import pandas as pd

# Load the data
df = pd.read_excel('Specialist_perfect.xlsx')

print("Dataset shape:", df.shape)
print("\nColumns:", df.columns.tolist()[:10])
print("\nDisease column exists:", 'Disease' in df.columns)

if 'Disease' in df.columns:
    print("\nTop 10 diseases/conditions:")
    print(df['Disease'].value_counts().head(10))
    
    print("\nTotal unique diseases:", df['Disease'].nunique())
else:
    print("\nNo 'Disease' column found. Available columns:")
    for col in df.columns:
        if 'disease' in col.lower() or 'condition' in col.lower():
            print(f"- {col}") 