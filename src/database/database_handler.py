import json
import os

from sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .models.base_table import BaseTable

INSTANCE = None

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))

DATABASE_CONFIG_FILE = open(os.path.join(parent_dir, "resources", "configs", "database.json"), "r")
DATABASE_CONFIG = json.load(DATABASE_CONFIG_FILE)
CONNECTION_URL = URL.create(
	drivername=DATABASE_CONFIG["drivername"] if DATABASE_CONFIG["drivername"] != "" else "sqlite",
	username=DATABASE_CONFIG["username"] if DATABASE_CONFIG["username"] != "" else None,
	password=DATABASE_CONFIG["password"] if DATABASE_CONFIG["password"] != "" else None,
	host=DATABASE_CONFIG["host"] if DATABASE_CONFIG["host"] != "" else None,
	port=DATABASE_CONFIG["port"] if DATABASE_CONFIG["port"] != "" else None,
	database=DATABASE_CONFIG["database"] if DATABASE_CONFIG["database"] != "" else "database.db"
)


class DatabaseHandler:
	def __init__(self):
		self.engine = create_engine(CONNECTION_URL)
		self.connection = None

	def get_connection(self):
		if self.connection is None or self.connection.closed:
			self.connection = self.engine.connect()
		return self.connection

	def get_session(self):
		return Session(bind=self.get_connection().engine)

	def create_tables(self):
		BaseTable.metadata.create_all(self.engine)


def get_instance_database():
	global INSTANCE
	if INSTANCE is None:
		INSTANCE = DatabaseHandler()
	return INSTANCE
