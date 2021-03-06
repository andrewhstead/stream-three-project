# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import store_front, store_team, store_product, shopping_cart, change_product,\
    remove_product, submit_order, order_confirmation, order_list, order_details,\
    premium_home, upgrade_account, cancel_subscription, subscription_renewal, register_premium
from django.core.urlresolvers import resolve
from django.conf import settings
from .forms import ChangeQuantityForm, SubmitOrderForm, SubscriptionForm, AddToCartForm
from users.models import User

# Test the front page of the merchandise store.
class StoreFrontTest(TestCase):

    fixtures = ['teams']

    def test_store_front_resolves(self):
        store_home = resolve('/store/')
        self.assertEqual(store_home.func, store_front)

    def test_store_front_code(self):
        store_home = self.client.get('/store/')
        self.assertEqual(store_home.status_code, 200)

    def test_store_front_content(self):
        store_home = self.client.get('/store/')
        self.assertTemplateUsed(store_home, 'store.html')


# Test the individual team store pages.
class StoreTeamTest(TestCase):

    fixtures = ['teams']

    def test_store_team_resolves(self):
        team_store = resolve('/store/liverpool/')
        self.assertEqual(team_store.func, store_team)

    def test_store_team_code(self):
        team_store = self.client.get('/store/liverpool/')
        self.assertEqual(team_store.status_code, 200)

    def test_store_team_content(self):
        team_store = self.client.get('/store/liverpool/')
        self.assertTemplateUsed(team_store, 'store_team.html')


# Test the individual product view.
class StoreProductTest(TestCase):

    fixtures = ['teams', 'store', 'users']

    def test_store_product_resolves(self):
        product = resolve('/store/product/4/')
        self.assertEqual(product.func, store_product)

    def test_store_product_code(self):
        product = self.client.get('/store/product/4/')
        self.assertEqual(product.status_code, 200)

    def test_store_product_content(self):
        product = self.client.get('/store/product/4/')
        self.assertTemplateUsed(product, 'product.html')


# Test the shopping cart view.
class ShoppingCartTest(TestCase):
    def test_shopping_cart_resolves(self):
        cart = resolve('/store/cart/')
        self.assertEqual(cart.func, shopping_cart)


# Test the view for changing the quantity of an item in the cart.
class ChangeProductTest(TestCase):
    def test_change_product_resolves(self):
        change = resolve('/store/cart/edit/3/')
        self.assertEqual(change.func, change_product)


# Test the view for removing an item from the cart.
class RemoveProductTest(TestCase):
    def test_remove_product_resolves(self):
        remove_item = resolve('/store/cart/remove/3/')
        self.assertEqual(remove_item.func, remove_product)


# Test the view for submitting a user's order.
class SubmitOrder(TestCase):
    def test_submit_order_resolves(self):
        checkout = resolve('/store/checkout/3/')
        self.assertEqual(checkout.func, submit_order)


# Test the order confirmation view.
class OrderConfirmationTest(TestCase):
    def test_order_confirmation_resolves(self):
        confirm = resolve('/store/confirmation/')
        self.assertEqual(confirm.func, order_confirmation)


# Test the view showing a list of the user's past orders.
class OrderListTest(TestCase):
    def test_order_list_resolves(self):
        user_orders = resolve('/store/orders/')
        self.assertEqual(user_orders.func, order_list)


# Test the view showing the details of a particular order.
class OrderDetailsTest(TestCase):
    def test_order_details_resolves(self):
        order = resolve('/store/order/6/')
        self.assertEqual(order.func, order_details)


# Test the premium content page.
class PremiumHomeTest(TestCase):

    fixtures = ['teams']

    def test_premium_home_resolves(self):
        premium = resolve('/premium/')
        self.assertEqual(premium.func, premium_home)

    def test_premium_home_code(self):
        premium = self.client.get('/premium/')
        self.assertEqual(premium.status_code, 200)

    def test_premium_home_content(self):
        premium = self.client.get('/premium/')
        self.assertTemplateUsed(premium, 'premium.html')


# Test the view for upgrading a user's account.
class UpgradeAccountTest(TestCase):

    fixtures = ['teams']

    def setUp(self):
        super(UpgradeAccountTest, self).setUp()
        self.user = User.objects.create(username='username')
        self.user.set_password('password')
        self.user.save()

    def test_upgrade_account_resolves(self):
        upgrade = resolve('/premium/upgrade/')
        self.assertEqual(upgrade.func, upgrade_account)

    def test_upgrade_account_code(self):
        self.client.login(username='username', password='password')
        upgrade = self.client.get('/premium/upgrade/')
        self.assertEqual(upgrade.status_code, 200)

    def test_upgrade_account_content(self):
        self.client.login(username='username', password='password')
        upgrade = self.client.get('/premium/upgrade/')
        self.assertTemplateUsed(upgrade, 'upgrade.html')


# Test the view for cancelling a user's subscription.
class CancelSubscriptionTest(TestCase):
    def test_cancel_subscription_resolves(self):
        cancel = resolve('/premium/cancel/')
        self.assertEqual(cancel.func, cancel_subscription)


# Test the view for automatically renewing a user's subscription.
class SubscriptionRenewalTest(TestCase):
    def test_subscription_renewal_resolves(self):
        renewal = resolve('/premium/renewal/')
        self.assertEqual(renewal.func, subscription_renewal)


# Test the view registering a new user with a premium account.
class RegisterPremiumTest(TestCase):

    fixtures = ['teams']

    def test_register_premium_resolves(self):
        premium_account = resolve('/register/premium/')
        self.assertEqual(premium_account.func, register_premium)

    def test_register_premium_code(self):
        premium_account = self.client.get('/register/premium/')
        self.assertEqual(premium_account.status_code, 200)

    def test_register_premium_content(self):
        premium_account = self.client.get('/register/premium/')
        self.assertTemplateUsed(premium_account, 'register_premium.html')


# Test the form which adds a product to a user's cart.
class AddToCartFormTest(TestCase):
    def test_add_to_cart_form(self):
        form = AddToCartForm({
            'size': 'L',
            'quantity': '3'
        }, item_options=[('M', 'M'), ('L', 'L')])
        self.assertTrue(form.is_valid())


# Test the form which changes the quantity of an item in a user's cart.
class ChangeQuantityFormTest(TestCase):
    def test_change_quantity_form(self):
        form = ChangeQuantityForm({
            'quantity': '3'
        })
        self.assertTrue(form.is_valid())


# Test the form which sets up a premium subscription.
class SubscriptionFormTest(TestCase):
    def test_subscription_form(self):
        form = SubscriptionForm({
            'name_on_card': 'User Name',
            'billing_cycle': 'BIBL_SIX',
            'card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': 1,
            'expiry_year': 2029,
            'stripe_id': settings.STRIPE_SECRET
        })
        self.assertTrue(form.is_valid())


# Test the form which submits an order in the store.
class SubmitOrderFormTest(TestCase):
    def test_submit_order_form(self):
        form = SubmitOrderForm({
            'name_on_card': 'User Name',
            'card_number': '4242424242424242',
            'cvv': '123',
            'expiry_month': 1,
            'expiry_year': 2029,
            'stripe_id': settings.STRIPE_SECRET
        })
        self.assertTrue(form.is_valid())
