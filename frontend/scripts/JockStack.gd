extends Control

var _api_base: String:
	get:
		return "" if OS.get_name() == "Web" else "http://localhost:8000"

@onready var _num_input:     SpinBox       = $VBox/InputRow/NumInput
@onready var _generate_btn:  Button        = $VBox/InputRow/GenerateBtn
@onready var _stats_btn:     Button        = $VBox/InputRow/StatsBtn
@onready var _status_label:  Label         = $VBox/StatusLabel
@onready var _reveal_row:    HBoxContainer = $VBox/RevealRow
@onready var _reveal_btn:    Button        = $VBox/RevealRow/RevealBtn
@onready var _counter_label: Label         = $VBox/RevealRow/CounterLabel
@onready var _word_balloon:  WordBalloon   = $VBox/WordBalloon
@onready var _jock_display:  JockDisplay   = $VBox/JockDisplay
@onready var _done_list:     VBoxContainer = $VBox/DoneScroll/DoneList
@onready var _http:          HTTPRequest   = $HTTP

const DONE_CARD_SCENE    := preload("res://scenes/DoneCard.tscn")
const BALLOON_FLY_SECS   := 0.45
const PUPPET_SETTLE_SECS := JockDisplay.TWEEN_DURATION + 0.08

var _jocks:    Array = []
var _revealed: int   = 0


func _ready() -> void:
	_generate_btn.pressed.connect(_on_generate)
	_reveal_btn.pressed.connect(_on_reveal_next)
	_stats_btn.pressed.connect(_on_stats_pressed)
	_http.request_completed.connect(_on_request_completed)
	_http.timeout = 10.0
	_reveal_row.visible = false
	_status_label.text  = ""


# ── Generate ─────────────────────────────────────────────────────────────────

func _on_generate() -> void:
	_jocks    = []
	_revealed = 0
	_reveal_row.visible   = false
	_word_balloon.visible = false
	for c in _done_list.get_children():
		c.queue_free()
	_jock_display.clear()
	_status_label.text     = "Stackin' the Jocks…"
	_generate_btn.disabled = true

	var body    := JSON.stringify({"num_jocks": int(_num_input.value)})
	var headers := PackedStringArray(["Content-Type: application/json"])
	if _http.request(_api_base + "/api/generate", headers, HTTPClient.METHOD_POST, body) != OK:
		_status_label.text     = "Crivens! Couldnae reach the server!"
		_generate_btn.disabled = false


func _on_request_completed(
	result: int, code: int, _h: PackedStringArray, body: PackedByteArray
) -> void:
	_generate_btn.disabled = false
	if result != HTTPRequest.RESULT_SUCCESS:
		match result:
			HTTPRequest.RESULT_CANT_CONNECT:
				_status_label.text = "Crivens! Couldnae connect — is the backend runnin'?"
			HTTPRequest.RESULT_TIMEOUT:
				_status_label.text = "Crivens! The server took too long tae respond!"
			_:
				_status_label.text = "Crivens! Connection failed (code %d)" % result
		return
	if code != 200:
		_status_label.text = "Crivens! Server error (HTTP %d)" % code
		return
	var data = JSON.parse_string(body.get_string_from_utf8())
	if data == null:
		_status_label.text = "Couldnae parse the response!"
		return
	_jocks = data.get("jocks", [])
	if _jocks.is_empty():
		_status_label.text = "T'ere hain't na Jocks here, Bigjob!"
		return
	_status_label.text  = "T'ere are to be %d Jocks this time!" % _jocks.size()
	_reveal_row.visible = true
	_update_counter()


# ── Reveal ────────────────────────────────────────────────────────────────────

func _on_reveal_next() -> void:
	if _revealed >= _jocks.size():
		return

	_reveal_btn.disabled = true

	var jock: Dictionary = _jocks[_revealed]
	_revealed += 1
	_update_counter()

	# Fly current balloon to done stack (fire-and-forget)
	if _word_balloon.visible:
		_launch_balloon_fly(_word_balloon.get_current_name())

	# Add puppet (slides into sorted position) and show new balloon immediately
	_jock_display.add_jock(jock.size, jock.name)
	_word_balloon.set_jock(jock.name)

	if _revealed >= _jocks.size():
		_reveal_row.visible = false
		_status_label.text  = "…and t'at's all the Jocks t'ere!"

	# After puppet settles, sharpen the balloon's triangle pointer
	_point_balloon_after_settle(jock.size)


func _point_balloon_after_settle(jock_size: int) -> void:
	await get_tree().create_timer(PUPPET_SETTLE_SECS).timeout
	if not is_instance_valid(_word_balloon) or not _word_balloon.visible:
		return
	var head := _jock_display.get_puppet_head_pos(jock_size)
	_word_balloon.update_pointer(head.x)
	_reveal_btn.disabled = false


# ── Balloon fly animation ─────────────────────────────────────────────────────

func _launch_balloon_fly(old_name: String) -> void:
	# Build a Panel that starts looking like the word balloon
	var fly     := Panel.new()
	var fly_lbl := Label.new()
	fly.add_child(fly_lbl)
	add_child(fly)
	fly.move_to_front()

	# Geometry: match balloon panel area (exclude triangle)
	fly.set_anchors_and_offsets_preset(Control.PRESET_TOP_LEFT)
	var balloon_h := maxf(_word_balloon.size.y - WordBalloon.TRIANGLE_HEIGHT, 60.0)
	fly.position  = _word_balloon.global_position - global_position
	fly.size      = Vector2(_word_balloon.size.x, balloon_h)

	# Initial style — white, rounded
	var style := StyleBoxFlat.new()
	style.bg_color                = Color.WHITE
	style.corner_radius_top_left  = WordBalloon.CORNER_RADIUS
	style.corner_radius_top_right = WordBalloon.CORNER_RADIUS
	style.corner_radius_bottom_left  = WordBalloon.CORNER_RADIUS
	style.corner_radius_bottom_right = WordBalloon.CORNER_RADIUS
	fly.add_theme_stylebox_override("panel", style)

	# Label — matches balloon text style
	fly_lbl.text                 = old_name
	fly_lbl.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	fly_lbl.vertical_alignment   = VERTICAL_ALIGNMENT_CENTER
	fly_lbl.autowrap_mode        = TextServer.AUTOWRAP_WORD_SMART
	fly_lbl.set_anchors_and_offsets_preset(Control.PRESET_FULL_RECT)
	fly_lbl.add_theme_font_size_override("font_size", 22)
	fly_lbl.add_theme_color_override("font_color", Color.BLACK)

	# Scale tween: shrink toward done-card size
	fly.pivot_offset  = Vector2(fly.size.x * 0.5, 0.0)
	var target_scale  := Vector2(
		_done_list.size.x / maxf(fly.size.x, 1.0),
		44.0              / maxf(balloon_h,   1.0)
	)
	var target_pos := _done_list.global_position - global_position

	var tw := create_tween()
	tw.set_parallel(true)
	tw.tween_property(fly, "position", target_pos, BALLOON_FLY_SECS)\
		.set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_CUBIC)
	tw.tween_property(fly, "scale", target_scale, BALLOON_FLY_SECS)\
		.set_ease(Tween.EASE_IN).set_trans(Tween.TRANS_CUBIC)
	tw.tween_method(
		func(t: float) -> void:
			style.bg_color = Color.WHITE.lerp(DoneCard.BG_COLOR, t)
			fly_lbl.add_theme_font_size_override("font_size", int(lerpf(22.0, 13.0, t)))
			fly_lbl.add_theme_color_override("font_color",
				Color.BLACK.lerp(DoneCard.FONT_COLOR, t)),
		0.0, 1.0, BALLOON_FLY_SECS
	)
	tw.set_parallel(false)
	tw.tween_callback(func() -> void:
		if not is_instance_valid(_done_list):
			fly.queue_free()
			return
		var card: DoneCard = DONE_CARD_SCENE.instantiate()
		_done_list.add_child(card)
		_done_list.move_child(card, 0)
		card.setup(old_name)
		fly.queue_free()
	)


# ── Helpers ───────────────────────────────────────────────────────────────────

func _update_counter() -> void:
	_counter_label.text = "%d / %d" % [_revealed, _jocks.size()]


func _on_stats_pressed() -> void:
	var url := _api_base + "/stats"
	if OS.get_name() == "Web":
		JavaScriptBridge.eval("window.open('%s', '_blank')" % url)
	else:
		OS.shell_open(url)
