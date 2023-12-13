from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_table import BaseTable


class Wall(BaseTable):
	__tablename__ = 'wall'

	name: Mapped[String] = mapped_column(String, primary_key=True, nullable=False)
	difficulty: Mapped[Integer] = mapped_column(Integer, nullable=False)
	description: Mapped[String] = mapped_column(String, nullable=False)
	image: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
	route = relationship("Route", backref="wall_route", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
