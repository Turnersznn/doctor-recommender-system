import json

with open("final_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

examples = []
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
                    # Get location
                    location = ''
                    if doc.get('addresses') and isinstance(doc['addresses'], list):
                        loc = next((a for a in doc['addresses'] if a.get('address_purpose') == 'LOCATION'), None)
                        if loc:
                            location = f"{loc.get('address_1', '')} {loc.get('city', '')} {loc.get('state', '')}".strip()
                    examples.append({
                        'name': name,
                        'specialty': desc,
                        'location': location
                    })
                    if len(examples) >= 10:
                        break
        if len(examples) >= 10:
            break

print("Example doctors with 'Ophthalmology' in taxonomy:")
for doc in examples:
    print(doc) 