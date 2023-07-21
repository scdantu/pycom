import hashlib
import os
from typing import Optional
import random
import string


def human_num(num):
    """Converts a number to a human-readable string.
    Adapted from: https://stackoverflow.com/a/45846841
    Distributed under: CC BY-SA 3.0"""
    if num == 1:
        return 'operation'
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


def generate_random_string(n: int) -> str:
    """Generates a random string of n uppercase letters and numbers.

    Args:
        n: The length of the string to generate.

    Returns:
        A random string of n letters and numbers.
    """
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(n))


def strip_whitespace(s: str) -> str:
    """Takes a string and removes double spaces, tabs, and newlines."""
    return ' '.join(s.split())


def md5_hash(s: str) -> str:
    """Returns the md5 hash of a string."""
    return hashlib.md5(s.encode()).hexdigest()


def user_path(s: str) -> Optional[str]:
    """Returns the path with user home directory expanded."""
    if s is None:
        return None
    if s.startswith('~'):
        return os.path.expanduser(s)
    return s
