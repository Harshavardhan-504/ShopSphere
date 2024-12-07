from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from .models import Category

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            category_name="Electronics",
            slug="electronics",
            description="All kinds of electronic items",
            cat_image=None
        )

    def test_category_str(self):
        self.assertEqual(str(self.category), "Electronics")

    def test_category_get_url(self):
        self.assertEqual(self.category.get_url(), reverse('products_by_category', args=["electronics"]))

class ContextProcessorTest(TestCase):
    def setUp(self):
        Category.objects.create(category_name="Books", slug="books", description="Various books")

    def test_menu_links(self):
        from .context_processors import menu_links
        request = None
        context = menu_links(request)
        self.assertIn("links", context)
        self.assertEqual(context["links"].count(), 1)

class CategoryAdminTest(TestCase):
    def test_admin_prepopulated_fields(self):
        from .admin import CategoryAdmin
        self.assertIn('slug', CategoryAdmin.prepopulated_fields)
        self.assertEqual(CategoryAdmin.prepopulated_fields['slug'], ('category_name',))

    def test_admin_list_display(self):
        from .admin import CategoryAdmin
        self.assertEqual(CategoryAdmin.list_display, ('category_name', 'slug'))

# Create your tests here.
