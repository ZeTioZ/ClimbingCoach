from .. import database_handler
from ..models.run import Run

from ...objects.skeletons_record import SkeletonsRecord
from ...utils.serializer import serialize_skeletons_record 

from .user_queries import get_user_by_username

DATABASE_HANDLER = database_handler.get_instance_database()


def create_run(skeletons_record: SkeletonsRecord, runtime: int, username: str, route: str):
    user = get_user_by_username(username)
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


def get_runs_by_user(user: str) -> list[Run]:
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Run).filter(Run.user.username == user).all()


def get_runs_by_route(route: str) -> list[Run]:
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Run).filter(Run.route.name == route).all()


def get_run_by_id(id: int) -> Run:
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Run).filter(Run.id == id).first()


def get_runs_by_user_and_route(user: str, route: str) -> list[Run]:
    with DATABASE_HANDLER.get_session() as session:
        return session.query(Run).filter(Run.user.username == user, Run.route.name == route).all()


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
