from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField
from django.utils.translation import gettext_lazy as _

from core.models import User

class AuthForm(AuthenticationForm):
    username = UsernameField(label=_("Email"), widget=forms.EmailInput(attrs={"autofocus": True, "placeholder": "name@example.com"}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Password"}),
    )


class SignupForm(UserCreationForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Password"

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "first_name", "last_name")
        labels = {
            "email": _("Email")
        }
        widgets = {
            "email": forms.EmailInput(attrs={"autofocus": True, "placeholder": "name@example.com"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name", "autocapitalize": "words"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name", "autocapitalize": "words"}),
        }
