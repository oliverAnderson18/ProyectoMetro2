extends Label

@onready var hour_selector = $VBoxContainer/Spinbox_Hora
@onready var minute_selector = $VBoxContainer/Spinbox_Minutos

func _ready():
	self.text = hour_selector.name
