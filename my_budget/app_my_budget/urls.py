from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('new_transaction/', views.new_transaction, name='new_transaction'),
    path('new_transfer/', views.new_transfer, name='new_transfer'),
    path('delete_selected_accounts/', views.delete_selected_accounts, name='delete_selected_accounts'),
    path('new_account/', views.new_account, name='new_account'),


]