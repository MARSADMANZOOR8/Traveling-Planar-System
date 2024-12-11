from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

class Graph:
    def __init__(self):
        self.graph = {}

    def add_location(self, location):
        if location not in self.graph:
            self.graph[location] = []

    def add_route(self, start, end, distance, time, cost):
        self.graph[start].append((end, distance, time, cost))
        self.graph[end].append((start, distance, time, cost))

    def dijkstra(self, start, end, weight_type='distance'):
        weight_index = {'distance': 1, 'time': 2, 'cost': 3}.get(weight_type, 1)
        pq = [(0, start)]
        distances = {start: 0}
        parents = {start: None}

        while pq:
            current_distance, current_location = heapq.heappop(pq)

            if current_location == end:
                path = []
                while current_location:
                    path.append(current_location)
                    current_location = parents[current_location]
                return path[::-1], current_distance

            for neighbor, distance, time, cost in self.graph[current_location]:
                weight = (distance, time, cost)[weight_index - 1]
                new_distance = current_distance + weight
                if neighbor not in distances or new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parents[neighbor] = current_location
                    heapq.heappush(pq, (new_distance, neighbor))

        return None, float('inf')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_route', methods=['POST'])
def get_route():
    start = request.form['start']
    end = request.form['end']
    preference = request.form['preference']

    graph = Graph()

    locations = ['CityA', 'CityB', 'CityC', 'CityD', 'CityE']
    for location in locations:
        graph.add_location(location)

    graph.add_route('CityA', 'CityB', distance=50, time=30, cost=100)
    graph.add_route('CityA', 'CityC', distance=80, time=50, cost=150)
    graph.add_route('CityB', 'CityD', distance=60, time=40, cost=120)
    graph.add_route('CityC', 'CityD', distance=30, time=20, cost=60)
    graph.add_route('CityD', 'CityE', distance=90, time=60, cost=180)

    route, total_cost = graph.dijkstra(start, end, weight_type=preference)

    if route:
        return render_template('index.html', route=route, total_cost=total_cost, preference=preference)
    else:
        return render_template('index.html', error="No route found between the selected cities.")

if __name__ == "__main__":
    app.run(debug=True)
