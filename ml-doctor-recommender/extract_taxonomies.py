import json

with open('final_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

taxonomies = set()
for entry in data:
    if isinstance(entry, list) and len(entry) == 2:
        city_data = entry[1]
        if city_data and 'results' in city_data and isinstance(city_data['results'], list):
            for doc in city_data['results']:
                for tax in doc.get('taxonomies', []):
                    desc = tax.get('desc')
                    if desc:
                        taxonomies.add(desc.strip())

for t in sorted(taxonomies):
    print(t) 