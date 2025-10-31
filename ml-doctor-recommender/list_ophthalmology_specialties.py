import json

with open("final_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

specialties = set()
for entry in data:
    if isinstance(entry, list) and len(entry) > 1 and 'results' in entry[1]:
        for doc in entry[1]['results']:
            for tax in doc.get('taxonomies', []):
                desc = tax.get('desc')
                if desc and 'ophthalmology' in desc.lower():
                    specialties.add(desc)

print("Unique taxonomy descriptions containing 'Ophthalmology':")
for s in sorted(specialties):
    print(f"- {s}") 