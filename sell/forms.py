from django import forms
from decimal import Decimal
from .models import Sale
from clients.models import Account
from products.models import Product

class SaleItemForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(quantity__gt=0),
        label="Mahsulot",
        widget=forms.Select(attrs={
            'class': 'product-select w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
        })
    )
    quantity = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Miqdor",
        widget=forms.NumberInput(attrs={
            'class': 'quantity-input w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
            'step': '0.01',
            'min': '0.01',
            'placeholder': 'Miqdor'
        })
    )
    unit_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Narx",
        widget=forms.NumberInput(attrs={
            'class': 'unit-price-input w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent bg-gray-100',
            'readonly': True
        })
    )

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['client', 'discount', 'payment_method']
        widgets = {
            'client': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent',
                'step': '0.01',
                'min': '0',
                'max': '100',
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-accent focus:border-transparent'
            })
        }
        labels = {
            'client': 'Mijoz',
            'discount': 'Umumiy chegirma (%)',
            'payment_method': "To'lov usuli"
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Account.objects.all()
        self.fields['client'].required = False