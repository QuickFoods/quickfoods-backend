# accounts/views.py
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Customer
from django.db.models import F


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    """
    Simple email + password signup.
    username == email
    """
    username = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    # auto Customer is created by signal
    token = Token.objects.create(user=user)

    return Response(
        {
            "message": "Account created successfully",
            "token": token.key,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    Email + password login.
    Returns auth token.
    """
    username = request.data.get("email")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Email and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)

    if not user:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)

    return Response(
        {
            "token": token.key,
            "message": "Login successful",
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def member_summary(request):
    """
    Used by:
      - Profile page
      - QR / Scan page

    Returns the member's barcode (unique code), current points, and dates.
    """
    user = request.user
    customer, _ = Customer.objects.get_or_create(user=user)

    data = {
        "email": user.username,
        "member_id": customer.barcode,           # use this for QR + profile
        "points": customer.points,
        "store_id": customer.store_id,
        "member_since": customer.created_at.date().isoformat(),
    }
    return Response(data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def admin_add_points(request):
    """
    For super admin only – adjust a member's points.

    POST body:
      - member_id (barcode)
      - points (can be positive or negative)
    """
    if not (request.user.is_staff or request.user.is_superuser):
        return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    member_id = request.data.get("member_id")
    delta = request.data.get("points")

    if member_id is None or delta is None:
        return Response(
            {"error": "member_id and points are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        delta = int(delta)
    except ValueError:
        return Response(
            {"error": "points must be an integer."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        customer = Customer.objects.get(barcode=member_id)
    except Customer.DoesNotExist:
        return Response(
            {"error": "Customer not found for that member_id."},
            status=status.HTTP_404_NOT_FOUND,
        )

    customer.points = F("points") + delta
    customer.save()
    customer.refresh_from_db()

    return Response(
        {
            "member_id": customer.barcode,
            "new_points": customer.points,
        }
    )
from .models import Customer

@api_view(['GET'])
def member_summary(request):
    """
    Returns basic member info for QR screen.

    Query param: ?email=<user email you used at signup>
    """
    email = request.query_params.get("email")
    if not email:
        return Response({"error": "email is required"}, status=400)

    # we used username=email when signing up
    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        return Response({"error": "member not found"}, status=404)

    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        # in case the signal didn't run for some reason, create now
        customer = Customer.objects.create(
            user=user,
            barcode=str(uuid.uuid4().int)[:12],
        )

    data = {
        "full_name": user.get_full_name() or user.username,
        "email": user.email or user.username,
        "barcode": customer.barcode,      # 👈 use this as QR/ID
        "points": customer.points,
        "member_since": customer.created_at.date().isoformat(),
        "member_id": customer.barcode,    # you can change later
    }
    return Response(data)
