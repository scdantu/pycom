# noinspection PyPackageRequirements
import pytest

from pycom.sql.constraints_utils import class_param


def test_cath_param_valid():
    assert class_param('1.2.3.4') == [1, 2, 3, 4]
    assert class_param('1.2.*.*') == [1, 2]
    assert class_param('1.2.3.*') == [1, 2, 3]
    assert class_param('1.*.*.*') == [1]
    assert class_param('1.*') == [1]
    assert class_param('1.*.*') == [1]
    assert class_param('1.2.*') == [1, 2]


def test_cath_param_invalid():
    with pytest.raises(AssertionError):
        class_param('1.2.3.4.5')
    with pytest.raises(AssertionError):
        class_param('1.2.3')
    with pytest.raises(AssertionError):
        class_param('1.2.*.3')
    with pytest.raises(AssertionError):
        class_param('1.2.3.4.*.5')
    with pytest.raises(AssertionError):
        class_param('1.2.3.*.4.*')
    with pytest.raises(AssertionError):
        class_param('1.2.3.4a')
    with pytest.raises(AssertionError):
        class_param('1.2.3.4.')
    with pytest.raises(AssertionError):
        class_param('test')
    with pytest.raises(AssertionError):
        class_param('t.e.s.t')
