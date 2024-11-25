from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UsernameField

# from django.forms.renderers import BaseRenderer
# from django.forms.utils import ErrorList
from django.utils.translation import gettext_lazy as _

from core.models import User


class ShareForm(forms.Form):
    file = forms.TextInput(attrs={"hidden": ""})
    share_with = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True))

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop("user_id")
        super().__init__(args, kwargs)
        self.fields["share_with"].queryset = self.fields["share_with"].queryset.exclude(id=user_id)
        print(self.fields["share_with"].queryset)


class AuthForm(AuthenticationForm):
    username = UsernameField(
        label=_("Email"), widget=forms.EmailInput(attrs={"autofocus": True, "placeholder": "name@example.com"})
    )
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
        labels = {"email": _("Email")}
        widgets = {
            "email": forms.EmailInput(attrs={"autofocus": True, "placeholder": "name@example.com"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First Name", "autocapitalize": "words"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name", "autocapitalize": "words"}),
        }
