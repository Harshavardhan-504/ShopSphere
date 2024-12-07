from django.test import TestCase
from django.test import TestCase
from .models import Payment, Order, OrderProduct
from accounts.models import Account

class PaymentModelTest(TestCase):
    def setUp(self):
        self.payment = Payment.objects.create(
            user=Account.objects.create(username="testuser"),
            payment_id="123456",
            payment_method="Credit Card",
            amount_paid="100.00",
            status="Completed"
        )

    def test_str(self):
        self.assertEqual(str(self.payment), "123456")

class OrderModelTest(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            first_name="John",
            last_name="Doe",
            phone="1234567890",
            email="johndoe@example.com",
            address_line_1="123 Main St",
            address_line_2="",
            country="USA",
            state="NY",
            city="New York",
            order_total=150.00,
            tax=15.00
        )

    def test_str(self):
        self.assertEqual(str(self.order), "John")

    def test_full_name(self):
        self.assertEqual(self.order.full_name(), "John Doe")

    def test_full_address(self):
        self.assertEqual(self.order.full_address(), "123 Main St ")

# Forms
from django.test import TestCase
from .forms import OrderForm

class OrderFormTest(TestCase):
    def test_valid_form(self):
        form = OrderForm(data={
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "email": "johndoe@example.com",
            "address_line_1": "123 Main St",
            "address_line_2": "",
            "country": "USA",
            "state": "NY",
            "city": "New York",
            "order_note": "Test order"
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = OrderForm(data={"first_name": ""})
        self.assertFalse(form.is_valid())