from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from .serializers import UserMeSerializer

User = get_user_model()


@extend_schema(
    tags=["Account"],
    summary="Get current logged-in user",
    description="Returns basic information about the currently authenticated user.",
    responses=UserMeSerializer,
)
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)
