"""This module defines the views for the home application."""

from django.shortcuts import render


def index(request):
    """Vue pour la page d'accueil."""
    return render(request, "home/index.html")
