from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import reset_password, request_password_reset, verify_reset_code
from .views import create_decision, list_decisions, get_one_decision, get_weekly_decisions_count, user_insights
from .views import health, test_ai, register
from .views import get_user_info


urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('register/', register),

# test
    path('test-ai/', test_ai),
    path('health/', health),

# reset password
    path('reset/request-code/', request_password_reset),
    path('reset/verify-code/', verify_reset_code),
    path('reset/password/', reset_password),

# decisions
    path('decision/', create_decision),
    path('decisions/list/', list_decisions),
    path('decisions/weekly-count/', get_weekly_decisions_count),
    path('decision/<int:pk>/', get_one_decision),
    path('insights/', user_insights),

# user
    path('user/me/', get_user_info)
]
