class_name JockDisplay
extends Control

const MAX_PER_LINE   := 12
const GAP_H          := 8.0
const GAP_V          := 16.0
const TWEEN_DURATION := 0.40

const JockPuppetScene := preload("res://scenes/JockPuppet.tscn")

# [{size: int, name: String, puppet: JockPuppet}] sorted by size ascending
var _entries: Array = []


func add_jock(jock_size: int, jock_name: String) -> void:
	var puppet: JockPuppet = JockPuppetScene.instantiate()
	add_child(puppet)
	puppet.setup(jock_size)

	# Insert in size-sorted position
	var idx := 0
	for i in _entries.size():
		if _entries[i].size < jock_size:
			idx = i + 1
	_entries.insert(idx, {size = jock_size, name = jock_name, puppet = puppet})

	_relayout(true)


func get_puppet_head_pos(jock_size: int) -> Vector2:
	for entry in _entries:
		if entry.size == jock_size:
			return (entry.puppet as JockPuppet).get_head_global_pos()
	return global_position


func clear() -> void:
	for entry in _entries:
		(entry.puppet as Control).queue_free()
	_entries.clear()


# ── Layout ───────────────────────────────────────────────────────────────────

func _relayout(animate: bool) -> void:
	var total := _entries.size()
	if total == 0:
		return

	var num_lines := ceili(float(total) / float(MAX_PER_LINE))
	var base      := total / num_lines
	var remainder := total % num_lines

	var slot_w := (size.x - (MAX_PER_LINE - 1) * GAP_H) / float(MAX_PER_LINE)
	var slot_h := (size.y - (num_lines - 1) * GAP_V) / float(num_lines)
	slot_w = maxf(slot_w, 20.0)
	slot_h = maxf(slot_h, 30.0)

	var idx := 0
	for line in num_lines:
		var count   := base + (1 if line < remainder else 0)
		var line_w  := count * slot_w + (count - 1) * GAP_H
		var start_x := (size.x - line_w) * 0.5
		var y       := line * (slot_h + GAP_V)

		for col in count:
			if idx >= total:
				break
			var entry: Dictionary = _entries[idx]
			var puppet := entry.puppet as JockPuppet
			var target := Vector2(start_x + col * (slot_w + GAP_H), y)

			puppet.size = Vector2(slot_w, slot_h)

			# Scale drawn height by rank: smallest ~42%, largest ~58% of slot
			var rank_pct := float(idx) / float(maxi(total - 1, 1))
			puppet.set_draw_scale(lerpf(0.42, 0.58, rank_pct))

			if animate and puppet.is_inside_tree() and puppet.position != Vector2.ZERO:
				create_tween()\
					.tween_property(puppet, "position", target, TWEEN_DURATION)\
					.set_ease(Tween.EASE_OUT)\
					.set_trans(Tween.TRANS_QUINT)
			else:
				puppet.position = target

			idx += 1


func _notification(what: int) -> void:
	if what == NOTIFICATION_RESIZED:
		_relayout(false)
