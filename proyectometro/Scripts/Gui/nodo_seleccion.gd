extends Control

@onready var selector_origen: OptionButton = get_node("../NodoRuta/SeleccionarRuta/Origen/listaEstaciones")
@onready var selector_destino: OptionButton = get_node("../NodoRuta/SeleccionarRuta/Destino/listaEstaciones")
@onready var mapa: Node2D = get_node("../Mapa")
@onready var lista_nodos = []
@onready var flecha_origen = $FlechaOrigen
@onready var flecha_destino = $FlechaDestino

# Called when the node enters the scene tree for the first time.
func _ready() -> void:	
	_establecer_flecha(selector_origen.get_selected_id(), "origen")
	_establecer_flecha(selector_destino.get_selected_id(), "destino")
	pass

func _on_lista_estaciones_origen_item_selected(index: int) -> void:
	var id = selector_origen.get_selected_id()
	_establecer_flecha(id, "origen")


func _on_lista_estaciones_destino_item_selected(index: int) -> void:
	var id = selector_destino.get_selected_id()
	_establecer_flecha(id, "destino")

func _establecer_flecha(id: int, tipo: String) -> void:
	print(id)
	var nodo_estacion: Node2D = get_node_mapa(id)
	print(nodo_estacion.name, nodo_estacion.global_position)
	
	var estacion_x = nodo_estacion.global_position.x
	var estacion_y = nodo_estacion.global_position.y
	
	match tipo:
		"origen":
			flecha_origen.global_position.x = estacion_x
			flecha_origen.global_position.y = estacion_y
		"destino":
			flecha_destino.global_position.x = estacion_x
			flecha_destino.global_position.y = estacion_y

func get_node_mapa(id: int) -> Node2D:
	var linea: Node2D = get_linea(id)
	
	var nodo_estaciones: Node2D = linea.get_child(0)
	var nodo_estacion: Node2D
	
	var lista_estaciones: Array = nodo_estaciones.get_children()
	for estacion in lista_estaciones:
		if str(id) == estacion.name:
			nodo_estacion = estacion
			break
	
	return nodo_estacion
	

func get_linea(id: int) -> Node2D:
	var num_linea = floor(id / 10)
	var linea: Node2D = mapa.get_child(num_linea)
	return linea
