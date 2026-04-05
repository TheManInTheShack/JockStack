class_name JockPuppet
extends Control

var _body_color:   Color
var _head_color:   Color
var _leg_color:    Color
var _accent_color: Color
var jock_size:     int   = 0
var _draw_scale:   float = 0.5  # fraction of slot_h actually drawn; set by JockDisplay


func setup(p_jock_size: int) -> void:
	jock_size     = p_jock_size
	var rng       := RandomNumberGenerator.new()
	rng.seed      = hash(p_jock_size)
	_body_color   = Color.from_hsv(rng.randf(), 0.55, 0.75)
	_head_color   = Color.from_hsv(rng.randf(), 0.40, 0.90)
	_leg_color    = Color.from_hsv(rng.randf(), 0.65, 0.55)
	_accent_color = Color.from_hsv(rng.randf(), 0.30, 0.95)
	queue_redraw()


func set_draw_scale(f: float) -> void:
	_draw_scale = f
	queue_redraw()


func get_head_global_pos() -> Vector2:
	# Figure is bottom-aligned in the slot; head is 13% down from figure top
	var drawn_h  := size.y * _draw_scale
	var y_offset := size.y - drawn_h
	return global_position + Vector2(size.x * 0.5, y_offset + drawn_h * 0.13)


func _draw() -> void:
	if size.x <= 0.0 or size.y <= 0.0:
		return
	var w       := size.x
	var h       := size.y * _draw_scale   # actual drawn height
	var yo      := size.y - h             # y offset — bottom-aligns the figure
	var cx      := w * 0.5

	# Feet
	draw_rect(Rect2(cx - w*0.18, yo + h*0.88, w*0.14, h*0.10), _leg_color)
	draw_rect(Rect2(cx + w*0.04, yo + h*0.88, w*0.14, h*0.10), _leg_color)
	# Legs
	draw_rect(Rect2(cx - w*0.14, yo + h*0.58, w*0.10, h*0.32), _leg_color)
	draw_rect(Rect2(cx + w*0.04, yo + h*0.58, w*0.10, h*0.32), _leg_color)
	# Kilt stripe
	draw_rect(Rect2(cx - w*0.20, yo + h*0.54, w*0.40, h*0.07), _accent_color)
	# Body
	draw_rect(Rect2(cx - w*0.18, yo + h*0.30, w*0.36, h*0.26), _body_color)
	# Arms
	draw_rect(Rect2(cx - w*0.34, yo + h*0.31, w*0.16, h*0.20), _body_color)
	draw_rect(Rect2(cx + w*0.18, yo + h*0.31, w*0.16, h*0.20), _body_color)
	# Neck
	draw_rect(Rect2(cx - w*0.06, yo + h*0.20, w*0.12, h*0.12), _head_color)
	# Head
	draw_circle(Vector2(cx, yo + h * 0.13), w * 0.18, _head_color)
	# Eyes
	draw_circle(Vector2(cx - w*0.07, yo + h*0.11), w * 0.030, Color(0.1, 0.1, 0.1))
	draw_circle(Vector2(cx + w*0.07, yo + h*0.11), w * 0.030, Color(0.1, 0.1, 0.1))
