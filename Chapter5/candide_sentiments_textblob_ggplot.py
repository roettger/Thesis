import requests
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import pandas as pd
from nltk import sent_tokenize
from plotnine import *

def fetch_text_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Fehler beim Abrufen des Textes von GitHub.")
        return None

github_url = "https://raw.githubusercontent.com/MiMoText/roman18/master/plain/files/Voltaire_Candide.txt"
voltaire_candide = fetch_text_from_github(github_url)

# Erstelle ein TextBlob-Objekt aus dem Text
voltaire_candide = TextBlob(voltaire_candide)

# Teile den Text anhand des Strings 'Chapitre'
voltaire_candideParts = voltaire_candide.split('CHAPITRE')

# Nimm alle Kapitel
allChapters = voltaire_candideParts[1:]  # skip 'CHAPITRE'
allBlobs = [TextBlob(text).sentiment for text in allChapters]

# Polarität pro Chapter
allSentiments = [item.polarity for item in allBlobs]

# Erstelle ein DataFrame für die Kapitel und deren Polarität
chapters_df = pd.DataFrame({
    'Chapter': ['Chapitre {}'.format(i) for i in range(1, len(allSentiments) + 1)],
    'Polarity': allSentiments
})

# Setze die Chapter-Spalte als kategorisch und ordne sie nach der Zahl
chapters_df['Chapter'] = pd.Categorical(chapters_df['Chapter'], 
                                         categories=['Chapitre {}'.format(i) for i in range(1, len(allSentiments) + 1)], 
                                         ordered=True)

# Visualisiere die Polarität mit ggplot 
plot = (ggplot(chapters_df, aes(x='Chapter', y='Polarity')) +
        geom_bar(stat='identity') +
        geom_smooth(method='lm', span=0.3, color='red', se=True) +
        labs(title='Sentiment Analysis with Textblob: Candide', x='Chapter', y='Polarity') +
        theme(axis_text_x=element_text(rotation=45, hjust=1)))

# Zeige den Plot an
print(plot)

# Speichern des Plots in einer Datei mit 300 DPI
plot.save("candide_sentiment_analysis.png", dpi=300)

print("Plot wurde gespeichert.")
