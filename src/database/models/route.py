from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base_table import BaseTable


class Route(BaseTable):
	__tablename__ = 'route'

	name: Mapped[String] = mapped_column(String, primary_key=True)
	description: Mapped[String] = mapped_column(String)
	difficulty: Mapped[Integer] = mapped_column(Integer)
	image: Mapped[LargeBinary] = mapped_column(LargeBinary)
	holds: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
