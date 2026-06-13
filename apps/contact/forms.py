from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ContactRequest


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'phone', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-field__input',
                'placeholder': _('Ваше ім\'я'),
                'autocomplete': 'name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-field__input',
                'placeholder': 'email@example.com',
                'autocomplete': 'email',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-field__input',
                'placeholder': '+420 000 000 000',
                'autocomplete': 'tel',
                'inputmode': 'tel',
            }),
            'service': forms.TextInput(attrs={
                'class': 'form-field__input',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-field__input',
                'rows': 4,
                'placeholder': _('Ваше повідомлення…'),
            }),
        }
        labels = {
            'name': _('Ім\'я'),
            'email': _('Email'),
            'phone': _('Телефон'),
            'service': _('Послуга'),
            'message': _('Повідомлення'),
        }
