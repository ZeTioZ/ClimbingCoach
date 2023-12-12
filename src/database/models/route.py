from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base_table import BaseTable


class Route(BaseTable):
	__tablename__ = 'route'

	name: Mapped[String] = mapped_column(String, primary_key=True, nullable=False)
	description: Mapped[String] = mapped_column(String, nullable=False)
	difficulty: Mapped[Integer] = mapped_column(Integer, nullable=False)
	image: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
	holds: Mapped[LargeBinary] = mapped_column(LargeBinary, nullable=False)
