from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

# Definiere SPARQL-Endpunkt
sparql_endpoint = "https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql"

# Definiere die SPARQL-Abfrage
sparql_query = """
PREFIX wd: <http://data.mimotext.uni-trier.de/entity/>
PREFIX wdt: <http://data.mimotext.uni-trier.de/prop/direct/>

SELECT (str(SAMPLE(year(?date))) as ?year) ((COUNT(?placelabel) / ?totalplaces) * 100 as ?proportion) ?placelabel 
WHERE {
  {
    SELECT (COUNT(?placelabel) as ?totalplaces) ?date
    WHERE {
      ?item wdt:P32 ?place.
      ?place rdfs:label ?placelabel.
      ?item wdt:P9 ?date.
      FILTER(LANG(?placelabel) = "en")
      BIND(str(year(?date)) as ?year)
    }
    GROUP BY ?date
  }
  
  ?item wdt:P32 ?place.
  ?place rdfs:label ?placelabel.
  ?item wdt:P9 ?date.
  FILTER(CONTAINS(LCASE(?placelabel), "rural"))
  FILTER(LANG(?placelabel) = "en")
  BIND(str(year(?date)) as ?year)
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}

GROUP BY ?placelabel ?year ?totalplaces
"""

# Führe die SPARQL-Abfrage aus
sparql = SPARQLWrapper(sparql_endpoint)
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Extrahiere die Ergebnisse und überführe sie in ein DataFrame
data = []
for result in results["results"]["bindings"]:
    year = int(result["year"]["value"])
    proportion = float(result["proportion"]["value"])
    placelabel = result["placelabel"]["value"]
    data.append({"year": year, "proportion": proportion, "placelabel": placelabel})

df = pd.DataFrame(data)

# Plotten der Daten
plt.figure(figsize=(10, 6))
sns.lineplot(x='year', y='proportion', data=df, marker='o')
plt.title("Proportion of 'rural area' as narrative location over the years")
plt.xlabel("Year")
plt.ylabel("Proportion (%)")
plt.grid(True)
plt.show()

# Lineare Regression zur Bestimmung des Trends
slope, intercept, r_value, p_value, std_err = linregress(df['year'], df['proportion'])

print(f"Slope: {slope}")
print(f"Intercept: {intercept}")
print(f"R-squared: {r_value**2}")
print(f"P-value: {p_value}")

# Interpretation der Ergebnisse
if p_value < 0.05:
    print("The decrease in the proportion of 'rural' placelabels over the years is statistically significant.")
else:
    print("The decrease in the proportion of 'rural' placelabels over the years is not statistically significant.")
