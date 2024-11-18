extends Node3D

@export var rotation_speed: float = 0.5

@onready var mesh: MeshInstance3D = $MeshInstance3D

func _physics_process(delta: float) -> void:
	mesh.rotation.y += PI * delta * rotation_speed
