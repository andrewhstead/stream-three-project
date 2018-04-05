# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Product, Item, Cart
from .forms import AddToCartForm
from users.forms import LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.context_processors import csrf


# Create your views here.
def store_front(request):
    products = Product.objects.all()
    return render(request, 'store.html', {'products': products})


def product_detail(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    items = product.items.all()
    cart = Cart.objects.get(user=user)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            size = request.POST.get('size')
            quantity = int(request.POST.get('quantity'))
            cost = int(product.price * quantity)

            for item in items:
                if item.size == size:
                    to_add = item

                    if cart:
                        cart.cost += cost
                        cart.items.add(to_add)
                        cart.save()

                    else:
                        cart = Cart(user=user)
                        cart.save()
                        cart.cost += cost
                        cart.items.add(to_add)
                        cart.save()

                    to_add.stock -= quantity
                    to_add.save()
                    return redirect(reverse('shopping_cart'))

    else:
        form = AddToCartForm()

    args = {'form': form, 'product': product, 'items': items, 'button_text': 'Add to Basket'}
    args.update(csrf(request))
    return render(request, 'product.html', args)


def shopping_cart(request):
    return render(request, 'cart.html')
