extends Control

# In the browser (HTML5 export) we use same-origin requests — no base needed.
# In the editor / native builds we talk directly to the local dev server.
var _api_base: String:
	get:
		return "" if OS.get_name() == "Web" else "http://localhost:8000"

@onready var _num_input: SpinBox       = $VBox/InputRow/NumInput
@onready var _generate_btn: Button     = $VBox/InputRow/GenerateBtn
@onready var _status_label: Label      = $VBox/StatusLabel
@onready var _reveal_row: HBoxContainer = $VBox/RevealRow
@onready var _reveal_btn: Button       = $VBox/RevealRow/RevealBtn
@onready var _show_all_btn: Button     = $VBox/RevealRow/ShowAllBtn
@onready var _counter_label: Label     = $VBox/RevealRow/CounterLabel
@onready var _jock_list: VBoxContainer = $VBox/Scroll/JockList
@onready var _stats_btn: Button        = $VBox/StatsBtn
@onready var _http: HTTPRequest        = $HTTP

const JOCK_CARD = preload("res://scenes/JockCard.tscn")

var _jocks: Array = []
var _revealed: int = 0


func _ready() -> void:
	_generate_btn.pressed.connect(_on_generate)
	_reveal_btn.pressed.connect(_on_reveal_next)
	_show_all_btn.pressed.connect(_on_show_all)
	_http.request_completed.connect(_on_request_completed)
	_stats_btn.pressed.connect(_on_stats_btn_pressed)
	_set_reveal_visible(false)
	_status_label.text = ""


# ------------------------------------------------------------------------------
# Generate
# ------------------------------------------------------------------------------

func _on_generate() -> void:
	_clear_list()
	_jocks = []
	_revealed = 0
	_set_reveal_visible(false)
	_status_label.text = "Stackin' the Jocks, haud yer wheesht..."
	_generate_btn.disabled = true

	var n := int(_num_input.value)
	var body := JSON.stringify({"num_jocks": n})
	var headers := PackedStringArray(["Content-Type: application/json"])
	var err := _http.request(_api_base + "/api/generate", headers, HTTPClient.METHOD_POST, body)
	if err != OK:
		_status_label.text = "Crivens! Couldnae reach the server!"
		_generate_btn.disabled = false


func _on_request_completed(
	result: int,
	response_code: int,
	_headers: PackedStringArray,
	body: PackedByteArray
) -> void:
	_generate_btn.disabled = false

	if result != HTTPRequest.RESULT_SUCCESS or response_code != 200:
		_status_label.text = "Crivens! Somethin' went wrong! (HTTP %d)" % response_code
		return

	var data = JSON.parse_string(body.get_string_from_utf8())
	if data == null:
		_status_label.text = "Crivens! Couldnae read the response!"
		return

	_jocks = data.get("jocks", [])
	if _jocks.is_empty():
		_status_label.text = "T'ere hain't na Jocks here, Bigjob!"
		return

	_status_label.text = "T'ere are to be %d Jocks this time! Press the button!" % _jocks.size()
	_set_reveal_visible(true)
	_update_counter()


# ------------------------------------------------------------------------------
# Reveal
# ------------------------------------------------------------------------------

func _on_reveal_next() -> void:
	if _revealed >= _jocks.size():
		return
	_reveal_one(_jocks[_revealed])
	_revealed += 1
	_update_counter()
	if _revealed >= _jocks.size():
		_finish_reveal()


func _on_show_all() -> void:
	while _revealed < _jocks.size():
		_reveal_one(_jocks[_revealed])
		_revealed += 1
	_update_counter()
	_finish_reveal()


func _reveal_one(jock: Dictionary) -> void:
	var card = JOCK_CARD.instantiate()
	_jock_list.add_child(card)
	card.set_jock(jock.get("name", "Unknown Jock"))


func _finish_reveal() -> void:
	_set_reveal_visible(false)
	_status_label.text = "...and t'at's all the Jocks t'ere!"


# ------------------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------------------

func _update_counter() -> void:
	_counter_label.text = "%d / %d" % [_revealed, _jocks.size()]


func _set_reveal_visible(show: bool) -> void:
	_reveal_row.visible = show


func _clear_list() -> void:
	for child in _jock_list.get_children():
		child.queue_free()


# ------------------------------------------------------------------------------
# Stats link — opens in browser tab on Web, shell_open in editor
# ------------------------------------------------------------------------------

func _on_stats_btn_pressed() -> void:
	var url := _api_base + "/stats"
	if OS.get_name() == "Web":
		JavaScriptBridge.eval("window.open('%s', '_blank')" % url)
	else:
		OS.shell_open(url)
