from django.test import TestCase
from carts.models import Cart, CartItem
from store.models import Product
from accounts.models import Account
from category.models import Category 

class CartItemModelTest(TestCase):
    def setUp(self):
        # Creating a category
        self.category = Category.objects.create(
            category_name="Electronics",
            slug="electronics"
        )
        # Creating a product with correct field names
        self.product = Product.objects.create(
            product_name="Test Product",
            slug="test-product",
            description="Test product description",
            price=100,
            stock=10,
            category=self.category,
            is_available=True
        )
        # Creating a user
        self.user = Account.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        # Creating a cart
        self.cart = Cart.objects.create(cart_id="testcart123")
        # Creating a cart item
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.product,
            cart=self.cart,
            quantity=2
        )
    
    def test_cart_item_sub_total(self):
        # Testing the sub_total method of CartItem
        self.assertEqual(self.cart_item.sub_total(), 200)

#Views testcase
from django.test import TestCase, Client
from carts.models import Cart, CartItem
from store.models import Product
from accounts.models import Account
from category.models import Category
from django.urls import reverse

class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            category_name="Electronics",
            slug="electronics"
        )
        self.product = Product.objects.create(
            product_name="Test Product",
            slug="test-product",
            description="Test product description",
            price=100,
            stock=10,
            category=self.category,
            is_available=True
        )
        self.cart = Cart.objects.create(cart_id="testcart123")
        self.user = Account.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
            first_name="Test",
            last_name="User"
        )
        self.checkout_url = reverse("checkout")
    
    def test_checkout_page(self):
        # Log in the test user
        self.client.login(email="testuser@example.com", password="password123")

        # Access the checkout page
        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "store/checkout.html")

#Urls
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from carts.views import cart, add_cart, remove_cart, checkout

class UrlsTest(SimpleTestCase):
    def test_cart_url_resolves(self):
        url = reverse("cart")
        self.assertEqual(resolve(url).func, cart)

    def test_add_cart_url_resolves(self):
        url = reverse("add_cart", args=[1])
        self.assertEqual(resolve(url).func, add_cart)

    def test_remove_cart_url_resolves(self):
        url = reverse("remove_cart", args=[1])
        self.assertEqual(resolve(url).func, remove_cart)

    def test_checkout_url_resolves(self):
        url = reverse("checkout")
        self.assertEqual(resolve(url).func, checkout)


