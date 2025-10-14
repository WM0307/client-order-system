from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_create, name='client_add'),
    path('clients/<int:pk>/edit/', views.client_update, name='client_edit'),
    path('clients/<int:pk>/delete/', views.client_delete, name='client_delete'),
]
