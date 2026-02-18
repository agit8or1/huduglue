"""
URL configuration for imports app
"""
from django.urls import path
from . import views

app_name = 'imports'

urlpatterns = [
    # Import job management
    path('', views.import_list, name='import_list'),
    path('create/', views.import_create, name='import_create'),
    path('<int:pk>/', views.import_detail, name='import_detail'),
    path('<int:pk>/edit/', views.import_edit, name='import_edit'),
    path('<int:pk>/delete/', views.import_delete, name='import_delete'),
    path('<int:pk>/start/', views.import_start, name='import_start'),
    path('<int:pk>/rollback/', views.import_rollback, name='import_rollback'),
    path('<int:pk>/log/', views.import_log, name='import_log'),
]
