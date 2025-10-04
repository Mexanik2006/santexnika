from django.db import models

class Product(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogramm'),
        ('dona', 'Dona'),
        ('kub', 'Kub'),
        ('litr', 'Litr'),
        ('metr', 'Metr'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    brand = models.CharField(max_length=100, verbose_name="Brend")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Narx")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Miqdor")
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, verbose_name="Oʻlchov birligi")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
    
    def __str__(self):
        return f"{self.name} - {self.brand}"
    
    def save(self, *args, **kwargs):
        # Katta-kichik harflarni standartlashtirish
        self.name = self.name.strip()
        self.brand = self.brand.strip()
        super().save(*args, **kwargs)