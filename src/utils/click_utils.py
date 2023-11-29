from objects.box import Box
from objects.position import Position


def find_selected_hold(holds: list[Box], click_x: int, click_y: int) -> Box | None:
	"""Return the hold selected by the user."""
	for hold in holds:
		if hold.position_collide(Position(click_x, click_y), margin=10):
			return hold
	return None
