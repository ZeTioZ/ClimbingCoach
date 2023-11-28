from sqlalchemy import Integer, String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from .base_table import BaseTable

class Route(BaseTable):

    __tablename__ = 'route'


    name: Mapped[str] = mapped_column(String, primary_key=True)
    description: Mapped[str] = mapped_column(String)
    difficulty: Mapped[int] = mapped_column(Integer)
    image: Mapped[bytes] = mapped_column(LargeBinary)
    holds: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)