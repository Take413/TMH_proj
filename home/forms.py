from django import forms
from home.models import Pet, UserProfile
from django.contrib.auth.models import User
import re


EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

#Add product - not finished
class PetForm (forms.ModelForm):
    name = forms.CharField(max_length = 128, help_text="Please enter the name of the pet.")
    description = forms.CharField(help_text="Enter short description of the pet.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model=Pet
        exclude=('subcategory',)


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    password2=forms.CharField(widget=forms.PasswordInput())

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not re.match(EMAIL_REGEX, email):
            raise forms.ValidationError('Invalid email format')
        return email

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','email','password',)

class UserProfileForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = UserProfile
        fields = ('picture',)

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['city', 'postcode', 'description', 'picture','address']
    field_order=['address', 'postcode', 'city', 'description', 'picture']
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    

