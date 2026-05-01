from django.urls import path
from .views import reset_password, request_password_reset, verify_reset_code
from .views import health, test_ai, register, create_decision, list_decisions, user_insights, get_one_decision
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('reset/request-code/', request_password_reset),
    path('reset/verify-code/', verify_reset_code),
    path('reset/password/', reset_password),

    path('test-ai/', test_ai),
    path('health/', health),

    path('register/', register),
    
    path('decision/', create_decision),
    path('decisions/list/', list_decisions),
    path("decision/<int:pk>/", get_one_decision),
    path('insights/', user_insights)
]
