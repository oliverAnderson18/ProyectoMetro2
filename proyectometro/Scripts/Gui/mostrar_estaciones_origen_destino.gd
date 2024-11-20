extends Node

signal loaded()

# Called when the node enters the scene tree for the first time.
func activate() -> void:
	pass

func load_scene() -> void:
	await get_tree().create_timer(0.1).timeout
	loaded.emit()

@onready var button = $Button
@onready var target_nodes = [
	$"Mapa/conexiones/2652",
	$"Mapa/conexiones/2756",
	$"Mapa/conexiones/2862",
	$"Mapa/conexiones/2970",
	$"Mapa/conexiones/3080",
	$"Mapa/conexiones/158400",
	$"Mapa/conexiones/178200",
	$"Mapa/conexiones/101200",
	$"Mapa/conexiones/252000",
	$"Mapa/conexiones/67200",
	$"Mapa/conexiones/54000",
	$"Mapa/conexiones/49000",
	$"Mapa/conexiones/1722",
	$"Mapa/conexiones/1806",
	$"Mapa/conexiones/1892",
	$"Mapa/conexiones/1980",
	$"Mapa/conexiones/992",
	$"Mapa/conexiones/1057",
	$"Mapa/conexiones/1122",
	$"Mapa/conexiones/1190",
	$"Mapa/conexiones/1260",
	$"Mapa/conexiones/1332",
	$"Mapa/conexiones/1406",
	$"Mapa/conexiones/1482",
	$"Mapa/conexiones/462",
	$"Mapa/conexiones/650",
	$"Mapa/conexiones/600",
	$"Mapa/conexiones/552",
	$"Mapa/conexiones/506",
	$"Mapa/conexiones/240",
	$"Mapa/conexiones/306",
	$"Mapa/conexiones/272",
	$"Mapa/conexiones/210",
	$"Mapa/conexiones/182",
	$"Mapa/conexiones/156",
	$"Mapa/conexiones/132",
]
@onready var mas_info = $MasInfo
@onready var pop_up = $DisplayMasInfo

func _ready() -> void:
<<<<<<< Updated upstream
	$CalcularRuta.connect("pressed", Callable(self, "_button_combined"))
=======
	$NodoRuta/CalcularRuta.connect("pressed", Callable(self, "_button_combined"))
	$MasInfo.connect("pressed", Callable(self, "_display_mas_info"))
>>>>>>> Stashed changes

func on_calcular_ruta_button_pressed():
	var origen = $SeleccionarRuta/Origen/listaEstaciones
	var destino = $SeleccionarRuta/Destino/listaEstaciones
	
	var id_origen = origen.get_selected_id()
	var id_destino = destino.get_selected_id()
	
	var python_call = preload("res://Scripts/python_call.gd").new()
	python_call.run_python_script(id_origen, id_destino)
	

func make_arist(list_stations_id: Array) -> Array:
	var list_id_arist = Array()
	for i in range(len(list_stations_id) - 1):
		if str(list_stations_id[i])[0] == str(list_stations_id[i + 1])[0]:
			list_id_arist.append("Mapa/conexiones/" + str(list_stations_id[i] * list_stations_id[i + 1]))
		else:
			list_id_arist.append("Mapa/conexiones/" + str(list_stations_id[i] * list_stations_id[i + 1] * 100))
	return list_id_arist

func _on_button_pressed():
	for node in target_nodes:
		if node:
			node.visible = false
		else:
			print("Node not found")

func desocultar(lista_aristas):
	for arista in lista_aristas:
		var nodo = get_node(arista)
		nodo.visible = true
		await get_tree().create_timer(1).timeout


func _button_combined():
	_on_button_pressed()
	on_calcular_ruta_button_pressed()
	var ruta = GlobalData.path
	var tiempo = GlobalData.total_time
	var id_path = GlobalData.path_ids
	var lista_aristas = make_arist(id_path)
	desocultar(lista_aristas)
	_show_mas_info()
		
func _show_mas_info():
	mas_info.visible = true
	
func _display_mas_info():
	pop_up.show()


func _on_display_mas_info_close_requested() -> void:
	pop_up.hide()
