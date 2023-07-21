from enum import Enum

import pandas as pd


class MatrixFormat(Enum):
    """
    MatrixFormat is an enum that specifies how the coevolution matrices are returned by the PyCom class.
    """
    NUMPY = lambda x: x
    PANDAS = lambda x: pd.DataFrame(x)
    LIST = lambda x: x.tolist()
    JSON = lambda x: x.tolist()
