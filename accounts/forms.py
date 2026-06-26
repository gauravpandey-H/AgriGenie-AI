from django import forms
from django.contrib.auth.models import User
from .models import Farmer

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['phone_number', 'village', 'district', 'state', 'preferred_language']
