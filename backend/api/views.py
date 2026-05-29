"""
Views for AgriSmartRwanda API.
"""

from rest_framework import viewsets, status, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import (
    Farmer, Crop, Recommendation, YieldPrediction, Disease,
    DiseaseDetection, MarketPrice, Buyer, ProductListing,
    Achievement, FarmerAchievement
)
from .serializers import (
    FarmerSerializer, CropSerializer, RecommendationSerializer,
    YieldPredictionSerializer, DiseaseSerializer, DiseaseDetectionSerializer,
    MarketPriceSerializer, BuyerSerializer, ProductListingSerializer,
    AchievementSerializer, UserSerializer
)


class RegisterView(generics.CreateAPIView):
    """User registration view."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        
        if not all([username, email, password]):
            return Response(
                {'error': 'username, email, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )


class FarmerViewSet(viewsets.ModelViewSet):
    """Farmer viewset."""
    
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__first_name', 'user__last_name', 'village', 'district']
    ordering_fields = ['rank_points', 'experience_years', 'created_at']
    ordering = ['-rank_points']
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        farmer = self.get_object()
        stats = {
            'total_recommendations': farmer.recommendations.count(),
            'total_yield_predictions': farmer.yield_predictions.count(),
            'total_disease_detections': farmer.disease_detections.count(),
            'active_listings': farmer.product_listings.filter(status='ACTIVE').count(),
            'total_achievements': farmer.achievements.count(),
            'rank_points': farmer.rank_points,
        }
        return Response(stats)


class CropViewSet(viewsets.ReadOnlyModelViewSet):
    """Crop viewset."""
    
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'scientific_name']


class RecommendationViewSet(viewsets.ModelViewSet):
    """Recommendation viewset."""
    
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Recommendation.objects.filter(farmer__user=self.request.user)


class YieldPredictionViewSet(viewsets.ModelViewSet):
    """Yield prediction viewset."""
    
    queryset = YieldPrediction.objects.all()
    serializer_class = YieldPredictionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return YieldPrediction.objects.filter(farmer__user=self.request.user)


class DiseaseViewSet(viewsets.ReadOnlyModelViewSet):
    """Disease viewset."""
    
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'scientific_name']


class DiseaseDetectionViewSet(viewsets.ModelViewSet):
    """Disease detection viewset."""
    
    queryset = DiseaseDetection.objects.all()
    serializer_class = DiseaseDetectionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DiseaseDetection.objects.filter(farmer__user=self.request.user)


class MarketPriceViewSet(viewsets.ReadOnlyModelViewSet):
    """Market price viewset."""
    
    queryset = MarketPrice.objects.all()
    serializer_class = MarketPriceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['crop__name', 'region']
    ordering = ['-date']


class BuyerViewSet(viewsets.ReadOnlyModelViewSet):
    """Buyer viewset."""
    
    queryset = Buyer.objects.filter(is_verified=True)
    serializer_class = BuyerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'company_name', 'location']


class ProductListingViewSet(viewsets.ModelViewSet):
    """Product listing viewset."""
    
    queryset = ProductListing.objects.all()
    serializer_class = ProductListingSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['crop__name', 'farmer__user__first_name']
    ordering_fields = ['price_per_kg', 'created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        if self.action == 'list':
            return ProductListing.objects.filter(status='ACTIVE')
        return ProductListing.objects.filter(farmer__user=self.request.user)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """Achievement viewset."""
    
    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]


class FarmerRankingView(generics.ListAPIView):
    """Farmer ranking view."""
    
    queryset = Farmer.objects.all().order_by('-rank_points')
    serializer_class = FarmerSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None