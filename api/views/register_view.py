from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def register(request):
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    email = request.data.get("email")
    username = request.data.get("username")
    password = request.data.get("password")

    if not all([email, username, password]):
        return Response({"message": "email, username, and password are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    email = email.lower().strip()
    
    if User.objects.filter(email=email).exists():
        return Response({"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        first_name=first_name or "",
        last_name=last_name or "",
        email=email,
        username=username,
        password=password
    )

    return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)