from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput
from django.utils.translation import gettext_lazy as _

from .models import User, Contact, CalculateCost, Feedback


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name', 'phone', 'email', 'message'
        ]


class CalculateForm(forms.ModelForm):
    class Meta:
        model = CalculateCost
        fields = [
            'name', 'email', 'phone', 'service', 'text'
        ]


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = [
            'name', 'email', 'phone', 'service', 'text'
        ]


class NewUserForm(UserCreationForm):
    phone = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'email', 'password1', 'password2']
        widgets = {
            'first_name': TextInput(attrs={'type': 'text', 'placeholder': _('Имя')}),
            'last_name': TextInput(attrs={'text': 'text', 'placeholder': _('Фамилия')}),
            'phone': TextInput(attrs={'type': 'text', 'placeholder': _('Телефон')}),
            'email': TextInput(attrs={'type': 'email', 'placeholder': _('Ваша электронная почта')}),
            'password1': TextInput(attrs={'type': 'password', 'placeholder': _('Новый пароль')}),
            'password2': TextInput(attrs={'type': 'password', 'placeholder': _('Повторите пароль')}),
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user
