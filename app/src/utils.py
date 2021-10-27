def hash_string(s: str) -> int:
    return abs(hash(s)) % (10 ** 8)
