from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_create, name='client_add'),
    path('clients/<int:pk>/edit/', views.client_update, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.order_create, name='order_add'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),

    path('clients/export/', views.export_clients_csv, name='export_clients_csv'),
    path('orders/export/', views.export_orders_csv, name='export_orders_csv'),
]
