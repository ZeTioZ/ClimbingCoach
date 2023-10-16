from .position import Position


class RouteConfigurator:
    """
    RouteConfigurator class for configuring a climbing route using a list of holds
    """
    def __init__(self, holds: list = list()):
        """
        Initializes the RouteConfigurator object with the given list of holds.

        :param holds: A list of Hold objects representing the available holds.
        """
        self.holds = holds
        self.route = []


    def step(self, position: Position) -> None:
        """
        Adds or removes a hold from the route based on the given position.

        If the position is inside a hold in the route, the hold is removed from the route.
        If the position is inside a hold not in the route, the hold is added to the route.
        If the position is not inside any hold, nothing happens.

        :param position: A tuple representing the (x, y) position of the climber.
        """
        for hold in self.route:
            if hold.collide(position):
                self.route.remove(hold)
                return

        for hold in self.holds:
            if hold.collide(position):
                self.route.append(hold)
                return


    def get_route(self) -> list:
        """
        :return: A list of Hold objects representing the holds in the current route.
        """
        return self.route
