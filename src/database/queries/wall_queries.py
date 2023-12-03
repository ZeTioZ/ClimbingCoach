from numpy import ndarray

from .. import database_handler
from ..models.wall import Wall

DATABASE_HANDLER = database_handler.get_instance_database()


def create_wall(name: str, difficulty: int, description: str = None, image: bytes = None):
	wall = Wall(name=name, difficulty=difficulty, description=description, image=image)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			session.add(wall)
			session.commit()
		except:
			session.rollback()
			raise


def get_wall_by_name(name: str) -> Wall:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Wall).filter(Wall.name == name).first()


def get_all_walls() -> list[Wall]:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Wall).all()


def delete_wall_by_name(name: str):
	wall = get_wall_by_name(name)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			wall.delete()
			session.commit()
		except:
			session.rollback()
			raise
