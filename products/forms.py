from django import forms
from .models import Product

class ExcelImportForm(forms.Form):
    excel_file = forms.FileField(
        label='Excel fayl',
        help_text='Quyidagi ustunlar boʻlgan Excel fayl: Nomi, Brend, Narx (so‘m), Dona/Miqdor, Oʻlchov birligi',
        widget=forms.FileInput(attrs={
            'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-accent file:text-accent-foreground hover:file:opacity-90',
            'accept': '.xlsx, .xls'
        })
    )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'price', 'quantity', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'placeholder': 'Mahsulot nomi'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'placeholder': 'Brend'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'placeholder': 'Narx',
                'step': '0.01'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'placeholder': 'Miqdor',
                'step': '0.01'
            }),
            'unit': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent'
            })
        }
        labels = {
            'name': 'Mahsulot nomi',
            'brand': 'Brend',
            'price': 'Narx',
            'quantity': 'Miqdor',
            'unit': 'Oʻlchov birligi'
        }