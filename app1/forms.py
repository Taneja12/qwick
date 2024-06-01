from django import forms
from .models import Contact

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "email","subject","message",
        ]
        labels = {
            'email': '',
            'subject': '',
            'message': '',
        }
        widgets = {
                    'email' : forms.EmailInput(attrs={'placeholder':'Email', 'name':'email'}),
                    'subject': forms.TextInput(attrs={'placeholder': 'Subject','class': 'custom-width', 'name':'subject'}),
                    'message': forms.Textarea(attrs={'placeholder': 'Message','rows': 5, 'cols': 25, 'name':'message'}),
                }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    first_name = forms.CharField(max_length=30, required=True, label='', widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    
    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2")
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
