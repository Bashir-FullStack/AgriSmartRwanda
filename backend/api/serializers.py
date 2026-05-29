"""
Serializers for AgriSmartRwanda API.
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Farmer, Crop, Recommendation, YieldPrediction, Disease,
    DiseaseDetection, MarketPrice, Buyer, ProductListing,
    Achievement, FarmerAchievement
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class FarmerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Farmer
        fields = [
            'id', 'user', 'phone', 'village', 'district', 'province',
            'farm_size', 'gender', 'date_of_birth', 'experience_years',
            'profile_picture', 'bio', 'is_verified', 'rank_points',
            'created_at', 'updated_at'
        ]


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = [
            'id', 'name', 'scientific_name', 'description', 'season',
            'optimal_temperature', 'optimal_rainfall', 'growth_period_days', 'image'
        ]


class RecommendationSerializer(serializers.ModelSerializer):
    crop = CropSerializer(read_only=True)
    crop_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Recommendation
        fields = ['id', 'farmer', 'crop', 'crop_id', 'confidence_score', 'reason', 'created_at']


class YieldPredictionSerializer(serializers.ModelSerializer):
    crop = CropSerializer(read_only=True)
    crop_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = YieldPrediction
        fields = [
            'id', 'farmer', 'crop', 'crop_id', 'predicted_yield',
            'confidence_score', 'based_on_factors', 'created_at'
        ]


class DiseaseSerializer(serializers.ModelSerializer):
    affected_crops = CropSerializer(many=True, read_only=True)
    
    class Meta:
        model = Disease
        fields = [
            'id', 'name', 'scientific_name', 'description', 'symptoms',
            'treatment', 'prevention', 'affected_crops', 'image'
        ]


class DiseaseDetectionSerializer(serializers.ModelSerializer):
    disease = DiseaseSerializer(read_only=True)
    
    class Meta:
        model = DiseaseDetection
        fields = ['id', 'farmer', 'disease', 'image', 'confidence_score', 'created_at']


class MarketPriceSerializer(serializers.ModelSerializer):
    crop = CropSerializer(read_only=True)
    
    class Meta:
        model = MarketPrice
        fields = ['id', 'crop', 'price_per_kg', 'region', 'date', 'updated_at']


class BuyerSerializer(serializers.ModelSerializer):
    interested_crops = CropSerializer(many=True, read_only=True)
    
    class Meta:
        model = Buyer
        fields = [
            'id', 'name', 'contact_email', 'contact_phone', 'location',
            'interested_crops', 'company_name', 'min_quantity_kg', 'is_verified'
        ]


class ProductListingSerializer(serializers.ModelSerializer):
    farmer = FarmerSerializer(read_only=True)
    crop = CropSerializer(read_only=True)
    crop_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = ProductListing
        fields = [
            'id', 'farmer', 'crop', 'crop_id', 'quantity_kg', 'price_per_kg',
            'description', 'image', 'status', 'created_at', 'updated_at'
        ]


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ['id', 'name', 'description', 'icon', 'criteria']


class FarmerAchievementSerializer(serializers.ModelSerializer):
    achievement = AchievementSerializer(read_only=True)
    
    class Meta:
        model = FarmerAchievement
        fields = ['id', 'farmer', 'achievement', 'unlocked_at']