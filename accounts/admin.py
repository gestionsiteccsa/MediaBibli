"""Admin configuration for the accounts application."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Library, ReaderProfile, User


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    """Admin configuration for Library model."""

    list_display = ("name", "code", "city", "is_active", "created_at")
    list_filter = ("is_active", "city")
    search_fields = ("name", "code", "city")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("name", "code", "is_active")}),
        (_("Adresse"), {"fields": ("address", "postal_code", "city")}),
        (_("Contact"), {"fields": ("phone", "email", "website")}),
        (
            _("Audit"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


class ReaderProfileInline(admin.StackedInline):
    """Inline admin for ReaderProfile within User admin."""

    model = ReaderProfile
    can_delete = False
    verbose_name_plural = _("Profil lecteur")
    fk_name = "user"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""

    list_display = (
        "username",
        "email",
        "user_type",
        "library",
        "is_active",
        "created_at",
    )
    list_filter = ("user_type", "library", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = BaseUserAdmin.fieldsets + (
        (_("MediaBib"), {"fields": ("user_type", "library")}),
        (
            _("Audit"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_("MediaBib"), {"fields": ("user_type", "library")}),
    )

    def get_inline_instances(self, request, obj=None):
        """Return inline instances for ReaderProfile if user is a reader."""
        if obj and obj.is_reader:
            return [ReaderProfileInline(self.model, self.admin_site)]
        return []


@admin.register(ReaderProfile)
class ReaderProfileAdmin(admin.ModelAdmin):
    """Admin configuration for ReaderProfile model."""

    list_display = (
        "card_number",
        "user",
        "category",
        "is_active",
        "is_blocked",
        "gdpr_consent",
    )
    list_filter = ("category", "is_active", "is_blocked", "gdpr_consent")
    search_fields = (
        "card_number",
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
    ordering = ("card_number",)
    readonly_fields = ("created_at", "updated_at", "card_issued_date")
    raw_id_fields = ("user",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "card_number",
                    "card_issued_date",
                    "card_expiry_date",
                    "category",
                )
            },
        ),
        (
            _("Informations personnelles"),
            {
                "fields": (
                    "birth_date",
                    "address",
                    "postal_code",
                    "city",
                    "phone",
                )
            },
        ),
        (
            _("RGPD"),
            {
                "fields": (
                    "gdpr_consent",
                    "gdpr_consent_date",
                    "newsletter_consent",
                )
            },
        ),
        (
            _("Statut"),
            {"fields": ("is_active", "is_blocked", "blocked_reason")},
        ),
        (
            _("Notes"),
            {"fields": ("internal_notes",), "classes": ("collapse",)},
        ),
        (
            _("Audit"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
