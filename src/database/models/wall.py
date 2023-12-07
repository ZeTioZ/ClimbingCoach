from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base_table import BaseTable


class Wall(BaseTable):
	__tablename__ = 'wall'

	name: Mapped[String] = mapped_column(String, primary_key=True)
	difficulty: Mapped[Integer] = mapped_column(Integer)
	description: Mapped[String] = mapped_column(String)
	image: Mapped[LargeBinary] = mapped_column(LargeBinary)
