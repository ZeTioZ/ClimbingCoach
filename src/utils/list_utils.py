from objects.skeleton import Skeleton


def list_filler(first: list[Skeleton | None], second: list[Skeleton | None]) -> list:
    """
    Fills the shortest list with None values to match the length of the longest list.
    """
    if len(first) > len(second):
        for i in range(len(first) - len(second)):
            second.append(None)
    elif len(second) > len(first):
        for i in range(len(second) - len(first)):
            first.append(None)
    return first, second