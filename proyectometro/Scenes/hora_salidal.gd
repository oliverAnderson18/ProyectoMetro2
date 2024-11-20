extends Label

@onready var salida_hora = $VBoxContainer/Spinbox_Hora
@onready var salida_minuto = $VBoxContainer/Spinbox_Minutos

func _ready() -> void:
	self.text = salida_hora
