import networkx as nx
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, atan2
import json
import sys

dict_estaciones = {
                   11: {"name": "plaza de mayo", "coordenadas": (-34.6088103091689, -58.3709684989674), "tiempo": 1},
                   12: {"name": "peru", "coordenadas": (-34.6085590738532, -58.3742677264304), "tiempo": 1},
                   13: {"name": "piedras", "coordenadas": (-34.608881721215, -58.3790851530908), "tiempo": 2},
                   14: {"name": "lima", "coordenadas": (-34.6090998065519, -58.3822324010181), "tiempo": 1},
                   15: {"name": "saenz peña", "coordenadas": (-34.6094125865027, -58.3867771940873), "tiempo": 1},
                   16: {"name": "congreso", "coordenadas": (-34.6092256843174, -58.3926688246648), "tiempo": 1},
                   17: {"name": "pasco", "coordenadas": (-34.6096459617052, -58.3984269918123), "tiempo": 1},
                   18: {"name": "alberti", "coordenadas": (-34.6098335784398, -58.401207534233), "tiempo": 0},
                   21: {"name": "leandro n. alem", "coordenadas": (-34.6029894966332, -58.369929850122300), "tiempo": 1},
                   22: {"name": "florida", "coordenadas": (-34.603297285577500, -58.375071518263500), "tiempo": 1},
                   23: {"name": "carlos pellegrini", "coordenadas": (-34.6036371051817, -58.380714847140800), "tiempo": 1},
                   24: {"name": "uruguay", "coordenadas": (-34.6040935531057, -58.387296133540700), "tiempo": 2},
                   25: {"name": "callaob", "coordenadas": (-34.604419542860700, -58.392314235088700), "tiempo": 1},
                   26: {"name": "pasteur", "coordenadas": (-34.604642967919300, -58.399474256679), "tiempo": 0},
                   31: {"name": "constitucion", "coordenadas": (-34.6276194522548, -58.381434433934295), "tiempo": 1},
                   32: {"name": "san juan", "coordenadas": (-34.6219167322081, -58.3799211788651), "tiempo": 2},
                   33: {"name": "independenciac", "coordenadas": (-34.6181255992933, -58.380173610475204), "tiempo": 2},
                   34: {"name": "moreno", "coordenadas": (-34.6126172798037, -58.38044446966), "tiempo": 1},
                   35: {"name": "avenida de mayo", "coordenadas": (-34.6089833148827, -58.3806107179579), "tiempo": 2},
                   36: {"name": "diagonal norte", "coordenadas": (-34.604843739913996, -58.3795299800739), "tiempo": 1},
                   37: {"name": "lavalle", "coordenadas": (-34.601769923011396, -58.3781557828244), "tiempo": 2},
                   38: {"name": "san martin", "coordenadas": (-34.5950574047792, -58.3778190509867), "tiempo": 1},
                   39: {"name": "retiro", "coordenadas": (-34.5911938083332, -58.3740182164816), "tiempo": 0},
                   41: {"name": "facultad de medicina", "coordenadas": (-34.5997570807639, -58.3979237555734), "tiempo": 1},
                   42: {"name": "callaod", "coordenadas": (-34.604419542860700, -58.392314235088700), "tiempo": 2},
                   43: {"name": "tribunales", "coordenadas": (-34.6015871651394, -58.385142358801200), "tiempo": 1},
                   44: {"name": "9 de julio", "coordenadas": (-34.6042452029629, -58.3805743428896), "tiempo": 2},
                   45: {"name": "catedral", "coordenadas": (-34.6078023364289, -58.3739558069511), "tiempo": 0},
                   51: {"name": "pichincha", "coordenadas": (-34.62310987, -58.39706807), "tiempo": 1},
                   52: {"name": "entre rios", "coordenadas": (-34.62271967, -58.3915116999715), "tiempo": 2},
                   53: {"name": "san jose", "coordenadas": (-34.62233949, -58.38514855), "tiempo": 1},
                   54: {"name": "endependenciae", "coordenadas": (-34.61793739, -58.38153494), "tiempo": 2},
                   55: {"name": "belgrano", "coordenadas": (-34.61284911, -58.37758089), "tiempo": 1},
                   56: {"name": "bolivar", "coordenadas": (-34.60924243, -58.37368422), "tiempo": 0}
    }

dict_tildes = {
    "á": "a",
    "é": "e",
    "í": "i",
    "ó": "o",
    "ú": "u"
}

def add_metro_network(graph):
    lineas_metro_ids = [
        list(range(11, 19)),  # Línea A
        list(range(21, 27)),  # Línea B
        list(range(31, 40)),  # Línea C
        list(range(41, 46)),  # Línea D
        list(range(51, 57)),  # Línea E
    ]

    for linea in lineas_metro_ids:
        for i in range(len(linea) - 1):
            graph.add_edge(linea[i], linea[i+1], weight = dict_estaciones[linea[i]]["tiempo"])

    # Correspondencias (peso de 5 min)
    graph.add_edge(44, 23, weight=5)
    graph.add_edge(44, 36, weight=5)
    graph.add_edge(14, 35, weight=5)
    graph.add_edge(12, 45, weight=5)
    graph.add_edge(12, 56, weight=5)
    graph.add_edge(33, 54, weight=5)
    graph.add_edge(45, 56, weight=5)

def conversion_strings(station_name) -> str:
    lower_case = station_name.lower()
    for i in range(len(lower_case)):
        if lower_case[i] in dict_tildes:
            lower_case[i] = dict_tildes[lower_case[i]]
    return lower_case


def find_station_id_by_name(station_name: str):
    try: 
        station_name = conversion_strings(station_name)
        for station_id, station_info in dict_estaciones.items():
            if station_info["name"] == station_name:
                return station_id
    except:
        raise ValueError(f"Estación '{station_name}' no encontrada en el diccionario.")


def heuristic_metro_stations(current, destination, velocidad_media = 0.8333333333333334):
    def tiempo_haversine(lat1, lon1, lat2, lon2):
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
        distancia = r * c  # distancia en kilómetros

        # Retorna el tiempo estimado dividiendo la distancia por la velocidad media
        return distancia / velocidad_media

    if current == destination:
        return 0

    coords_current = dict_estaciones[current]["coordenadas"]
    coords_destination = dict_estaciones[destination]["coordenadas"]

    return tiempo_haversine(coords_current[0], coords_current[1], coords_destination[0], coords_destination[1])

<<<<<<< HEAD:proyectometro/backend.py

def main():

    if len(sys.argv) != 3:
        print(f"Number of arguments passed: {len(sys.argv)} - expected 2 arguments.")

    source_id = int(sys.argv[1])
    target_id = int(sys.argv[2])

    metro = nx.Graph()
    add_metro_network(metro)
    
    path_ids = nx.astar_path(metro, source_id, target_id, heuristic_metro_stations, weight="weight")
    tiempo_path = nx.astar_path_length(metro, source_id, target_id, heuristic_metro_stations)

    path_nombres = []
    for elem in path_ids:
        path_nombres.append(dict_estaciones[elem]["name"])
=======
def path_time(current_station, final_station):
    metro = nx.Graph()
    add_metro_network(metro)
    path = create_path(metro, current_station, final_station)
    time = calculate_time(metro, current_station, final_station)
    return path, time


def create_path(graph, current_station, final_station):
    path_ids = nx.astar_path(graph, current_station, final_station, heuristic_metro_stations, weight="weight")
    path_nombres = []
    for elem in path_ids:
        path_nombres.append(dict_estaciones[elem]["name"])
    return path_nombres


def calculate_time(graph, current_station, final_station):
    tiempo_path = nx.astar_path_length(graph, current_station, final_station, heuristic_metro_stations)
    return tiempo_path


def main():
    source = input("Ingrese la estación de partida: ")
    source_id = find_station_id_by_name(source)
    target = input("Ingrese la estación de destino: ")
    target_id = find_station_id_by_name(target)

    path_nombres, tiempo_path = path_time(source_id, target_id)
    print(path_nombres)
    print(f"Tiempo estimado: {tiempo_path} minutos.")
>>>>>>> eb4001d899413576f39b2176fa2e13b3057f4cec:python_code/backend.py
    
    output = {
        "estaciones_path": path_nombres,
        "path_ids": path_ids,
        "time": tiempo_path
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
