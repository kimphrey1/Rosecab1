from django import forms
from .models import Customer, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "example@email.com",
            }
        ),
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        ),
    )
    phone = forms.IntegerField(
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "0771234567",
            }
        ),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "**********",
            }
        ),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "**********",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def save(self, commit=True):  # pragma: no cover
        user = super(UserRegisterForm, self).save(commit=False)
        if commit:
            user.save()
            Customer.objects.create(user=user)
        return user


class CustomLoginForm(AuthenticationForm):
    """Modifying styling of login inputs"""

    username = forms.CharField(label="Email / Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Username or Email",
                "class": "form-control",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "**********",
                "class": "form-control",
            }
        )


class CustomUserCreation(UserCreationForm):
    """Customizing User creation for use in admin panel"""

    class Meta:
        model = User
        fields = "__all__"
