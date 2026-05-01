import random

from django.contrib.auth.models import User
from django.core.mail import send_mail

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.models import PasswordResetCode

@api_view(['POST'])
def request_password_reset(request):
    email = request.data.get("email")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "If email exists, code was sent"})
    
    code = str(random.randint(10000, 99999))

    PasswordResetCode.objects.create(user=user, code=code)

    send_mail(
        "Password Reset Code",
        f"Your code is: {code}",
        "no-reply@webapp.com",
        [email],
    )

    return Response({"message": "Reset code sent"}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def verify_reset_code(request):
    email = request.data.get("email")
    code = request.data.get("code")

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"message": "Invalid request", "verified": False}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        reset_obj = PasswordResetCode.objects.filter(user=user, code=code).latest("created_at")
    except PasswordResetCode.DoesNotExist:
        return Response({"message": "Invalid code", "verified": False}, status=status.HTTP_404_NOT_FOUND)
    
    if reset_obj.is_expired():
        return Response({"message": "Code expired", "verified": False}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Code valid", "verified": True}, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def reset_password(request):
    email = request.data.get("email")
    code = request.data.get("code")
    new_password = request.data.get("new_password")

    user = User.objects.get(email=email)
    reset_obj = PasswordResetCode.objects.filter(user=user, code=code).latest("created_at")

    if reset_obj.is_expired():
        return Response({"message": "Code expired", "verified": False}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()

    PasswordResetCode.objects.filter(user=user).delete()

    return Response({"message": "Password updated successfully"})


