from django import forms
from .models import IndexPageContent, Accreditation, QualityTimeline, ExtractCategory, CorePromise, OfficeLocation, SolutionFeature, AboutPageContent

class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPageContent
        fields = '__all__'
        widgets = {
            'top_banner_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'top_banner_subheading': forms.TextInput(attrs={'class': 'form-control'}),
            'main_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'main_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'main_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'middle_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'bottom_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'box_1_title': forms.TextInput(attrs={'class': 'form-control'}),
            'box_1_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'box_2_title': forms.TextInput(attrs={'class': 'form-control'}),
            'box_2_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'box_3_title': forms.TextInput(attrs={'class': 'form-control'}),
            'box_3_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
        }


class IndexPageForm(forms.ModelForm):
    class Meta:
        model = IndexPageContent
        fields = '__all__'
        widgets = {
            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hero_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            'about_title': forms.TextInput(attrs={'class': 'form-control'}),
            'about_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'about_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'about_feature_1_title': forms.TextInput(attrs={'class': 'form-control'}),
            'about_feature_1_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'about_feature_2_title': forms.TextInput(attrs={'class': 'form-control'}),
            'about_feature_2_subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            
            'about_image_1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'about_image_2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            'extracts_title': forms.TextInput(attrs={'class': 'form-control'}),
            'extracts_subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            'solutions_badge': forms.TextInput(attrs={'class': 'form-control'}),
            'solutions_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'solutions_subheading': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            'quality_title': forms.TextInput(attrs={'class': 'form-control'}),
            'quality_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            'accred_kicker': forms.TextInput(attrs={'class': 'form-control'}),
            'accred_title': forms.TextInput(attrs={'class': 'form-control'}),
            'accred_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            'cta_title': forms.TextInput(attrs={'class': 'form-control'}),
            'cta_subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            'difference_kicker': forms.TextInput(attrs={'class': 'form-control'}),
            'difference_title': forms.TextInput(attrs={'class': 'form-control'}),
            'difference_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'difference_stat1_number': forms.TextInput(attrs={'class': 'form-control'}),
            'difference_stat1_label': forms.TextInput(attrs={'class': 'form-control'}),
            'difference_stat2_number': forms.TextInput(attrs={'class': 'form-control'}),
            'difference_stat2_label': forms.TextInput(attrs={'class': 'form-control'}),
            
            'map_badge': forms.TextInput(attrs={'class': 'form-control'}),
            'map_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'map_subheading': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AccreditationForm(forms.ModelForm):
    class Meta:
        model = Accreditation
        fields = ['name', 'image', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class QualityTimelineForm(forms.ModelForm):
    class Meta:
        model = QualityTimeline
        fields = ['title', 'description', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ExtractCategoryForm(forms.ModelForm):
    class Meta:
        model = ExtractCategory
        fields = ['title', 'subtitle', 'description', 'image', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

ICON_CHOICES = [
    ('ph-fill ph-stars', 'Stars (Solid)'),
    ('ph ph-stars', 'Stars (Outline)'),
    ('ph ph-leaf', 'Leaf'),
    ('ph-fill ph-leaf', 'Leaf (Solid)'),
    ('ph ph-plant', 'Plant'),
    ('ph-fill ph-plant', 'Plant (Solid)'),
    ('ph ph-flask', 'Flask'),
    ('ph-fill ph-flask', 'Flask (Solid)'),
    ('ph ph-drop', 'Drop'),
    ('ph-fill ph-drop', 'Drop (Solid)'),
    ('ph ph-heartbeat', 'Heartbeat'),
    ('ph ph-first-aid', 'First Aid'),
    ('ph ph-shield-check', 'Shield Check'),
    ('ph-fill ph-shield-check', 'Shield Check (Solid)'),
    ('ph ph-globe-hemisphere-west', 'Globe'),
    ('ph ph-certificate', 'Certificate'),
    ('ph ph-medal', 'Medal'),
    ('ph ph-package', 'Package'),
    ('ph ph-truck', 'Truck'),
    ('ph ph-sparkle', 'Sparkle'),
    ('ph-fill ph-sparkle', 'Sparkle (Solid)'),
    ('ph ph-handshake', 'Handshake'),
]

class CorePromiseForm(forms.ModelForm):
    class Meta:
        model = CorePromise
        fields = ['title', 'description', 'icon_class', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon_class': forms.Select(choices=ICON_CHOICES, attrs={'class': 'form-select premium-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class OfficeLocationForm(forms.ModelForm):
    class Meta:
        model = OfficeLocation
        fields = ['country', 'top_percentage', 'left_percentage', 'is_hq']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'top_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'left_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'is_hq': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SolutionFeatureForm(forms.ModelForm):
    class Meta:
        model = SolutionFeature
        fields = ['title', 'description', 'icon_class', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'icon_class': forms.Select(choices=ICON_CHOICES, attrs={'class': 'form-select premium-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
