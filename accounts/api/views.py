"""
API views for the accounts application.
"""

from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from accounts.models import Library, ReaderProfile

from .serializers import (
    CustomTokenObtainPairSerializer,
    LibrarySerializer,
    ReaderMeSerializer,
    ReaderMeUpdateSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view that returns additional user information.
    """

    serializer_class = CustomTokenObtainPairSerializer


class LibraryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing libraries.

    list: List all active libraries
    retrieve: Get details of a specific library
    """

    queryset = Library.objects.filter(is_active=True)
    serializer_class = LibrarySerializer
    permission_classes = [AllowAny]


class ReaderMeViewSet(viewsets.ViewSet):
    """
    API endpoint for the authenticated reader's own data.

    Provides endpoints for:
    - GET /readers/me/ - Reader's profile
    - PATCH /readers/me/ - Update profile (limited fields)
    - GET /readers/me/loans/ - Current loans (placeholder)
    - GET /readers/me/reservations/ - Current reservations (placeholder)
    - GET /readers/me/history/ - Loan history (placeholder)
    """

    permission_classes = [IsAuthenticated]

    def get_reader_profile(self, request):
        """Get the authenticated reader's profile or return None."""
        user = request.user
        if not user.is_reader:
            return None
        try:
            return user.reader_profile
        except ReaderProfile.DoesNotExist:
            return None

    def list(self, request):
        """GET /readers/me/ - Returns the authenticated reader's profile."""
        profile = self.get_reader_profile(request)
        if not profile:
            return Response(
                {"detail": "Vous n'êtes pas un lecteur ou votre profil n'existe pas."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ReaderMeSerializer(profile)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        """PATCH /readers/me/ - Update the reader's profile (limited fields)."""
        profile = self.get_reader_profile(request)
        if not profile:
            return Response(
                {"detail": "Vous n'êtes pas un lecteur ou votre profil n'existe pas."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer = ReaderMeUpdateSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ReaderMeSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def loans(self, request):
        """
        GET /readers/me/loans/ - Returns the reader's current loans.

        Note: This is a placeholder that returns an empty list.
        Will be implemented when the loans module is created.
        """
        profile = self.get_reader_profile(request)
        if not profile:
            return Response(
                {"detail": "Vous n'êtes pas un lecteur ou votre profil n'existe pas."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Placeholder: return empty list
        # TODO: Implement when loans module is created
        return Response({"count": 0, "results": []})

    @action(detail=False, methods=["get"])
    def reservations(self, request):
        """
        GET /readers/me/reservations/ - Returns the reader's current reservations.

        Note: This is a placeholder that returns an empty list.
        Will be implemented when the reservations module is created.
        """
        profile = self.get_reader_profile(request)
        if not profile:
            return Response(
                {"detail": "Vous n'êtes pas un lecteur ou votre profil n'existe pas."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Placeholder: return empty list
        # TODO: Implement when reservations module is created
        return Response({"count": 0, "results": []})

    @action(detail=False, methods=["get"])
    def history(self, request):
        """
        GET /readers/me/history/ - Returns the reader's loan history.

        Note: This is a placeholder that returns an empty list.
        Will be implemented when the loans module is created.
        """
        profile = self.get_reader_profile(request)
        if not profile:
            return Response(
                {"detail": "Vous n'êtes pas un lecteur ou votre profil n'existe pas."},
                status=status.HTTP_403_FORBIDDEN,
            )
        # Placeholder: return empty list
        # TODO: Implement when loans module is created
        return Response({"count": 0, "results": []})
