import base64
import pickle
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