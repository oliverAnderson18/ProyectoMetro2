import networkx as nx
from math import radians, sin, cos, sqrt, atan2
import json
import sys
from datetime import datetime, timedelta
import math


def add_metro_network(graph, dict_stations):
	lines_metro_ids = [
		list(range(11, 19)),  # Línea A
		list(range(21, 27)),  # Línea B
		list(range(31, 40)),  # Línea C
		list(range(41, 46)),  # Línea D
		list(range(51, 57)),  # Línea E
	]

	for line in lines_metro_ids:
		for i in range(len(line) - 1):
			graph.add_edge(line[i], line[i+1], weight = dict_stations[line[i]]["time"])

	# Correspondencias (peso de 5 min)
	graph.add_edge(44, 23, weight=5)
	graph.add_edge(44, 36, weight=5)
	graph.add_edge(14, 35, weight=5)
	graph.add_edge(12, 45, weight=5)
	graph.add_edge(12, 56, weight=5)
	graph.add_edge(33, 54, weight=5)
	graph.add_edge(45, 56, weight=5)


def find_station_id_by_name(station_name, dict_stations):
	for station_id, station_info in dict_stations.items():
		if station_info["name"] == station_name:
			return station_id
	raise ValueError(f"Estación '{station_name}' no encontrada en el diccionario.")


def heuristic_metro_stations(current, destination, dict_stations, avg_velocity = 0.8333333333333334):
	def time_haversine(lat1, lon1, lat2, lon2):
		"""
		Calcula el tiempo estimado de viaje entre dos puntos geográficos usando la fórmula de Haversine.
		Parameters:
		lat1, lon1: Coordenadas (latitud y longitud) del punto inicial en grados.
		lat2, lon2: Coordenadas (latitud y longitud) del punto final en grados.
		velocidad_media: Velocidad media en kilómetros por minuto.
		Returns:
		float: Tiempo estimado en minutos entre los dos puntos.
		"""
		# Radio de la Tierra en kilómetros
		r = 6371.0

		# Convertir coordenadas de grados a radianes
		lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

		# Aplicar la fórmula de Haversine para calcular la distancia
		dlat = lat2 - lat1
		dlon = lon2 - lon1
		a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))
		distance = r * c  # distancia en kilómetros

		# Retorna el tiempo estimado dividiendo la distancia por la velocidad media
		return distance / avg_velocity

	if current == destination:
		return 0

	coords_current = dict_stations[current]["coordinates"]
	coords_destination = dict_stations[destination]["coordinates"]

	return time_haversine(coords_current[0], coords_current[1], coords_destination[0], coords_destination[1])


def is_weekend(day) -> bool:
	return day in [6, 7]

def normalize_station_name(name) -> str:
	if "Independencia" in name:
		return "Independencia"
	elif "Callao" in name:
		return "Callao"
	return name
		

def main():
	if len(sys.argv) != 6:
		print(f"Number of arguments passed: {len(sys.argv)} - expected 6 arguments.")
		sys.exit(1)

	source_id = int(sys.argv[1])
	target_id = int(sys.argv[2])
	day = int(sys.argv[3])
	hour = int(sys.argv[4])
	minute = int(sys.argv[5])

	# Añadir un sesgo si es el fin de semana
	bias = 1
	if is_weekend(day):
		bias = 1.5

	dict_stations = {
				   11: {"name": "Plaza de Mayo", "coordinates": (-34.6088103091689, -58.3709684989674), "time": 1*bias, "line": "A"},
				   12: {"name": "Perú", "coordinates": (-34.6085590738532, -58.3742677264304), "time": 1*bias, "line": "A"},
				   13: {"name": "Piedras", "coordinates": (-34.608881721215, -58.3790851530908), "time": 2*bias, "line": "A"},
				   14: {"name": "Lima", "coordinates": (-34.6090998065519, -58.3822324010181), "time": 1*bias, "line": "A"},
				   15: {"name": "Saenz Peña", "coordinates": (-34.6094125865027, -58.3867771940873), "time": 1*bias, "line": "A"},
				   16: {"name": "Congreso", "coordinates": (-34.6092256843174, -58.3926688246648), "time": 1*bias, "line": "A"},
				   17: {"name": "Pasco", "coordinates": (-34.6096459617052, -58.3984269918123), "time": 1*bias, "line": "A"},
				   18: {"name": "Alberti", "coordinates": (-34.6098335784398, -58.401207534233), "time": 0, "line": "A"},
				   21: {"name": "Leandro N. Alem", "coordinates": (-34.6029894966332, -58.369929850122300), "time": 1*bias,"line": "B"},
				   22: {"name": "Florida", "coordinates": (-34.603297285577500, -58.375071518263500), "time": 1*bias, "line": "B"},
				   23: {"name": "Carlos Pellegrini", "coordinates": (-34.6036371051817, -58.380714847140800), "time": 1*bias, "line": "B"},
				   24: {"name": "Uruguay", "coordinates": (-34.6040935531057, -58.387296133540700), "time": 2*bias, "line": "B"},
				   25: {"name": "CallaoB", "coordinates": (-34.604419542860700, -58.392314235088700), "time": 1*bias, "line": "B"},
				   26: {"name": "Pasteur", "coordinates": (-34.604642967919300, -58.399474256679), "time": 0, "line": "B"},
				   31: {"name": "Constitución", "coordinates": (-34.6276194522548, -58.381434433934295), "time": 1*bias, "line": "C"},
				   32: {"name": "San Juan", "coordinates": (-34.6219167322081, -58.3799211788651), "time": 2*bias, "line": "C"},
				   33: {"name": "IndependenciaC", "coordinates": (-34.6181255992933, -58.380173610475204), "time": 2*bias, "line": "C"},
				   34: {"name": "Moreno", "coordinates": (-34.6126172798037, -58.38044446966), "time": 1*bias, "line": "C"},
				   35: {"name": "Avenida de Mayo", "coordinates": (-34.6089833148827, -58.3806107179579), "time": 2*bias, "line": "C"},
				   36: {"name": "Diagonal Norte", "coordinates": (-34.604843739913996, -58.3795299800739), "time": 1*bias, "line": "C"},
				   37: {"name": "Lavalle", "coordinates": (-34.601769923011396, -58.3781557828244), "time": 2*bias, "line": "C"},
				   38: {"name": "San Martín", "coordinates": (-34.5950574047792, -58.3778190509867), "time": 1*bias, "line": "C"},
				   39: {"name": "Retiro", "coordinates": (-34.5911938083332, -58.3740182164816), "time": 0, "line": "C"},
				   41: {"name": "Facultad de Medicina", "coordinates": (-34.5997570807639, -58.3979237555734), "time": 1*bias, "line": "D"},
				   42: {"name": "CallaoD", "coordinates": (-34.604419542860700, -58.392314235088700), "time": 2*bias, "line": "D"},
				   43: {"name": "Tribunales", "coordinates": (-34.6015871651394, -58.385142358801200), "time": 1*bias, "line": "D"},
				   44: {"name": "9 de Julio", "coordinates": (-34.6042452029629, -58.3805743428896), "time": 2*bias, "line": "D"},
				   45: {"name": "Catedral", "coordinates": (-34.6078023364289, -58.3739558069511), "time": 0, "line": "D"},
				   51: {"name": "Pichincha", "coordinates": (-34.62310987, -58.39706807), "time": 1*bias, "line": "E"},
				   52: {"name": "Entre Ríos", "coordinates": (-34.62271967, -58.3915116999715), "time": 2*bias, "line": "E"},
				   53: {"name": "San José", "coordinates": (-34.62233949, -58.38514855), "time": 1*bias, "line": "E"},
				   54: {"name": "IndependenciaE", "coordinates": (-34.61793739, -58.38153494), "time": 2*bias, "line": "E"},
				   55: {"name": "Belgrano", "coordinates": (-34.61284911, -58.37758089), "time": 1*bias, "line": "E"},
				   56: {"name": "Bolívar", "coordinates": (-34.60924243, -58.37368422), "time": 0, "line": "E"}
	}

	# Para poder pasar todos los argumentos correctamente a heuristic_metro_stations
	def heuristic_wrapper(current, destination):
		return heuristic_metro_stations(current, destination, dict_stations)

	# Creación del grafo del metro
	metro = nx.Graph()
	add_metro_network(metro, dict_stations)

	# Calcular el camino más corto usando A*
	path_ids = nx.astar_path(metro, source_id, target_id, heuristic_wrapper, weight="weight")
	travel_duration_minutes = math.ceil(nx.astar_path_length(metro, source_id, target_id, heuristic_wrapper))

	# Obtener los nombres de las estaciones
	path_nombres = [dict_stations[station]["name"] for station in path_ids]

	# Agrupar las estaciones por sus líneas
	grouped_path = []
	transfers = []
	current_line = dict_stations[path_ids[0]]["line"]
	current_group = [dict_stations[path_ids[0]]["name"]]

	for i in range(1, len(path_ids)):
		station_id = path_ids[i]
		station_line = dict_stations[station_id]["line"]

		if station_line == current_line:
			current_group.append(normalize_station_name(dict_stations[station_id]["name"]))
		else:
			grouped_path.append({"line": current_line, "stations": current_group})
			transfers.append(normalize_station_name(dict_stations[station_id]["name"]))
			current_line = station_line
			current_group = [normalize_station_name(dict_stations[station_id]["name"])]

	# Añadir el último grupo
	grouped_path.append({"line": current_line, "stations": current_group})

	# Calcular el time de llegada
	current_time = datetime(year=2024, month=1, day=1, hour=hour, minute=minute)
	travel_duration = timedelta(minutes=travel_duration_minutes)
	arrival_time = current_time + travel_duration


	# Preparar la salida de JSON
	output = {
		"estaciones_path": path_nombres,
		"path_ids": path_ids,
		"travel_duration": travel_duration_minutes,
		"arrival_time": arrival_time.strftime("%H:%M"),
		"grouped_path": grouped_path,
		"transfers": transfers
	}
	print(json.dumps(output))


if __name__ == "__main__":
	main()
