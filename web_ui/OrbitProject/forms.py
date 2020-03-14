
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
  # email = forms.EmailField(max_length=254)
	class Meta:
		model = User
		fields = ('username','email')

class EditProfile(forms.Form):
    username = forms.CharField(required = False)
    email = forms.EmailField(required = False)
    old_password = forms.CharField(required = False)
    new_password = forms.CharField(required = False)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
