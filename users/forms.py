from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm) : 
    email = forms.EmailField()

    #class Meta gives us nested namespace for config and keeps the config in one place 
    #and it includes the model for the User that has been successfully made and saved

    class Meta : 
        model = User 
        fields = ['username' , 'email' , 'password1']

class UserUpdateForm(forms.ModelForm) : 
    email = forms.EmailField()

    #class Meta gives us nested namespace for config and keeps the config in one place 
    #and it includes the model for the User that has been successfully made and saved

    class Meta : 
        model = User 
        fields = ['username' , 'email']

class ProfileUpdateForm(forms.ModelForm) : 
    class Meta : 
        model = Profile 
        fields = ['image']