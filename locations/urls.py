"""
URL patterns for locations app
"""
from django.urls import path
from . import views
from . import wan_views

app_name = 'locations'

urlpatterns = [
    # Location CRUD
    path('', views.location_list, name='location_list'),
    path('create/', views.location_create, name='location_create'),
    path('<int:location_id>/', views.location_detail, name='location_detail'),
    path('<int:location_id>/edit/', views.location_edit, name='location_edit'),
    path('<int:location_id>/delete/', views.location_delete, name='location_delete'),

    # WAN Connection Management
    path('<int:location_id>/wan/', wan_views.wan_list, name='wan_list'),
    path('<int:location_id>/wan/create/', wan_views.wan_create, name='wan_create'),
    path('<int:location_id>/wan/<int:wan_id>/', wan_views.wan_detail, name='wan_detail'),
    path('<int:location_id>/wan/<int:wan_id>/edit/', wan_views.wan_edit, name='wan_edit'),
    path('<int:location_id>/wan/<int:wan_id>/delete/', wan_views.wan_delete, name='wan_delete'),
    path('<int:location_id>/wan/<int:wan_id>/check-status/', wan_views.wan_check_status, name='wan_check_status'),

    # Floor plan generation
    path('<int:location_id>/generate-floor-plan/', views.generate_floor_plan, name='generate_floor_plan'),

    # Floor plan import
    path('floor-plan-import/', views.floor_plan_import, name='floor_plan_import'),

    # AJAX endpoints for data refresh
    path('<int:location_id>/refresh-geocoding/', views.refresh_geocoding, name='refresh_geocoding'),
    path('<int:location_id>/refresh-property-data/', views.refresh_property_data, name='refresh_property_data'),
    path('<int:location_id>/refresh-satellite-image/', views.refresh_satellite_image, name='refresh_satellite_image'),
    path('<int:location_id>/import-property-from-url/', views.import_property_from_url, name='import_property_from_url'),

    # Map data endpoints
    path('map-data/', views.location_map_data, name='location_map_data'),
    path('global-map-data/', views.global_location_map_data, name='global_location_map_data'),

    # Send navigation link
    path('<int:location_id>/send-navigation/', views.send_navigation_link, name='send_navigation_link'),
]
