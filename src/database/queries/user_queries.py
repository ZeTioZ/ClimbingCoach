import bcrypt

from .. import database_handler
from ..models.user import User

DATABASE_HANDLER = database_handler.get_instance_database()


def create_user(username: str, password: str, role: str = "user"):
	"""
	Creates a new user in the database.

	:param username: The name of the user.
	:param password: The password of the user.
	:param role: The role of the user.
	"""
	with DATABASE_HANDLER.get_session() as session:
		if get_user_by_name(username) is not None:
			raise ValueError("A user with the same name already exists.")

		salt = bcrypt.gensalt()
		password = bcrypt.hashpw(password.encode(), salt)
		user = User(username=username, password=password, role=role)
		session.begin()
		try:
			session.add(user)
			session.commit()
		except:
			session.rollback()
			raise


def get_user_by_name(username: str) -> User:
	"""
	Gets a user from the database by its username.

	:param username: The name of the user.
	:return: The user.
	"""
	with DATABASE_HANDLER.get_session() as session:
		return session.query(User).filter(User.username == username).first()


def get_all_users() -> list[User]:
	"""
	Gets all the users from the database.

	:return: A list of users.
	"""
	with DATABASE_HANDLER.get_session() as session:
		return session.query(User).all()


def delete_user_by_name(username: str):
	"""
	Deletes a user from the database by its username.

	:param username: The name of the user.
	"""
	user = get_user_by_name(username)
	with DATABASE_HANDLER.get_session() as session:
		session.begin()
		try:
			user.delete()
			session.commit()
		except:
			session.rollback()
			raise


def user_can_connect(username: str, password: str) -> (bool, User):
	"""
	Checks if a user is in the database and if the password is correct.

	:param username: The name of the user.
	:param password: The password of the user.
	:return: A boolean indicating whether the user can connect with the given password and the user object itself.
	"""
	with DATABASE_HANDLER.get_session() as session:
		user = session.query(User).filter(User.username == username).first()
		can_connect = user is not None and bcrypt.checkpw(password.encode(), user.password)
		return can_connect, user if can_connect else None
