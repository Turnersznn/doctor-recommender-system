import pandas as pd

print("=== EXPLORING DOCTOR RECOMMENDER DATASETS ===\n")

# Let's look at each file one by one
files = [
    'Disease_Description.csv',
    'Doctor_Specialist.csv', 
    'Doctor_Versus_Disease.csv',
    'Original_Dataset.csv',
    'Symptom_Weights.csv'
]

for file in files:
    try:
        print(f"--- {file} ---")
        data = pd.read_csv(file)
        print(f"Shape: {data.shape}")
        print(f"Columns: {data.columns.tolist()}")
        print("First few rows:")
        print(data.head(3))
        print("\n" + "="*50 + "\n")
    except Exception as e:
        print(f"Error reading {file}: {e}\n")

# Let's also check the Excel file
try:
    print("--- Specialist.xlsx ---")
    excel_data = pd.read_excel('Specialist.xlsx')
    print(f"Shape: {excel_data.shape}")
    print(f"Columns: {excel_data.columns.tolist()}")
    print("First few rows:")
    print(excel_data.head(3))
except Exception as e:
    print(f"Error reading Specialist.xlsx: {e}")