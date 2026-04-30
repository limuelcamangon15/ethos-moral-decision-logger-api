from django.urls import path
from .views import health, test_ai, register, create_decision, list_decisions, user_insights
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('test-ai/', test_ai),
    path('health/', health),

    path('register/', register),
    
    path('decision/', create_decision),
    path('decisions/list/', list_decisions),
    path('insights/', user_insights)
]
