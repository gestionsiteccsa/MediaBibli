"""
URL configuration for the accounts application.
"""

from django.urls import path

from . import views

app_name = "accounts"  # pylint: disable=invalid-name

urlpatterns = [
    # Authentication
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path(
        "register/success/",
        views.RegisterSuccessView.as_view(),
        name="register_success",
    ),
    # Profile
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.ProfileUpdateView.as_view(), name="profile_edit"),
    # Library management (superadmin only)
    path("libraries/", views.LibraryListView.as_view(), name="library_list"),
    path(
        "libraries/create/",
        views.LibraryCreateView.as_view(),
        name="library_create",
    ),
    path(
        "libraries/<int:pk>/",
        views.LibraryDetailView.as_view(),
        name="library_detail",
    ),
    path(
        "libraries/<int:pk>/edit/",
        views.LibraryUpdateView.as_view(),
        name="library_update",
    ),
    path(
        "libraries/<int:pk>/delete/",
        views.LibraryDeleteView.as_view(),
        name="library_delete",
    ),
    # Reader management (library staff)
    path("readers/", views.ReaderListView.as_view(), name="reader_list"),
    path(
        "readers/create/",
        views.ReaderCreateView.as_view(),
        name="reader_create",
    ),
    path(
        "readers/<int:pk>/",
        views.ReaderDetailView.as_view(),
        name="reader_detail",
    ),
    path(
        "readers/<int:pk>/edit/",
        views.ReaderUpdateView.as_view(),
        name="reader_update",
    ),
    path(
        "readers/<int:pk>/delete/",
        views.ReaderDeleteView.as_view(),
        name="reader_delete",
    ),
    path(
        "readers/<int:pk>/password-reset/",
        views.ReaderPasswordResetView.as_view(),
        name="reader_password_reset",
    ),
]
