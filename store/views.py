# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Product, Cart, CartItem
from users.models import User
from games.models import Game
from teams.models import Team
from .forms import AddToCartForm, ChangeQuantityForm, SubmitOrderForm, SubscriptionForm, AddressForm
from users.forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages, auth
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
import stripe
import arrow
import json

stripe.api_key = settings.STRIPE_SECRET


# Create your views here.
def store_front(request):
    user = request.user
    products = Product.objects.all()
    teams = Team.objects.all().order_by('geographic_name')

    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user, status='Pending')
            return render(request, 'store.html', {'products': products, 'cart': cart})

        except Cart.DoesNotExist:
            pass

    return render(request, 'store.html', {'products': products, 'teams': teams})


def store_team(request, team_name):
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())

    return render(request, 'store_team.html', {'team': team})


def add_product(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    items = product.items.all()
    sizes = []

    for item in items:
        sizes.append((item.size, item.size))

    if request.method == 'POST':
        form = AddToCartForm(request.POST, item_options=sizes)

        if form.is_valid():
            size = request.POST.get('size')
            quantity = int(request.POST.get('quantity'))
            cost = product.price * quantity

            for item in items:
                if item.size == size and item.stock >= quantity:

                    try:
                        cart = Cart.objects.get(user=user, status='Pending')
                        cart.cost += cost
                        if cart.cost >= 50:
                            cart.postage = 0
                        else:
                            cart.postage = Decimal(4.99)
                        cart.total = cart.postage + cart.cost
                        cart.save()
                        try:
                            new_item = CartItem.objects.get(cart=cart, item=item)
                            new_item.quantity += quantity
                            new_item.save()
                        except CartItem.DoesNotExist:
                            new_item = CartItem(cart=cart, item=item, quantity=quantity)
                            new_item.save()
                    except Cart.DoesNotExist:
                        cart = Cart(user=user, status='Pending', cost=cost)
                        if cart.cost >= 50:
                            cart.postage = 0
                        else:
                            cart.postage = Decimal(4.99)
                        cart.total = cart.postage + cart.cost
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

                elif item.stock < quantity:
                    messages.error(request, 'Sorry, not enough items in stock to complete that order.')
        else:
            messages.error(request, 'Sorry, we were unable to add that item. Please try again.')

    else:
        form = AddToCartForm(item_options=sizes)
        form.order_fields(['size', 'quantity'])

    args = {'form': form, 'product': product, 'items': items, 'button_text': 'Add to Basket'}
    args.update(csrf(request))
    return render(request, 'product.html', args)


@login_required(login_url='/login/')
def shopping_cart(request):
    user = request.user
    cart = Cart.objects.get(user=user, status='Pending')
    return render(request, 'cart.html', {'cart': cart})


@login_required(login_url='/login/')
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

            if cart.cost >= 50:
                cart.postage = 0
            else:
                cart.postage = Decimal(4.99)

            cart.total = cart.postage + cart.cost

            cart.save()

            return redirect(reverse('shopping_cart'))

        else:
            messages.error(request, 'Sorry, we were unable to change your order. Please try again.')

    else:
        form = ChangeQuantityForm()

    args = {'form': form, 'item': item, 'button_text': 'Change'}
    args.update(csrf(request))

    return render(request, 'change_quantity.html', args)


@login_required(login_url='/login/')
def remove_product(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)

    if item:
        quantity = item.quantity
        price = item.item.product.price
        total = quantity * price

        item.item.stock += quantity
        item.item.save()

        cart = item.cart

        cart.cost -= total

        if cart.cost >= 50:
            cart.postage = 0
        else:
            cart.postage = Decimal(4.99)

        cart.total = cart.postage + cart.cost

        cart.save()
        item.delete()

        if cart.items.count() == 0:
            cart.delete()
            return redirect(reverse('store_front'))

        else:
            return redirect(reverse('shopping_cart'))

    return render(request, 'cart.html')


@login_required(login_url='/login/')
def submit_order(request, order_id):
    user = request.user

    data = {
        'name': user.first_name + ' ' + user.last_name,
        'address_line_1': user.address_line_1,
        'address_line_2': user.address_line_2,
        'city': user.city,
        'postcode': user.postcode,
        'country': user.country,
    }

    order = get_object_or_404(Cart, pk=order_id)

    if request.method == 'POST':
        address_form = AddressForm(request.POST)
        card_form = SubmitOrderForm(request.POST)

        if address_form.is_valid() and card_form.is_valid():

            order.delivery_name = request.POST.get('name')
            order.address_line_1 = request.POST.get('address_line_1')
            order.address_line_2 = request.POST.get('address_line_2')
            order.city = request.POST.get('city')
            order.postcode = request.POST.get('postcode')
            order.country = request.POST.get('country')
            order.save()

            if request.POST.get('set_address_as_default'):
                user.address_line_1 = order.address_line_1
                user.address_line_2 = order.address_line_2
                user.city = order.city
                user.postcode = order.postcode
                user.country = order.country
                user.save()

            try:
                invoice = stripe.Charge.create(
                    amount=int(order.total * 100),
                    currency='GBP',
                    description=order.user.username,
                    card=card_form.cleaned_data['stripe_id'],
                )

                if invoice.paid:
                    order.stripe_id = request.POST.get('stripe_id')
                    order.status = 'Received'
                    order.date = datetime.now()
                    order.save()
                    return redirect(reverse('order_confirmation'))

                else:
                    messages.error(request, "Sorry, we were unable to take your payment. Please try again.")

            except stripe.error.CardError, e:
                messages.error(request, 'Sorry, your card was declined. Please try again with a different card.')

    else:
        address_form = AddressForm(initial=data)
        card_form = SubmitOrderForm()

    args = {'address_form': address_form, 'card_form': card_form, 'order': order,
            'order_id': order_id, 'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'checkout.html', args)


@login_required(login_url='/login/')
def order_confirmation(request):
    return render(request, 'confirmation.html')


@login_required(login_url='/login/')
def order_list(request):
    user = request.user
    orders = Cart.objects.filter(user=user, status='Received').order_by('-date')
    return render(request, 'orders.html', {'orders': orders})


@login_required(login_url='/login/')
def order_details(request, order_id):
    order = get_object_or_404(Cart, pk=order_id)
    items = CartItem.objects.filter(cart_id=order_id)
    return render(request, 'order_detail.html', {'order': order, 'items': items})


def premium_home(request):
    schedule = Game.objects.filter(game_status='Scheduled').filter(is_premium=True)
    return render(request, 'premium.html', {'schedule': schedule})


@login_required(login_url='/login/')
def upgrade_account(request):
    user = request.user

    if user.subscription_ends and user.subscription_ends >= timezone.now():
        return redirect(reverse('premium_home'))

    else:

        if request.method == 'POST':
            form = SubscriptionForm(request.POST)
            form.order_fields(['name_on_card', 'billing_cycle', 'card_number', 'cvv',
                              'expiry_month', 'expiry_year', 'stripe_id'])

            billing_cycle = request.POST.get('billing_cycle')

            if billing_cycle == 'BIBL_MONTHLY':
                months = 1
            elif billing_cycle == 'BIBL_THREE':
                months = 3
            elif billing_cycle == 'BIBL_SIX':
                months = 6
            elif billing_cycle == 'BIBL_YEARLY':
                months = 12

            if form.is_valid():
                try:
                    customer = stripe.Customer.create(
                        plan=billing_cycle,
                        description=user.username,
                        card=form.cleaned_data['stripe_id'],
                    )

                    if customer:
                        user.stripe_id = customer.id
                        user.subscription_ends = arrow.now().replace(months=+months).datetime
                        user.subscription_plan = billing_cycle
                        user.subscription_renews = True
                        user.save()
                        messages.success(request, 'Upgrade successful. You are now a Premium user.')
                        return redirect(reverse('premium_home'))

                    else:
                        messages.error(request, "Sorry, we were unable to take your payment. Please try again.")

                except stripe.error.CardError, e:
                    messages.error(request, 'Sorry, your card was declined. Please try again with a different card.')

        else:
            form = SubscriptionForm()
            form.order_fields(['name_on_card', 'billing_cycle', 'card_number', 'cvv',
                              'expiry_month', 'expiry_year', 'stripe_id'])

        args = {'form': form, 'publishable': settings.STRIPE_PUBLISHABLE}
        args.update(csrf(request))

        return render(request, 'upgrade.html', args)


@login_required(login_url='/login/')
def cancel_subscription(request):

    user = request.user

    try:
        customer = stripe.Customer.retrieve(user.stripe_id)
        customer.cancel_subscription(at_period_end=True)
        user.subscription_renews = False
        user.save()
        messages.success(request, 'Your subscription has been cancelled.'
                                  'You will still have access until the end of your current payment period.')
        return redirect(reverse('user_profile'))

    except Exception:
        messages.error(request, 'Sorry, we were unable to process cancellation. Please try again.')

    return redirect(reverse('user_profile'))


@csrf_exempt
def subscription_renewal(request):
    renewal_json = json.loads(request.body)

    try:
        # Commented out while testing.
        # event = stripe.Event.retrieve(renewal_json['object']['id'])
        subscriber = renewal_json['object']['customer']
        paid = renewal_json['object']['paid']
        plan = renewal_json['object']['lines']['data'][0]['plan']['id']

        if plan == 'BIBL_MONTHLY':
            months = 1
        elif plan == 'BIBL_THREE':
            months = 3
        elif plan == 'BIBL_SIX':
            months = 6
        elif plan == 'BIBL_YEARLY':
            months = 12

        user = User.objects.get(stripe_id=subscriber)

        if user and paid:
            user.subscription_ends = arrow.now().replace(months=+months).datetime
            user.save()

    except stripe.InvalidRequestError, e:
        return HttpResponse(status=404)
    return HttpResponse(status=200)


def register_premium(request):

    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        subscription_form = SubscriptionForm(request.POST)
        subscription_form.order_fields(['billing_cycle', 'card_number', 'cvv',
                                        'expiry_month', 'expiry_year', 'stripe_id'])

        billing_cycle = request.POST.get('billing_cycle')

        if billing_cycle == 'BIBL_MONTHLY':
            months = 1
        elif billing_cycle == 'BIBL_THREE':
            months = 3
        elif billing_cycle == 'BIBL_SIX':
            months = 6
        elif billing_cycle == 'BIBL_YEARLY':
            months = 12

        if registration_form.is_valid() and subscription_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password1'))

            if user:
                try:
                    customer = stripe.Customer.create(
                        plan=billing_cycle,
                        description=user.username,
                        card=subscription_form.cleaned_data['stripe_id'],
                    )

                    if customer:
                        user.stripe_id = customer.id
                        user.subscription_ends = arrow.now().replace(months=+months).datetime
                        user.subscription_plan = billing_cycle
                        user.subscription_renews = True
                        user.save()
                        messages.success(request, 'Your premium registration was successful!')
                        auth.login(request, user)
                        return redirect(reverse('user_profile'))

                    else:
                        messages.error(request, 'Sorry, we were unable to take your payment. '
                                                'Standard account created.')

                except stripe.error.CardError, e:
                    messages.error(request, 'Sorry, your card was declined. '
                                            'Standard account created.')

            else:
                messages.error(request, 'Sorry, we were unable to register your account. '
                                        'Please try again.')

    else:
        registration_form = RegistrationForm()
        subscription_form = SubscriptionForm()
        subscription_form.order_fields(['billing_cycle', 'card_number', 'cvv',
                                        'expiry_month', 'expiry_year', 'stripe_id'])

    args = {'registration_form': registration_form, 'subscription_form': subscription_form,
            'publishable': settings.STRIPE_PUBLISHABLE}
    args.update(csrf(request))

    return render(request, 'register_premium.html', args)
