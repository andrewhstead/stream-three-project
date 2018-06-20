# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Product, Cart, CartItem
from users.models import User
from games.models import Game
from teams.models import Team
from .forms import AddToCartForm, ChangeQuantityForm, SubmitOrderForm, SubscriptionForm, AddressForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
# The main store page, which displays all available items.
def store_front(request):
    user = request.user
    all_products = Product.objects.all().order_by('-team').order_by('-description')
    teams = Team.objects.all().order_by('geographic_name')

    # Pagination is used to show six products at a time.
    view_products = Paginator(all_products, 6)

    page = request.GET.get('page')

    if page:
        current_page = int(page)
    else:
        current_page = 1

    page_count = view_products.num_pages

    try:
        products = view_products.page(page)
    except EmptyPage:
        products = view_products.page(page_count)
    except PageNotAnInteger:
        products = view_products.page(1)

    # If a user is authenticated, check whether or not they already have a pending shopping cart.
    # If they do, it should be made available to be linked from the template.
    # If not, the variable 'cart' is given the value 'False'.
    if user.is_authenticated:
        try:
            cart = Cart.objects.get(user=user, status='Pending')
            return render(request, 'store.html', {'products': products, 'cart': cart, "current_page": current_page})

        except Cart.DoesNotExist:
            cart = False
            return render(request, 'store.html', {'products': products, 'teams': teams, "current_page": current_page,
                                                  'cart': cart})

    else:
        cart = False
        return render(request, 'store.html', {'products': products, 'teams': teams, "current_page": current_page,
                                              'cart': cart})


# Individual store pages for each time, showing at a glance all the products relating to that team.
def store_team(request, team_name):
    team = get_object_or_404(Team, geographic_name=team_name.capitalize())

    return render(request, 'store_team.html', {'team': team})


# An individual product, giving the user more details and the option to add to their cart.
def store_product(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)
    items = product.items.all()
    sizes = []
    out_of_stock = []

    # Create a list of sizes which are available for the product in question.
    for item in items:
        if item.stock > 0:
            sizes.append((item.size, item.size))
        elif item.stock == 0:
            out_of_stock.append(item.size)

    if request.method == 'POST':
        form = AddToCartForm(request.POST, item_options=sizes)

        if form.is_valid():
            size = request.POST.get('size')
            quantity = int(request.POST.get('quantity'))
            cost = product.price * quantity

            for item in items:
                # First select the right size item and check that there is enough stock for the order.
                if item.size == size and item.stock >= quantity:

                    # If the user has a pending cart, use that cart.
                    try:
                        cart = Cart.objects.get(user=user, status='Pending')
                        # Give free postage on order over £50, otherwise add a £4.99 postage charge.
                        cart.cost += cost
                        if cart.cost >= 50:
                            cart.postage = 0
                        else:
                            cart.postage = Decimal(4.99)
                        cart.total = cart.postage + cart.cost
                        cart.save()
                        # If the item being added is already in the cart, change the quantity.
                        try:
                            new_item = CartItem.objects.get(cart=cart, item=item)
                            new_item.quantity += quantity
                            new_item.save()
                        # If the item is not in the cart, add it.
                        except CartItem.DoesNotExist:
                            new_item = CartItem(cart=cart, item=item, quantity=quantity)
                            new_item.save()
                    # If the user has no cart, create one.
                    except Cart.DoesNotExist:
                        cart = Cart(user=user, status='Pending', cost=cost)
                        # Give free postage on order over £50, otherwise add a £4.99 postage charge.
                        if cart.cost >= 50:
                            cart.postage = 0
                        else:
                            cart.postage = Decimal(4.99)
                        cart.total = cart.postage + cart.cost
                        cart.save()
                        # Add the item to the newly created cart.
                        new_item = CartItem(cart=cart, item=item, quantity=quantity)
                        new_item.save()

                    # Adjust the stock levels to reflect the quantity in the user's cart, which are deemed to be
                    # unavailable for others to buy unless they are removed from the cart.
                    item.stock -= quantity
                    item.save()
                    return redirect(reverse('shopping_cart'))

                # If more are ordered than available stock, do not add them. Display an error instead.
                elif item.stock < quantity:
                    messages.error(request, 'Sorry, not enough items in stock to complete that order.')
        else:
            messages.error(request, 'Sorry, we were unable to add that item. Please try again.')

    # Default for GET request with available size options passed to the form.
    else:
        form = AddToCartForm(item_options=sizes)
        form.order_fields(['size', 'quantity'])

    args = {'form': form, 'product': product, 'items': items,
            'button_text': 'Add to Basket', 'out_of_stock': out_of_stock}
    args.update(csrf(request))
    return render(request, 'product.html', args)


# Display the user's current pending shopping cart.
@login_required(login_url='/login/')
def shopping_cart(request):
    user = request.user
    cart = Cart.objects.get(user=user, status='Pending')
    return render(request, 'cart.html', {'cart': cart})


# Change the quantity of a particular item in the user's cart.
@login_required(login_url='/login/')
def change_product(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)
    user = request.user
    cart = Cart.objects.get(user=user, status='Pending')

    if request.method == 'POST':
        form = ChangeQuantityForm(request.POST)

        if form.is_valid():
            # Get old and new quantities ready to change the total cost.
            old_quantity = item.quantity
            new_quantity = int(request.POST.get('quantity'))
            # Set the new quantity and save.
            item.quantity = new_quantity
            item.save()

            # Check the price of the product and work out the difference between the old and new quantity.
            cart = item.cart
            price = item.item.product.price
            item_change = new_quantity - old_quantity
            price_change = price * item_change

            # Change the stock level to reflect the new quantity in the cart.
            item.item.stock -= item_change
            item.item.save()

            # Change the total cost of the items in the cart accordingly
            # and check again whether the user qualifies for free postage.
            cart.cost += price_change
            if cart.cost >= 50:
                cart.postage = 0
            else:
                cart.postage = Decimal(4.99)

            # Set the order total.
            cart.total = cart.postage + cart.cost

            cart.save()

            return redirect(reverse('shopping_cart'))

        else:
            messages.error(request, 'Sorry, we were unable to change your order. Please try again.')

    else:
        form = ChangeQuantityForm()

    args = {'form': form, 'item': item, 'cart': cart, 'button_text': 'Change'}
    args.update(csrf(request))

    return render(request, 'change_quantity.html', args)


# Remove an item from the user's shopping cart.
@login_required(login_url='/login/')
def remove_product(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id)

    if item:
        # Get the quantity and price of the item so that the order cost can be changed accordingly.
        quantity = item.quantity
        price = item.item.product.price
        total = quantity * price

        # Return the removed items into stock for other users to buy.
        item.item.stock += quantity
        item.item.save()

        cart = item.cart

        # Recalculate the cost of the items and check again whether the user
        # still qualifies for free postage.
        cart.cost -= total
        if cart.cost >= 50:
            cart.postage = 0
        else:
            cart.postage = Decimal(4.99)

        # Set the new total cost of the order, and delete the item from the cart.
        cart.total = cart.postage + cart.cost
        cart.save()
        item.delete()

        # If the removal of the item leaves the cart empty, delete the cart.
        if cart.items.count() == 0:
            cart.delete()
            return redirect(reverse('store_front'))

        else:
            return redirect(reverse('shopping_cart'))

    return render(request, 'cart.html')


# Submit the user's order from the store.
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
            # Add the address details from the Address form to the cart details.
            order.delivery_name = request.POST.get('name')
            order.address_line_1 = request.POST.get('address_line_1')
            order.address_line_2 = request.POST.get('address_line_2')
            order.city = request.POST.get('city')
            order.postcode = request.POST.get('postcode')
            order.country = request.POST.get('country')
            order.save()

            if request.POST.get('set_address_as_default'):
                # If the user has ticked to set the address as default, add it to their profile.
                user.address_line_1 = order.address_line_1
                user.address_line_2 = order.address_line_2
                user.city = order.city
                user.postcode = order.postcode
                user.country = order.country
                user.save()

            # Submit payment details to Stripe.
            try:
                invoice = stripe.Charge.create(
                    amount=int(order.total * 100),
                    currency='GBP',
                    description=order.user.username,
                    card=card_form.cleaned_data['stripe_id'],
                )

                if invoice.paid:
                    # If the payment is successful, set the order status to 'Received' and add the current date.
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


# Show the user a confirmation message.
@login_required(login_url='/login/')
def order_confirmation(request):
    return render(request, 'confirmation.html')


# Show a list of all the user's past received or dispatched orders.
@login_required(login_url='/login/')
def order_list(request):
    user = request.user
    orders = Cart.objects.filter(user=user, status__in=['Received', 'Dispatched']).order_by('-date')
    return render(request, 'orders.html', {'orders': orders})


# Show the details of a particular order.
@login_required(login_url='/login/')
def order_details(request, order_id):
    order = get_object_or_404(Cart, pk=order_id)
    items = CartItem.objects.filter(cart_id=order_id)
    return render(request, 'order_detail.html', {'order': order, 'items': items})


# Show the premium content page.
def premium_home(request):
    schedule = Game.objects.filter(game_status='Scheduled').filter(is_premium=True)\
        .values('game_date', 'game_time', 'home_team', 'away_team')
    live_games = Game.objects.filter(game_status='In Progress').filter(is_premium=True)
    return render(request, 'premium.html', {'schedule': schedule, 'live_games': live_games})


# Upgrade the user's account from standard to premium.
@login_required(login_url='/login/')
def upgrade_account(request):
    user = request.user

    # If the user has an active subscription, show them the premium page instead of the upgrade form.
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
                    # Submit the payment details to Stripe.
                    customer = stripe.Customer.create(
                        plan=billing_cycle,
                        description=user.username,
                        card=form.cleaned_data['stripe_id'],
                    )

                    if customer:
                        # If the payment goes through, update the user's subscription details.
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


# Cancel the user's subscription.
@login_required(login_url='/login/')
def cancel_subscription(request):

    user = request.user

    try:
        # Send the cancellation to Stripe and update the user's subscription details.
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


# Webhook for processing renewal data from Stripe.
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


# Register a new user and set their account up as premium.
def register_premium(request):

    if request.method == 'POST':
        # Use both the standard user registration form and the subscription form.
        registration_form = RegistrationForm(request.POST)
        subscription_form = SubscriptionForm(request.POST)
        subscription_form.order_fields(['name_on_card', 'billing_cycle', 'card_number', 'cvv',
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
            # First create the user's account.
            registration_form.save()
            user = auth.authenticate(username=request.POST.get('username'),
                                     password=request.POST.get('password1'))

            if user:
                try:
                    # Once the user exists, send their payment details to Stripe.
                    customer = stripe.Customer.create(
                        plan=billing_cycle,
                        description=user.username,
                        card=subscription_form.cleaned_data['stripe_id'],
                    )

                    if customer:
                        # If the payment goes through, set the user's subscription details.
                        user.stripe_id = customer.id
                        user.subscription_ends = arrow.now().replace(months=+months).datetime
                        user.subscription_plan = billing_cycle
                        user.subscription_renews = True
                        user.save()
                        messages.success(request, 'Your premium registration was successful!')
                        auth.login(request, user)
                        return redirect(reverse('premium_home'))

                    else:
                        # If the payment fails, inform the user that they only have a standard account and must try
                        # again to upgrade.
                        messages.error(request, 'Sorry, we were unable to take your payment. '
                                                'Standard account created, please try to upgrade.')

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
