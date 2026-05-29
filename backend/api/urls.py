"""
URL configuration for API.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    FarmerViewSet, CropViewSet, RecommendationViewSet, YieldPredictionViewSet,
    DiseaseViewSet, DiseaseDetectionViewSet, MarketPriceViewSet,
    BuyerViewSet, ProductListingViewSet, AchievementViewSet,
    RegisterView, FarmerRankingView
)

router = DefaultRouter()
router.register(r'farmers', FarmerViewSet)
router.register(r'crops', CropViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'yield-predictions', YieldPredictionViewSet)
router.register(r'diseases', DiseaseViewSet)
router.register(r'disease-detections', DiseaseDetectionViewSet)
router.register(r'market-prices', MarketPriceViewSet)
router.register(r'buyers', BuyerViewSet)
router.register(r'product-listings', ProductListingViewSet)
router.register(r'achievements', AchievementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('farmers/ranking/', FarmerRankingView.as_view(), name='farmer-ranking'),
]