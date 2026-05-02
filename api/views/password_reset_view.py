import random

from django.contrib.auth.models import User
from django.core.mail import send_mail

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from api.models import PasswordResetCode

# send a request for password reset code
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
        subject="Ethos: Password Reset Code",
        message="Your password reset code is: " + code,
        from_email="Ethos <no-reply@ethosapp.com>",
        recipient_list=[email],
        html_message=f"""
        <div
            style="
                margin: 0;
                padding: 0;
                background: #f4f6f8;
                border-radius: 12px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                Helvetica, Arial, sans-serif;
            "
            >
            <div
                style="
                max-width: 520px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
                "
            >
                <!-- Header -->
                <div style="padding: 24px 16px; background-color: #292424;">
                    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px; margin:auto;">
                        <tr>
                        
                        <!-- Logo -->
                        <td align="left" style="padding: 10px 0;">
                            <img
                            src="https://res.cloudinary.com/du7dfx3qm/image/upload/v1777634646/logo-and-text_yeepoe.png"
                            width="140"
                            style="display:block; max-width:100%; height:auto;"
                            />
                        </td>

                        <!-- Text -->
                        <td align="right" style="padding: 10px 0;">
                            <p style="margin:0; font-size:14px; color:#e7e7e7;">
                            Moral Decision Logger
                            </p>
                        </td>

                        </tr>
                    </table>
                </div>

                <!-- Body -->
                <div style="padding: 28px">
                <p style="font-size: 14px; color: #333; margin: 0 0 14px">Hello,</p>

                <p
                    style="
                    font-size: 14px;
                    color: #333;
                    line-height: 1.6;
                    margin: 0 0 18px;
                    "
                >
                    We received a request to reset your Ethos account password.
                </p>

                <p style="font-size: 13px; color: #666; margin: 0 0 10px">
                    Your verification code:
                </p>

                <!-- OTP Box -->
                <div
                    style="
                    font-size: 28px;
                    font-weight: 600;
                    letter-spacing: 6px;
                    text-align: center;
                    padding: 14px 0;
                    background: #f7f9fb;
                    border: 1px solid #e6e8eb;
                    border-radius: 10px;
                    color: #111;
                    "
                >
                    {code}
                </div>

                <p style="font-size: 12px; color: #888; margin: 16px 0 0">
                    This code expires in <b>10 minutes</b>.
                </p>

                <p style="font-size: 12px; color: #888; margin-top: 8px">
                    If you did not request this, you can safely ignore this email.
                </p>
                </div>

                <!-- Footer -->
                <div
                style="
                    padding: 18px 28px;
                    border-top: 1px solid #eee;
                    font-size: 11px;
                    color: #999;
                "
                >
                Ethos helps you reflect on moral decisions with clarity.
                </div>
            </div>
        </div>
        """
    )

    return Response({"message": "Reset code sent"}, status=status.HTTP_201_CREATED)


# verify the received code
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


# submit the new password
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

    return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)


# submit new password (not via forgot)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_password_via_profile(request):
    user = request.user
    new_password = request.data.get("new_password")

    if not new_password:
        return Response({
            "message": "New password cannot be empty."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()

    return Response({
        "message": "Password changed successfully"
    }, status=status.HTTP_200_OK)






