from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if None in [username, password]:
        return Response({"message": "Error, username and password is empty"}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"message": "User alreadt exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(
        username=username,
        password=password
    )

    return Response({"message": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)