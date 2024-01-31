import hashlib
import os
from typing import Optional
import random
import string

import numpy as np


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


def embed_in_larger_matrix(m: np.ndarray, length: int, offset: int = 0, value: int = -1) -> np.ndarray:
    """
    Embeds a smaller matrix in a larger matrix

    m must be a square matrix

    :param m: smaller matrix
    :param length: length of new matrix
    :param offset: offset, along the diagonal, to place the smaller matrix (default: 0)
    :param value: value to fill the larger matrix with (default: -1)
    """
    assert m.shape[0] == m.shape[1], 'Matrix must be square'
    assert m.shape[0] + offset <= length, 'Matrix does not fit in larger matrix'
    out = np.full((length, length), value)
    out[offset:offset + m.shape[0], offset:offset + m.shape[1]] = m
    return out
