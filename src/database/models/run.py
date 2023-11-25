from sqlalchemy import Integer, LargeBinary, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database.models.user import User
from database.models.route import Route

from .base_table import BaseTable

class Run(BaseTable):

    __tablename__ = 'run'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    skeletons: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    runtime: Mapped[int] = mapped_column(Integer, nullable=False)
    username: Mapped[User] = mapped_column(String, ForeignKey('user.username', ondelete='CASCADE'), nullable=False)
    route_name: Mapped[Route] = mapped_column(String, ForeignKey('route.name', ondelete='CASCADE'), nullable=False)