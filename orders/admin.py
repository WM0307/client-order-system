from django.contrib import admin
from .models import Client, Order

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'created_at')
    search_fields = ('name', 'email', 'company')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'amount', 'status', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'client__name', 'description')
