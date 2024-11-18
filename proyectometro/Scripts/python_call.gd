extends Node

func get_python_path() -> String:
	var command = "where" if OS.get_name() == "Windows" else "which"
	var result = []
	var res = OS.execute(command, ["python"], result, true)
	
	if res == 0 and result.size() > 0:
		return result[0].strip_edges()
	else:
		return ""
	
	
func run_python_script(source_id, target_id):
	var python_path = get_python_path()
	print(python_path)
	if python_path == "":
		print("Error: Unable to find Python executable.")
		return
		
	var output = []
	var python_file = ProjectSettings.globalize_path("res://Scripts/backend.py")
	var result = OS.execute(python_path, [python_file, str(source_id), str(target_id)], output, true, false)
	
	if result == 0:
		var parsedOutput = JSON.parse_string(output[0])
		
		GlobalData.path = parsedOutput["estaciones_path"]
		print(GlobalData.path)
		GlobalData.total_time = parsedOutput["time"]
		print(GlobalData.total_time)
		GlobalData.path_ids = parsedOutput["path_ids"]
		print(GlobalData.path_ids)
		
	else:
		print("Error running Python script:", result)
