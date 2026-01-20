from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Library(models.Model):
    """
    Modèle représentant une médiathèque/bibliothèque.
    Peut faire partie d'un réseau de lecture publique.
    """

    objects = models.Manager()

    name = models.CharField(_("Nom"), max_length=200)
    code = models.CharField(
        _("Code"),
        max_length=20,
        unique=True,
        help_text=_("Code unique d'identification (ex: BIB01)"),
    )

    # Adresse
    address = models.TextField(_("Adresse"), blank=True)
    postal_code = models.CharField(_("Code postal"), max_length=10, blank=True)
    city = models.CharField(_("Ville"), max_length=100, blank=True)

    # Contact
    phone = models.CharField(_("Téléphone"), max_length=20, blank=True)
    email = models.EmailField(_("Email"), blank=True)
    website = models.URLField(_("Site web"), blank=True)

    # Configuration
    is_active = models.BooleanField(_("Active"), default=True)

    # Audit RGPD
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date de modification"), auto_now=True)

    class Meta:
        verbose_name = _("Médiathèque")
        verbose_name_plural = _("Médiathèques")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class User(AbstractUser):
    """
    Modèle utilisateur personnalisé pour MediaBib.
    Gère trois types d'utilisateurs : superadmin, library (personnel), reader (lecteur).
    """

    objects = UserManager()

    class UserType(models.TextChoices):
        SUPERADMIN = "superadmin", _("Super administrateur")
        LIBRARY = "library", _("Personnel de médiathèque")
        READER = "reader", _("Lecteur")

    user_type = models.CharField(
        _("Type d'utilisateur"),
        max_length=20,
        choices=UserType.choices,
        default=UserType.READER,
    )

    # Association à une médiathèque (pour personnel et lecteurs)
    library = models.ForeignKey(
        Library,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
        verbose_name=_("Médiathèque"),
    )

    # Audit RGPD
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date de modification"), auto_now=True)

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_superadmin(self):
        return self.user_type == self.UserType.SUPERADMIN

    @property
    def is_library_staff(self):
        return self.user_type == self.UserType.LIBRARY

    @property
    def is_reader(self):
        return self.user_type == self.UserType.READER

    def save(self, *args, **kwargs):
        # Les superadmins sont toujours staff et superuser
        if self.user_type == self.UserType.SUPERADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)


class ReaderProfile(models.Model):
    """
    Profil détaillé du lecteur (informations de carte, données personnelles).
    Conforme aux exigences RGPD avec consentement explicite.
    """

    objects = models.Manager()

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="reader_profile",
        verbose_name=_("Utilisateur"),
    )

    # Carte de bibliothèque
    card_number = models.CharField(
        _("Numéro de carte"),
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z0-9-]+$",
                message=_(
                    "Le numéro de carte ne peut contenir que des "
                    "lettres majuscules, chiffres et tirets."
                ),
            )
        ],
    )
    card_issued_date = models.DateField(
        _("Date d'émission de la carte"), auto_now_add=True
    )
    card_expiry_date = models.DateField(
        _("Date d'expiration de la carte"), null=True, blank=True
    )

    # Informations personnelles
    birth_date = models.DateField(_("Date de naissance"), null=True, blank=True)
    address = models.TextField(_("Adresse"), blank=True)
    postal_code = models.CharField(_("Code postal"), max_length=10, blank=True)
    city = models.CharField(_("Ville"), max_length=100, blank=True)
    phone = models.CharField(_("Téléphone"), max_length=20, blank=True)

    # Catégorie de lecteur (enfant, adulte, étudiant, senior, etc.)
    CATEGORY_CHOICES = [
        ("child", _("Enfant (0-12 ans)")),
        ("teen", _("Adolescent (13-17 ans)")),
        ("adult", _("Adulte")),
        ("student", _("Étudiant")),
        ("senior", _("Senior")),
        ("professional", _("Professionnel")),
    ]
    category = models.CharField(
        _("Catégorie"),
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="adult",
    )

    # Consentement RGPD
    gdpr_consent = models.BooleanField(
        _("Consentement RGPD"),
        default=False,
        help_text=_(
            "L'utilisateur a accepté le traitement de ses données personnelles."
        ),
    )
    gdpr_consent_date = models.DateTimeField(
        _("Date du consentement RGPD"),
        null=True,
        blank=True,
    )
    newsletter_consent = models.BooleanField(
        _("Consentement newsletter"),
        default=False,
        help_text=_("L'utilisateur accepte de recevoir des communications."),
    )

    # Notes internes (réservé au personnel)
    internal_notes = models.TextField(_("Notes internes"), blank=True)

    # Statut
    is_active = models.BooleanField(_("Actif"), default=True)
    is_blocked = models.BooleanField(_("Bloqué"), default=False)
    blocked_reason = models.TextField(_("Raison du blocage"), blank=True)

    # Audit RGPD
    created_at = models.DateTimeField(_("Date de création"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Date de modification"), auto_now=True)

    class Meta:
        verbose_name = _("Profil lecteur")
        verbose_name_plural = _("Profils lecteurs")

    def __str__(self):
        return f"{self.card_number} - {self.user.get_full_name() or self.user.username}"

    @property
    def full_address(self):
        parts = [self.address, f"{self.postal_code} {self.city}".strip()]
        return ", ".join(p for p in parts if p)
