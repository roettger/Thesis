# Pakete laden
library(ggplot2)
library(tidyr)
library(dplyr)
library(readr)

# Daten einlesen
df <- read_delim("GitHub/Thesis/Chapter4/Lieux_BGRF - data_bgrf.tsv", 
                 delim = "\t", escape_double = FALSE, 
                 trim_ws = TRUE)

# Relevante Spalten auswählen und umbenennen
df_clean <- df %>%
  select(
    year,
    France = `(a) France`,
    Angleterre = `(b) Angleterre`,
    Pays_imaginaires = `(l) Pays imaginaires`,
    Allemagne = `(c) Allemagne`,
    Italie = `(d) Italie`,
    Espagne = `(e) Espagne`,
    Grèce = `(f) Grèce`,
    Autres_Europe = `(g) Autre pays d'Europe`,
    Egypte = `(h) Egypte`,
    Autres_Afrique = `(i) Autre pays d'Afrique`,
    Amérique = `(j) Amérique`,
    Orient = `(k)Orient`
  )

# Sicherstellen, dass year numerisch ist
df_clean$year <- as.numeric(df_clean$year)

# Prozente berechnen: alle Länder als Basis
df_pct <- df_clean %>%
  rowwise() %>%
  mutate(total = sum(c_across(-year), na.rm = TRUE)) %>%  # Summe über alle Länder
  mutate(across(-c(year, total), ~ ifelse(total > 0, .x / total * 100, 0))) %>%
  ungroup() %>%
  select(-total)

# Long-Format für ggplot (nur die interessanten Länder)
df_long <- df_pct %>%
  pivot_longer(cols = c("France", "Angleterre", "Pays_imaginaires"),
               names_to = "Lieu", values_to = "Percent") %>%
  mutate(Lieu = ifelse(Lieu == "Pays_imaginaires", "Pays imaginaires", Lieu))

# Visualisierung
ggplot(df_long, aes(x = year, y = Percent)) +
  geom_line(color = "steelblue", size = 1.2) +
  facet_wrap(~Lieu, ncol = 1) +
  labs(title = " ",
       x = "Jahr", y = "Anteil (%) an allen Orten") +
  theme_minimal() +
  theme(strip.text = element_text(size = 12, face = "bold"))




df_long %>%
  filter(year == 1775) %>%
  select(year, Lieu, Percent)


