from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
from PIL import Image
from io import BytesIO
from django.utils.text import slugify

import os

def compress_uploaded_image(image_field, max_width=1920, quality=80):
    if not image_field or getattr(image_field, '_committed', True):
        return image_field
        
    try:
        img = Image.open(image_field.file)
    except Exception:
        return image_field
        
    # Check if it's a transparent PNG
    is_transparent_png = False
    if img.format == 'PNG':
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            is_transparent_png = True
        
    if img.width > max_width:
        ratio = max_width / img.width
        new_height = int(img.height * ratio)
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
        
    output = BytesIO()
    save_kwargs = {}
    
    if is_transparent_png:
        target_format = 'PNG'
        content_type = 'image/png'
        filename = image_field.name
        save_kwargs['optimize'] = True
    else:
        target_format = 'WEBP'
        content_type = 'image/webp'
        
        # Convert to RGB to safely save as WEBP without alpha channel issues
        if img.mode in ("RGBA", "P", "LA"):
            bg = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode in ("RGBA", "LA"):
                bg.paste(img, mask=img.split()[-1])
            else:
                img_rgba = img.convert("RGBA")
                bg.paste(img_rgba, mask=img_rgba.split()[-1])
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
            
        save_kwargs['quality'] = quality
        
        # Change file extension to .webp
        base_name = os.path.splitext(image_field.name)[0]
        filename = f"{base_name}.webp"
        
    try:
        img.save(output, format=target_format, **save_kwargs)
        output.seek(0)
    except Exception:
        return image_field # Fallback if save fails
    
    return InMemoryUploadedFile(
        output,
        'ImageField',
        filename,
        content_type,
        sys.getsizeof(output),
        None
    )
class IndexPageContent(models.Model):
    # Singleton pattern - we'll only ever have one of these
    
    # Hero Section
    hero_title = models.CharField(max_length=255, default='We Integrate<br><span class="text-accent-gold">technology with nature.</span>', help_text="HTML allowed")
    hero_subtitle = models.TextField(default="Catering to the nutraceutical, cosmeceutical, pharmaceutical and food industries. Suppliers of organically and naturally produced herbal & spice extracts, plant extracts and oleoresins.")
    
    hero_image = models.ImageField(upload_to='hero/', blank=True, null=True, help_text="Background image for hero section")
    
    # About Section
    about_title = models.CharField(max_length=255, default="Bio Med Ingredients Australia")
    about_subtitle = models.CharField(max_length=255, default="WHO WE ARE")
    about_text = models.TextField(default="Biomed Ingredients Australia is committed towards good health and protection of the environment. Our mission has been to manufacture and supply organically and naturally produced herbal extracts, spice extracts, plant extracts and oleoresins. With decades of botanical expertise, we source the finest raw materials to formulate premium ingredients that power the world's leading brands.")
    about_feature_1_title = models.CharField(max_length=255, default="100% Organic")
    about_feature_1_subtitle = models.CharField(max_length=255, default="Certified Extracts")
    about_feature_2_title = models.CharField(max_length=255, default="R&D Driven")
    about_feature_2_subtitle = models.CharField(max_length=255, default="Advanced Innovation")
    
    about_image_1 = models.ImageField(upload_to='about/', blank=True, null=True, help_text="Main Background Image")
    about_image_2 = models.ImageField(upload_to='about/', blank=True, null=True, help_text="Overlapping Foreground Image")

    # Extracts Section
    extracts_title = models.CharField(max_length=255, default="Our Extract Portfolio")
    extracts_subtitle = models.TextField(default="Discover our meticulously curated categories of high-potency ingredients.")

    # Solutions Section
    solutions_badge = models.CharField(max_length=255, default="What We Offer")
    solutions_heading = models.CharField(max_length=255, default="Premium Botanical Solutions")
    solutions_subheading = models.TextField(default="Discover our wide range of meticulously crafted natural ingredients, designed to elevate your products and support holistic wellness.")

    # Quality Section
    quality_title = models.CharField(max_length=255, default="Quality, Consistency, Commitment")
    quality_description = models.TextField(default="Biomed Ingredients Australia is committed towards good health and protection of the environment.")
    
    # Accreditation Section
    accred_kicker = models.CharField(max_length=255, default="✦ Trusted & Certified")
    accred_title = models.CharField(max_length=255, default="Accreditation & Licensing.")
    accred_description = models.TextField(default="We're here to help you provide the best products. Learn about our commitment to quality through our Accreditation & Licensing.")
    
    # CTA Banner
    cta_title = models.CharField(max_length=255, default="We Promise")
    cta_subtitle = models.TextField(default="We strictly stand against synthetic products. Since we are into the business of supplying medicinal plants, we took the organic route to cultivate these herbs with the help of our well-experienced R&D team.")

    # The Bio Med Difference Section
    difference_kicker = models.CharField(max_length=255, default="The Bio Med Difference")
    difference_title = models.CharField(max_length=255, default='Why People <span style="color:var(--gold);">Love Us!</span>', help_text="HTML allowed")
    difference_text = models.TextField(default="Our products are distinguished by exceptional quality, consistency, and proven efficacy. We carefully select research-based, high-potential ingredients to ensure optimal performance — enhancing value and market position.")
    difference_stat1_number = models.CharField(max_length=50, default="99")
    difference_stat1_label = models.CharField(max_length=255, default="Client Retention")
    difference_stat2_number = models.CharField(max_length=50, default="100")
    difference_stat2_label = models.CharField(max_length=255, default="Quality Tested")

    # Global Map Section
    map_badge = models.CharField(max_length=255, default="Global Reach")
    map_heading = models.CharField(max_length=255, default="Our Global Presence")
    map_subheading = models.TextField(default="Operating from our headquarters in India, with strategic offices in Australia, Germany, and Jordan to serve you globally.")


    def save(self, *args, **kwargs):
        # Ensure there is only one instance
        self.pk = 1
        self.hero_image = compress_uploaded_image(self.hero_image)
        self.about_image_1 = compress_uploaded_image(self.about_image_1)
        self.about_image_2 = compress_uploaded_image(self.about_image_2)
        super(IndexPageContent, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Index Page Content"


class Accreditation(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='accreditations/')
    order = models.IntegerField(default=0, help_text="Order in the marquee")
    
    class Meta:
        ordering = ['order', 'id']
        
    def save(self, *args, **kwargs):
        self.image = compress_uploaded_image(self.image)
        super(Accreditation, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class QualityTimeline(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text="Order of appearance")
    
    class Meta:
        ordering = ['order', 'id']
        
    def __str__(self):
        return self.title

class ExtractCategory(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, help_text="e.g., Bio-Active")
    description = models.TextField(blank=True, null=True, help_text="Product description")
    image = models.ImageField(upload_to='extracts/', help_text="Background image for the category card")
    order = models.IntegerField(default=0, help_text="Order of appearance")
    
    class Meta:
        ordering = ['order', 'id']
        
    def save(self, *args, **kwargs):
        self.image = compress_uploaded_image(self.image)
        super(ExtractCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class CorePromise(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, default="ph-check", help_text="Phosphor icon class, e.g., 'ph-truck'")
    order = models.IntegerField(default=0, help_text="Order of appearance")
    
    class Meta:
        ordering = ['order', 'id']
        
    def __str__(self):
        return self.title

class OfficeLocation(models.Model):
    country = models.CharField(max_length=255)
    top_percentage = models.FloatField(help_text="Y coordinate percentage (0-100) for map dot")
    left_percentage = models.FloatField(help_text="X coordinate percentage (0-100) for map dot")
    is_hq = models.BooleanField(default=False, help_text="Is this the headquarters? (changes dot styling)")
    
    class Meta:
        ordering = ['country']
        
    def __str__(self):
        return self.country

class Enquiry(models.Model):
    full_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    product_name = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Enquiries"
        
    def __str__(self):
        return f"{self.full_name} ({self.product_name})"

class SolutionFeature(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    icon_class = models.CharField(max_length=100, default="ph ph-stars", help_text="Phosphor icon class (e.g., ph ph-leaf)")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        
    def __str__(self):
        return self.title

class AboutPageContent(models.Model):
    # Top Banner
    top_banner_heading = models.CharField(max_length=255, default="Biomed Ingredients, Your Responsible Manufacturer")
    top_banner_subheading = models.CharField(max_length=255, default="Biomed Ingredients - Where Quality Matters")
    
    # Main Section
    main_image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    main_heading = models.CharField(max_length=255, default="About US")
    main_text = models.TextField(default="Biomed Ingredients Australia is committed towards good health and protection of the environment.\n\nWhen Bio-Med Ingredients was born in 2014, our mission has been to manufacture and supply organically produced medicinal plants to the nutritional, cosmetic, pharmaceutical and food industries.\n\nWe live in an era, where health is not wealth but it is seen as a means of making wealth...")
    
    # Middle Text Section
    mission_text = models.TextField(default="To deliver superior natural ingredients that meet global standards, fostering health and sustainability.")
    vision_text = models.TextField(default="To be the leading global provider of natural ingredients, driving innovation and responsible sourcing.")
    values_text = models.TextField(default="Integrity, Quality, Innovation, Sustainability, Customer Focus.")
    middle_text = models.TextField(default="IFOAM – Organics International (an organization that promotes organic farming) says, \"Organic Agriculture is a production of a system that sustains the health of soils, ecosystems, and people...\"")
    
    # Bottom Section
    bottom_image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    box_1_title = models.CharField(max_length=255, default="Team")
    box_1_subtitle = models.CharField(max_length=255, default="OUR TEAM")
    box_1_link = models.CharField(max_length=255, blank=True, null=True, help_text="Link for Box 1")
    box_2_title = models.CharField(max_length=255, default="Farming")
    box_2_subtitle = models.CharField(max_length=255, default="OUR FARMING")
    box_2_link = models.CharField(max_length=255, blank=True, null=True, help_text="Link for Box 2")
    box_3_title = models.CharField(max_length=255, default="C S R")
    box_3_subtitle = models.CharField(max_length=255, default="CORPORATE SOCIAL RESPONSIBILITIES")
    box_3_link = models.CharField(max_length=255, blank=True, null=True, help_text="Link for Box 3")

        # Product Lines Section
    product_lines_intro = models.CharField(max_length=255, default="We have an array of organically and naturally developed products. Our product lines are:")
    product_line_1 = models.CharField(max_length=100, default="Herbal & Spice Extract")
    product_line_1_url = models.CharField(max_length=255, default="/herbal-extracts/", blank=True)
    product_line_2 = models.CharField(max_length=100, default="Plant Extract")
    product_line_2_url = models.CharField(max_length=255, default="/nutritional-fine-chemicals/", blank=True)
    product_line_3 = models.CharField(max_length=100, default="Oleoresin")
    product_line_3_url = models.CharField(max_length=255, default="/spices-and-oleoresins/", blank=True)
    product_line_4 = models.CharField(max_length=100, default="Herbal Powder")
    product_line_4_url = models.CharField(max_length=255, default="/raw-herbal-powders/", blank=True)
    product_line_5 = models.CharField(max_length=100, default="Food Color")
    product_line_5_url = models.CharField(max_length=255, default="/natural-food-colors/", blank=True)
    product_line_6 = models.CharField(max_length=100, default="Health Supplement")
    product_line_6_url = models.CharField(max_length=255, default="/product-range/", blank=True)
    
    # ── Story Section (Premium About Us) ──────────────────────────
    story_eyebrow        = models.CharField(max_length=100, default="OUR STORY")
    story_heading        = models.CharField(max_length=255, default="About Us")
    story_paragraph_1    = models.TextField(default="Born in 2014, our mission has been to bring the best of nature to support health and wellbeing.")
    story_paragraph_2    = models.TextField(default="We believe that true wealth is health. That\u2019s why we follow sustainable cultivation and advanced extraction methods to deliver ingredients you can trust.")
    story_cta_label      = models.CharField(max_length=100, default="Learn More")

    # Stats
    stat_1_number  = models.CharField(max_length=20, default="10+")
    stat_1_label   = models.CharField(max_length=100, default="Years of Experience")
    stat_2_number  = models.CharField(max_length=20, default="50+")
    stat_2_label   = models.CharField(max_length=100, default="Happy Clients")
    stat_3_number  = models.CharField(max_length=20, default="100+")
    stat_3_label   = models.CharField(max_length=100, default="Natural Ingredients")
    stat_4_number  = models.CharField(max_length=20, default="30+")
    stat_4_label   = models.CharField(max_length=100, default="Countries Served")

    # Visual composition images
    story_main_image     = models.ImageField(upload_to='about_story/', blank=True, null=True, help_text="Main large circle image")
    story_field_image    = models.ImageField(upload_to='about_story/', blank=True, null=True, help_text="Top-left small circle (e.g. agricultural field)")
    story_facility_image = models.ImageField(upload_to='about_story/', blank=True, null=True, help_text="Bottom-left medium circle (e.g. facility)")
    story_lab_image      = models.ImageField(upload_to='about_story/', blank=True, null=True, help_text="Bottom-right small circle (e.g. lab / scientist)")

    # Belief Quote
    belief_quote_prefix = models.CharField(max_length=100, default="We strongly believe,")
    belief_quote = models.CharField(max_length=255, default="Nature is the best physician")


    def save(self, *args, **kwargs):
        # Ensure there is only one instance
        self.pk = 1
        self.main_image          = compress_uploaded_image(self.main_image)
        self.bottom_image        = compress_uploaded_image(self.bottom_image)
        self.story_main_image    = compress_uploaded_image(self.story_main_image)
        self.story_field_image   = compress_uploaded_image(self.story_field_image)
        self.story_facility_image = compress_uploaded_image(self.story_facility_image)
        self.story_lab_image     = compress_uploaded_image(self.story_lab_image)
        super(AboutPageContent, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "About Page Content"

class CSRPageContent(models.Model):
    # Hero Section
    hero_title = models.CharField(max_length=255, default="Corporate Social Responsibility")
    hero_subtitle = models.TextField(default="Giving back to the community and nurturing the environment for a sustainable future.")
    hero_badge_text = models.CharField(max_length=255, default="Impact & Responsibility")
    hero_image = models.ImageField(upload_to='csr/', blank=True, null=True, help_text="Background image for hero section")
    
    # Intro Section
    intro_title = models.CharField(max_length=255, default="Corporate Social Responsibilities")
    intro_content = models.TextField(default="Our global CR policy focuses on four key areas where we believe we can make the most difference.\n\nFor three of these – Industry, Environment and People – we have established a global framework for our operating companies to work within, allowing them flexibility over which area to invest in according to what will have the most meaning and impact locally.\n\nWhilst local legal standards apply as an absolute minimum, we aim to achieve good practice in our local markets and share this across the Group. The fourth area – Community – is entirely locally driven, allowing our people to support causes close to them and to become involved in their communities.")

    # Pillar 1: Industry
    pillar_1_kicker = models.CharField(max_length=255, default="INDUSTRY")
    pillar_1_title = models.CharField(max_length=255, default="Understanding Customer Challenges")
    pillar_1_content = models.TextField(default="We aim to leverage the unique relationships that we have with our customers across the globe to continue to understand and support the issues and challenges that they face.")
    pillar_1_image = models.ImageField(upload_to='csr/', blank=True, null=True)

    # Pillar 2: Environment
    pillar_2_kicker = models.CharField(max_length=255, default="ENVIRONMENT")
    pillar_2_title = models.CharField(max_length=255, default="Reducing Our Impact")
    pillar_2_content = models.TextField(default="We continue to analyse our impact on our environment. We remain committed to reducing our energy consumption and related emissions where possible, as well as reducing our wider impacts such as resource use and waste to landfill.")
    pillar_2_image = models.ImageField(upload_to='csr/', blank=True, null=True)

    # Pillar 3: People
    pillar_3_kicker = models.CharField(max_length=255, default="PEOPLE")
    pillar_3_title = models.CharField(max_length=255, default="Fairness & Equality")
    pillar_3_content = models.TextField(default="We have a Code of Ethics which recognizes the importance of treating all of our employees fairly, covering issues such as responsible employment, diversity and equal opportunities. This is an effective way of communicating, at a high level, the principles which should be applied in the conduct of our business.")
    pillar_3_image = models.ImageField(upload_to='csr/', blank=True, null=True)

    # Pillar 4: Community
    pillar_4_kicker = models.CharField(max_length=255, default="COMMUNITY")
    pillar_4_title = models.CharField(max_length=255, default="Supporting Local Causes")
    pillar_4_content = models.TextField(default="Our local communities are important to us. We support a number of charities and community organisations worldwide in order to make a positive impact on the communities where we have a presence.")
    pillar_4_image = models.ImageField(upload_to='csr/', blank=True, null=True)

    # Pillar 5: Green Initiative
    pillar_5_kicker = models.CharField(max_length=255, default="GREEN INITIATIVE")
    pillar_5_title = models.CharField(max_length=255, default="The Green Initiative Program")
    pillar_5_content = models.TextField(default="As a part of corporate social responsibility, we at Biomed Ingredients has started a program called the “Green Initiative”. We care for the mother nature and with this initiative, we are involving each and every human being directly or indirectly in saving our planet.")
    pillar_5_image = models.ImageField(upload_to='csr/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Ensure there is only one instance
        self.pk = 1
        self.hero_image = compress_uploaded_image(self.hero_image)
        self.pillar_1_image = compress_uploaded_image(self.pillar_1_image)
        self.pillar_2_image = compress_uploaded_image(self.pillar_2_image)
        self.pillar_3_image = compress_uploaded_image(self.pillar_3_image)
        self.pillar_4_image = compress_uploaded_image(self.pillar_4_image)
        self.pillar_5_image = compress_uploaded_image(self.pillar_5_image)
        super(CSRPageContent, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "CSR Page Content"

class TeamMember(models.Model):
    ALIGNMENT_CHOICES = [
        ('left', 'Left Aligned'),
        ('right', 'Right Aligned'),
    ]

    name = models.CharField(max_length=200)
    primary_designation = models.CharField(max_length=200)
    secondary_designation = models.TextField(blank=True, null=True, help_text="Vertical text on the side (use newlines)")
    bio = models.TextField()
    image_upload = models.ImageField(upload_to="team/", blank=True, null=True)
    alignment = models.CharField(max_length=10, choices=ALIGNMENT_CHOICES, default='left')
    order = models.IntegerField(default=0, help_text="Order in which they appear")

    def save(self, *args, **kwargs):
        if self.image_upload:
            self.image_upload = compress_uploaded_image(self.image_upload)
        super(TeamMember, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'id']


class OperationTeamMember(models.Model):
    ALIGNMENT_CHOICES = [
        ('left', 'Left Aligned'),
        ('right', 'Right Aligned'),
    ]

    name = models.CharField(max_length=200)
    primary_designation = models.CharField(max_length=200)
    secondary_designation = models.TextField(
        blank=True, null=True,
        help_text="Vertical text on the side (use newlines)"
    )
    bio = models.TextField()
    image_upload = models.ImageField(upload_to="operation_team/", blank=True, null=True)
    alignment = models.CharField(max_length=10, choices=ALIGNMENT_CHOICES, default='left')
    order = models.IntegerField(default=0, help_text="Order in which they appear")

    def save(self, *args, **kwargs):
        if self.image_upload:
            self.image_upload = compress_uploaded_image(self.image_upload)
        super(OperationTeamMember, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'id']

class InfrastructurePageContent(models.Model):
    # Hero Section
    main_heading = models.CharField(max_length=255, default="Infrastructure & Services")

    # Farming Section
    farming_badge = models.CharField(max_length=100, default="Sustainable Agriculture")
    farming_heading = models.CharField(max_length=255, default="Vertical Integration")
    farming_text_1 = models.TextField(default="We always start from the basic. so we start from cultivation...")
    farming_text_2 = models.TextField(default="To ensure the seamless supply chain of products Bio Med Ingredients directly connected with farmers...")
    farming_text_3 = models.TextField(default="While farming is important for a number of reasons, it is equally important for farmers...")
    farming_img_upload = models.ImageField(upload_to="infrastructure/", blank=True, null=True)

    # Services Section
    services_badge = models.CharField(max_length=100, default="Capabilities & Support")
    services_heading = models.CharField(max_length=255, default="Our Services")
    services_text_1 = models.TextField(default="Since inception of our brand, we have tried to gain the customer reliance by offering them solutions...")
    services_text_2 = models.TextField(default="We are the one manufacturer you can trust and turn to for everything from an ingredient...")
    services_text_3 = models.TextField(default="When you work with BMI, we'll not only deliver premium ingredients at reasonable prices...")
    services_img_upload = models.ImageField(upload_to="infrastructure/", blank=True, null=True)

    # Quality Section
    quality_badge = models.CharField(max_length=100, default="Structured & Science-Led Framework")
    quality_heading = models.CharField(max_length=255, default="Quality Assurance for Botanical Ingredients")
    quality_text_1 = models.TextField(default="Quality at Bio Med Ingredients is guided by a structured, science-led framework...")
    quality_text_2 = models.TextField(default="We work with trusted cultivation and raw material partners who follow responsible agricultural...")
    quality_text_3 = models.TextField(default="Our manufacturing operations are supported by a DSIR Recognised R and D Unit...")
    quality_text_highlight = models.TextField(default="Production is carried out in controlled environments with standardised operating procedures...")
    quality_text_4 = models.TextField(default="Documentation, batch traceability and specification transparency form a critical part...")
    quality_text_5 = models.TextField(default="For Bio Med Ingredients, quality is not an isolated function. It is an organisational discipline...")
    quality_img_upload = models.ImageField(upload_to="infrastructure/", blank=True, null=True)

    # Standards Section
    standards_heading = models.CharField(max_length=255, default="International Standards")
    standards_text_1 = models.TextField(default="Premium ingredients tested by us as per international standards...")
    standards_text_2 = models.TextField(default="State-of-the-art quality controls and quality assurance systems to meet out cGMP and ISO standards.")
    standards_img_upload = models.ImageField(upload_to="infrastructure/", blank=True, null=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        if self.farming_img_upload:
            self.farming_img_upload = compress_uploaded_image(self.farming_img_upload)
        if self.services_img_upload:
            self.services_img_upload = compress_uploaded_image(self.services_img_upload)
        if self.quality_img_upload:
            self.quality_img_upload = compress_uploaded_image(self.quality_img_upload)
        if self.standards_img_upload:
            self.standards_img_upload = compress_uploaded_image(self.standards_img_upload)
        super(InfrastructurePageContent, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Infrastructure & Services Page Content"

# ---------------------------------------------------------
# Signals for Auto-Deleting Old Images from the Filesystem
# ---------------------------------------------------------
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

@receiver(post_delete)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem when corresponding `Model` object is deleted.
    """
    # Only apply to models in this app
    if sender._meta.app_label != 'main':
        return
        
    for field in instance._meta.fields:
        if isinstance(field, (models.ImageField, models.FileField)):
            file_field = getattr(instance, field.name)
            # Use Django's storage API to work on any host (Local, S3, etc.)
            if file_field and file_field.name:
                try:
                    file_field.storage.delete(file_field.name)
                except Exception:
                    pass

@receiver(pre_save)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem when corresponding `Model` object is updated with a new file.
    """
    if sender._meta.app_label != 'main':
        return
        
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return

    for field in instance._meta.fields:
        if isinstance(field, (models.ImageField, models.FileField)):
            old_file = getattr(old_instance, field.name)
            new_file = getattr(instance, field.name)
            
            # Use Django's storage API to work on any host (Local, S3, etc.)
            if old_file and old_file.name and old_file != new_file:
                try:
                    old_file.storage.delete(old_file.name)
                except Exception:
                    pass

class ResearchArea(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description = models.TextField()
    image_upload = models.ImageField(upload_to='research/', blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True)
    pdf_upload = models.FileField(upload_to='research_pdfs/', blank=True, null=True, help_text="Optional PDF document for this research area")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.image_upload:
            self.image_upload = compress_uploaded_image(self.image_upload)
        super().save(*args, **kwargs)

class ResearchCoreAreaLink(models.Model):
    title = models.CharField(max_length=200)
    target_url = models.CharField(max_length=255, help_text="e.g. 'product_range' or an absolute URL")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, blank=True, help_text="Optional title for the image")
    image_upload = models.ImageField(upload_to='gallery/')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title if self.title else f"Gallery Image {self.id}"
    
    def save(self, *args, **kwargs):
        if self.image_upload:
            self.image_upload = compress_uploaded_image(self.image_upload)
        super().save(*args, **kwargs)

class Brand(models.Model):
    name = models.CharField(max_length=255)
    trademark = models.CharField(max_length=100)
    ingredient = models.CharField(max_length=255)
    dose = models.CharField(max_length=100)
    description = models.TextField()
    applications = models.TextField()
    logo_path = models.CharField(max_length=255, blank=True, help_text="Static path (e.g. images/brands/brand1.png)")
    logo_upload = models.ImageField(upload_to='brands/', blank=True, null=True, help_text="Upload a new logo")
    layer_image_upload = models.ImageField(upload_to='brands/layers/', blank=True, null=True, help_text="Upload a layered image (e.g. shadow or bottom layer)")
    bg_image_upload = models.ImageField(upload_to='brands/backgrounds/', blank=True, null=True, help_text="Upload a background image for the brand card")
    health_benefits = models.TextField(blank=True, null=True, help_text="Text details for health benefits")
    recommended_daily_dose = models.TextField(blank=True, null=True, help_text="Text details for recommended daily dose")
    detailed_description = models.TextField(blank=True, null=True, help_text="Detailed description")
    mechanism = models.TextField(blank=True, null=True, help_text="Text details for mechanism")
    structure_img_upload = models.ImageField(upload_to='brands/structures/', blank=True, null=True, help_text="Upload structure image")
    family = models.CharField(max_length=255, blank=True, null=True, help_text="Family")
    botanical_name = models.CharField(max_length=255, blank=True, null=True, help_text="Botanical name")
    plant_part = models.CharField(max_length=255, blank=True, null=True, help_text="Plant Part")
    shelf_life = models.CharField(max_length=100, blank=True, null=True, help_text="Shelf Life")
    moq = models.CharField(max_length=100, blank=True, null=True, help_text="MOQ")
    solubility = models.CharField(max_length=255, blank=True, null=True, help_text="Solubility")
    preclinical_studies = models.TextField(blank=True, null=True, help_text="Preclinical studies")
    pdf_upload = models.FileField(upload_to='brands/pdfs/', blank=True, null=True, help_text="Upload PDF brochure")

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.logo_upload:
            self.logo_upload = compress_uploaded_image(self.logo_upload)
        if self.layer_image_upload:
            self.layer_image_upload = compress_uploaded_image(self.layer_image_upload)
        if self.bg_image_upload:
            self.bg_image_upload = compress_uploaded_image(self.bg_image_upload)
        if self.structure_img_upload:
            self.structure_img_upload = compress_uploaded_image(self.structure_img_upload)
        super().save(*args, **kwargs)


class ProductRangeSlide(models.Model):
    title = models.CharField(max_length=200, help_text="Slide heading")
    description = models.TextField(help_text="Main description text")
    extra_text = models.TextField(blank=True, null=True, help_text="Optional extra text (e.g. Key ingredients)")
    image_upload = models.ImageField(upload_to='product_range/', blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, help_text="Fallback static path if no upload")
    button_url = models.CharField(max_length=255, default="#", help_text="URL for the 'View Products' button")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('herbal_extracts', 'Herbal Extracts'),
        ('natural_food_colors', 'Natural Food Colors'),
        ('nutritional_fine_chemicals', 'Nutritional Fine Chemicals'),
        ('spices_and_oleoresins', 'Spices and Oleoresins'),
        ('raw_herbal_powders', 'Raw Herbal Powders'),
        ('organic_product_list', 'Organic Product List'),
    ]

    SUB_CATEGORY_CHOICES = [
        ('leaves_herbs', 'Leaves & Herbs (Aerial Parts)'),
        ('roots_rhizomes', 'Roots & Rhizomes'),
        ('fruits_seeds', 'Fruits & Seeds'),
        ('bark_stems', 'Bark & Stems'),
        ('other', 'Other (Blends, Flowers, Juices & Extracts)'),
        ('joint_health', 'Joint Health & Amino Sugars'),
        ('vitamins_coenzymes', 'Vitamins, Coenzymes & Antioxidants'),
        ('minerals', 'Minerals & Trace Elements'),
        ('essential_oils', 'Essential Oils'),
        ('oleoresins', 'Oleoresins'),
        ('spices_powders', 'Whole Spices & Powders'),
    ]

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=50, choices=SUB_CATEGORY_CHOICES, blank=True, null=True, help_text="Optional: Used for grouping Raw Herbal Powders")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)
    image_upload = models.ImageField(upload_to="products/", blank=True, null=True)
    pdf_path = models.CharField(max_length=255, blank=True, null=True)
    pdf_upload = models.FileField(upload_to="product_pdfs/", blank=True, null=True)
    pdf_title = models.CharField(max_length=255, blank=True, null=True, help_text="Text for the PDF button")

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class NaturalFoodColor(models.Model):
    name = models.CharField(max_length=255)
    color_hex = models.CharField(max_length=7, help_text='Hex color code (e.g. #f4a261)')
    order = models.IntegerField(default=0, help_text='Order of display')

    def __str__(self):
        return self.name

class NaturalFlavour(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255, blank=True, null=True, help_text='E.g. Fruit Based Flavour')
    color_hex = models.CharField(max_length=7, help_text='Hex color code (e.g. #f4a261)', blank=True, null=True)
    order = models.IntegerField(default=0, help_text='Order of display')

    def __str__(self):
        return self.name

class ProductBrochure(models.Model):
    title = models.CharField(max_length=200)
    image_upload = models.ImageField(upload_to='brochures/images/', blank=True, null=True, help_text="Upload cover image")
    image_path = models.CharField(max_length=255, blank=True, help_text="Fallback static path if no image uploaded (e.g. assets/images/flags/01.jpg)")
    pdf_upload = models.FileField(upload_to='brochures/pdfs/', blank=True, null=True, help_text="Upload PDF brochure")
    pdf_path = models.CharField(max_length=255, blank=True, help_text="Fallback static path if no PDF uploaded")
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class ProductDocumentCategory(models.Model):
    name = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Product Document Category'
        verbose_name_plural = 'Product Document Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

class ProductDocument(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductDocumentCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='product_documents')
    image = models.ImageField(upload_to='product_documents/images/', null=True, blank=True, help_text='Optional image for the product')
    pdfs = models.TextField(blank=True, help_text='Comma-separated list of PDF file paths')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Document'
        verbose_name_plural = 'Product Documents'

    def __str__(self):
        return self.name

class ExhibitionEvent(models.Model):
    tag = models.CharField(help_text='e.g., # Herbal Extracts', max_length=100)
    description = models.TextField()
    background_image = models.ImageField(help_text='Upload high-res background image', upload_to='exhibitions/')
    order = models.PositiveIntegerField(default=0, help_text='Order in which they appear (1, 2, 3...)')
    is_active = models.BooleanField(default=True)
    booth_number = models.CharField(blank=True, help_text='e.g., Booth No. A1', max_length=100, null=True)
    logo = models.ImageField(blank=True, help_text='Upload exhibition logo', null=True, upload_to='exhibitions/logos/')
    event_date = models.DateField(blank=True, help_text='Start date of the exhibition event', null=True)
    event_end_date = models.DateField(blank=True, help_text='End date of the exhibition event (optional, for date ranges)', null=True)

    class Meta:
        verbose_name = 'Exhibition Event'
        verbose_name_plural = 'Exhibition Events'
        ordering = ['order', 'id']

    def __str__(self):
        return self.tag

class EventSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Event Subscriber'
        verbose_name_plural = 'Event Subscribers'

class ExpoMeetingBooking(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    company = models.CharField(blank=True, max_length=150, null=True)
    phone = models.CharField(max_length=20)
    expo = models.ForeignKey(ExhibitionEvent, on_delete=models.CASCADE, related_name='meeting_bookings')
    meeting_date = models.DateField()
    meeting_time = models.TimeField()
    message = models.TextField(blank=True, null=True)
    status = models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Expo Meeting Booking'
        verbose_name_plural = 'Expo Meeting Bookings'
        ordering = ['-created_at']

    def __str__(self):
        return f"Meeting with {self.name} at {self.expo.tag}"

class InstagramPost(models.Model):
    image_upload = models.ImageField(upload_to="instagram_posts/", help_text="Upload the square Instagram photo")
    caption = models.TextField(blank=True, null=True, help_text="Optional caption for the post")
    link = models.URLField(max_length=500, blank=True, null=True, help_text="Link to the real Instagram post (e.g., https://instagram.com/p/...)")
    is_visible = models.BooleanField(default=True, help_text="Uncheck to hide this post from the website without deleting it")
    order = models.IntegerField(default=0, help_text="Order in which it appears (lower numbers appear first)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = "Instagram Post"
        verbose_name_plural = "Instagram Posts"

    def __str__(self):
        return f"Instagram Post {self.id}"


class JobOpening(models.Model):
    THEME_CHOICES = [
        ('success', 'Green (Success)'),
        ('info', 'Light Blue (Info)'),
        ('warning', 'Yellow (Warning)'),
        ('danger', 'Red (Danger)'),
        ('primary', 'Blue (Primary)'),
        ('secondary', 'Gray (Secondary)')
    ]
    
    ICON_CHOICES = [
        ('fa-briefcase', 'Briefcase (General/Business)'),
        ('fa-microscope', 'Microscope (R&D/Lab)'),
        ('fa-industry', 'Industry/Factory (Manufacturing)'),
        ('fa-flask', 'Flask (Chemistry/Formulation)'),
        ('fa-users', 'Users (HR/Management)'),
        ('fa-chart-line', 'Chart Line (Sales/Marketing)'),
        ('fa-laptop-code', 'Laptop Code (IT/Tech)'),
        ('fa-cogs', 'Cogs (Operations/Maintenance)'),
        ('fa-seedling', 'Seedling (Agriculture/Herbal)'),
        ('fa-leaf', 'Leaf (Nature/Organic)'),
        ('fa-vial', 'Vial (Testing/QA)'),
        ('fa-shipping-fast', 'Shipping (Logistics/Supply)'),
        ('fa-clipboard-check', 'Clipboard Check (QA/Compliance)'),
        ('fa-calculator', 'Calculator (Finance/Accounting)'),
        ('fa-headset', 'Headset (Customer Support)')
    ]
    
    title = models.CharField(max_length=200, help_text="Job title (e.g., Plant Head)")
    category = models.CharField(max_length=200, help_text="Department/Category (e.g., Manufacturing Operations)")
    description = models.TextField(help_text="Short description of the role")
    academic_excellence = models.TextField(blank=True, null=True)
    professional_expertise = models.TextField(blank=True, null=True)
    core_responsibilities = models.TextField(blank=True, null=True, help_text="Enter each responsibility on a new line. They will automatically be converted to bullet points.")
    core_competencies = models.TextField(blank=True, null=True)
    professional_edge = models.TextField(blank=True, null=True)
    commitment_statement = models.TextField(blank=True, null=True)

    @property
    def core_responsibilities_list(self):
        if self.core_responsibilities:
            return [line.strip() for line in self.core_responsibilities.split('\n') if line.strip()]
        return []
        
    icon = models.CharField(max_length=50, choices=ICON_CHOICES, default="fa-briefcase", help_text="Select an icon representing the job role")
    color_theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='success')
    link = models.CharField(max_length=255, default="#", help_text="Link for 'Know More' button (can be mailto: link)")
    order = models.PositiveIntegerField(default=0, help_text="Order in which it appears on the page")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    job = models.ForeignKey(JobOpening, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    experience = models.IntegerField(help_text="Years of experience")
    address = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes/')
    details = models.TextField(blank=True, null=True, help_text="Cover letter or additional details")
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'contact_messages_tb'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

class EmailConfiguration(models.Model):
    enquiry_email = models.CharField(max_length=500, default='design1@biomedingredients.com', help_text="Email for Contact/Enquiries (comma separated for multiple)")
    booking_email = models.CharField(max_length=500, default='design1@biomedingredients.com', help_text="Email for Meeting Bookings (comma separated for multiple)")
    career_email = models.CharField(max_length=500, default='design1@biomedingredients.com', help_text="Email for Career Applications (comma separated for multiple)")
    subscription_email = models.CharField(max_length=500, default='design1@biomedingredients.com', help_text="Email for Subscriptions (comma separated for multiple)")

    class Meta:
        verbose_name = "Email Configuration"
        verbose_name_plural = "Email Configurations"

    def __str__(self):
        return "Global Email Configuration"


