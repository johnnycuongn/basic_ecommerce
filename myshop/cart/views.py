from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart
from .forms import CartAddProductForm
from shop.models import Product


def cart_detail(request: HttpRequest):
  cart = Cart(request)
  for item in cart:
    item["update_quantity_form"] = CartAddProductForm(initial={
      'quantity': item['quantity'],
      'override': True
    })

  return render(request, 'cart/detail.html', {
    'cart': cart
  })

@require_POST
def cart_add(request: HttpRequest, product_id):
  cart = Cart(request=request)
  product = get_object_or_404(Product, id=product_id)

  form = CartAddProductForm(request.POST)
  if form.is_valid():
    cd = form.cleaned_data
    cart.add(
      product=product,
      quantity=cd['quantity'],
      override_quantity=cd['override']
    )
  
  return redirect('cart:cart_detail')

@require_POST
def cart_remove(request: HttpRequest, product_id):
  cart = Cart(request=request)
  product = get_object_or_404(Product, id=product_id)
  cart.remove(product=product)

  return redirect('cart:cart_detail')