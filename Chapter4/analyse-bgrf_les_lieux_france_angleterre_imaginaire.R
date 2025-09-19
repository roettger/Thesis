# Frankreich
p1 <- ggplot(filter(df_long, Lieu == "France"), aes(x = year, y = Percent)) +
  geom_line(color = "steelblue", size = 1.2) +
  labs(title = "France", x = "Jahr", y = "Anteil (%)") +
  theme_minimal()

ggsave("plot_france.png", p1, width = 7, height = 5, dpi = 300)

# Angleterre
p2 <- ggplot(filter(df_long, Lieu == "Angleterre"), aes(x = year, y = Percent)) +
  geom_line(color = "steelblue", size = 1.2) +
  labs(title = "Angleterre", x = "Jahr", y = "Anteil (%)") +
  theme_minimal()

ggsave("plot_angleterre.png", p2, width = 7, height = 5, dpi = 300)

# Pays imaginaires
p3 <- ggplot(filter(df_long, Lieu == "Pays imaginaires"), aes(x = year, y = Percent)) +
  geom_line(color = "steelblue", size = 1.2) +
  labs(title = "Pays imaginaires", x = "Jahr", y = "Anteil (%)") +
  theme_minimal()

ggsave("plot_pays_imaginaires.png", p3, width = 7, height = 5, dpi = 300)
