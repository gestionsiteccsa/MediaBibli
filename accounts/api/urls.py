"""
API URL configuration for the accounts application.
"""

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import CustomTokenObtainPairView, LibraryViewSet, ReaderMeViewSet

router = DefaultRouter()
router.register(r"libraries", LibraryViewSet, basename="library")

urlpatterns = [
    # JWT Authentication
    path(
        "auth/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    # Reader self-service endpoints
    path(
        "readers/me/",
        ReaderMeViewSet.as_view(
            {
                "get": "list",
                "patch": "partial_update",
            }
        ),
        name="reader-me",
    ),
    path(
        "readers/me/loans/",
        ReaderMeViewSet.as_view(
            {
                "get": "loans",
            }
        ),
        name="reader-me-loans",
    ),
    path(
        "readers/me/reservations/",
        ReaderMeViewSet.as_view(
            {
                "get": "reservations",
            }
        ),
        name="reader-me-reservations",
    ),
    path(
        "readers/me/history/",
        ReaderMeViewSet.as_view(
            {
                "get": "history",
            }
        ),
        name="reader-me-history",
    ),
    # Router URLs (libraries)
    path("", include(router.urls)),
]
