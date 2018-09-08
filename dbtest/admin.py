from django.contrib import admin
from .models import Users, Invoices, Purchases


admin.site.register(Users)
admin.site.register(Invoices)
admin.site.register(Purchases)
