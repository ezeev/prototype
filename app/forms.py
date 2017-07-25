
from django import forms
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import EmailField
from django.utils.translation import ugettext_lazy as _

class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True,
        help_text=_("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

'''
class UserUpdateForm(UserChangeForm):
    email = EmailField(label=_("Email address"), required=True,
        help_text=_("Required."))

    class Meta:
        model = User
        fields = ("email", "password1", "password2")
'''

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('organization_name',)