extends Control

signal loaded()

# Called when the node enters the scene tree for the first time.
func activate() -> void:
	pass

func load_scene() -> void:
	await get_tree().create_timer(1.0).timeout
	loaded.emit()
