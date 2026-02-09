"""
URL Configuration for Reports and Analytics
"""
from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Dashboard and Analytics
    path('', views.reports_home, name='home'),
    path('dashboards/', views.dashboard_list, name='dashboard_list'),
    path('dashboards/<int:pk>/', views.dashboard_detail, name='dashboard_detail'),
    path('dashboards/create/', views.dashboard_create, name='dashboard_create'),
    path('dashboards/<int:pk>/edit/', views.dashboard_edit, name='dashboard_edit'),
    path('dashboards/<int:pk>/delete/', views.dashboard_delete, name='dashboard_delete'),

    # Report Templates
    path('templates/', views.template_list, name='template_list'),
    path('templates/<int:pk>/', views.template_detail, name='template_detail'),
    path('templates/create/', views.template_create, name='template_create'),
    path('templates/<int:pk>/edit/', views.template_edit, name='template_edit'),
    path('templates/<int:pk>/delete/', views.template_delete, name='template_delete'),
    path('templates/<int:pk>/generate/', views.generate_report, name='generate_report'),

    # Generated Reports
    path('generated/', views.generated_list, name='generated_list'),
    path('generated/<int:pk>/', views.generated_detail, name='generated_detail'),
    path('generated/<int:pk>/download/', views.generated_download, name='generated_download'),
    path('generated/<int:pk>/delete/', views.generated_delete, name='generated_delete'),

    # Scheduled Reports
    path('scheduled/', views.scheduled_list, name='scheduled_list'),
    path('scheduled/create/', views.scheduled_create, name='scheduled_create'),
    path('scheduled/<int:pk>/edit/', views.scheduled_edit, name='scheduled_edit'),
    path('scheduled/<int:pk>/delete/', views.scheduled_delete, name='scheduled_delete'),
    path('scheduled/<int:pk>/toggle/', views.scheduled_toggle, name='scheduled_toggle'),

    # Analytics
    path('analytics/', views.analytics_overview, name='analytics_overview'),
    path('analytics/events/', views.analytics_events, name='analytics_events'),
]
