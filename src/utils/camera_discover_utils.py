from pygrabber.dshow_graph import FilterGraph


def get_available_cameras_names() -> list[str]:
	graph = FilterGraph()
	devices = graph.get_input_devices()
	return devices


if __name__ == "__main__":
	print(get_available_cameras_names())
