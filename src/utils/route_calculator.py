import numpy as np
from objects.route_configurator import RouteConfigurator
from objects.holds_detector import HoldsDetector


def process_route_from_image(image: np.ndarray, holds_detector: HoldsDetector) -> RouteConfigurator:
    """
    Processes a climbing route from an image.

    Args:
        image: The image to process.

    Returns:
        A list of Hold objects representing the holds in the route.
    """
    route_configurator = RouteConfigurator(holds_detector.detect_holds(image))
    return route_configurator
