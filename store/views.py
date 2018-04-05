# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Product, Cart, CartItem
from .forms import AddToCartForm
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

    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            size = request.POST.get('size')
            quantity = int(request.POST.get('quantity'))
            cost = int(product.price * quantity)

            for item in items:
                if item.size == size:

                    try:
                        cart = Cart.objects.get(user=user)
                        cart.cost += cost
                        cart.save()
                        try:
                            new_item = CartItem.objects.get(cart=cart, item=item)
                            new_item.quantity += quantity
                            new_item.save()
                        except CartItem.DoesNotExist:
                            new_item = CartItem(cart=cart, item=item, quantity=quantity)
                            new_item.save()
                    except Cart.DoesNotExist:
                        cart = Cart(user=user, cost=cost)
                        cart.save()
                        try:
                            new_item = CartItem.objects.get(cart=cart, item=item)
                            new_item.quantity += quantity
                            new_item.save()
                        except CartItem.DoesNotExist:
                            new_item = CartItem(cart=cart, item=item, quantity=quantity)
                            new_item.save()

                    item.stock -= quantity
                    item.save()
                    return redirect(reverse('shopping_cart'))

    else:
        form = AddToCartForm()

    args = {'form': form, 'product': product, 'items': items, 'button_text': 'Add to Basket'}
    args.update(csrf(request))
    return render(request, 'product.html', args)


@login_required()
def shopping_cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    return render(request, 'cart.html', {'cart': cart})
