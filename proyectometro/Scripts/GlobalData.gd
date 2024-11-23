extends Node

var path = []
var travel_duration = 0
var path_ids = []
var arrival_time = 0
var grouped_path = []
var transfers = []

func clear():
	path = []
	travel_duration = 0
	path_ids = []
	arrival_time = 0
	grouped_path = []
	transfers = []
	
func get_array() -> String:
	var s = ""
	for i in range(len(path)):
		if i == len(path)-1:
			s += String(path[i]) + "."
		else:
			s += String(path[i]) + ", "
	return s
