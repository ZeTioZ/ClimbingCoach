from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.orm import Mapped

from .base_table import BaseTable

class Route(BaseTable):

    __tablename__ = 'route'

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String)
    description: Mapped[str] = Column(String)
    difficulty: Mapped[int] = Column(Integer)
    image: Mapped[bytes] = Column(LargeBinary)
    holds: Mapped[bytes] = Column(LargeBinary, nullable=False)