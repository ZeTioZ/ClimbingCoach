from numpy import ndarray

from objects.route import Route as RouteObject
from utils.serializer_utils import serialize_route
from .. import database_handler
from ..models.route import Route

DATABASE_HANDLER = database_handler.get_instance_database()


def create_route(route: RouteObject, description: str = None, difficulty: int = None, image: ndarray = None):
	serialized_route = serialize_route(route)
	route = Route(name=RouteObject.name, description=description, difficulty=difficulty, image=image,
	              holds=serialized_route)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			session.add(route)
			session.commit()
		except:
			session.rollback()
			raise


def get_route_by_name(name: str) -> Route:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Route).filter(Route.name == name).first()


def get_all_routes() -> list[Route]:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Route).all()


def delete_route_by_name(name: str):
	route = get_route_by_name(name)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			route.delete()
			session.commit()
		except:
			session.rollback()
			raise
