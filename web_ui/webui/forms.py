from django import forms
import re
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

# class EditProfile(forms.Form):
#     new_name = forms.CharField(required = False)
#     new_email = forms.EmailField(required = False)
#     old_password = forms.CharField(required = False)
#     new_password = forms.CharField(required = False)

class EditProfile(forms.Form):
    username = forms.CharField(required = False, widget=forms.TextInput(
    attrs={
        'placeholder':'Изменить имя...',
        'class': 'form-control'
    }))

    def clean_username(self):
        username = self.cleaned_data['username']
        if re.match(r'\d', username):
            raise ValidationError('Имя не должно начинаться с цыфры')
        return username
        
    email = forms.EmailField(required = False, widget=forms.TextInput(
        attrs={
            'placeholder':'Изменить мыло...',
            'class': 'form-control',
        }))
    new_password = forms.CharField(required = False, widget=forms.TextInput(
        attrs={
            'type':'password',
            'placeholder':'Новый пароль...',
            'class': 'form-control',
        }))
    old_password = forms.CharField(widget=forms.TextInput(
        attrs={
            'type':'password',
            'placeholder':'Новый пароль...',
            'class': 'form-control'
        }))

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RestoreForm(forms.Form):
    user_email = forms.CharField()
 
class ChangePassForm(forms.Form):
    new_pass = forms.CharField(required = True)
    repeat_new_pass = forms.CharField(required = True)

 
