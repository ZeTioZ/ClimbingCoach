import numpy as np
from objects.route_configurator import RouteConfigurator
from libs.model_loader import ModelLoader


def process_route_from_image(image: np.ndarray, holds_detector: ModelLoader) -> RouteConfigurator:
    """
    Processes a climbing route from an image.

    :param image: The image to process.
    :return: A list of Hold objects representing the holds in the route.
    """
    route_configurator = RouteConfigurator(holds_detector.prefict(image))
    return route_configurator
