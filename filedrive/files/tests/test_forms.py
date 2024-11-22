import pytest
from files.forms import SignupForm

@pytest.mark.django_db
def test_signup_form_valid():
    form_data = {
        "email": "test@example.com",
        "password1": "StrongerPassword@123", 
        "password2": "StrongerPassword@123",
        "first_name": "John",
        "last_name": "Doe",
    }
    form = SignupForm(data=form_data)
    assert form.is_valid(), f"Form errors: {form.errors}"


@pytest.mark.django_db
def test_signup_form_invalid():
    form_data = {
        "email": "test@example.com",
        "password1": "password123",
        "password2": "wrongpassword",
    }
    form = SignupForm(data=form_data)
    assert not form.is_valid()
