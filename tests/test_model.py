"""Regression test for output consistency.

To update reference data, run:

python test_model.py update-reference
"""

import sys

import pandas as pd
from classmodel.config import CLASSConfig
from classmodel.model import Model

REFERENCE_DATA = "tests/test_output.csv"


def update_reference_data():
    """(Re)Generate data for regression test.

    Should be run only once when the expected output changes.
    """
    config = CLASSConfig()
    r1 = Model(config)
    r1.run()
    output = r1.out.to_pandas()
    output.to_csv(REFERENCE_DATA)


def test_model():
    """Verify that model with default config reproduces previous result."""
    config = CLASSConfig()
    r1 = Model(config)
    r1.run()
    output = r1.out
    expected_output = pd.read_csv(REFERENCE_DATA, index_col=0)

    pd.testing.assert_frame_equal(output, expected_output)


if __name__ == "__main__":
    if len(sys.argv == 0):
        print("Use `pytest` to run test")
        print("Use `python test_model update-reference` to update reference data")

    if sys.argv[1] == "update-reference":
        print("Updating reference data")
        update_reference_data()
