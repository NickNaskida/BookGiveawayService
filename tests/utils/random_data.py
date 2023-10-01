import uuid


def random_suffix():
    return uuid.uuid4().hex[:6]


def random_author() -> str:
    return f"Author-{random_suffix()}"
