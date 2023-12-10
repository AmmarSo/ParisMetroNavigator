from flask import Flask, render_template, request
import pandas as pd
from graph import Graph
from carte import create_map, create_map_with_path


app = Flask(__name__)

stations = pd.read_csv('stations.csv', delimiter=';')
relations = pd.read_csv('relations.csv', delimiter=';')

graph = Graph()

for index, row in stations.iterrows():
    graph.add_node(row['nom'])

for index, row in relations.iterrows():
    id1 = row['id1']
    id2 = row['id2']
    station1 = stations.loc[stations['id'] == id1]['nom'].values[0]
    station2 = stations.loc[stations['id'] == id2]['nom'].values[0]
    graph.add_edge(station1, station2, row['temps'])

# Stocker nom et ligne dans le datatframe
stations['nom_ligne'] = stations['nom'] + ' ' + stations['ligne']

@app.route('/', methods=['GET', 'POST'])
def index():
    map_html = create_map()
    if request.method == 'POST':
        start_station = request.form['start_station']
        end_station = request.form['end_station']
        shortest_distances, shortest_paths = graph.bellman_ford(start_station)
        shortest_distance = shortest_distances[end_station]
        shortest_path = shortest_paths[end_station]
        map_html = create_map_with_path(shortest_path)
        return render_template('index.html', stations=stations['nom_ligne'].values, shortest_distance=shortest_distance, shortest_path=shortest_path, map_html=map_html)
    return render_template('index.html', stations=stations['nom_ligne'].values, map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)
