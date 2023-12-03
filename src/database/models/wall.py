from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base_table import BaseTable


class Wall(BaseTable):
	__tablename__ = 'wall'

	name: Mapped[str] = mapped_column(String, primary_key=True)
	difficulty: Mapped[int] = mapped_column(Integer)
	description: Mapped[str] = mapped_column(String)
	image: Mapped[bytes] = mapped_column(LargeBinary)
