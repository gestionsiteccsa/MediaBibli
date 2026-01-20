"""
Ce module définit les URLS pour l'application home.
"""

from django.urls import path

from . import views

app_name = "home"  # pylint: disable=invalid-name


urlpatterns = [
    path("", views.index, name="index"),
]
