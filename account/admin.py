from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_name', 'last_name', 'email')
    # list_filter = ('name', 'price', 'doctor',)
    # search_fields = ('name', 'description',)
    # raw_id_fields = ('doctor',)
    # ordering = ('name', 'price',)