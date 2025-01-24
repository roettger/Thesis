# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'theme_year_count_format_themelabel.tsv'
data = pd.read_csv(file_path, sep='\t')

# Display basic information about the dataset
print("Dataset Info:")
print(data.info())
print("\nFirst Few Rows:")
print(data.head())

# 1. Analyze trends in book formats over time
format_trends = data.groupby(['period', 'formatCategory'])['count'].sum().reset_index()

# Pivot data for visualization
format_pivot = format_trends.pivot(index='period', columns='formatCategory', values='count').fillna(0)

# Plot trends of book formats over time
plt.figure(figsize=(12, 6))
format_pivot.plot(kind='line', marker='o', linewidth=2, figsize=(12, 6))
plt.title('Trends of Book Formats Over Time', fontsize=16)
plt.xlabel('Period', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.legend(title='Format Category', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# 2. Analyze the most common themes by format category
top_themes = data.groupby(['formatCategory', 'themeLabel'])['count'].sum().reset_index()
top_themes = top_themes.sort_values(by=['formatCategory', 'count'], ascending=[True, False])

# Plot the top 5 themes per format category
plt.figure(figsize=(12, 8))
sns.barplot(
    data=top_themes.groupby('formatCategory').head(5),
    x='count',
    y='themeLabel',
    hue='formatCategory',
    dodge=False
)
plt.title('Top 5 Themes by Format Category', fontsize=16)
plt.xlabel('Total Count', fontsize=12)
plt.ylabel('Theme Label', fontsize=12)
plt.legend(title='Format Category', fontsize=10)
plt.tight_layout()
plt.show()

# 3. Analyze co-occurrence of formats and themes in a heatmap
co_occurrence = data.groupby(['formatCategory', 'themeLabel'])['count'].sum().unstack().fillna(0)

plt.figure(figsize=(14, 8))
sns.heatmap(co_occurrence, cmap="Blues", annot=False, cbar=True)
plt.title('Co-occurrence of Book Formats and Themes', fontsize=16)
plt.xlabel('Theme Label', fontsize=12)
plt.ylabel('Format Category', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
