# Load and inspect the content of the uploaded TSV file
import pandas as pd

# Load the TSV file into a DataFrame
file_path = 'theme_year_count_format_themelabel.tsv'
data = pd.read_csv(file_path, sep='\t')

# Display the first few rows and basic info to understand the structure
data.head(), data.info()


import matplotlib.pyplot as plt
import seaborn as sns

# Ensure proper display of non-ASCII characters in plots
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.unicode_minus"] = False

# Aggregate data: total counts of formats over time
format_trends = data.groupby(['period', 'formatCategory'])['count'].sum().reset_index()

# Pivot data for visualization
format_pivot = format_trends.pivot(index='period', columns='formatCategory', values='count').fillna(0)

# Plot trends of formats over time
plt.figure(figsize=(12, 6))
format_pivot.plot(kind='line', marker='o', linewidth=2, figsize=(12, 6))
plt.title('Bookformats over Time', fontsize=16)
plt.xlabel('Period', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.legend(title='Format Category', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Analyze top themes by format category
top_themes = data.groupby(['formatCategory', 'themeLabel'])['count'].sum().reset_index()
top_themes = top_themes.sort_values(by=['formatCategory', 'count'], ascending=[True, False])

# Plot top 5 themes per format category
plt.figure(figsize=(12, 8))
sns.barplot(
    data=top_themes.groupby('formatCategory').head(5),
    x='count',
    y='themeLabel',
    hue='formatCategory',
    dodge=False
)
plt.title('Themes per Bookformat', fontsize=16)
plt.xlabel('Total Count', fontsize=12)
plt.ylabel('Theme Label', fontsize=12)
plt.legend(title='Format Category', fontsize=10)
plt.tight_layout()
plt.show()
