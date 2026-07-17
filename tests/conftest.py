import copy

import pytest

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activity_state():
    # Arrange
    original_state = copy.deepcopy(app_module.activities)

    yield

    # Teardown
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original_state))
