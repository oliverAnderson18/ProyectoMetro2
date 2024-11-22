extends Control

@onready var menu = $Filtro_Clicks
@onready var animationPlayer = $AnimationPlayer

func _on_button_pressed() -> void:
	if menu.visible == true:
		animationPlayer.play("hide_menu")
		await animationPlayer.animation_finished
		menu.visible = false
	else:
		menu.visible = true
		animationPlayer.play("show_menu")
