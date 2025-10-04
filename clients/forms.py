from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'lname', 'skidka']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'placeholder': 'Ism'
            }),
            'lname': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'placeholder': 'Familiya'
            }),
            'skidka': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'placeholder': 'Chegirma foizi'
            })
        }
        labels = {
            'name': 'Ism',
            'lname': 'Familiya',
            'skidka': 'Chegirma (%)'
        }