import folium
import pandas as pd
from folium import plugins
import base64


def create_map():
    # Lire les fichiers CSV
    stations = pd.read_csv("stations.csv", delimiter=";")
    relations = pd.read_csv("relations.csv", delimiter=";")

    # Créer une carte centrée sur Paris
    map_paris = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Dictionnaire de couleurs pour chaque ligne de métro
    colors = {"1": "#FFCD00", "2": "#003CA6", "3": "#837902", "3b": "#6EC4E8", "4": "#BE5C00", "5": "#FF7E2E", "6": "#6ECA97", "7": "#FA9ABA", "7b": "#6ECA97", "8": "#E19BDF", "9": "#B6BD00", "10": "#C9910D", "11": "#704B1C", "12": "#007852", "13": "#6ECA97", "14": "#62259D",  "RER_A": "#B9006E",  "RER_B": "#006E51",  "RER_C": "#FCCC0A", "RER_D": "#932A85", "RER_E": "#9F973D"}

    # Ajouter des marqueurs pour chaque station de métro
    for index, row in stations.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        name = row['nom']
        line = row['ligne']
        terminus = row['terminus']
        popup_text = f"{name}"
        if line in colors:
            if line not in ["RER_A", "RER_B", "RER_C", "RER_D", "RER_E"]:
                icon_url = f"https://cdn.pixabay.com/photo/2012/04/23/17/06/metro-39112_960_720.png"  # Remplacez cette URL par l'URL de l'icône de métro correspondant à la ligne
                icon = folium.CustomIcon(icon_url, icon_size=(17, 17))
                marker = folium.Marker([lat, lon], icon=icon)
                marker.add_child(folium.Tooltip(popup_text))
                marker.add_to(map_paris)
            else:
                icon_url = f"https://upload.wikimedia.org/wikipedia/commons/archive/1/13/20170116163948%21RER.svg"  # Remplacez cette URL par l'URL de l'icône de métro correspondant à la ligne
                icon = folium.CustomIcon(icon_url, icon_size=(17, 17))
                marker = folium.Marker([lat, lon], icon=icon)
                marker.add_child(folium.Tooltip(popup_text))
                marker.add_to(map_paris)
            

    # Ajouter des tracés entre les stations de métro
    for index, row in relations.iterrows():
        id1 = row['id1']
        id2 = row['id2']
        station1 = stations.loc[stations['id'] == id1]
        station2 = stations.loc[stations['id'] == id2]
        lat1 = station1['latitude'].values[0]
        lon1 = station1['longitude'].values[0]
        lat2 = station2['latitude'].values[0]
        lon2 = station2['longitude'].values[0]
        line1 = station1['ligne'].values[0]
        line2 = station2['ligne'].values[0]
        if line1 in colors and line2 in colors and line1 == line2:
            color = colors[line1]
            folium.PolyLine([(lat1, lon1), (lat2, lon2)], color=color, weight=5.5).add_to(map_paris)

    #Déclarer où se trouve l'image
    chemin_image = "légende.png"

    # Lire le fichier d'image en tant que bytes
    with open(chemin_image, "rb") as f:
        donnees_image = f.read()

    # Encoder les données de l'image en base64
    légende = base64.b64encode(donnees_image).decode("utf-8")

    # Générer le HTML de la légende avec l'image locale
    legend_html = f'''
    <div style="position: fixed;
                bottom: 320px; left: 50px; width: 200px; height: 110px;
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; opacity:0.9">
        <div style="display: flex; justify-content: space-around; align-items: center;">
            <img src="data:image/png;base64,{légende}" alt="Image de la légende" width="100%" height="100%">
        </div>
    </div>
'''


    map_paris.get_root().html.add_child(folium.Element(legend_html))

    # Ajouter le plugin MousePosition pour afficher les pop-ups au survol
    plugins.MousePosition().add_to(map_paris)

    # Afficher la carte
    map_paris = map_paris._repr_html_()
    return map_paris

def create_map_with_path(shortest_path):
    # Lire les fichiers CSV
    stations = pd.read_csv("stations.csv", delimiter=";")
    relations = pd.read_csv("relations.csv", delimiter=";")

    # Créer une carte centrée sur Paris
    map_paris = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Dictionnaire de couleurs pour chaque ligne de métro
    colors = {"1": "#FFCD00", "2": "#003CA6", "3": "#837902", "3b": "#6EC4E8", "4": "#BE5C00", "5": "#FF7E2E", "6": "#6ECA97", "7": "#FA9ABA", "7b": "#6ECA97", "8": "#E19BDF", "9": "#B6BD00", "10": "#C9910D", "11": "#704B1C", "12": "#007852", "13": "#6ECA97", "14": "#62259D"}

    # Ajouter des marqueurs pour chaque station de métro
    for index, row in stations.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        name = row['nom']
        line = row['ligne']
        terminus = row['terminus']
        popup_text = f"{name}"
        if name in shortest_path:
            if line not in ["RER_A", "RER_B", "RER_C", "RER_D", "RER_E"]:
                icon_url = f"https://cdn.pixabay.com/photo/2012/04/23/17/06/metro-39112_960_720.png"  # Remplacez cette URL par l'URL de l'icône de métro correspondant à la ligne
                icon = folium.CustomIcon(icon_url, icon_size=(17, 17))
                marker = folium.Marker([lat, lon], icon=icon)
                marker.add_child(folium.Tooltip(popup_text))
                marker.add_to(map_paris)
            else:
                icon_url = f"https://upload.wikimedia.org/wikipedia/commons/archive/1/13/20170116163948%21RER.svg"  # Remplacez cette URL par l'URL de l'icône de métro correspondant à la ligne
                icon = folium.CustomIcon(icon_url, icon_size=(17, 17))
                marker = folium.Marker([lat, lon], icon=icon)
                marker.add_child(folium.Tooltip(popup_text))
                marker.add_to(map_paris)
    # Ajouter des tracés entre les stations de métro du chemin le plus court
    for i in range(len(shortest_path) - 1):
        station1 = shortest_path[i]
        station2 = shortest_path[i+1]
        station1_info = stations.loc[stations['nom'] == station1]
        station2_info = stations.loc[stations['nom'] == station2]
        lat1 = station1_info['latitude'].values[0]
        lon1 = station1_info['longitude'].values[0]
        lat2 = station2_info['latitude'].values[0]
        lon2 = station2_info['longitude'].values[0]
        folium.PolyLine([(lat1, lon1), (lat2, lon2)], color='#0080FF', weight=5.5).add_to(map_paris)

    # Ajouter le plugin MousePosition pour afficher les pop-ups au survol
    plugins.MousePosition().add_to(map_paris)

    # Afficher la carte
    map_paris = map_paris._repr_html_()
    return map_paris

