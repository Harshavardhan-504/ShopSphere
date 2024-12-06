from audioop import reverse
from django.urls import reverse
from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, max_length=255)
    cat_image = models.ImageField(upload_to='photos/categories', blank=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args = [self.slug])

    def __str__(self):
        return self.category_name