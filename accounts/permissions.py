from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class SuperadminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin qui restreint l'accès aux super administrateurs uniquement.
    """

    def test_func(self):
        return self.request.user.is_superadmin

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Accès réservé aux super administrateurs.")
        return super().handle_no_permission()


class LibraryStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin qui restreint l'accès au personnel de médiathèque et super administrateurs.
    """

    def test_func(self):
        user = self.request.user
        return user.is_superadmin or user.is_library_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Accès réservé au personnel de médiathèque.")
        return super().handle_no_permission()


class LibraryContextMixin:
    """
    Mixin qui ajoute le contexte de la médiathèque pour les utilisateurs staff.
    Utile pour filtrer les données par médiathèque.
    """

    def get_user_library(self):
        """Retourne la médiathèque de l'utilisateur connecté."""
        user = self.request.user
        if user.is_superadmin:
            # Superadmin peut accéder à toutes les médiathèques
            # On peut ajouter une session variable pour sélectionner une médiathèque
            return getattr(self, "_selected_library", None)
        return user.library

    def get_queryset(self):
        """Filtre le queryset par médiathèque si applicable."""
        qs = super().get_queryset()
        library = self.get_user_library()
        if library and hasattr(qs.model, "library"):
            return qs.filter(library=library)
        return qs


class ReaderRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin qui vérifie que l'utilisateur est un lecteur.
    """

    def test_func(self):
        return self.request.user.is_reader

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Accès réservé aux lecteurs.")
        return super().handle_no_permission()


class OwnerOrStaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin qui vérifie que l'utilisateur est soit le propriétaire de la ressource,
    soit un membre du staff (médiathèque ou superadmin).
    """

    owner_field = "user"  # Champ qui référence le propriétaire

    def test_func(self):
        user = self.request.user
        if user.is_superadmin or user.is_library_staff:
            return True
        # Vérifier si l'utilisateur est le propriétaire
        obj = self.get_object()
        owner = getattr(obj, self.owner_field, None)
        return owner == user

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Vous n'avez pas accès à cette ressource.")
        return super().handle_no_permission()
