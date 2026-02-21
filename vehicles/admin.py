"""
Admin interface for Service Vehicles
"""
from django.contrib import admin
from .models import (
    ServiceVehicle, VehicleInventoryItem, VehicleDamageReport,
    VehicleMaintenanceRecord, VehicleFuelLog, VehicleAssignment
)


@admin.register(ServiceVehicle)
class ServiceVehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'make', 'model', 'year', 'license_plate', 'status', 'condition', 'current_mileage', 'assigned_to']
    list_filter = ['status', 'condition', 'vehicle_type']
    search_fields = ['name', 'make', 'model', 'vin', 'license_plate']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'vehicle_type', 'make', 'model', 'year', 'color')
        }),
        ('Identification', {
            'fields': ('vin', 'license_plate')
        }),
        ('Status', {
            'fields': ('status', 'condition', 'current_mileage', 'assigned_to')
        }),
        ('Insurance', {
            'fields': ('insurance_provider', 'insurance_policy_number', 'insurance_expires_at', 'insurance_premium')
        }),
        ('Registration', {
            'fields': ('registration_expires_at',)
        }),
        ('GPS Location', {
            'fields': ('latitude', 'longitude', 'last_location_update')
        }),
        ('Purchase Information', {
            'fields': ('purchase_date', 'purchase_price')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(VehicleInventoryItem)
class VehicleInventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'vehicle', 'category', 'quantity', 'unit', 'is_low_stock']
    list_filter = ['category']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(VehicleDamageReport)
class VehicleDamageReportAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'incident_date', 'severity', 'repair_status', 'actual_cost']
    list_filter = ['severity', 'repair_status']
    search_fields = ['description', 'vehicle__name']
    date_hierarchy = 'incident_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(VehicleMaintenanceRecord)
class VehicleMaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'maintenance_type', 'service_date', 'mileage_at_service', 'total_cost', 'is_overdue']
    list_filter = ['maintenance_type', 'is_scheduled']
    search_fields = ['description', 'vehicle__name', 'performed_by']
    date_hierarchy = 'service_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(VehicleFuelLog)
class VehicleFuelLogAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'date', 'mileage', 'gallons', 'total_cost', 'mpg']
    search_fields = ['vehicle__name', 'station']
    date_hierarchy = 'date'
    readonly_fields = ['created_at', 'updated_at', 'miles_driven', 'mpg']


@admin.register(VehicleAssignment)
class VehicleAssignmentAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'user', 'start_date', 'end_date', 'starting_mileage', 'ending_mileage', 'is_active']
    search_fields = ['vehicle__name', 'user__username', 'user__first_name', 'user__last_name']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at', 'updated_at']
