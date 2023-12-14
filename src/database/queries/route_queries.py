from numpy import ndarray
from sqlalchemy.exc import SQLAlchemyError

from objects.route import Route as RouteObject
from utils.serializer_utils import serialize_holds
from .. import database_handler
from ..models.route import Route

DATABASE_HANDLER = database_handler.get_instance_database()


def create_route(route: RouteObject, wall_name: str, description: str = None, difficulty: int = None,
                 image: ndarray = None):
	serialized_holds = serialize_holds(route.get_holds())
	route = Route(name=route.name, description=description, difficulty=difficulty, image=image,
	              holds=serialized_holds, wall_name=wall_name)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			session.add(route)
			session.commit()
		except SQLAlchemyError:
			session.rollback()
			raise


def get_route_by_name(name: str) -> Route:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Route).filter(Route.name == name).first()


def get_route_by_wall_name(wall_name: str) -> list[Route]:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Route).filter(Route.wall_name == wall_name).all()


def get_all_routes() -> list[Route]:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Route).all()


def delete_route_by_name(name: str):
	route = get_route_by_name(name)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			session.delete(route)
			session.commit()
		except SQLAlchemyError:
			session.rollback()
			raise
