from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'lname', 'skidka']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'lname']
    list_filter = ['skidka']