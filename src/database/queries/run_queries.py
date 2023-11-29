from .. import database_handler
from ..models.run import Run

from objects.skeletons_record import SkeletonsRecord
from utils.serializer import serialize_skeletons_record 

from database import user_queries

DATABASE_HANDLER = database_handler.get_instance_database()


def create_run(skeletons_record: SkeletonsRecord, runtime: int, username: str, route: str):
    user = user_queries.get_user_by_username(username)
    skeletons_record_serialized = serialize_skeletons_record(skeletons_record)
    run = Run(skeletons=skeletons_record_serialized, runtime=runtime, user=user, route=route)
    with DATABASE_HANDLER.get_session() as session:
        session.begin()
        try:
            session.add(run)
            session.commit()
        except:
            session.rollback()
            raise


def get_runs_by_user(username: str) -> list[Run]:
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Run).filter(Run.username == username).all()


def get_runs_by_route(route_name: str) -> list[Run]:
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Run).filter(Run.route_name == route_name).all()


def get_run_by_id(id: int) -> Run:
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Run).filter(Run.id == id).first()


def get_runs_by_user_and_route(username: str, route_name: str) -> list[Run]:
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Run).filter(Run.username == username, Run.route_name == route_name).all()


def delete_run_by_id(id: int):
    run = get_run_by_id(id)
    with DATABASE_HANDLER.get_session() as session:
        session.begin()
        try:
            run.delete()
            session.commit()
        except:
            session.rollback()
            raise