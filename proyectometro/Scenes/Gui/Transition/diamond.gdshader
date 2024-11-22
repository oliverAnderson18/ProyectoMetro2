shader_type canvas_item;

uniform float progress: hint_range(0.0, 1.0, 0.1);
uniform float size = 20.0;
uniform bool fill = true;



void fragment() {
	float x = abs(fract(FRAGCOORD.x / size) - 0.5);
	float y = abs(fract(FRAGCOORD.y / size) - 0.5);
	
	if (x + y  + UV.x  + UV.y > progress * 3.0){
		if (fill){
			discard;
		}
	} else if (!fill){
		discard;
	}
}

//void light() {
	// Called for every pixel for every light affecting the CanvasItem.
	// Uncomment to replace the default light processing function with this one.
//}
