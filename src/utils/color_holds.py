from typing import Union
color = Union[tuple[int, int, int, int], tuple[int, int, int]]


def rgb_to_hex(rgb):
	return '#{:02x}{:02x}{:02x}'.format(*rgb)

def hex_to_rgb(hex):
	hex = hex.lstrip('#')
	hlen = len(hex)
	return tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

__COLORS = [
	(255, 0, 0), #red
	(255, 165, 0), #orange
	(255, 255, 0), #yellow
	(0, 128, 0), #green
	(0, 0, 255), #blue
	(75, 0, 130), #purple
	(238, 130, 238), #rose
	(0, 0, 0), #black
	(128, 128, 128), #grey
	(255, 255, 255), #white
	(128, 0, 0), #brown
	(128, 128, 0)  #olive
]

# __COLOR_1 = (41, 0, 255)
# __COLOR_2 = (255, 0, 0)

__COLOR_1 = hex_to_rgb("#0b7687")
__COLOR_2 = hex_to_rgb("#7f6360")

def get_nth_color(n: int) -> color:
	"""Return the nth color."""
	return __COLORS[n % len(__COLORS)]


def get_color_for_inside(n:int) -> color:
	"""Return the color for the inside."""
	return __COLORS[n % len(__COLORS)] +(0.35,)


def get_color_for_border(n:int) -> color:
	"""Return the color for the border."""
	return __COLORS[(n // len(__COLORS)) % len(__COLORS)]


def generate_gradient_colors(n: int) -> list[color]:
	"""Generate n gradient colors between color1 and color2."""
	if n <= 0:
		return []
	if n == 1:
		return [__COLOR_1]
	if n == 2:
		return [__COLOR_1, __COLOR_2]
	
	gradient_colors = []
	
	# Calculate the difference between each color channel
	r_diff = (__COLOR_2[0] - __COLOR_1[0]) / (n - 1)
	g_diff = (__COLOR_2[1] - __COLOR_1[1]) / (n - 1)
	b_diff = (__COLOR_2[2] - __COLOR_1[2]) / (n - 1)
	
	# Generate the gradient colors
	for i in range(n):
		r = int(__COLOR_1[0] + i * r_diff)
		g = int(__COLOR_1[1] + i * g_diff)
		b = int(__COLOR_1[2] + i * b_diff)
		gradient_colors.append((r, g, b))
	
	return gradient_colors
