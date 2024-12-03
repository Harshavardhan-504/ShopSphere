from django.test import TestCase
from .models import Account
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from .views import register, login, logout, forgotPassword
from django.test import TestCase, Client
from django.urls import reverse
from .models import Account

class AccountModelTest(TestCase):
    def setUp(self):
        self.user = Account.objects.create_user(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john.doe@example.com",
            password="securepassword123"
        )

    def test_account_creation(self):
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_admin)

from .forms import RegistrationForm

class RegistrationFormTest(TestCase):
    def test_registration_form_valid(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'jane.doe@example.com',
            'password': 'securepassword123',
            'confirm_password': 'securepassword123'
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self):
        form_data = {
            'first_name': 'Jane',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'jane.doe@example.com',
            'password': 'securepassword123',
            'confirm_password': 'differentpassword'
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'], ["Password does not match!"])

class UrlsTest(SimpleTestCase):
    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, register)

    def test_login_url(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, login)

    def test_logout_url(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout)

    def test_forgot_password_url(self):
        url = reverse('forgotPassword')
        self.assertEqual(resolve(url).func, forgotPassword)

class ViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Account.objects.create_user(
            first_name="John",
            last_name="Doe",
            username="johndoe",
            email="john.doe@example.com",
            password="securepassword123"
        )

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        login_data = {'email': 'john.doe@example.com', 'password': 'securepassword123'}
        response = self.client.post(reverse('login'), login_data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful login

    def test_logout_view(self):
        self.client.login(email='john.doe@example.com', password='securepassword123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect after logout
