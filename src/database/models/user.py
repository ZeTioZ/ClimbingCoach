from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base_table import BaseTable


class User(BaseTable):

    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String(50), primary_key=True, nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False)