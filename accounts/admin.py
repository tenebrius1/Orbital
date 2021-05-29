from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item', 'date', 'company', 'price') # Changes what is displayed in the admin page for Transaction model
    list_filter = ('user',) # Sort by user
    search_fields = ('user__username', 'item', 'date', 'price')
    list_per_page = 50

admin.site.register(Transaction, TransactionAdmin)