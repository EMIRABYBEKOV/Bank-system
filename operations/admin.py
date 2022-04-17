from django.contrib import admin
from .models import Wallet, Transfer, Credit

admin.site.register(Wallet)
admin.site.register(Transfer)
admin.site.register(Credit)
