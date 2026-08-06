from django.db import models

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
    middle_text = models.TextField(default="IFOAM – Organics International (an organization that promotes organic farming) says, \"Organic Agriculture is a production of a system that sustains the health of soils, ecosystems, and people...\"")
    
    # Bottom Section
    bottom_image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    box_1_title = models.CharField(max_length=255, default="Team")
    box_1_subtitle = models.CharField(max_length=255, default="OUR TEAM")
    box_2_title = models.CharField(max_length=255, default="Farming")
    box_2_subtitle = models.CharField(max_length=255, default="OUR FARMING")
    box_3_title = models.CharField(max_length=255, default="C S R")
    box_3_subtitle = models.CharField(max_length=255, default="CORPORATE SOCIAL RESPONSIBILITIES")

    def save(self, *args, **kwargs):
        # Ensure there is only one instance
        self.pk = 1
        super(AboutPageContent, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "About Page Content"
