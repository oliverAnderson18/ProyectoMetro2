extends Window

@onready var content_container = $VScrollBar/VBoxContainer	# Reference to the main container

func populate_route(start_station, grouped_path, final_station, transfers):
	# Reset the popup
	for n in content_container.get_children():
		content_container.remove_child(n)
		n.queue_free()		
		
	# Add the start station
	var start_label = Label.new()
	start_label.text = "Estación de Inicio: " + start_station
	content_container.add_child(start_label)
	
	for i in range(grouped_path.size()):
		var segment = grouped_path[i]
		
		#HBoxContainer for line section
		var line_container = HBoxContainer.new()
		content_container.add_child(line_container)
		
		# Rectangle that represents the color of the line
		var color_rect = ColorRect.new()
		color_rect.color = _get_line_color(segment["line"]) # Get the line's color
		color_rect.size_flags_horizontal = Control.SIZE_SHRINK_CENTER # Thin vertical line
		color_rect.custom_minimum_size = Vector2(10, 0) # Width 10 px
		line_container.add_child(color_rect)
		
		var line_details = VBoxContainer.new()
		line_container.add_child(line_details)
		
		# Add line name
		var line_label = Label.new()
		line_label.text = segment["line"]
		line_details.add_child(line_label)
	
		# Toggle button
		var toggle_button = Button.new()
		toggle_button.text = "Mostrar Estaciones"
		line_details.add_child(toggle_button)
		
		# Hidden container for station names
		var station_container = VBoxContainer.new()
		station_container.visible = false
		for station in segment["stations"]:
			var station_label = Label.new()
			station_label.text = station
			station_container.add_child(station_label)
		
		line_details.add_child(station_container)
		
		toggle_button.connect("pressed", Callable(self, "_on_toggle_stations_pressed").bind(station_container))
		
		if i < transfers.size():
			var transfer_label = Label.new()
			transfer_label.text = "Transbordo en: " + transfers[i]
			content_container.add_child(transfer_label)
	
	var final_label = Label.new()
	final_label.text = "Estación Final: " + final_station
	content_container.add_child(final_label)
	
	
func _on_toggle_stations_pressed(station_container):
	station_container.visible = !station_container.visible
	

func show_popup():
	self.popup_centered()
	
func _get_line_color(line_name: String) -> Color:
	match line_name:
		"A": return Color(92/255.0, 196/255.0, 247/255.0)
		"B": return Color(255/255.0, 15/255.0, 0/255.0)
		"C": return Color(39/255.0, 97/255.0, 241/255.0)
		"D": return Color(11/255.0, 188/255.0, 0/255.0)
		"E": return Color(122/255.0, 44/255.0, 244/255.0)
		_: return Color(191/255.0, 191/255.0, 191/255.0)
