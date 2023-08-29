from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django import forms


class ChangePasswordForm(PasswordChangeForm):
    pass


class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'author', 'article']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'article': forms.Textarea(attrs={'class': 'form-control textArea'})
        }


class UserRegister(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = Profile
        fields = [
            'first_name',
            'last_name',
            'username',
            'occupation',
            'email',
            'password1',
            'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(UserRegister, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super(UserRegister, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username', 'email', 'occupation']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control'})

        }

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profilePicture']


class DeleteAccountForm(forms.Form):
    confirmation = forms.BooleanField(label='Confirm Account Deletion')

    def clean_confirmation(self):
        confirmation = self.cleaned_data.get('confirmation')
        if not confirmation:
            raise forms.ValidationError(
                'You must confirm the account deletion.')
        return confirmation


class Search(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
