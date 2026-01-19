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

    # Execution list - MUST come before slug patterns
    path('executions/', views.execution_list, name='execution_list'),

    # Global processes (superuser only) - MUST come before slug patterns
    path('global/', views.global_process_list, name='global_process_list'),
    path('global/create/', views.global_process_create, name='global_process_create'),

    # Process detail/edit/delete - slug patterns come AFTER specific paths
    path('<slug:slug>/', views.process_detail, name='process_detail'),
    path('<slug:slug>/generate-diagram/', views.process_generate_diagram, name='process_generate_diagram'),
    path('<slug:slug>/edit/', views.process_edit, name='process_edit'),
    path('<slug:slug>/delete/', views.process_delete, name='process_delete'),
    path('<slug:slug>/reorder/', views.stage_reorder, name='stage_reorder'),

    # Process Execution
    path('<slug:slug>/execute/', views.execution_create, name='execution_create'),
    path('execution/<int:pk>/', views.execution_detail, name='execution_detail'),
    path('execution/<int:pk>/audit-log/', views.execution_audit_log, name='execution_audit_log'),
    path('completion/<int:pk>/complete/', views.stage_complete, name='stage_complete'),
    path('completion/<int:pk>/uncomplete/', views.stage_uncomplete, name='stage_uncomplete'),
]
