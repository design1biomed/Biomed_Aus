from django import forms
from .models import IndexPageContent, Accreditation, QualityTimeline, ExtractCategory, CorePromise, OfficeLocation, SolutionFeature, AboutPageContent, CSRPageContent, TeamMember, OperationTeamMember, InfrastructurePageContent, ResearchArea, ResearchCoreAreaLink, GalleryImage, Brand, ProductRangeSlide, Product, NaturalFoodColor, NaturalFlavour, ProductBrochure, ProductDocumentCategory, ProductDocument, ExhibitionEvent, InstagramPost, JobOpening, JobApplication, ContactMessage, EmailConfiguration

PAGE_CHOICES = [
    ('', 'Select a page...'),
    ('/', 'Home'),
    ('/about-us/', 'About Us'),
    ('/team/', 'Team'),
    ('/csr/', 'CSR'),
    ('/infrastructure-and-services/', 'Infrastructure and Services'),
    ('/facility/', 'Facility'),
    ('/research/', 'Research'),
    ('/accreditations/', 'Accreditations'),
    ('/product-range/', 'Product Range'),
    ('/herbal-extracts/', 'Herbal Extracts'),
    ('/natural-food-colors/', 'Natural Food Colors'),
    ('/nutritional-fine-chemicals/', 'Nutritional Fine Chemicals'),
    ('/organic-product-list/', 'Organic Product List'),
    ('/spices-and-oleoresins/', 'Spices and Oleoresins'),
    ('/raw-herbal-powders/', 'Raw Herbal Powders'),
    ('/product-brochures/', 'Product Brochures'),
    ('/product-documents/', 'Product Documents'),
    ('/news-events/', 'News & Events'),
    ('/career/', 'Career'),
    ('/contact-us/', 'Contact Us'),
]

class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPageContent
        fields = '__all__'
        widgets = {
            # Legacy fields
            'top_banner_heading':   forms.TextInput(attrs={'class': 'form-control'}),
            'top_banner_subheading':forms.TextInput(attrs={'class': 'form-control'}),
            'main_image':           forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'main_heading':         forms.TextInput(attrs={'class': 'form-control'}),
            'main_text':            forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'mission_text':         forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vision_text':          forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'values_text':          forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'middle_text':          forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'bottom_image':         forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'box_1_title':          forms.TextInput(attrs={'class': 'form-control'}),
            'box_1_subtitle':       forms.TextInput(attrs={'class': 'form-control'}),
            'box_1_link':           forms.Select(choices=PAGE_CHOICES, attrs={'class': 'form-select'}),
            'box_2_title':          forms.TextInput(attrs={'class': 'form-control'}),
            'box_2_subtitle':       forms.TextInput(attrs={'class': 'form-control'}),
            'box_2_link':           forms.Select(choices=PAGE_CHOICES, attrs={'class': 'form-select'}),
            'box_3_title':          forms.TextInput(attrs={'class': 'form-control'}),
            'box_3_subtitle':       forms.TextInput(attrs={'class': 'form-control'}),
            'box_3_link':           forms.Select(choices=PAGE_CHOICES, attrs={'class': 'form-select'}),
            'product_lines_intro':  forms.TextInput(attrs={'class': 'form-control'}),
            'product_line_1':       forms.TextInput(attrs={'class': 'form-control'}),
            'product_line_1_url':   forms.Select(choices=PAGE_CHOICES, attrs={'class': 'form-select'}),
            'product_line_2':       forms.TextInput(attrs={'class': 'form-control'}),
            'product_line_2_url':   forms.Select(choices=PAGE_CHOICES, attrs={'class': 'form-select'}),
            'product_line_3':       forms.TextInput(attrs={'class': 'form-control'}),
            'product_line_3_url':   forms.Select(choices=PAGE_CHOICES, attrs={'class': 'form-select'}),
            'product_line_4':       forms.TextInput(attrs={'class': 'form-control'}),
            'product_line_4_url':   forms.Select(choices=PAGE_CHOICES, attrs={'class': 'form-select'}),
            'product_line_5':       forms.TextInput(attrs={'class': 'form-control'}),
            'product_line_5_url':   forms.Select(choices=PAGE_CHOICES, attrs={'class': 'form-select'}),
            'product_line_6':       forms.TextInput(attrs={'class': 'form-control'}),
            'product_line_6_url':   forms.Select(choices=PAGE_CHOICES, attrs={'class': 'form-select'}),
            'belief_quote_prefix':  forms.TextInput(attrs={'class': 'form-control'}),
            'belief_quote':         forms.TextInput(attrs={'class': 'form-control'}),
            # Story Section
            'story_eyebrow':        forms.TextInput(attrs={'class': 'form-control'}),
            'story_heading':        forms.TextInput(attrs={'class': 'form-control'}),
            'story_paragraph_1':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'story_paragraph_2':    forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'story_cta_label':      forms.TextInput(attrs={'class': 'form-control'}),
            'stat_1_number':        forms.TextInput(attrs={'class': 'form-control'}),
            'stat_1_label':         forms.TextInput(attrs={'class': 'form-control'}),
            'stat_2_number':        forms.TextInput(attrs={'class': 'form-control'}),
            'stat_2_label':         forms.TextInput(attrs={'class': 'form-control'}),
            'stat_3_number':        forms.TextInput(attrs={'class': 'form-control'}),
            'stat_3_label':         forms.TextInput(attrs={'class': 'form-control'}),
            'stat_4_number':        forms.TextInput(attrs={'class': 'form-control'}),
            'stat_4_label':         forms.TextInput(attrs={'class': 'form-control'}),
            'story_main_image':     forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'story_field_image':    forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'story_facility_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'story_lab_image':      forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class CSRPageForm(forms.ModelForm):
    class Meta:
        model = CSRPageContent
        fields = '__all__'
        widgets = {
            'hero_title': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_subtitle': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'hero_badge_text': forms.TextInput(attrs={'class': 'form-control'}),
            'hero_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            'intro_title': forms.TextInput(attrs={'class': 'form-control'}),
            'intro_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            
            'pillar_1_kicker': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_1_title': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_1_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'pillar_1_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            'pillar_2_kicker': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_2_title': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_2_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'pillar_2_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            'pillar_3_kicker': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_3_title': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_3_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'pillar_3_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            
            'pillar_4_kicker': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_4_title': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_4_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'pillar_4_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),

            'pillar_5_kicker': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_5_title': forms.TextInput(attrs={'class': 'form-control'}),
            'pillar_5_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'pillar_5_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
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
        fields = ['name', 'category', 'image', 'certificate_file', 'certificate_no', 'issuing_body', 'validity', 'scope', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ISO 9001:2015, WHO-GMP, USDA Organic'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'certificate_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'certificate_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. BMI-ISO-9001-2024'}),
            'issuing_body': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. SGS / Bureau Veritas / US FDA'}),
            'validity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Valid Through Dec 2026'}),
            'scope': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Scope of manufacturing & export certified under this standard'}),
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


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_designation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'alignment': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class OperationTeamMemberForm(forms.ModelForm):
    class Meta:
        model = OperationTeamMember
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'primary_designation': forms.TextInput(attrs={'class': 'form-control'}),
            'secondary_designation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'alignment': forms.Select(attrs={'class': 'form-select'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class InfrastructurePageForm(forms.ModelForm):
    class Meta:
        model = InfrastructurePageContent
        fields = '__all__'
        widgets = {
            'main_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'farming_badge': forms.TextInput(attrs={'class': 'form-control'}),
            'farming_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'farming_text_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'farming_text_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'farming_text_3': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'farming_img_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'services_badge': forms.TextInput(attrs={'class': 'form-control'}),
            'services_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'services_text_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'services_text_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'services_text_3': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'services_img_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),

            'quality_badge': forms.TextInput(attrs={'class': 'form-control'}),
            'quality_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'quality_text_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'quality_text_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'quality_text_3': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'quality_text_highlight': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'quality_text_4': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'quality_text_5': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'quality_img_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'standards_heading': forms.TextInput(attrs={'class': 'form-control'}),
            'standards_text_1': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'standards_text_2': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'standards_img_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ResearchAreaForm(forms.ModelForm):
    class Meta:
        model = ResearchArea
        fields = ['title', 'slug', 'description', 'image_upload', 'image_path', 'pdf_upload', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Leave blank to auto-generate'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_path': forms.TextInput(attrs={'class': 'form-control'}),
            'pdf_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ResearchCoreAreaLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import ResearchArea
        choices = [('', '--- Select a Research Area ---')]
        for area in ResearchArea.objects.all():
            choices.append((f'/research/{area.slug}/', f'{area.title} (/research/{area.slug}/)'))
        self.fields['target_url'].widget = forms.Select(choices=choices, attrs={'class': 'form-select'})

    class Meta:
        model = ResearchCoreAreaLink
        fields = ['title', 'target_url', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['title', 'image_upload', 'order']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'trademark': forms.TextInput(attrs={'class': 'form-control'}),
            'ingredient': forms.TextInput(attrs={'class': 'form-control'}),
            'dose': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'applications': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'logo_path': forms.TextInput(attrs={'class': 'form-control'}),
            'logo_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'layer_image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bg_image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'botanical_name': forms.TextInput(attrs={'class': 'form-control'}),
            'plant_part': forms.TextInput(attrs={'class': 'form-control'}),
            'shelf_life': forms.TextInput(attrs={'class': 'form-control'}),
            'moq': forms.TextInput(attrs={'class': 'form-control'}),
            'solubility': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'applications': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'health_benefits': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'recommended_daily_dose': forms.TextInput(attrs={'class': 'form-control'}),
            'detailed_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'mechanism': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'preclinical_studies': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'logo_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'logo_path': forms.TextInput(attrs={'class': 'form-control'}),
            'layer_image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'structure_img_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProductRangeSlideForm(forms.ModelForm):
    class Meta:
        model = ProductRangeSlide
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'extra_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_path': forms.TextInput(attrs={'class': 'form-control'}),
            'button_url': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'sub_category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image_path': forms.TextInput(attrs={'class': 'form-control'}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_path': forms.TextInput(attrs={'class': 'form-control'}),
            'pdf_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_title': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NaturalFoodColorForm(forms.ModelForm):
    class Meta:
        model = NaturalFoodColor
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'color_hex': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class NaturalFlavourForm(forms.ModelForm):
    class Meta:
        model = NaturalFlavour
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'color_hex': forms.TextInput(attrs={'class': 'form-control', 'type': 'color'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProductBrochureForm(forms.ModelForm):
    class Meta:
        model = ProductBrochure
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'image_path': forms.TextInput(attrs={'class': 'form-control'}),
            'pdf_upload': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_path': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ProductDocumentCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductDocumentCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductDocumentForm(forms.ModelForm):
    class Meta:
        model = ProductDocument
        fields = ['name', 'category', 'image', 'pdfs']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdfs': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. assets/pdfs/doc1.pdf, assets/pdfs/doc2.pdf'}),
        }

class ExhibitionEventForm(forms.ModelForm):
    class Meta:
        model = ExhibitionEvent
        fields = ['tag', 'description', 'background_image', 'order', 'is_active', 'booth_number', 'logo', 'event_date', 'event_end_date']
        widgets = {
            'tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., # Herbal Extracts'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'background_image': forms.FileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'booth_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Booth No. A1'}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'event_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'event_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class InstagramPostForm(forms.ModelForm):
    class Meta:
        model = InstagramPost
        fields = ['image_upload', 'caption', 'link', 'is_visible', 'order']
        widgets = {
            'image_upload': forms.FileInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Optional caption for the post'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Link to the real Instagram post (e.g., https://instagram.com/p/...)'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class JobOpeningForm(forms.ModelForm):
    class Meta:
        model = JobOpening
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'academic_excellence': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'professional_expertise': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'core_responsibilities': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'core_competencies': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'professional_edge': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'commitment_statement': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'icon': forms.Select(attrs={'class': 'form-select'}),
            'color_theme': forms.Select(attrs={'class': 'form-select'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'experience', 'address', 'resume', 'details']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 XXXXX XXXXX'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, State'}),
            'resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
            'details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': "Tell us why you're a great fit...", 'rows': 4}),
        }



COUNTRY_CHOICES = [
    ('', 'Select Country'),
    ('Afghanistan', 'Afghanistan'),
    ('Albania', 'Albania'),
    ('Algeria', 'Algeria'),
    ('Andorra', 'Andorra'),
    ('Angola', 'Angola'),
    ('Antigua and Barbuda', 'Antigua and Barbuda'),
    ('Argentina', 'Argentina'),
    ('Armenia', 'Armenia'),
    ('Australia', 'Australia'),
    ('Austria', 'Austria'),
    ('Azerbaijan', 'Azerbaijan'),
    ('Bahamas', 'Bahamas'),
    ('Bahrain', 'Bahrain'),
    ('Bangladesh', 'Bangladesh'),
    ('Barbados', 'Barbados'),
    ('Belarus', 'Belarus'),
    ('Belgium', 'Belgium'),
    ('Belize', 'Belize'),
    ('Benin', 'Benin'),
    ('Bhutan', 'Bhutan'),
    ('Bolivia', 'Bolivia'),
    ('Bosnia and Herzegovina', 'Bosnia and Herzegovina'),
    ('Botswana', 'Botswana'),
    ('Brazil', 'Brazil'),
    ('Brunei', 'Brunei'),
    ('Bulgaria', 'Bulgaria'),
    ('Burkina Faso', 'Burkina Faso'),
    ('Burundi', 'Burundi'),
    ('Cabo Verde', 'Cabo Verde'),
    ('Cambodia', 'Cambodia'),
    ('Cameroon', 'Cameroon'),
    ('Canada', 'Canada'),
    ('Central African Republic', 'Central African Republic'),
    ('Chad', 'Chad'),
    ('Chile', 'Chile'),
    ('China', 'China'),
    ('Colombia', 'Colombia'),
    ('Comoros', 'Comoros'),
    ('Congo', 'Congo'),
    ('Costa Rica', 'Costa Rica'),
    ('Croatia', 'Croatia'),
    ('Cuba', 'Cuba'),
    ('Cyprus', 'Cyprus'),
    ('Czech Republic', 'Czech Republic'),
    ('Democratic Republic of the Congo', 'Democratic Republic of the Congo'),
    ('Denmark', 'Denmark'),
    ('Djibouti', 'Djibouti'),
    ('Dominica', 'Dominica'),
    ('Dominican Republic', 'Dominican Republic'),
    ('Ecuador', 'Ecuador'),
    ('Egypt', 'Egypt'),
    ('El Salvador', 'El Salvador'),
    ('Equatorial Guinea', 'Equatorial Guinea'),
    ('Eritrea', 'Eritrea'),
    ('Estonia', 'Estonia'),
    ('Eswatini', 'Eswatini'),
    ('Ethiopia', 'Ethiopia'),
    ('Fiji', 'Fiji'),
    ('Finland', 'Finland'),
    ('France', 'France'),
    ('Gabon', 'Gabon'),
    ('Gambia', 'Gambia'),
    ('Georgia', 'Georgia'),
    ('Germany', 'Germany'),
    ('Ghana', 'Ghana'),
    ('Greece', 'Greece'),
    ('Grenada', 'Grenada'),
    ('Guatemala', 'Guatemala'),
    ('Guinea', 'Guinea'),
    ('Guinea-Bissau', 'Guinea-Bissau'),
    ('Guyana', 'Guyana'),
    ('Haiti', 'Haiti'),
    ('Honduras', 'Honduras'),
    ('Hungary', 'Hungary'),
    ('Iceland', 'Iceland'),
    ('India', 'India'),
    ('Indonesia', 'Indonesia'),
    ('Iran', 'Iran'),
    ('Iraq', 'Iraq'),
    ('Ireland', 'Ireland'),
    ('Israel', 'Israel'),
    ('Italy', 'Italy'),
    ('Jamaica', 'Jamaica'),
    ('Japan', 'Japan'),
    ('Jordan', 'Jordan'),
    ('Kazakhstan', 'Kazakhstan'),
    ('Kenya', 'Kenya'),
    ('Kiribati', 'Kiribati'),
    ('Kuwait', 'Kuwait'),
    ('Kyrgyzstan', 'Kyrgyzstan'),
    ('Laos', 'Laos'),
    ('Latvia', 'Latvia'),
    ('Lebanon', 'Lebanon'),
    ('Lesotho', 'Lesotho'),
    ('Liberia', 'Liberia'),
    ('Libya', 'Libya'),
    ('Liechtenstein', 'Liechtenstein'),
    ('Lithuania', 'Lithuania'),
    ('Luxembourg', 'Luxembourg'),
    ('Madagascar', 'Madagascar'),
    ('Malawi', 'Malawi'),
    ('Malaysia', 'Malaysia'),
    ('Maldives', 'Maldives'),
    ('Mali', 'Mali'),
    ('Malta', 'Malta'),
    ('Marshall Islands', 'Marshall Islands'),
    ('Mauritania', 'Mauritania'),
    ('Mauritius', 'Mauritius'),
    ('Mexico', 'Mexico'),
    ('Micronesia', 'Micronesia'),
    ('Moldova', 'Moldova'),
    ('Monaco', 'Monaco'),
    ('Mongolia', 'Mongolia'),
    ('Montenegro', 'Montenegro'),
    ('Morocco', 'Morocco'),
    ('Mozambique', 'Mozambique'),
    ('Myanmar', 'Myanmar'),
    ('Namibia', 'Namibia'),
    ('Nauru', 'Nauru'),
    ('Nepal', 'Nepal'),
    ('Netherlands', 'Netherlands'),
    ('New Zealand', 'New Zealand'),
    ('Nicaragua', 'Nicaragua'),
    ('Niger', 'Niger'),
    ('Nigeria', 'Nigeria'),
    ('North Korea', 'North Korea'),
    ('North Macedonia', 'North Macedonia'),
    ('Norway', 'Norway'),
    ('Oman', 'Oman'),
    ('Pakistan', 'Pakistan'),
    ('Palau', 'Palau'),
    ('Palestine', 'Palestine'),
    ('Panama', 'Panama'),
    ('Papua New Guinea', 'Papua New Guinea'),
    ('Paraguay', 'Paraguay'),
    ('Peru', 'Peru'),
    ('Philippines', 'Philippines'),
    ('Poland', 'Poland'),
    ('Portugal', 'Portugal'),
    ('Qatar', 'Qatar'),
    ('Romania', 'Romania'),
    ('Russia', 'Russia'),
    ('Rwanda', 'Rwanda'),
    ('Saint Kitts and Nevis', 'Saint Kitts and Nevis'),
    ('Saint Lucia', 'Saint Lucia'),
    ('Saint Vincent and the Grenadines', 'Saint Vincent and the Grenadines'),
    ('Samoa', 'Samoa'),
    ('San Marino', 'San Marino'),
    ('Sao Tome and Principe', 'Sao Tome and Principe'),
    ('Saudi Arabia', 'Saudi Arabia'),
    ('Senegal', 'Senegal'),
    ('Serbia', 'Serbia'),
    ('Seychelles', 'Seychelles'),
    ('Sierra Leone', 'Sierra Leone'),
    ('Singapore', 'Singapore'),
    ('Slovakia', 'Slovakia'),
    ('Slovenia', 'Slovenia'),
    ('Solomon Islands', 'Solomon Islands'),
    ('Somalia', 'Somalia'),
    ('South Africa', 'South Africa'),
    ('South Korea', 'South Korea'),
    ('South Sudan', 'South Sudan'),
    ('Spain', 'Spain'),
    ('Sri Lanka', 'Sri Lanka'),
    ('Sudan', 'Sudan'),
    ('Suriname', 'Suriname'),
    ('Sweden', 'Sweden'),
    ('Switzerland', 'Switzerland'),
    ('Syria', 'Syria'),
    ('Taiwan', 'Taiwan'),
    ('Tajikistan', 'Tajikistan'),
    ('Tanzania', 'Tanzania'),
    ('Thailand', 'Thailand'),
    ('Timor-Leste', 'Timor-Leste'),
    ('Togo', 'Togo'),
    ('Tonga', 'Tonga'),
    ('Trinidad and Tobago', 'Trinidad and Tobago'),
    ('Tunisia', 'Tunisia'),
    ('Turkey', 'Turkey'),
    ('Turkmenistan', 'Turkmenistan'),
    ('Tuvalu', 'Tuvalu'),
    ('Uganda', 'Uganda'),
    ('Ukraine', 'Ukraine'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('United Kingdom', 'United Kingdom'),
    ('United States', 'United States'),
    ('Uruguay', 'Uruguay'),
    ('Uzbekistan', 'Uzbekistan'),
    ('Vanuatu', 'Vanuatu'),
    ('Vatican City', 'Vatican City'),
    ('Venezuela', 'Venezuela'),
    ('Vietnam', 'Vietnam'),
    ('Yemen', 'Yemen'),
    ('Zambia', 'Zambia'),
    ('Zimbabwe', 'Zimbabwe')
]

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'country', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'country': forms.Select(choices=COUNTRY_CHOICES, attrs={'class': 'form-select', 'placeholder': 'Select Country'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'How can we help you?', 'rows': 3}),
        }

class EmailConfigurationForm(forms.ModelForm):
    class Meta:
        model = EmailConfiguration
        fields = ['enquiry_email', 'booking_email', 'career_email', 'subscription_email']
        widgets = {
            'enquiry_email': forms.TextInput(attrs={'class': 'form-control'}),
            'booking_email': forms.TextInput(attrs={'class': 'form-control'}),
            'career_email': forms.TextInput(attrs={'class': 'form-control'}),
            'subscription_email': forms.TextInput(attrs={'class': 'form-control'}),
        }



