import unittest
from decimal import Decimal

from cart import Cart, CartItem
from product import ProductStore


class CartTest(unittest.TestCase):

    def test_get_total_is_decimal(self):
        '''Cart.get_total() returns a Decimal.'''
        cart = Cart()
        self.assertTrue(type(cart.get_total()) is Decimal)

    def test_add_single_item(self):
        '''Cart.add() a single item is successful.'''
        cart = Cart()
        cart.add('apple')
        self.assertEqual(len(cart), 1)

    def test_add_item_is_cartitem(self):
        '''Cart contains a single CartItem after cart.add().'''
        cart = Cart()
        cart.add('apple')
        self.assertTrue(type(cart[0]) is CartItem)

    def test_add_two_items(self):
        '''Adding more than one item increases cart length.'''
        cart = Cart()
        cart.add('apple')
        cart.add('orange')
        self.assertEqual(len(cart), 2)

    def test_add_two_same_item(self):
        '''Adding more than one of the same item does not create duplicate
        CartItems.'''
        cart = Cart()
        cart.add('apple')
        cart.add('apple')
        self.assertEqual(len(cart), 1)

    def test_add_two_same_item_increases_quantity(self):
        '''Adding an item that is already in the cart increases its
        quantity.'''
        cart = Cart()
        cart.add('apple')
        cart.add('apple')
        cartitem = cart.get_item('apple')
        self.assertEqual(cartitem.quantity, 2)

    def test_add_with_no_quantity(self):
        '''Adding an item without defining a quantity creates an item with a
        quantity of 1.'''
        cart = Cart()
        cart.add('apple')
        self.assertEqual(cart.get_item('apple').quantity, 1)

    def test_add_with_quantity(self):
        '''Adding an item with a quantity creates cart item with appropriate
        quantity.'''
        cart = Cart()
        cart.add('apple', 3)
        self.assertEqual(cart.get_item('apple').quantity, 3)

    def test_add_with_quantity_to_existing_item(self):
        '''Adding an item with a quantity increases the quantity of an
        existing item.'''
        cart = Cart()
        cart.add('apple', 2)
        cart.add('apple', 3)
        self.assertEqual(cart.get_item('apple').quantity, 5)

    def test_get_item(self):
        '''cart.get_item() returns expected CartItem.'''
        cart = Cart()
        cart.add('apple')
        cart.add('orange')
        returned_cart_item = cart.get_item('apple')
        self.assertTrue(type(returned_cart_item) is CartItem)
        self.assertEqual(returned_cart_item.product, 'apple')

    def test_get_item_not_in_cart(self):
        '''Attempt to get item with no corresponding CartItem returns None.'''
        cart = Cart()
        self.assertEqual(cart.get_item('apple'), None)


class CartItemTest(unittest.TestCase):

    def _create_product_store(self):
        '''Helper method to create populated ProductStore.'''
        products = [
            ('apple', Decimal('0.15')),
            ('ice cream', Decimal('3.49')),
            ('strawberries', Decimal('2.00')),
            ('snickers bar', Decimal('0.70')),
        ]
        return ProductStore(products)

    def test_get_line_total_is_decimal(self):
        '''Cart.get_line_total() returns a Decimal.'''
        product_store = self._create_product_store()
        cartitem = CartItem('apple')
        self.assertTrue(type(cartitem.get_line_total(product_store) is Decimal))

    def test_quantity_on_create_with_no_value(self):
        '''Creating a CartItem without passing a quantity initialises quantity
        with 1.'''
        cartitem = CartItem('apple')
        self.assertEqual(cartitem.quantity, 1)

    def test_quantity_on_create_with_value(self):
        '''Creating a CartItem with a passed quantity initialises with that
        quantity.'''
        cartitem = CartItem('apple', 3)
        self.assertEqual(cartitem.quantity, 3)

    def test_get_line_total(self):
        '''Cart.get_line_total() returns the correct price for product.'''
        product_store = self._create_product_store()
        cartitem = CartItem('apple')
        self.assertEqual(cartitem.get_line_total(product_store), Decimal('0.15'))

    def test_get_line_total_multiple_quantity(self):
        '''get_line_total returns the correct price for item with multiple
        quantity.'''
        product_store = self._create_product_store()
        cartitem = CartItem('apple', 3)
        self.assertEqual(cartitem.get_line_total(product_store), Decimal('0.45'))


class ProductStoreTest(unittest.TestCase):

    def test_get_product_price(self):
        '''ProductStore returns corresponding price for product.'''
        products = [
            ('apple', Decimal('0.15')),
            ('ice cream', Decimal('3.49')),
            ('strawberries', Decimal('2.00')),
            ('snickers bar', Decimal('0.70')),
        ]
        product_store = ProductStore(products)
        self.assertEqual(product_store.get_product_price('strawberries'), Decimal('2.00'))

    def test_get_product_price_no_product(self):
        '''ProductStore returns None when no product matches.'''
        products = [
            ('apple', Decimal('0.15')),
            ('ice cream', Decimal('3.49')),
            ('strawberries', Decimal('2.00')),
            ('snickers bar', Decimal('0.70')),
        ]
        product_store = ProductStore(products)
        self.assertTrue(product_store.get_product_price('bike') is None)
