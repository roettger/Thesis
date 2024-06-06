import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON
import matplotlib.pyplot as plt
import seaborn as sns

# SPARQL-Endpunkt definieren
sparql_endpoint = "https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql"
sparql = SPARQLWrapper(sparql_endpoint)

# SPARQL-Query
query = """
PREFIX wd:<http://data.mimotext.uni-trier.de/entity/>
PREFIX wdt:<http://data.mimotext.uni-trier.de/prop/direct/> 
Select ?year ?placelabel(count(*) as ?countyear) 
   WHERE{
   ?item wdt:P10 ?place.
   ?place rdfs:label ?placelabel .
   ?item wdt:P9 ?date .
   FILTER(lang(?placelabel) = "fr")
   BIND(str(year(?date)) as ?year)
   SERVICE wikibase:label {bd:serviceParam wikibase:language "{AUTO_LANGUAGE}","fr" .}
  }

GROUP BY ?year ?placelabel
having (?countyear > 1)
ORDER BY asc(?year) desc(?placelabel)
"""

# SPARQL-Query ausführen
sparql.setQuery(query)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# Ergebnisse in ein Pandas DataFrame umwandeln
data = []
for result in results["results"]["bindings"]:
    year = result["year"]["value"]
    placelabel = result["placelabel"]["value"]
    data.append({"year": year, "placelabel": placelabel})

df = pd.DataFrame(data)

# Daten visualisieren
plt.figure(figsize=(12, 8))
sns.scatterplot(data=df, x="year", y="placelabel", hue="placelabel", marker='s', s=100, legend=None, palette="tab20")


#plt.title("Publikationsorte pro Jahr")
plt.xlabel("Year")
plt.ylabel("Place of publication")
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot with high resolution
plt.savefig('places_of_publication.png', dpi=300)
plt.show()
