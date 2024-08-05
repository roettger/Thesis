import requests
import pandas as pd
from geopy.distance import geodesic
from scipy.stats import ttest_rel

# SPARQL-Abfrage
query = """
SELECT ?author ?authorLabel ?mimoTextId ?geobirth ?geodeath WHERE {
  ?author wdt:P31 wd:Q5.
  ?author wdt:P12047 ?mimoTextId.     # MiMOText-ID
  ?author wdt:P19 ?birthplace. 
  ?author wdt:P20 ?deathplace. 
  ?birthplace wdt:P625 ?geobirth.
  ?deathplace wdt:P625 ?geodeath.
  SERVICE wikibase:label {           # Einschließen von Labels in der Abfrage
    bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en".
  }
}
"""

url = 'https://query.wikidata.org/sparql'
headers = {
    'User-Agent': 'Mozilla/5.0',
    'Accept': 'application/sparql-results+json'
}

# Anfrage senden
response = requests.get(url, headers=headers, params={'query': query})
data = response.json()

# Datenframe erstellen
results = data['results']['bindings']
authors = []
for result in results:
    author = result['authorLabel']['value']
    geobirth = result['geobirth']['value'][6:-1].split()
    geodeath = result['geodeath']['value'][6:-1].split()
    authors.append({
        'author': author,
        'birth_lat': float(geobirth[1]),
        'birth_lon': float(geobirth[0]),
        'death_lat': float(geodeath[1]),
        'death_lon': float(geodeath[0])
    })

df = pd.DataFrame(authors)

# Koordinaten von Paris
paris_coords = (48.8566, 2.3522)

# Entfernungen berechnen
df['birth_distance_to_paris'] = df.apply(lambda row: geodesic((row['birth_lat'], row['birth_lon']), paris_coords).km, axis=1)
df['death_distance_to_paris'] = df.apply(lambda row: geodesic((row['death_lat'], row['death_lon']), paris_coords).km, axis=1)

# T-Test durchführen
t_stat, p_value = ttest_rel(df['birth_distance_to_paris'], df['death_distance_to_paris'])

# Ergebnisse ausgeben
print(f"T-Statistik: {t_stat}")
print(f"P-Wert: {p_value}")
if p_value < 0.05:
    print("Die Todesorte sind statistisch signifikant näher an Paris als die Geburtsorte.")
else:
    print("Es gibt keinen statistisch signifikanten Unterschied zwischen den Entfernungen der Geburts- und Todesorte zu Paris.")
