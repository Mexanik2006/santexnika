from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand', 'price', 'quantity', 'unit', 'created_at']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'brand']
    list_filter = ['unit', 'created_at']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')