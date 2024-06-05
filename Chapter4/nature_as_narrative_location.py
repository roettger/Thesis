from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import matplotlib.pyplot as plt

# SPARQL endpoint URL
sparql_endpoint = "https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql"

# SPARQL query
sparql_query = """
prefix wd:<http://data.mimotext.uni-trier.de/entity/>
prefix wdt:<http://data.mimotext.uni-trier.de/prop/direct/>
prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?date (?countNature / ?countAll AS ?rel)
WHERE {
 {  
   SELECT ?date (count(*) AS ?countNature)
   WHERE {
     ?item wdt:P9 ?date;
           wdt:P36 ?topic .
     ?topic rdfs:label ?topicLabel .
     filter(lang(?topicLabel) = "en")
     filter(lcase(?topicLabel) = "nature"@en)
   }
   GROUP BY ?date
 }
 {
   SELECT ?date (count(*) AS ?countAll)
   WHERE {
     ?item wdt:P9 ?date;
         wdt:P36 ?topic .
     ?topic rdfs:label ?topicLabel .
     filter(lang(?topicLabel) = "en")
   }
   GROUP BY ?date
 }
}
ORDER BY ?date
"""

# Initialize SPARQLWrapper
sparql = SPARQLWrapper(sparql_endpoint)
sparql.setQuery(sparql_query)
sparql.setReturnFormat(JSON)

# Execute the query and parse the results
sparql_results = sparql.query().convert()

# Convert SPARQL results to a DataFrame
bindings = sparql_results['results']['bindings']
sparql_data = []
for binding in bindings:
    date = binding['date']['value']
    rel = float(binding['rel']['value'])
    sparql_data.append({'date': date, 'rel': rel})
df = pd.DataFrame(sparql_data)

# Convert date column to datetime type
df['date'] = pd.to_datetime(df['date'])

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['rel'], marker='o')
plt.title('Nature as a narrative place in French Novels 1751-1800')
plt.xlabel('year')
plt.ylabel('ratio')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot with high resolution
plt.savefig('nature_narrat_french_novels.png', dpi=300)
plt.show()
