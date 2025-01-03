extends Control

@onready var check_button: CheckButton = $Menu/CheckButton

signal loaded

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	$Menu.visible = false



func _input(event) -> void:
	if (event is InputEventKey or event is InputEventMouseButton) and event.is_pressed() and $StartScreen.visible == true:
		show_menu()

func show_menu():
	# Oculta el menú inicial
	$StartScreen.visible = false
	
	$AnimationPlayer.play("startMenu")
	$Menu.visible = true

func activate() -> void:
	pass

func load_scene() -> void:
	await get_tree().create_timer(0.1).timeout
	loaded.emit()

func _on_start_pressed() -> void:
	if GlobalData.animaciones:
		Transition.transition_to("res://Scenes/estacion_entrada.tscn")
	else:
		Transition.transition_to("res://Scenes/SeleccionEstaciones.tscn")

func _on_exit_pressed() -> void:
	get_tree().quit()


func _on_check_button_toggled(toggled_on: bool) -> void:
	if toggled_on:
		GlobalData.animaciones = true
	else:
		GlobalData.animaciones = false
		
