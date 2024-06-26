import numpy as np
import pytest

from pysindy.utils import AxesArray
from pysindy.utils import reorder_constraints
from pysindy.utils import validate_control_variables


def test_reorder_constraints_1D():
    target_order = np.arange(6)
    row_order = np.array([0, 3, 1, 4, 2, 5])
    n_feats = 3

    np.testing.assert_array_equal(
        reorder_constraints(target_order, n_feats).flatten(), row_order
    )
    np.testing.assert_array_equal(
        reorder_constraints(row_order, n_feats, output_order="target").flatten(),
        target_order,
    )


def test_reorder_constraints_2D():
    target_order = np.arange(12).reshape((2, 6))
    row_order = np.array([[0, 3, 1, 4, 2, 5], [6, 9, 7, 10, 8, 11]])
    n_feats = 3

    np.testing.assert_array_equal(reorder_constraints(target_order, n_feats), row_order)
    np.testing.assert_array_equal(
        reorder_constraints(row_order, n_feats, output_order="target"), target_order
    )


def test_validate_controls():
    with pytest.raises(ValueError):
        validate_control_variables(1, [])
    with pytest.raises(ValueError):
        validate_control_variables([], 1)
    with pytest.raises(ValueError):
        validate_control_variables([], [1])
    arr = AxesArray(np.ones(4).reshape((2, 2)), axes={"ax_time": 0, "ax_coord": 1})
    with pytest.raises(ValueError):
        validate_control_variables([arr], [arr[:1]])
    u_mod = validate_control_variables([arr], [arr], trim_last_point=True)
    assert u_mod[0].n_time == 1
