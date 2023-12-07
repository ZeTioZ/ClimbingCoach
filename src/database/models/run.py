from sqlalchemy import Integer, LargeBinary, ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from database.models.route import Route
from database.models.user import User
from .base_table import BaseTable


class Run(BaseTable):
	__tablename__ = 'run'

	id: Mapped[Integer] = mapped_column(Integer, primary_key=True, autoincrement=True)
	skeletons: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
	holds: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
	runtime: Mapped[Float] = mapped_column(Float, nullable=False)
	username: Mapped[User] = mapped_column(String, ForeignKey('user.username', ondelete='CASCADE'), nullable=False)
	route_name: Mapped[Route] = mapped_column(String, ForeignKey('route.name', ondelete='CASCADE'), nullable=False)
