from sqlalchemy import Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base_table import BaseTable
from database.models.wall import Wall


class Route(BaseTable):
	__tablename__ = 'route'

	name: Mapped[String] = mapped_column(String, primary_key=True, nullable=False)
	description: Mapped[String] = mapped_column(String, nullable=False)
	difficulty: Mapped[Integer] = mapped_column(Integer, nullable=False)
	image: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
	holds: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
	wall_name: Mapped[Wall] = mapped_column(String, ForeignKey('wall.name', ondelete='CASCADE'), nullable=False)
