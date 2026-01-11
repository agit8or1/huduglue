"""
Forms for IT Glue/Hudu import
"""
from django import forms
from .models import ImportJob


class ImportJobForm(forms.ModelForm):
    """Form for creating import jobs."""

    class Meta:
        model = ImportJob
        fields = [
            'source_type', 'source_url', 'source_api_key', 'target_organization',
            'import_assets', 'import_passwords', 'import_documents',
            'import_contacts', 'import_locations', 'import_networks',
            'dry_run'
        ]
        widgets = {
            'source_type': forms.Select(attrs={'class': 'form-control'}),
            'source_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://api.itglue.com or https://your-hudu.com'}),
            'source_api_key': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Your API key'}),
            'target_organization': forms.Select(attrs={'class': 'form-control'}),
            'import_assets': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'import_passwords': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'import_documents': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'import_contacts': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'import_locations': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'import_networks': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dry_run': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'source_url': 'Full API URL (e.g., https://api.itglue.com or https://demo.hudu.com)',
            'source_api_key': 'API key for authentication',
            'dry_run': 'Preview import without saving data (recommended for first run)',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filter organizations based on user permissions
        if user:
            if user.is_superuser or hasattr(user, 'is_staff_user') and user.is_staff_user:
                # Staff can see all organizations
                pass
            else:
                # Regular users only see their organizations
                self.fields['target_organization'].queryset = user.organizations.all()

    def clean(self):
        cleaned_data = super().clean()
        source_type = cleaned_data.get('source_type')
        source_url = cleaned_data.get('source_url', '')

        # Validate URL matches source type
        if source_type == 'itglue' and 'itglue' not in source_url.lower():
            self.add_error('source_url', 'URL should contain "itglue" for IT Glue imports')
        elif source_type == 'hudu' and 'itglue' in source_url.lower():
            self.add_error('source_url', 'URL should not contain "itglue" for Hudu imports')

        return cleaned_data
