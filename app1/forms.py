from django import forms
from .models import Contact

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "email","subject","message",
        ]



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='Email')  # Define the email field directly in the class

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")  # Include email field in Meta

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None


