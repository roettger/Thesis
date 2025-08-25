# pip install sparqlwrapper pandas matplotlib

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import matplotlib.pyplot as plt

# SPARQL-Endpoint
endpoint_url = "https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql"

# SPARQL-Abfrage
query = """
PREFIX mmd: <http://data.mimotext.uni-trier.de/entity/> 
PREFIX mmdt: <http://data.mimotext.uni-trier.de/prop/direct/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?date
       (COUNT(DISTINCT ?sensItem) AS ?countSentimental)
       (COUNT(DISTINCT ?allItem) AS ?countAll)
       (COUNT(DISTINCT ?sensItem)/COUNT(DISTINCT ?allItem)*100 AS ?rel)
WHERE {
  ?allItem mmdt:P9 ?date; mmdt:P36 ?topicAll .
  ?topicAll rdfs:label ?topicAllLabel .
  FILTER(lang(?topicAllLabel) = "en")
  
  OPTIONAL {
    ?sensItem mmdt:P9 ?date; mmdt:P38 ?topicSens .
    ?topicSens rdfs:label ?topicSensLabel .
    FILTER(lang(?topicSensLabel) = "en")
    FILTER(LCASE(STR(?topicSensLabel)) = "sensibility")
  }
}
GROUP BY ?date
ORDER BY ?date
"""

# SPARQL-Abfrage ausführen
def fetch_sparql(endpoint, query):
    sparql = SPARQLWrapper(endpoint, agent="Python/SPARQLWrapper")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

results = fetch_sparql(endpoint_url, query)

# Ergebnisse in DataFrame (nur Jahr extrahieren)
df = pd.DataFrame([
    {
        "date": int(r["date"]["value"][:4]),  # Jahr extrahieren
        "rel": float(r["rel"]["value"]),
        "count_sens": int(r["countSentimental"]["value"]),
        "count_all": int(r["countAll"]["value"])
    }
    for r in results["results"]["bindings"]
]).sort_values("date")

# Visualisierung
# Visualisierung mit Linie um die Bars
plt.figure(figsize=(12,6))

# Bars mit schwarzer Kontur
plt.bar(df["date"], df["rel"], color="salmon", edgecolor="black", linewidth=1.5)

plt.xlabel("Year")
plt.ylabel("Relative frequency (%)")
plt.title('Evolution of "sensibility" theme in French novels (1751-1800)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

