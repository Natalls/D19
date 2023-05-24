from django.db import models
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django import forms


class Profile(models.Model):
    user = models.ForeignKey(User, related_name='profile', default=None, on_delete=models.CASCADE)
    code = models.CharField(max_length=10, blank=True, null=True, default=None)
    date = models.DateField(blank=True, null=True)


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)

        return user



