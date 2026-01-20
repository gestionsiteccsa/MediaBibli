from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
    View,
)

from .forms import (
    LibraryForm,
    LibraryUserCreationForm,
    LoginForm,
    ReaderCreationForm,
    ReaderPasswordResetForm,
    ReaderRegistrationForm,
    ReaderUpdateForm,
    UserProfileForm,
)
from .models import Library, ReaderProfile, User
from .permissions import (
    LibraryContextMixin,
    LibraryStaffRequiredMixin,
    SuperadminRequiredMixin,
)

# =============================================================================
# Authentication Views
# =============================================================================


class CustomLoginView(LoginView):
    """Vue de connexion personnalisée."""

    form_class = LoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_superadmin:
            return reverse_lazy("accounts:library_list")
        elif user.is_library_staff:
            return reverse_lazy("accounts:reader_list")
        else:
            return reverse_lazy("accounts:profile")


class CustomLogoutView(LogoutView):
    """Vue de déconnexion."""

    next_page = "home:index"


class RegisterView(View):
    """
    Vue d'inscription pour les lecteurs.
    Permet aux utilisateurs de créer leur propre compte lecteur.
    """

    template_name = "accounts/register.html"

    def dispatch(self, request, *args, **kwargs):
        # Rediriger les utilisateurs déjà connectés
        if request.user.is_authenticated:
            return redirect("accounts:profile")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = ReaderRegistrationForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ReaderRegistrationForm(request.POST)
        if form.is_valid():
            user, profile = form.save()

            # Envoyer un email de confirmation si configuré
            if user.email:
                self._send_welcome_email(user, profile)

            messages.success(
                request,
                _(
                    "Votre compte a été créé avec succès ! "
                    "Votre numéro de carte est : {}"
                ).format(profile.card_number),
            )
            return redirect("accounts:register_success")

        return render(request, self.template_name, {"form": form})

    def _send_welcome_email(self, user, profile):
        """Envoie un email de bienvenue au nouveau lecteur."""
        subject = _("Bienvenue sur MediaBib !")
        message = _(
            "Bonjour {name},\n\n"
            "Votre compte lecteur a été créé avec succès sur MediaBib.\n\n"
            "Votre numéro de carte : {card_number}\n"
            "Votre médiathèque : {library}\n\n"
            "Vous pouvez dès maintenant vous connecter avec votre identifiant "
            "et votre mot de passe.\n\n"
            "Cordialement,\n"
            "L'équipe MediaBib"
        ).format(
            name=user.get_full_name() or user.username,
            card_number=profile.card_number,
            library=user.library.name if user.library else "-",
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )


class RegisterSuccessView(TemplateView):
    """Vue de confirmation d'inscription."""

    template_name = "accounts/register_success.html"


# =============================================================================
# Profile Views
# =============================================================================


class ProfileView(LoginRequiredMixin, TemplateView):
    """Vue du profil utilisateur."""

    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["user"] = user
        if user.is_reader and hasattr(user, "reader_profile"):
            context["reader_profile"] = user.reader_profile
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Vue de modification du profil utilisateur."""

    model = User
    form_class = UserProfileForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _("Profil mis à jour avec succès."))
        return super().form_valid(form)


# =============================================================================
# Library Management Views (Superadmin only)
# =============================================================================


class LibraryListView(SuperadminRequiredMixin, ListView):
    """Liste des médiathèques."""

    model = Library
    template_name = "accounts/library/list.html"
    context_object_name = "libraries"
    paginate_by = 20


class LibraryCreateView(SuperadminRequiredMixin, View):
    """
    Création d'une médiathèque avec son utilisateur associé.
    Utilise deux formulaires : LibraryForm et LibraryUserCreationForm.
    """

    template_name = "accounts/library/create.html"

    def get(self, request):
        library_form = LibraryForm()
        user_form = LibraryUserCreationForm()
        return render(
            request,
            self.template_name,
            {
                "library_form": library_form,
                "user_form": user_form,
            },
        )

    def post(self, request):
        library_form = LibraryForm(request.POST)
        user_form = LibraryUserCreationForm(request.POST)

        if library_form.is_valid() and user_form.is_valid():
            # Sauvegarder la médiathèque
            library = library_form.save()

            # Créer l'utilisateur associé
            user_form.library = library
            user = user_form.save(commit=False)
            user.library = library
            user.save()

            messages.success(
                request,
                _("Médiathèque '{}' créée avec succès. Utilisateur '{}' créé.").format(
                    library.name, user.username
                ),
            )
            return redirect("accounts:library_detail", pk=library.pk)

        return render(
            request,
            self.template_name,
            {
                "library_form": library_form,
                "user_form": user_form,
            },
        )


class LibraryDetailView(SuperadminRequiredMixin, DetailView):
    """Détail d'une médiathèque."""

    model = Library
    template_name = "accounts/library/detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.object
        context["staff_users"] = library.users.filter(user_type=User.UserType.LIBRARY)
        context["reader_count"] = library.users.filter(
            user_type=User.UserType.READER
        ).count()
        return context


class LibraryUpdateView(SuperadminRequiredMixin, UpdateView):
    """Modification d'une médiathèque."""

    model = Library
    form_class = LibraryForm
    template_name = "accounts/library/update.html"
    context_object_name = "library"

    def get_success_url(self):
        return reverse_lazy("accounts:library_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _("Médiathèque mise à jour avec succès."))
        return super().form_valid(form)


class LibraryDeleteView(SuperadminRequiredMixin, DeleteView):
    """Suppression d'une médiathèque."""

    model = Library
    template_name = "accounts/library/delete.html"
    context_object_name = "library"
    success_url = reverse_lazy("accounts:library_list")

    def form_valid(self, form):
        messages.success(self.request, _("Médiathèque supprimée avec succès."))
        return super().form_valid(form)


# =============================================================================
# Reader Management Views (Library Staff and Superadmin)
# =============================================================================


class ReaderListView(LibraryStaffRequiredMixin, LibraryContextMixin, ListView):
    """Liste des lecteurs."""

    model = ReaderProfile
    template_name = "accounts/reader/list.html"
    context_object_name = "readers"
    paginate_by = 20

    def get_queryset(self):
        qs = ReaderProfile.objects.select_related("user", "user__library")
        user = self.request.user

        # Filtrer par médiathèque si l'utilisateur n'est pas superadmin
        if not user.is_superadmin and user.library:
            qs = qs.filter(user__library=user.library)

        # Recherche par nom ou numéro de carte
        search = self.request.GET.get("search", "")
        if search:
            qs = qs.filter(
                Q(card_number__icontains=search)
                | Q(user__username__icontains=search)
                | Q(user__first_name__icontains=search)
                | Q(user__last_name__icontains=search)
            )

        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search"] = self.request.GET.get("search", "")
        return context


class ReaderCreateView(LibraryStaffRequiredMixin, View):
    """
    Création d'un lecteur avec génération du mot de passe.
    Affiche le mot de passe généré après création.
    """

    template_name = "accounts/reader/create.html"

    def get_library(self):
        user = self.request.user
        if user.is_superadmin:
            # Le superadmin doit choisir une médiathèque
            library_pk = self.request.GET.get("library") or self.request.POST.get(
                "library"
            )
            if library_pk:
                return get_object_or_404(Library, pk=library_pk)
            return None
        return user.library

    def get(self, request):
        library = self.get_library()
        form = ReaderCreationForm(library=library)
        libraries = (
            Library.objects.filter(is_active=True)
            if request.user.is_superadmin
            else None
        )
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "library": library,
                "libraries": libraries,
            },
        )

    def post(self, request):
        library = self.get_library()
        if not library:
            messages.error(request, _("Veuillez sélectionner une médiathèque."))
            return redirect("accounts:reader_create")

        form = ReaderCreationForm(request.POST, library=library)
        if form.is_valid():
            profile = form.save()
            generated_password = form.get_generated_password()

            # Envoyer par email si demandé
            if form.cleaned_data.get("send_password_email") and profile.user.email:
                self._send_password_email(profile.user, generated_password)
                messages.info(request, _("Le mot de passe a été envoyé par email."))

            # Rediriger vers la page de confirmation avec le mot de passe
            return render(
                request,
                "accounts/reader/created.html",
                {
                    "reader": profile,
                    "password": generated_password,
                },
            )

        libraries = (
            Library.objects.filter(is_active=True)
            if request.user.is_superadmin
            else None
        )
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "library": library,
                "libraries": libraries,
            },
        )

    def _send_password_email(self, user, password):
        subject = _("Votre compte MediaBib a été créé")
        message = _(
            "Bonjour {name},\n\n"
            "Votre compte lecteur a été créé sur MediaBib.\n\n"
            "Identifiant : {username}\n"
            "Mot de passe : {password}\n\n"
            "Nous vous conseillons de changer ce mot de passe "
            "après votre première connexion.\n\n"
            "Cordialement,\n"
            "L'équipe MediaBib"
        ).format(
            name=user.get_full_name() or user.username,
            username=user.username,
            password=password,
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )


class ReaderDetailView(LibraryStaffRequiredMixin, DetailView):
    """Détail d'un lecteur."""

    model = ReaderProfile
    template_name = "accounts/reader/detail.html"
    context_object_name = "reader"

    def get_queryset(self):
        qs = ReaderProfile.objects.select_related("user", "user__library")
        user = self.request.user
        if not user.is_superadmin and user.library:
            qs = qs.filter(user__library=user.library)
        return qs


class ReaderUpdateView(LibraryStaffRequiredMixin, UpdateView):
    """Modification d'un lecteur."""

    model = ReaderProfile
    form_class = ReaderUpdateForm
    template_name = "accounts/reader/update.html"
    context_object_name = "reader"

    def get_queryset(self):
        qs = ReaderProfile.objects.select_related("user", "user__library")
        user = self.request.user
        if not user.is_superadmin and user.library:
            qs = qs.filter(user__library=user.library)
        return qs

    def get_success_url(self):
        return reverse_lazy("accounts:reader_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, _("Lecteur mis à jour avec succès."))
        return super().form_valid(form)


class ReaderDeleteView(LibraryStaffRequiredMixin, DeleteView):
    """Suppression d'un lecteur."""

    model = ReaderProfile
    template_name = "accounts/reader/delete.html"
    context_object_name = "reader"
    success_url = reverse_lazy("accounts:reader_list")

    def get_queryset(self):
        qs = ReaderProfile.objects.select_related("user", "user__library")
        user = self.request.user
        if not user.is_superadmin and user.library:
            qs = qs.filter(user__library=user.library)
        return qs

    def form_valid(self, form):
        # Supprimer aussi l'utilisateur associé
        user = self.object.user
        response = super().form_valid(form)
        user.delete()
        messages.success(self.request, _("Lecteur supprimé avec succès."))
        return response


class ReaderPasswordResetView(LibraryStaffRequiredMixin, View):
    """Réinitialisation du mot de passe d'un lecteur."""

    template_name = "accounts/reader/password_reset.html"

    def get_reader(self, pk):
        qs = ReaderProfile.objects.select_related("user", "user__library")
        user = self.request.user
        if not user.is_superadmin and user.library:
            qs = qs.filter(user__library=user.library)
        return get_object_or_404(qs, pk=pk)

    def get(self, request, pk):
        reader = self.get_reader(pk)
        form = ReaderPasswordResetForm(reader_profile=reader)
        return render(
            request,
            self.template_name,
            {
                "form": form,
                "reader": reader,
            },
        )

    def post(self, request, pk):
        reader = self.get_reader(pk)
        form = ReaderPasswordResetForm(request.POST, reader_profile=reader)

        if form.is_valid():
            new_password = form.save()

            # Envoyer par email si demandé
            if form.cleaned_data.get("send_email") and reader.user.email:
                self._send_password_email(reader.user, new_password)
                messages.info(
                    request,
                    _("Le nouveau mot de passe a été envoyé par email."),
                )

            return render(
                request,
                "accounts/reader/password_reset_done.html",
                {
                    "reader": reader,
                    "password": new_password,
                },
            )

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "reader": reader,
            },
        )

    def _send_password_email(self, user, password):
        subject = _("Réinitialisation de votre mot de passe MediaBib")
        message = _(
            "Bonjour {name},\n\n"
            "Votre mot de passe MediaBib a été réinitialisé.\n\n"
            "Nouveau mot de passe : {password}\n\n"
            "Nous vous conseillons de changer ce mot de passe "
            "après votre connexion.\n\n"
            "Cordialement,\n"
            "L'équipe MediaBib"
        ).format(
            name=user.get_full_name() or user.username,
            password=password,
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
