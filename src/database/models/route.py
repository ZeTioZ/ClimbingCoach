from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped

from .base_table import BaseTable

class Route(BaseTable):

    __tablename__ = 'route'

    name: Mapped[str] = Column(String, primary_key=True)
    description: Mapped[str] = Column(String)
    difficulty: Mapped[int] = Column(Integer)
    image: Mapped[bytes] = Column(LargeBinary)
    holds: Mapped[bytes] = Column(LargeBinary, nullable=False)