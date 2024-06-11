from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import matplotlib.pyplot as plt

# SPARQL endpoint URL
sparql_endpoint = "https://query.mimotext.uni-trier.de/proxy/wdqs/bigdata/namespace/wdq/sparql"

# SPARQL query
sparql_query = """
prefix wd:<http://data.mimotext.uni-trier.de/entity/> 
prefix wdt:<http://data.mimotext.uni-trier.de/prop/direct/> 

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
HAVING (COUNT(?placelabel) > 2)
ORDER BY ?year
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
    year = binding['year']['value']
    proportion = float(binding['proportion']['value'])
    placelabel = binding['placelabel']['value']
    sparql_data.append({'year': year, 'proportion': proportion, 'placelabel': placelabel})
df = pd.DataFrame(sparql_data)

# Plotting
plt.figure(figsize=(10, 6))
for label, df_group in df.groupby('placelabel'):
    plt.bar(df_group['year'], df_group['proportion'], label=label, color='grey')
#plt.title('Narrative location "Rural Area" in French Novels (1751-1800)')
plt.xlabel('Year')
plt.ylabel('Proportion (%)')
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot with high resolution
plt.savefig('rural_area_french_novels.png', dpi=300)
plt.show()
