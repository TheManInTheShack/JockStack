class_name WordBalloon
extends Control

const TRIANGLE_HEIGHT := 36.0
const CORNER_RADIUS   := 14

var _pointer_x:  float  = -1.0  # local x for triangle tip; -1 = centred
var _raw_name:   String = ""    # name without display prefix

@onready var _label: Label = $NameLabel

var _style: StyleBoxFlat


func _ready() -> void:
	_style = StyleBoxFlat.new()
	_style.bg_color = Color.WHITE
	_style.corner_radius_top_left     = CORNER_RADIUS
	_style.corner_radius_top_right    = CORNER_RADIUS
	_style.corner_radius_bottom_left  = CORNER_RADIUS
	_style.corner_radius_bottom_right = CORNER_RADIUS
	visible = false
	# Keep label inside the panel area, above the triangle
	_label.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	_label.offset_bottom = -TRIANGLE_HEIGHT


func set_jock(jock_name: String) -> void:
	_raw_name   = jock_name
	_label.text = "Oi! We be " + jock_name + "."
	_pointer_x  = -1.0
	visible     = true
	queue_redraw()


func update_pointer(global_x: float) -> void:
	_pointer_x = global_x - global_position.x
	queue_redraw()


func get_current_name() -> String:
	return _raw_name  # raw name, without display prefix


func _draw() -> void:
	var panel_h := size.y - TRIANGLE_HEIGHT
	_style.draw(get_canvas_item(), Rect2(Vector2.ZERO, Vector2(size.x, panel_h)))

	var cx := _pointer_x if _pointer_x >= 0.0 else size.x * 0.5
	cx = clampf(cx, 20.0, size.x - 20.0)

	draw_colored_polygon(
		PackedVector2Array([
			Vector2(cx - 14.0, panel_h),
			Vector2(cx + 14.0, panel_h),
			Vector2(cx,        size.y),
		]),
		Color.WHITE
	)
