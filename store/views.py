from itertools import product

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from category.models import Category
from .models import Product
from carts.models import CartItem
from carts.views import _cart_id

def store(request, category_slug=None):
    categories = None
    products = None
    product_count = 0

    # Get min and max price from GET parameters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    # Apply price range filter
    if min_price or max_price:
        try:
            if min_price:
                min_price = int(min_price)
                products = products.filter(price__gte=min_price)
            if max_price:
                max_price = int(max_price)
                products = products.filter(price__lte=max_price)
        except ValueError:
            pass  # If conversion fails, just ignore the filter

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product = single_product).exists()
    except Exception as e:
        raise e

    context = {
        'single_product': single_product,
        'in_cart':in_cart,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)
