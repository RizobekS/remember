from django import forms
from .models import Contact, CalculateCost, Feedback


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
