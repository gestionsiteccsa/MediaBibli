"""
Tests for the accounts application.
"""

from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Library, ReaderProfile, User


class LibraryModelTests(TestCase):
    """Tests for the Library model."""

    def test_create_library(self):
        """Test creating a library."""
        library = Library.objects.create(
            name="Médiathèque Centrale", code="MED01", city="Paris"
        )
        self.assertEqual(str(library), "Médiathèque Centrale (MED01)")
        self.assertTrue(library.is_active)

    def test_library_code_unique(self):
        """Test that library codes must be unique."""
        Library.objects.create(name="Lib 1", code="LIB01")
        with self.assertRaises(IntegrityError):
            Library.objects.create(name="Lib 2", code="LIB01")


class UserModelTests(TestCase):
    """Tests for the User model."""

    def setUp(self):
        self.library = Library.objects.create(name="Test Library", code="TEST01")

    def test_create_superadmin(self):
        """Test creating a superadmin user."""
        user = User.objects.create_user(
            username="admin",
            password="testpass123",
            user_type=User.UserType.SUPERADMIN,
        )
        user.save()
        self.assertTrue(user.is_superadmin)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_library_staff(self):
        """Test creating a library staff user."""
        user = User.objects.create_user(
            username="staff",
            password="testpass123",
            user_type=User.UserType.LIBRARY,
            library=self.library,
        )
        self.assertTrue(user.is_library_staff)
        self.assertFalse(user.is_superadmin)
        self.assertFalse(user.is_reader)
        self.assertEqual(user.library, self.library)

    def test_create_reader(self):
        """Test creating a reader user."""
        user = User.objects.create_user(
            username="reader",
            password="testpass123",
            user_type=User.UserType.READER,
            library=self.library,
        )
        self.assertTrue(user.is_reader)
        self.assertFalse(user.is_superadmin)
        self.assertFalse(user.is_library_staff)

    def test_user_str(self):
        """Test user string representation."""
        user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            user_type=User.UserType.READER,
        )
        self.assertIn("testuser", str(user))
        self.assertIn("Lecteur", str(user))


class ReaderProfileModelTests(TestCase):
    """Tests for the ReaderProfile model."""

    def setUp(self):
        self.library = Library.objects.create(name="Test Library", code="TEST01")
        self.user = User.objects.create_user(
            username="reader",
            password="testpass123",
            user_type=User.UserType.READER,
            library=self.library,
            first_name="Jean",
            last_name="Dupont",
        )

    def test_create_reader_profile(self):
        """Test creating a reader profile."""
        profile = ReaderProfile.objects.create(
            user=self.user,
            card_number="CARD001",
            category="adult",
            gdpr_consent=True,
            gdpr_consent_date=timezone.now(),
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.card_number, "CARD001")
        self.assertTrue(profile.gdpr_consent)

    def test_card_number_unique(self):
        """Test that card numbers must be unique."""
        ReaderProfile.objects.create(
            user=self.user, card_number="CARD001", gdpr_consent=True
        )
        user2 = User.objects.create_user(
            username="reader2",
            password="testpass123",
            user_type=User.UserType.READER,
        )
        with self.assertRaises(IntegrityError):
            ReaderProfile.objects.create(
                user=user2, card_number="CARD001", gdpr_consent=True
            )

    def test_full_address(self):
        """Test the full_address property."""
        profile = ReaderProfile.objects.create(
            user=self.user,
            card_number="CARD002",
            address="123 Rue de la Paix",
            postal_code="75001",
            city="Paris",
            gdpr_consent=True,
        )
        self.assertIn("123 Rue de la Paix", profile.full_address)
        self.assertIn("75001", profile.full_address)
        self.assertIn("Paris", profile.full_address)


class AuthenticationViewTests(TestCase):
    """Tests for authentication views."""

    def setUp(self):
        self.client = Client()
        self.library = Library.objects.create(name="Test Lib", code="TL01")
        self.superadmin = User.objects.create_user(
            username="admin",
            password="adminpass123",
            user_type=User.UserType.SUPERADMIN,
        )
        self.staff = User.objects.create_user(
            username="staff",
            password="staffpass123",
            user_type=User.UserType.LIBRARY,
            library=self.library,
        )
        self.reader_user = User.objects.create_user(
            username="reader",
            password="readerpass123",
            user_type=User.UserType.READER,
            library=self.library,
        )
        self.reader_profile = ReaderProfile.objects.create(
            user=self.reader_user, card_number="RDR001", gdpr_consent=True
        )

    def test_login_page_loads(self):
        """Test that login page loads correctly."""
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Connexion")

    def test_login_superadmin_redirect(self):
        """Test superadmin login redirects to library list."""
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "admin", "password": "adminpass123"},
        )
        self.assertRedirects(response, reverse("accounts:library_list"))

    def test_login_staff_redirect(self):
        """Test library staff login redirects to reader list."""
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "staff", "password": "staffpass123"},
        )
        self.assertRedirects(response, reverse("accounts:reader_list"))

    def test_login_reader_redirect(self):
        """Test reader login redirects to profile."""
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "reader", "password": "readerpass123"},
        )
        self.assertRedirects(response, reverse("accounts:profile"))

    def test_profile_requires_login(self):
        """Test that profile page requires authentication."""
        response = self.client.get(reverse("accounts:profile"))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:profile')}",
        )

    def test_profile_shows_user_info(self):
        """Test that profile page shows user information."""
        self.client.login(username="reader", password="readerpass123")
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "reader")


class LibraryManagementViewTests(TestCase):
    """Tests for library management views (superadmin only)."""

    def setUp(self):
        self.client = Client()
        self.superadmin = User.objects.create_user(
            username="admin",
            password="adminpass123",
            user_type=User.UserType.SUPERADMIN,
        )
        self.library = Library.objects.create(name="Existing Library", code="EXIST01")
        self.staff = User.objects.create_user(
            username="staff",
            password="staffpass123",
            user_type=User.UserType.LIBRARY,
            library=self.library,
        )

    def test_library_list_requires_superadmin(self):
        """Test that library list requires superadmin."""
        self.client.login(username="staff", password="staffpass123")
        response = self.client.get(reverse("accounts:library_list"))
        self.assertEqual(response.status_code, 403)

    def test_library_list_accessible_by_superadmin(self):
        """Test that superadmin can access library list."""
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get(reverse("accounts:library_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Existing Library")

    def test_library_create(self):
        """Test creating a new library with user."""
        self.client.login(username="admin", password="adminpass123")
        self.client.post(
            reverse("accounts:library_create"),
            {
                "name": "New Library",
                "code": "NEW01",
                "username": "newstaff",
                "password1": "complexpass123!",
                "password2": "complexpass123!",
            },
        )
        self.assertEqual(Library.objects.filter(code="NEW01").count(), 1)

    def test_library_detail(self):
        """Test viewing library detail."""
        self.client.login(username="admin", password="adminpass123")
        response = self.client.get(
            reverse("accounts:library_detail", kwargs={"pk": self.library.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Existing Library")


class ReaderManagementViewTests(TestCase):
    """Tests for reader management views (library staff)."""

    def setUp(self):
        self.client = Client()
        self.library = Library.objects.create(name="Test Lib", code="TL01")
        self.staff = User.objects.create_user(
            username="staff",
            password="staffpass123",
            user_type=User.UserType.LIBRARY,
            library=self.library,
        )
        self.reader_user = User.objects.create_user(
            username="reader",
            password="readerpass123",
            user_type=User.UserType.READER,
            library=self.library,
            first_name="Jean",
            last_name="Test",
        )
        self.reader_profile = ReaderProfile.objects.create(
            user=self.reader_user, card_number="RDR001", gdpr_consent=True
        )

    def test_reader_list_requires_staff(self):
        """Test that reader list requires library staff."""
        self.client.login(username="reader", password="readerpass123")
        response = self.client.get(reverse("accounts:reader_list"))
        self.assertEqual(response.status_code, 403)

    def test_reader_list_accessible_by_staff(self):
        """Test that library staff can access reader list."""
        self.client.login(username="staff", password="staffpass123")
        response = self.client.get(reverse("accounts:reader_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RDR001")

    def test_reader_detail(self):
        """Test viewing reader detail."""
        self.client.login(username="staff", password="staffpass123")
        response = self.client.get(
            reverse("accounts:reader_detail", kwargs={"pk": self.reader_profile.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "RDR001")


class APITests(APITestCase):
    """Tests for the REST API."""

    def setUp(self):
        self.library = Library.objects.create(
            name="API Test Library", code="API01", city="Paris"
        )
        self.reader_user = User.objects.create_user(
            username="apireader",
            password="apipass123",
            user_type=User.UserType.READER,
            library=self.library,
            first_name="API",
            last_name="Reader",
        )
        self.reader_profile = ReaderProfile.objects.create(
            user=self.reader_user,
            card_number="APIRDR001",
            category="adult",
            gdpr_consent=True,
            gdpr_consent_date=timezone.now(),
        )

    def test_obtain_token(self):
        """Test obtaining JWT token."""
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "apireader", "password": "apipass123"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["user_type"], "reader")

    def test_token_refresh(self):
        """Test refreshing JWT token."""
        # First get tokens
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "apireader", "password": "apipass123"},
        )
        refresh_token = response.data["refresh"]

        # Then refresh
        response = self.client.post(
            reverse("token_refresh"), {"refresh": refresh_token}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_libraries_list(self):
        """Test listing libraries (public endpoint)."""
        response = self.client.get(reverse("library-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["code"], "API01")

    def test_reader_me_requires_auth(self):
        """Test that reader/me endpoint requires authentication."""
        response = self.client.get(reverse("reader-me"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_reader_me_with_auth(self):
        """Test reader/me endpoint with authentication."""
        # Get token
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "apireader", "password": "apipass123"},
        )
        token = response.data["access"]

        # Access reader/me with token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("reader-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["card_number"], "APIRDR001")
        self.assertEqual(response.data["username"], "apireader")

    def test_reader_me_loans_empty(self):
        """Test that loans endpoint returns empty list (placeholder)."""
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "apireader", "password": "apipass123"},
        )
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("reader-me-loans"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)
        self.assertEqual(response.data["results"], [])

    def test_reader_me_reservations_empty(self):
        """Test that reservations endpoint returns empty list (placeholder)."""
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "apireader", "password": "apipass123"},
        )
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("reader-me-reservations"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_reader_me_history_empty(self):
        """Test that history endpoint returns empty list (placeholder)."""
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "apireader", "password": "apipass123"},
        )
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.get(reverse("reader-me-history"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_reader_me_update(self):
        """Test updating reader profile via API."""
        response = self.client.post(
            reverse("token_obtain_pair"),
            {"username": "apireader", "password": "apipass123"},
        )
        token = response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        response = self.client.patch(
            reverse("reader-me"),
            {"phone": "0123456789", "city": "Lyon"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "0123456789")
        self.assertEqual(response.data["city"], "Lyon")


class PermissionsTests(TestCase):
    """Tests for permission mixins."""

    def setUp(self):
        self.client = Client()
        self.library = Library.objects.create(name="Test Lib", code="TL01")
        self.library2 = Library.objects.create(name="Other Lib", code="TL02")

        self.superadmin = User.objects.create_user(
            username="admin",
            password="adminpass123",
            user_type=User.UserType.SUPERADMIN,
        )
        self.staff = User.objects.create_user(
            username="staff",
            password="staffpass123",
            user_type=User.UserType.LIBRARY,
            library=self.library,
        )
        self.staff2 = User.objects.create_user(
            username="staff2",
            password="staffpass123",
            user_type=User.UserType.LIBRARY,
            library=self.library2,
        )
        self.reader_user = User.objects.create_user(
            username="reader",
            password="readerpass123",
            user_type=User.UserType.READER,
            library=self.library,
        )
        self.reader_profile = ReaderProfile.objects.create(
            user=self.reader_user, card_number="RDR001", gdpr_consent=True
        )

    def test_staff_can_only_see_own_library_readers(self):
        """Test that staff can only see readers from their library."""
        # Create a reader in another library
        other_reader = User.objects.create_user(
            username="otherreader",
            password="pass123",
            user_type=User.UserType.READER,
            library=self.library2,
        )
        ReaderProfile.objects.create(
            user=other_reader, card_number="OTHER001", gdpr_consent=True
        )

        # Staff from library1 should not see reader from library2
        self.client.login(username="staff", password="staffpass123")
        response = self.client.get(reverse("accounts:reader_list"))
        self.assertContains(response, "RDR001")
        self.assertNotContains(response, "OTHER001")

    def test_superadmin_can_see_all_readers(self):
        """Test that superadmin can see readers from all libraries."""
        # Create a reader in another library
        other_reader = User.objects.create_user(
            username="otherreader",
            password="pass123",
            user_type=User.UserType.READER,
            library=self.library2,
        )
        ReaderProfile.objects.create(
            user=other_reader, card_number="OTHER001", gdpr_consent=True
        )

        self.client.login(username="admin", password="adminpass123")
        response = self.client.get(reverse("accounts:reader_list"))
        self.assertContains(response, "RDR001")
        self.assertContains(response, "OTHER001")


class RegistrationTests(TestCase):
    """Tests for the self-registration system."""

    def setUp(self):
        self.client = Client()
        self.library = Library.objects.create(
            name="Test Library", code="TEST01", city="Paris"
        )

    def test_register_page_loads(self):
        """Test that registration page loads correctly."""
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Créer un compte")

    def test_register_page_shows_libraries(self):
        """Test that registration page shows available libraries."""
        response = self.client.get(reverse("accounts:register"))
        self.assertContains(response, "Test Library")

    def test_register_success(self):
        """Test successful registration."""
        response = self.client.post(
            reverse("accounts:register"),
            {
                "library": self.library.pk,
                "username": "newreader",
                "email": "newreader@example.com",
                "password1": "securepass123",
                "password2": "securepass123",
                "first_name": "Jean",
                "last_name": "Dupont",
                "category": "adult",
                "gdpr_consent": True,
            },
        )
        self.assertRedirects(response, reverse("accounts:register_success"))

        # Vérifier que l'utilisateur a été créé
        self.assertTrue(User.objects.filter(username="newreader").exists())
        user = User.objects.get(username="newreader")
        self.assertEqual(user.user_type, User.UserType.READER)
        self.assertEqual(user.library, self.library)

        # Vérifier que le profil lecteur a été créé
        self.assertTrue(hasattr(user, "reader_profile"))
        profile = user.reader_profile
        self.assertTrue(profile.card_number.startswith("TEST01-"))
        self.assertTrue(profile.gdpr_consent)

    def test_register_duplicate_username(self):
        """Test registration with duplicate username fails."""
        User.objects.create_user(username="existinguser", password="pass123")
        response = self.client.post(
            reverse("accounts:register"),
            {
                "library": self.library.pk,
                "username": "existinguser",
                "email": "new@example.com",
                "password1": "securepass123",
                "password2": "securepass123",
                "first_name": "Jean",
                "last_name": "Dupont",
                "category": "adult",
                "gdpr_consent": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "déjà utilisé")

    def test_register_duplicate_email(self):
        """Test registration with duplicate email fails."""
        User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="pass123",
        )
        response = self.client.post(
            reverse("accounts:register"),
            {
                "library": self.library.pk,
                "username": "newuser",
                "email": "existing@example.com",
                "password1": "securepass123",
                "password2": "securepass123",
                "first_name": "Jean",
                "last_name": "Dupont",
                "category": "adult",
                "gdpr_consent": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "déjà utilisée")

    def test_register_password_mismatch(self):
        """Test registration with mismatched passwords fails."""
        response = self.client.post(
            reverse("accounts:register"),
            {
                "library": self.library.pk,
                "username": "newreader",
                "email": "new@example.com",
                "password1": "securepass123",
                "password2": "differentpass",
                "first_name": "Jean",
                "last_name": "Dupont",
                "category": "adult",
                "gdpr_consent": True,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ne correspondent pas")

    def test_register_without_gdpr_consent(self):
        """Test registration without GDPR consent fails."""
        response = self.client.post(
            reverse("accounts:register"),
            {
                "library": self.library.pk,
                "username": "newreader",
                "email": "new@example.com",
                "password1": "securepass123",
                "password2": "securepass123",
                "first_name": "Jean",
                "last_name": "Dupont",
                "category": "adult",
                "gdpr_consent": False,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newreader").exists())

    def test_register_redirects_authenticated_user(self):
        """Test that authenticated users are redirected from registration."""
        User.objects.create_user(username="existinguser", password="pass123")
        self.client.login(username="existinguser", password="pass123")
        response = self.client.get(reverse("accounts:register"))
        self.assertRedirects(response, reverse("accounts:profile"))

    def test_register_success_page(self):
        """Test that success page loads after registration."""
        response = self.client.get(reverse("accounts:register_success"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "réussie")

    def test_register_can_login_after(self):
        """Test that new user can login after registration."""
        self.client.post(
            reverse("accounts:register"),
            {
                "library": self.library.pk,
                "username": "newreader",
                "email": "new@example.com",
                "password1": "securepass123",
                "password2": "securepass123",
                "first_name": "Jean",
                "last_name": "Dupont",
                "category": "adult",
                "gdpr_consent": True,
            },
        )

        # Tester la connexion
        login_success = self.client.login(
            username="newreader", password="securepass123"
        )
        self.assertTrue(login_success)

    def test_inactive_library_not_shown(self):
        """Test that inactive libraries are not shown in registration."""
        Library.objects.create(name="Inactive Library", code="INACT01", is_active=False)
        response = self.client.get(reverse("accounts:register"))
        self.assertNotContains(response, "Inactive Library")
