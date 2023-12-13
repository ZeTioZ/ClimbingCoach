from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_table import BaseTable


class User(BaseTable):
	__tablename__ = 'user'

	username: Mapped[String] = mapped_column(String(50), primary_key=True, nullable=False)
	password: Mapped[String] = mapped_column(String(50), nullable=False)
	role: Mapped[String] = mapped_column(String(50), nullable=False)
	run = relationship("Run", backref="user_run", cascade='save-update, merge, delete, delete-orphan', lazy='dynamic')
