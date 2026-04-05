class_name DoneCard
extends PanelContainer

const BG_COLOR   := Color(0.12, 0.12, 0.28)
const FONT_COLOR := Color(0.88, 0.88, 1.00)


func _ready() -> void:
	var style := StyleBoxFlat.new()
	style.bg_color                = BG_COLOR
	style.corner_radius_top_left  = 6
	style.corner_radius_top_right = 6
	style.corner_radius_bottom_left  = 6
	style.corner_radius_bottom_right = 6
	style.content_margin_left   = 10
	style.content_margin_right  = 10
	style.content_margin_top    = 5
	style.content_margin_bottom = 5
	add_theme_stylebox_override("panel", style)


func setup(jock_name: String) -> void:
	$Margin/NameLabel.text = "Oi! We be " + jock_name + "."
