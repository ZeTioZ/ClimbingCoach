import pickle

from objects.hold import Hold
from objects.skeletons_record import SkeletonsRecord


def serialize_skeletons_record(skeletons_record: SkeletonsRecord) -> bytes:
	"""
	Serializes the given skeletons record into a pickle bytes object.
	"""
	return pickle.dumps(skeletons_record)


def deserialize_skeletons_record(serialized_skeletons_record: bytes) -> SkeletonsRecord:
	"""
	Deserializes the given pickle bytes object into a SkeletonsRecord object.
	"""
	return pickle.loads(serialized_skeletons_record)


def serialize_holds(holds: list[Hold]) -> bytes:
	"""
	Serializes the given holds into a pickle bytes object.
	"""
	return pickle.dumps(holds)


def deserialize_holds(serialized_holds: bytes) -> list[Hold]:
	"""
	Deserializes the given pickle bytes object into a list of Hold objects.
	"""
	return pickle.loads(serialized_holds)
