"""
Locations admin interface
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Location, LocationFloorPlan


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'organization',
        'location_type',
        'city',
        'state',
        'is_primary',
        'status',
        'has_coordinates_display',
        'floorplan_status_display',
    ]
    list_filter = [
        'organization',
        'location_type',
        'status',
        'is_primary',
        'floorplan_generated',
        'state',
        'country',
    ]
    search_fields = [
        'name',
        'street_address',
        'city',
        'state',
        'postal_code',
        'organization__name',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'floorplan_generated_at',
        'google_maps_link',
    ]

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'organization',
                'name',
                'location_type',
                'is_primary',
                'status',
            )
        }),
        ('Address', {
            'fields': (
                'street_address',
                'street_address_2',
                'city',
                'state',
                'postal_code',
                'country',
            )
        }),
        ('Geocoding', {
            'fields': (
                'latitude',
                'longitude',
                'google_maps_link',
            ),
            'classes': ('collapse',),
        }),
        ('Building Information', {
            'fields': (
                'building_sqft',
                'floors_count',
                'year_built',
                'property_type',
            ),
            'classes': ('collapse',),
        }),
        ('External Data', {
            'fields': (
                'property_id',
                'google_place_id',
                'external_data',
            ),
            'classes': ('collapse',),
        }),
        ('Contact Information', {
            'fields': (
                'phone',
                'email',
                'website',
            ),
            'classes': ('collapse',),
        }),
        ('Generated Assets', {
            'fields': (
                'satellite_image',
                'street_view_image',
                'area_map_image',
            ),
            'classes': ('collapse',),
        }),
        ('Floor Plan Generation', {
            'fields': (
                'floorplan_generated',
                'floorplan_generated_at',
                'floorplan_generation_status',
                'floorplan_error',
            ),
            'classes': ('collapse',),
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )

    def has_coordinates_display(self, obj):
        """Display geocoding status."""
        if obj.has_coordinates:
            return format_html('<span style="color: green;">✓ Yes</span>')
        return format_html('<span style="color: gray;">✗ No</span>')
    has_coordinates_display.short_description = 'Geocoded'

    def floorplan_status_display(self, obj):
        """Display floor plan generation status."""
        if obj.floorplan_generated:
            color = 'green'
            icon = '✓'
            text = 'Generated'
        elif obj.floorplan_generation_status == 'processing':
            color = 'orange'
            icon = '⏳'
            text = 'Processing'
        elif obj.floorplan_generation_status == 'failed':
            color = 'red'
            icon = '✗'
            text = 'Failed'
        else:
            color = 'gray'
            icon = '○'
            text = 'Not Generated'

        return format_html(
            '<span style="color: {};">{} {}</span>',
            color, icon, text
        )
    floorplan_status_display.short_description = 'Floor Plan'

    def google_maps_link(self, obj):
        """Display clickable Google Maps link."""
        if obj.has_coordinates:
            url = obj.google_maps_url
            return format_html(
                '<a href="{}" target="_blank">Open in Google Maps</a>',
                url
            )
        return '—'
    google_maps_link.short_description = 'Google Maps'


@admin.register(LocationFloorPlan)
class LocationFloorPlanAdmin(admin.ModelAdmin):
    list_display = [
        'location',
        'floor_name',
        'floor_number',
        'dimensions_str',
        'source',
        'confidence_display',
        'has_diagram_display',
    ]
    list_filter = [
        'location__organization',
        'source',
        'template_used',
        'include_network',
        'include_furniture',
    ]
    search_fields = [
        'location__name',
        'floor_name',
        'location__organization__name',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'area_sqft',
    ]

    fieldsets = (
        ('Location', {
            'fields': (
                'location',
                'floor_number',
                'floor_name',
            )
        }),
        ('Dimensions', {
            'fields': (
                'width_feet',
                'length_feet',
                'total_sqft',
                'area_sqft',
                'ceiling_height_feet',
            )
        }),
        ('Data Source', {
            'fields': (
                'source',
                'confidence_score',
                'ai_analysis',
            ),
            'classes': ('collapse',),
        }),
        ('Generation Settings', {
            'fields': (
                'template_used',
                'include_network',
                'include_furniture',
            )
        }),
        ('Generated Diagram', {
            'fields': (
                'diagram',
                'diagram_xml',
            ),
            'classes': ('collapse',),
        }),
        ('Metadata', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )

    def confidence_display(self, obj):
        """Display confidence score with color coding."""
        if obj.confidence_score is None:
            return '—'

        score = float(obj.confidence_score)
        if score >= 0.80:
            color = 'green'
        elif score >= 0.60:
            color = 'orange'
        else:
            color = 'red'

        return format_html(
            '<span style="color: {};">{:.0%}</span>',
            color, score
        )
    confidence_display.short_description = 'Confidence'

    def has_diagram_display(self, obj):
        """Display diagram status."""
        if obj.has_diagram:
            return format_html('<span style="color: green;">✓ Yes</span>')
        return format_html('<span style="color: gray;">✗ No</span>')
    has_diagram_display.short_description = 'Has Diagram'
