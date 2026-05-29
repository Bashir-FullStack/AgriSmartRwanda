"""
Django admin configuration for API models.
"""

from django.contrib import admin
from .models import (
    Farmer, Crop, Recommendation, YieldPrediction, Disease,
    DiseaseDetection, MarketPrice, Buyer, ProductListing,
    Achievement, FarmerAchievement
)


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'phone', 'district', 'farm_size', 'rank_points', 'is_verified']
    list_filter = ['is_verified', 'province', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'phone']
    ordering = ['-rank_points']
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Name'


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name', 'season', 'growth_period_days']
    list_filter = ['season']
    search_fields = ['name', 'scientific_name']


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'crop', 'confidence_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['farmer__user__first_name', 'crop__name']


@admin.register(YieldPrediction)
class YieldPredictionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'crop', 'predicted_yield', 'confidence_score']
    list_filter = ['created_at']
    search_fields = ['farmer__user__first_name', 'crop__name']


@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'scientific_name']
    search_fields = ['name', 'scientific_name']


@admin.register(DiseaseDetection)
class DiseaseDetectionAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'disease', 'confidence_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['farmer__user__first_name', 'disease__name']


@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['crop', 'region', 'price_per_kg', 'date']
    list_filter = ['date', 'region']
    search_fields = ['crop__name', 'region']


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_name', 'location', 'is_verified']
    list_filter = ['is_verified']
    search_fields = ['name', 'company_name']


@admin.register(ProductListing)
class ProductListingAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'crop', 'quantity_kg', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['farmer__user__first_name', 'crop__name']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(FarmerAchievement)
class FarmerAchievementAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'achievement', 'unlocked_at']
    list_filter = ['unlocked_at']
    search_fields = ['farmer__user__first_name', 'achievement__name']