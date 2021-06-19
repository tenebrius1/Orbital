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
    path('settings', views.settings,name='settings'),
    path('forgetpassword', views.forgetpassword, name='forgetpassword'),
    path('resetpasswordsuccess', views.resetpasswordsuccess, name='resetpasswordsuccess'),
    path('ship/<group_name>', views.groupmainpage, name='groupmainpage'),
    path('deleteGroup', views.deleteGroup, name='deleteGroup'),
    path('joinGroup', views.joinGroup, name='joinGroup'),
    path('leaveGroup', views.leaveGroup, name='leaveGroup'),
    path('ship/<group_name>/locked', views.grouplocked, name='grouplocked'),
    path('lockGroup', views.lockGroup, name='lockGroup'),
    path('report', views.report, name='report'), 

    # Handles AJAX requests
    path('deleteTransaction', views.deleteTransaction, name='deleteTransaction'),
    path('displayExpenses', views.displayExpenses, name='displayExpenses'),
    path('editTransaction', views.editTransaction, name='editTransaction'),
    path('displayDeliveries', views.displayDeliveries, name='displayDeliveries'),
    path('deleteDelivery', views.deleteDelivery, name='deleteDelivery'),
]
