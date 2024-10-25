import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def create_user():
    def _create_user(**kwargs):
        return get_user_model().objects.create_user(**kwargs)

    return _create_user
