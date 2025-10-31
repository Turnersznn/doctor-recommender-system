import pandas as pd

# Load the training data
df = pd.read_excel("Specialist_clean_clinical.xlsx")

# Check itching
itching_rows = df[df['itching'] == 1]
print("Itching rows:")
print(itching_rows['Specialist'].value_counts())

# Check headache
headache_rows = df[df['headache'] == 1]
print("\nHeadache rows:")
print(headache_rows['Specialist'].value_counts())

# Check if there are any rows where itching is 1 and specialist is Ophthalmologist
itching_ophthalmologist = df[(df['itching'] == 1) & (df['Specialist'] == 'Ophthalmologist')]
print(f"\nRows with itching=1 and Ophthalmologist: {len(itching_ophthalmologist)}")

# Check if there are any rows where headache is 1 and specialist is Ophthalmologist
headache_ophthalmologist = df[(df['headache'] == 1) & (df['Specialist'] == 'Ophthalmologist')]
print(f"Rows with headache=1 and Ophthalmologist: {len(headache_ophthalmologist)}") 