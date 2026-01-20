from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .models import Library, ReaderProfile, User


class LoginForm(AuthenticationForm):
    """Formulaire de connexion personnalisé."""

    username = forms.CharField(
        label=_("Nom d'utilisateur"),
        widget=forms.TextInput(attrs={"autofocus": True}),
    )
    password = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(),
    )


class LibraryForm(forms.ModelForm):
    """Formulaire de création/édition d'une médiathèque."""

    class Meta:
        model = Library
        fields = [
            "name",
            "code",
            "address",
            "postal_code",
            "city",
            "phone",
            "email",
            "website",
            "is_active",
        ]


class LibraryUserCreationForm(UserCreationForm):
    """Formulaire de création d'un utilisateur personnel de médiathèque."""

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, library=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.library = library

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = User.UserType.LIBRARY
        user.library = self.library
        user.is_staff = True  # Accès à l'admin Django
        if commit:
            user.save()
        return user


class ReaderCreationForm(forms.ModelForm):
    """
    Formulaire de création d'un lecteur.
    Génère automatiquement le mot de passe.
    """

    # Champs utilisateur
    username = forms.CharField(
        label=_("Nom d'utilisateur"),
        help_text=_("Sera utilisé pour la connexion."),
    )
    email = forms.EmailField(
        label=_("Email"),
        required=False,
    )
    first_name = forms.CharField(
        label=_("Prénom"),
    )
    last_name = forms.CharField(
        label=_("Nom"),
    )

    # Envoi du mot de passe par email
    send_password_email = forms.BooleanField(
        label=_("Envoyer le mot de passe par email"),
        required=False,
        initial=False,
        help_text=_("Cochez pour envoyer automatiquement le mot de passe par email."),
    )

    class Meta:
        model = ReaderProfile
        fields = [
            "card_number",
            "category",
            "birth_date",
            "address",
            "postal_code",
            "city",
            "phone",
            "gdpr_consent",
            "newsletter_consent",
        ]

    def __init__(self, *args, library=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.library = library
        self._generated_password = None

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Ce nom d'utilisateur existe déjà."))
        return username

    def clean_card_number(self):
        card_number = self.cleaned_data.get("card_number")
        if ReaderProfile.objects.filter(card_number=card_number).exists():
            raise forms.ValidationError(_("Ce numéro de carte existe déjà."))
        return card_number.upper()

    def clean_gdpr_consent(self):
        consent = self.cleaned_data.get("gdpr_consent")
        if not consent:
            raise forms.ValidationError(
                _("Le consentement RGPD est obligatoire pour créer un compte lecteur.")
            )
        return consent

    def save(self, commit=True):
        import secrets
        import string

        # Générer un mot de passe aléatoire
        alphabet = string.ascii_letters + string.digits
        self._generated_password = "".join(secrets.choice(alphabet) for _ in range(12))

        # Créer l'utilisateur
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data.get("email", ""),
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            password=self._generated_password,
            user_type=User.UserType.READER,
            library=self.library,
        )

        # Créer le profil lecteur
        profile = super().save(commit=False)
        profile.user = user
        if profile.gdpr_consent:
            profile.gdpr_consent_date = timezone.now()
        if commit:
            profile.save()

        return profile

    def get_generated_password(self):
        return self._generated_password


class ReaderUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour d'un lecteur (sans modification du mot de passe)."""

    # Champs utilisateur (lecture seule ou édition limitée)
    email = forms.EmailField(
        label=_("Email"),
        required=False,
    )
    first_name = forms.CharField(
        label=_("Prénom"),
    )
    last_name = forms.CharField(
        label=_("Nom"),
    )

    class Meta:
        model = ReaderProfile
        fields = [
            "category",
            "birth_date",
            "address",
            "postal_code",
            "city",
            "phone",
            "card_expiry_date",
            "gdpr_consent",
            "newsletter_consent",
            "is_active",
            "is_blocked",
            "blocked_reason",
            "internal_notes",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            user = self.instance.user
            self.fields["email"].initial = user.email
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            profile.save()
        return profile


class ReaderPasswordResetForm(forms.Form):
    """Formulaire pour réinitialiser le mot de passe d'un lecteur."""

    send_email = forms.BooleanField(
        label=_("Envoyer le nouveau mot de passe par email"),
        required=False,
        initial=False,
    )

    def __init__(self, *args, reader_profile=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.reader_profile = reader_profile
        self._generated_password = None

    def save(self):
        import secrets
        import string

        # Générer un nouveau mot de passe
        alphabet = string.ascii_letters + string.digits
        self._generated_password = "".join(secrets.choice(alphabet) for _ in range(12))

        # Mettre à jour le mot de passe de l'utilisateur
        user = self.reader_profile.user
        user.set_password(self._generated_password)
        user.save()

        return self._generated_password

    def get_generated_password(self):
        return self._generated_password


class UserProfileForm(forms.ModelForm):
    """Formulaire pour qu'un utilisateur modifie son propre profil."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class ReaderSelfProfileForm(forms.ModelForm):
    """Formulaire pour qu'un lecteur modifie ses propres informations."""

    class Meta:
        model = ReaderProfile
        fields = [
            "address",
            "postal_code",
            "city",
            "phone",
            "newsletter_consent",
        ]


class ReaderRegistrationForm(forms.Form):
    """
    Formulaire d'inscription en ligne pour les lecteurs.
    Permet aux lecteurs de créer leur propre compte.
    """

    # Sélection de la médiathèque
    library = forms.ModelChoiceField(
        queryset=Library.objects.filter(is_active=True),
        label=_("Médiathèque"),
        help_text=_("Sélectionnez votre médiathèque de rattachement."),
        empty_label=_("-- Choisir une médiathèque --"),
    )

    # Informations de connexion
    username = forms.CharField(
        label=_("Nom d'utilisateur"),
        min_length=3,
        max_length=150,
        help_text=_("Choisissez un identifiant unique pour vous connecter."),
    )
    email = forms.EmailField(
        label=_("Adresse email"),
        help_text=_(
            "Utilisée pour les notifications et la récupération de mot de passe."
        ),
    )
    password1 = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(),
        min_length=8,
        help_text=_("Au moins 8 caractères."),
    )
    password2 = forms.CharField(
        label=_("Confirmer le mot de passe"),
        widget=forms.PasswordInput(),
    )

    # Informations personnelles
    first_name = forms.CharField(
        label=_("Prénom"),
        max_length=150,
    )
    last_name = forms.CharField(
        label=_("Nom"),
        max_length=150,
    )
    birth_date = forms.DateField(
        label=_("Date de naissance"),
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    phone = forms.CharField(
        label=_("Téléphone"),
        max_length=20,
        required=False,
    )

    # Adresse
    address = forms.CharField(
        label=_("Adresse"),
        widget=forms.Textarea(attrs={"rows": 2}),
        required=False,
    )
    postal_code = forms.CharField(
        label=_("Code postal"),
        max_length=10,
        required=False,
    )
    city = forms.CharField(
        label=_("Ville"),
        max_length=100,
        required=False,
    )

    # Catégorie
    category = forms.ChoiceField(
        label=_("Catégorie"),
        choices=ReaderProfile.CATEGORY_CHOICES,
        initial="adult",
    )

    # Consentements RGPD
    gdpr_consent = forms.BooleanField(
        label=_("J'accepte le traitement de mes données personnelles"),
        help_text=_(
            "Conformément au RGPD, vos données sont utilisées uniquement "
            "pour la gestion de votre compte lecteur."
        ),
    )
    newsletter_consent = forms.BooleanField(
        label=_("J'accepte de recevoir les actualités de la médiathèque"),
        required=False,
        initial=False,
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                _(
                    "Ce nom d'utilisateur est déjà utilisé. "
                    "Veuillez en choisir un autre."
                )
            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Cette adresse email est déjà utilisée."))
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                _("Les deux mots de passe ne correspondent pas.")
            )
        return password2

    def clean_gdpr_consent(self):
        consent = self.cleaned_data.get("gdpr_consent")
        if not consent:
            raise forms.ValidationError(
                _(
                    "Vous devez accepter le traitement de vos données "
                    "pour vous inscrire."
                )
            )
        return consent

    def _generate_card_number(self, library):
        """Génère un numéro de carte unique pour la médiathèque."""
        import random

        prefix = library.code.upper()
        while True:
            number = f"{prefix}-{random.randint(100000, 999999)}"
            if not ReaderProfile.objects.filter(card_number=number).exists():
                return number

    def save(self):
        """Crée l'utilisateur et le profil lecteur."""
        library = self.cleaned_data["library"]

        # Créer l'utilisateur
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            user_type=User.UserType.READER,
            library=library,
        )

        # Créer le profil lecteur
        profile = ReaderProfile.objects.create(
            user=user,
            card_number=self._generate_card_number(library),
            category=self.cleaned_data["category"],
            birth_date=self.cleaned_data.get("birth_date"),
            phone=self.cleaned_data.get("phone", ""),
            address=self.cleaned_data.get("address", ""),
            postal_code=self.cleaned_data.get("postal_code", ""),
            city=self.cleaned_data.get("city", ""),
            gdpr_consent=True,
            gdpr_consent_date=timezone.now(),
            newsletter_consent=self.cleaned_data.get("newsletter_consent", False),
        )

        return user, profile
