from sqlalchemy import Column, String
from sqlalchemy.orm import DeclarativeBase, Mapped

from .base_table import BaseTable


class User(BaseTable):

    __tablename__ = 'user'

    username: Mapped[str] = Column(String(50), primary_key=True, nullable=False)
    password: Mapped[str] = Column(String(50), nullable=False)
    role: Mapped[str] = Column(String(50), nullable=False)
