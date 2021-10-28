import hashlib


def hash_string(s: str) -> int:
    return int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
