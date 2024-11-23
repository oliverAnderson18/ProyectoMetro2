extends Control  # Asegúrate de que tu nodo principal sea de tipo Control

@onready var panel = $Panel  # Referencia al Panel
@onready var nombre_estacion = $ID

signal obtener_estacion(nombre)

func _ready():
	panel.hide()  # Oculta el Panel al inicio

func _on_control_51_mouse_entered():
	panel.show()  # Muestra el Panel cuando el cursor está encima
	obtener_estacion.emit(nombre_estacion.text)
	

func _on_control_51_mouse_exited():
	panel.hide()  # Oculta el Panel cuando el cursor se sale
