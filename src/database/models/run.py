from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped

from user import User
from route import Route

from .base_table import BaseTable

class Run(BaseTable):

    __tablename__ = 'run'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    skeletons: Mapped[bytes] = Column(LargeBinary, nullable=False)
    runtime: Mapped[int] = Column(Integer, nullable=False)
    user: Mapped[User] = Column(User, ForeignKey('user.username'), on_delete='CASCADE', nullable=False)
    route: Mapped[Route] = Column(Route, ForeignKey('route.name'), on_delete='CASCADE', nullable=False)
