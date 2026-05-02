from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from api.serializers import UserSerializer

# get logged-in user info
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user

    serializer = UserSerializer(user)

    return Response(serializer.data ,status=status.HTTP_200_OK)