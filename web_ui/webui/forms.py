from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username','email','password1','password2')

class EditProfile(forms.Form):
    new_name = forms.CharField(required = False)
    new_email = forms.EmailField(required = False)
    old_password = forms.CharField(required = False)
    new_password = forms.CharField(required = False)

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RestoreForm(forms.Form):
    user_email = forms.CharField()
 
class ChangePassForm(forms.Form):
    new_pass = forms.CharField(required = True)
    repeat_new_pass = forms.CharField(required = True)

 
