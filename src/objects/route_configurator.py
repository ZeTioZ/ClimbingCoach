class RouteConfigurator:
    """
    RouteConfigurator class for configuring a climbing route using a list of holds.

    Attributes:
        holds: A list of Hold objects representing the available holds.
        route: A list of Hold objects representing the holds in the current route.
    """

    def __init__(self, holds):
        """
        Initializes the RouteConfigurator object with the given list of holds.

        Args:
            holds: A list of Hold objects representing the available holds.
        """
        self.holds = holds
        self.route = []

    def step(self, position):
        """
        Adds or removes a hold from the route based on the given position.

        If the position is inside a hold in the route, the hold is removed from the route.
        If the position is inside a hold not in the route, the hold is added to the route.
        If the position is not inside any hold, nothing happens.

        Args:
            position: A tuple representing the (x, y) position of the climber.
        """
        for hold in self.route:
            if hold.is_position_inside(position):
                self.route.remove(hold)
                return

        for hold in self.holds:
            if hold.is_position_inside(position):
                self.route.append(hold)
                return

    def get_route(self) -> list:
        """
        Returns the list of holds in the current route.

        Returns:
            A list of Hold objects representing the holds in the current route.
        """
        return self.route