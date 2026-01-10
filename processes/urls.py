"""
Process URLs
"""
from django.urls import path
from . import views

app_name = 'processes'

urlpatterns = [
    # Process CRUD
    path('', views.process_list, name='process_list'),
    path('create/', views.process_create, name='process_create'),

    # Global processes (superuser only) - MUST come before slug patterns
    path('global/', views.global_process_list, name='global_process_list'),
    path('global/create/', views.global_process_create, name='global_process_create'),

    # Process detail/edit/delete - slug patterns come AFTER specific paths
    path('<slug:slug>/', views.process_detail, name='process_detail'),
    path('<slug:slug>/edit/', views.process_edit, name='process_edit'),
    path('<slug:slug>/delete/', views.process_delete, name='process_delete'),
    path('<slug:slug>/reorder/', views.stage_reorder, name='stage_reorder'),

    # Process Execution
    path('<slug:slug>/execute/', views.execution_create, name='execution_create'),
    path('execution/<int:pk>/', views.execution_detail, name='execution_detail'),
    path('completion/<int:pk>/complete/', views.stage_complete, name='stage_complete'),
]
