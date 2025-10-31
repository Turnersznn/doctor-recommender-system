import json

with open("final_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ophthalmology_doctors = []
for entry in data:
    if isinstance(entry, list) and len(entry) > 1 and 'results' in entry[1]:
        for doc in entry[1]['results']:
            for tax in doc.get('taxonomies', []):
                desc = tax.get('desc')
                if desc and 'ophthalmology' in desc.lower():
                    # Get name
                    name = ''
                    if doc.get('basic'):
                        name = doc['basic'].get('organization_name') or (
                            f"{doc['basic'].get('first_name', '')} {doc['basic'].get('last_name', '')}".strip()
                        )
                    ophthalmology_doctors.append({
                        'name': name,
                        'specialty': desc
                    })
                    if len(ophthalmology_doctors) >= 10:
                        break
        if len(ophthalmology_doctors) >= 10:
            break

print(f"Found {len(ophthalmology_doctors)} doctors with 'Ophthalmology' in their specialty:")
for doc in ophthalmology_doctors[:5]:
    print(f"- {doc['name']}: {doc['specialty']}") 