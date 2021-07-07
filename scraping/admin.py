from django.contrib import admin
from .models import Price


class PriceAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'company', 'url')
    list_filter = ('user', 'company')
    search_fields = ('user__username', 'name', 'url')
    list_per_page = 20


# admin.site.register(Price, PriceAdmin)
