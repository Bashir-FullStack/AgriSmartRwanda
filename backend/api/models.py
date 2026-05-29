"""
Models for AgriSmartRwanda API.
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Farmer(models.Model):
    """Farmer profile model."""
    
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    phone = models.CharField(max_length=20, unique=True)
    village = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    farm_size = models.FloatField(help_text="Farm size in hectares")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    experience_years = models.IntegerField(default=0)
    profile_picture = models.ImageField(upload_to='farmer_profiles/', null=True, blank=True)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    rank_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-rank_points']
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Crop(models.Model):
    """Crop model."""
    
    name = models.CharField(max_length=255, unique=True)
    scientific_name = models.CharField(max_length=255)
    description = models.TextField()
    season = models.CharField(max_length=50, choices=[
        ('RAINY', 'Rainy Season'),
        ('DRY', 'Dry Season'),
        ('BOTH', 'Both Seasons'),
    ])
    optimal_temperature = models.CharField(max_length=50)
    optimal_rainfall = models.CharField(max_length=50)
    growth_period_days = models.IntegerField()
    image = models.ImageField(upload_to='crops/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Recommendation(models.Model):
    """AI Crop recommendation model."""
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='recommendations')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('farmer', 'crop')
    
    def __str__(self):
        return f"{self.farmer} -> {self.crop}"


class YieldPrediction(models.Model):
    """Yield prediction model."""
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='yield_predictions')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    predicted_yield = models.FloatField(help_text="Predicted yield in kg/hectare")
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    based_on_factors = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.farmer.user.first_name} - {self.crop.name}: {self.predicted_yield} kg/ha"


class Disease(models.Model):
    """Plant disease model."""
    
    name = models.CharField(max_length=255)
    scientific_name = models.CharField(max_length=255)
    description = models.TextField()
    symptoms = models.TextField()
    treatment = models.TextField()
    prevention = models.TextField()
    affected_crops = models.ManyToManyField(Crop)
    image = models.ImageField(upload_to='diseases/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Diseases"
    
    def __str__(self):
        return self.name


class DiseaseDetection(models.Model):
    """Disease detection result model."""
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='disease_detections')
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='disease_detections/')
    confidence_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.farmer} - {self.disease}"


class MarketPrice(models.Model):
    """Market price model."""
    
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='market_prices')
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    region = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('crop', 'region', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.crop.name} - {self.region}: {self.price_per_kg} RWF"


class Buyer(models.Model):
    """Buyer model."""
    
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    interested_crops = models.ManyToManyField(Crop)
    company_name = models.CharField(max_length=255, blank=True)
    min_quantity_kg = models.FloatField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class ProductListing(models.Model):
    """Product listing model."""
    
    STATUS_CHOICES = [('DRAFT', 'Draft'), ('ACTIVE', 'Active'), ('SOLD', 'Sold'), ('EXPIRED', 'Expired')]
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='product_listings')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity_kg = models.FloatField()
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_listings/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.farmer} - {self.crop.name} ({self.quantity_kg}kg)"


class Achievement(models.Model):
    """Achievement/Badge model."""
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to='achievements/')
    criteria = models.JSONField(help_text="Criteria for unlocking achievement")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class FarmerAchievement(models.Model):
    """Farmer achievement model."""
    
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('farmer', 'achievement')
    
    def __str__(self):
        return f"{self.farmer} - {self.achievement.name}"