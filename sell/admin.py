from django.contrib import admin
from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'product', 'client', 'quantity', 'unit_price', 
        'final_price', 'sale_date', 'seller'
    ]
    list_filter = ['sale_date', 'payment_method', 'seller']
    search_fields = ['product__name', 'client__name', 'client__lname']
    readonly_fields = ['sale_date']
    date_hierarchy = 'sale_date'