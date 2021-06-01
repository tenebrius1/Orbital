from django.urls import path
from . import views

urlpatterns = [
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('transaction', views.transaction, name='transaction'),
    path('price', views.price, name='price'),
    path('delivery', views.delivery, name='delivery'),
    path('ship', views.ship, name='ship'),

    # Handles AJAX requests
    path('deleteTransaction', views.deleteTransaction, name='deleteTransaction'),
    path('displayExpenses', views.displayExpenses, name='displayExpenses'),
    path('editTransaction', views.editTransaction, name='editTransaction'),
]
