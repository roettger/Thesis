import folium

# Create a map centered at a specific location
map = folium.Map(location=[20, 0], zoom_start=2)

# Add markers to the map based on the provided data
data = {
    "Le palais du silence": (23.0, 38.5),
    "Le diable amoureux": (12.331944444, 45.439722222),
    "Lieb-Rose": (29.743333333, 45.221944444),
    "La princesse de Babilone": (29.0, 27.0),
    "Le vieux de la montagne": (29.0, 27.0),
    "Numa Pompilius": (12.48, 41.89),
    "Ma-gakou": (74.043333, 15.401944),
    "Histoire de Fortunatus": (-1.0, 53.0),
    "Anecdotes de la cour de Bonhommie": (-9.183333333, 38.7),
    "Vathek": (43.151944444, 16.139722222),
    "Mirza et Fatmé": (83.0, 22.8),
    "Les folies philosophiques": (83.0, 22.8),
    "Lettres de deux amans, habitans d’une petite ville au pied des Alpes": (8.231973, 46.798562),
    "Ancienne chronique de Gérard d’Euphrate": (2.0, 47.0),
    "La cabane mystérieuse": (2.0, 47.0),
    "Le crocodile": (2.0, 47.0),
    "Le diable amoureux": (14.248611111, 40.835833333),
    "Seconde suite de l’Aventurier françois": (12.5, 42.5),
    "La princesse de Babilone": (44.5, 32.5),
    "Lieb-Rose": (7.1881, 21.09375),
    "L’Amérique découverte": (-3.5, 40.2),
    "Relation véridique qui a l’air d’un songe": (26.683611, 40.343889),
    "Les deux cousins": (52.0, 30.0),
    "Lettres de deux amans, habitans d’une petite ville au pied des Alpes": (-0.1275, 51.507222222),
    "Les hauts faits d’Esplandian": (28.98, 41.0125),
    "Lisvart de Grèce": (28.98, 41.0125)
}

for label, coords in data.items():
    folium.Marker(location=coords, popup=label).add_to(map)

# Save the map
map.save("map.html")
