from sqlalchemy.exc import SQLAlchemyError

from database import user_queries
from objects.skeletons_record import SkeletonsRecord
from utils.serializer_utils import serialize_skeletons_record
from .. import database_handler
from ..models.run import Run

DATABASE_HANDLER = database_handler.get_instance_database()


def create_run(skeletons_record: SkeletonsRecord, runtime: int, username: str, route_name: str):
	user = user_queries.get_user_by_username(username)
	if user is None:
		raise ValueError(f"User {username} does not exist.")
	skeletons_record_serialized = serialize_skeletons_record(skeletons_record)
	run = Run(skeletons=skeletons_record_serialized, runtime=runtime, username=username, route_name=route_name)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			session.add(run)
			session.commit()
		except SQLAlchemyError:
			session.rollback()
			raise


def get_runs_by_user(username: str) -> list[Run]:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Run).filter(Run.username == username).all()


def get_runs_by_route(route_name: str) -> list[Run]:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Run).filter(Run.route_name == route_name).all()


def get_run_by_id(run_id: int) -> Run:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Run).filter(Run.id == run_id).first()


def get_runs_by_user_and_route(username: str, route_name: str) -> list[Run]:
	with DATABASE_HANDLER.get_session() as session:
		return session.query(Run).filter(Run.username == username, Run.route_name == route_name).all()


def delete_run_by_id(run_id: int):
	run = get_run_by_id(run_id)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			run.delete()
			session.commit()
		except:
			session.rollback()
			raise
