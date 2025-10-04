from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from decimal import Decimal
from clients.models import Account
from products.models import Product

class Sale(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Naqd'),
        ('card', 'Karta'),
        ('transfer', "O'tkazma"),
    ]
    
    client = models.ForeignKey(
        Account, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Mijoz"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        verbose_name="Mahsulot"
    )
    quantity = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Miqdor"
    )
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Narx"
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Jami narx"
    )
    discount = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0, 
        verbose_name="Chegirma (%)"
    )
    final_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Yakuniy narx"
    )
    payment_method = models.CharField(
        max_length=10, 
        choices=PAYMENT_METHODS, 
        default='cash', 
        verbose_name="To'lov usuli"
    )
    seller = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Sotuvchi"
    )
    sale_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Sotilgan sana"
    )
    
    class Meta:
        verbose_name = "Sotuv"
        verbose_name_plural = "Sotuvlar"
        ordering = ['-sale_date']
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.product.unit}"
    
    def save(self, *args, **kwargs):
        # Calculate total price
        self.total_price = self.quantity * self.unit_price
        
        # Apply discount
        discount_amount = (self.total_price * self.discount) / Decimal('100')
        self.final_price = self.total_price - discount_amount
        
        # Stock validation and update
        if self.pk:  # Updating
            old_sale = Sale.objects.get(pk=self.pk)
            available = self.product.quantity + old_sale.quantity
            if self.quantity > available:
                raise ValidationError(f"Mahsulot '{self.product.name}' uchun yetarli miqdor yo'q. Mavjud: {self.product.quantity}")
            quantity_diff = self.quantity - old_sale.quantity
            self.product.quantity -= quantity_diff
        else:  # Creating new
            if self.quantity > self.product.quantity:
                raise ValidationError(f"Mahsulot '{self.product.name}' uchun yetarli miqdor yo'q. Mavjud: {self.product.quantity}")
            self.product.quantity -= self.quantity
        
        self.product.save()
        super().save(*args, **kwargs)