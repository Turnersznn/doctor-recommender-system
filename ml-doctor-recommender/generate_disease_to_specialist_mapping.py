import pandas as pd

df = pd.read_csv('Doctor_Versus_Disease.csv', encoding='latin1')
df.columns = ['Disease', 'Specialist']
mapping = dict(zip(df['Disease'].str.strip(), df['Specialist'].str.strip()))

print('const DISEASE_TO_SPECIALIST = {')
for disease, specialist in mapping.items():
    print(f'  \"{disease}\": \"{specialist}\",')
print('};') 