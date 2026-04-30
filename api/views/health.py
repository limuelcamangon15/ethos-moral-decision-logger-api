from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import datetime

@api_view(['GET'])
def health(request):
    system_info = {
        "system_name": "Ethos",
        "title": "AI-Driven Moral Decision Logger",
        "developers": ["Limuel Camangon", "John Patrick Soriaga"],
        "api_version": "v1.0.0",
        "environment": "production",
        "database": "connected",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    return Response(system_info, status=status.HTTP_200_OK)