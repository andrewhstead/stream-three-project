# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from .views import store_front, store_team, add_product, shopping_cart, change_product,\
    remove_product, submit_order, order_confirmation, order_list, order_details,\
    premium_home, upgrade_account, cancel_subscription, subscription_renewal, register_premium
from django.core.urlresolvers import resolve


class StoreFrontTest(TestCase):
    def test_store_front_resolves(self):
        store_home = resolve('/store/')
        self.assertEqual(store_home.func, store_front)


class StoreTeamTest(TestCase):
    def test_store_team_resolves(self):
        team_store = resolve('/store/liverpool/')
        self.assertEqual(team_store.func, store_team)


class AddProductTest(TestCase):
    def test_add_product_resolves(self):
        product = resolve('/store/product/4/')
        self.assertEqual(product.func, add_product)


class ShoppingCartTest(TestCase):
    def test_shopping_cart_resolves(self):
        cart = resolve('/store/cart/')
        self.assertEqual(cart.func, shopping_cart)


class ChangeProductTest(TestCase):
    def test_change_product_resolves(self):
        change = resolve('/store/cart/edit/3/')
        self.assertEqual(change.func, change_product)


class RemoveProductTest(TestCase):
    def test_remove_product_resolves(self):
        remove_item = resolve('/store/cart/remove/3/')
        self.assertEqual(remove_item.func, remove_product)


class SubmitOrder(TestCase):
    def test_submit_order_resolves(self):
        checkout = resolve('/store/checkout/3/')
        self.assertEqual(checkout.func, submit_order)


class OrderConfirmationTest(TestCase):
    def test_order_confirmation_resolves(self):
        confirm = resolve('/store/confirmation/')
        self.assertEqual(confirm.func, order_confirmation)


class OrderListTest(TestCase):
    def test_order_list_resolves(self):
        user_orders = resolve('/store/orders/')
        self.assertEqual(user_orders.func, order_list)


class OrderDetailsTest(TestCase):
    def test_order_details_resolves(self):
        order = resolve('/store/order/6/')
        self.assertEqual(order.func, order_details)


class PremiumHomeTest(TestCase):
    def test_premium_home_resolves(self):
        premium = resolve('/premium/')
        self.assertEqual(premium.func, premium_home)


class UpgradeAccountTest(TestCase):
    def test_upgrade_account_resolves(self):
        upgrade = resolve('/premium/upgrade/')
        self.assertEqual(upgrade.func, upgrade_account)


class CancelSubscriptionTest(TestCase):
    def test_cancel_subscription_resolves(self):
        cancel = resolve('/premium/cancel/')
        self.assertEqual(cancel.func, cancel_subscription)


class SubscriptionRenewalTest(TestCase):
    def test_subscription_renewal_resolves(self):
        renewal = resolve('/premium/renewal/')
        self.assertEqual(renewal.func, subscription_renewal)


class RegisterPremiumTest(TestCase):
    def test_register_premium_resolves(self):
        premium_account = resolve('/register/premium/')
        self.assertEqual(premium_account.func, register_premium)
