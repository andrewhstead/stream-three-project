# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Product, Cart, CartItem
from .forms import AddToCartForm, ChangeQuantityForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.contrib import messages


# Create your views here.
def store_front(request):
    products = Product.objects.all()
    return render(request, 'store.html', {'products': products})


def add_product(request, product_id):
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
            messages.error(request, 'Sorry, we were unable to add that item. Please try again.')

    else:
        form = AddToCartForm()

    args = {'form': form, 'product': product, 'items': items, 'button_text': 'Add to Basket'}
    args.update(csrf(request))
    return render(request, 'product.html', args)


@login_required
def shopping_cart(request):
    user = request.user
    cart = Cart.objects.get(user=user)
    return render(request, 'cart.html', {'cart': cart})


@login_required
def change_product(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)

    if request.method == 'POST':
        form = ChangeQuantityForm(request.POST)

        if form.is_valid():
            old_quantity = item.quantity
            new_quantity = int(request.POST.get('quantity'))
            item.quantity = new_quantity
            item.save()

            cart = item.cart
            price = item.item.product.price
            item_change = new_quantity - old_quantity
            price_change = price * item_change

            item.item.stock -= item_change
            item.item.save()

            cart.cost += price_change
            cart.save()

            return redirect(reverse('shopping_cart'))

        else:
            messages.error(request, 'Sorry, we were unable to change your order. Please try again.')

    else:
        form = ChangeQuantityForm()

    args = {'form': form, 'item': item, 'button_text': 'Change'}
    args.update(csrf(request))

    return render(request, 'change_quantity.html', args)


@login_required
def remove_product(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)

    if item:
        quantity = item.quantity
        price = item.item.product.price
        total = quantity * price

        item.item.stock += quantity
        item.item.save(

        )
        cart = item.cart

        cart.cost -= total
        cart.save()
        item.delete()

        return redirect(reverse('shopping_cart'))

    return render(request, 'cart.html')
