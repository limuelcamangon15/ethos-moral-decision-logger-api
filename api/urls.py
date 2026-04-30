from django.urls import path
from .views import test_ai, register, create_decision, list_decisions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path('test-ai/', test_ai),
    path('register/', register),
    path('decision/', create_decision),
    path('decisions/list/', list_decisions)
]
