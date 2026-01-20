"""Serializers for the accounts API."""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers

from accounts.models import Library, ReaderProfile, User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that includes user type in the token.
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["user_type"] = user.user_type
        token["username"] = user.username
        if user.library:
            token["library_id"] = user.library.id
            token["library_code"] = user.library.code
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra response data
        data["user_type"] = self.user.user_type
        data["username"] = self.user.username
        data["full_name"] = self.user.get_full_name()
        if self.user.library:
            data["library"] = {
                "id": self.user.library.id,
                "name": self.user.library.name,
                "code": self.user.library.code,
            }
        return data


class LibrarySerializer(serializers.ModelSerializer):
    """Serializer for Library model (public info)."""

    class Meta:
        model = Library
        fields = [
            "id",
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
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model (basic info)."""

    library = LibrarySerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "user_type",
            "library",
        ]
        read_only_fields = fields


class ReaderProfileSerializer(serializers.ModelSerializer):
    """Serializer for ReaderProfile model."""

    user = UserSerializer(read_only=True)

    class Meta:
        model = ReaderProfile
        fields = [
            "id",
            "user",
            "card_number",
            "card_issued_date",
            "card_expiry_date",
            "category",
            "birth_date",
            "address",
            "postal_code",
            "city",
            "phone",
            "gdpr_consent",
            "newsletter_consent",
            "is_active",
            "is_blocked",
        ]
        read_only_fields = fields


class ReaderMeSerializer(serializers.ModelSerializer):
    """
    Serializer for the authenticated reader's own profile.
    Used for /api/v1/readers/me/ endpoint.
    """

    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    full_name = serializers.SerializerMethodField()
    library = LibrarySerializer(source="user.library", read_only=True)

    class Meta:
        model = ReaderProfile
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "full_name",
            "card_number",
            "card_issued_date",
            "card_expiry_date",
            "category",
            "birth_date",
            "address",
            "postal_code",
            "city",
            "phone",
            "gdpr_consent",
            "newsletter_consent",
            "is_active",
            "is_blocked",
            "library",
        ]
        read_only_fields = fields

    def get_full_name(self, obj):
        return obj.user.get_full_name()


class ReaderMeUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating reader's own profile (limited fields).
    """

    email = serializers.EmailField(source="user.email", required=False)

    class Meta:
        model = ReaderProfile
        fields = [
            "email",
            "address",
            "postal_code",
            "city",
            "phone",
            "newsletter_consent",
        ]

    def update(self, instance, validated_data):
        # Update user email if provided
        user_data = validated_data.pop("user", {})
        if "email" in user_data:
            instance.user.email = user_data["email"]
            instance.user.save()

        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


# Placeholder serializers for future features
class LoanSerializer(serializers.Serializer):
    """Placeholder serializer for loans (to be implemented)."""

    id = serializers.IntegerField()
    document_title = serializers.CharField()
    loan_date = serializers.DateField()
    due_date = serializers.DateField()
    renewed_count = serializers.IntegerField()


class ReservationSerializer(serializers.Serializer):
    """Placeholder serializer for reservations (to be implemented)."""

    id = serializers.IntegerField()
    document_title = serializers.CharField()
    reservation_date = serializers.DateTimeField()
    status = serializers.CharField()
    position_in_queue = serializers.IntegerField()


class HistorySerializer(serializers.Serializer):
    """Placeholder serializer for loan history (to be implemented)."""

    id = serializers.IntegerField()
    document_title = serializers.CharField()
    loan_date = serializers.DateField()
    return_date = serializers.DateField()
