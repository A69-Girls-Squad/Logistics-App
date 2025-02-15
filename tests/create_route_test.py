import unittest
from unittest.mock import Mock

from commands.create_route import CreateRouteCommand


def _create_fake_params(
        *,
        name='MyMan',
        brand='TrashyOverpricedBrand',
        price='10.99',
        gender='Men',
        milliliters='1000',
        usage_type='Every_Day'):
    return [name, brand, price, gender, milliliters, usage_type]


def _create_mock(*, product_exists_return_value: bool):
    fake_data = Mock()

    def product_exists(name):
        return product_exists_return_value

    def create_shampoo(name, brand, price, gender, usage_type, milliliters):
        product = Mock()
        product.name = name
        fake_data.products.append(product)

        return product

    fake_data.products = []
    fake_data.product_exists = product_exists
    fake_data.create_shampoo = create_shampoo

    return fake_data


class CreateRouteCommandTest_Should(unittest.TestCase):
    def test_initializer_raisesError_tooFewParamsCount(self):
        with self.assertRaises(ValueError):
            cmd = CreateRouteCommand(['a'] * 5, Mock())

    def test_initializer_raisesError_tooManyParamsCount(self):
        with self.assertRaises(ValueError):
            cmd = CreateRouteCommand(['a'] * 7, Mock())

    def test_initializer_passes_validParamsCount(self):
        CreateRouteCommand(['a'] * 6, Mock())

    def test_execute_createsShampoo_validParams(self):
        # Arrange
        fake_params = _create_fake_params()
        cmd = CreateShampooCommand(
            fake_params,
            _create_mock(product_exists_return_value=False))

        # Act
        output = cmd.execute()

        # Assert
        self.assertEqual(
            f'Shampoo with name {fake_params[0]} was created!', output)

    def test_execute_raisesError_productExists(self):
        # Arrange
        cmd = CreateShampooCommand(
            _create_fake_params(),
            _create_mock(product_exists_return_value=True))

        # Act & Assert
        with self.assertRaises(ValueError):
            cmd.execute()

    def test_execute_raisesError_invalidPrice(self):
        # Arrange
        cmd = CreateShampooCommand(
            _create_fake_params(price='not a float'),
            _create_mock(product_exists_return_value=False))

        # Act & Assert
        with self.assertRaises(ValueError):
            cmd.execute()

    def test_execute_raisesError_invalidGender(self):
        # Arrange
        cmd = CreateShampooCommand(
            _create_fake_params(gender='not a gender'),
            _create_mock(product_exists_return_value=False))

        # Act & Assert
        with self.assertRaises(ValueError):
            cmd.execute()

    def test_execute_raisesError_invalidMilliliters(self):
        # Arrange
        cmd = CreateShampooCommand(
            _create_fake_params(milliliters='not an int'),
            _create_mock(product_exists_return_value=False))

        # Act & Assert
        with self.assertRaises(ValueError):
            cmd.execute()

    def test_execute_raisesError_invalidUsageType(self):
        # Arrange
        cmd = CreateShampooCommand(
            _create_fake_params(usage_type='not a usage_type'),
            _create_mock(product_exists_return_value=False))

        # Act & Assert
        with self.assertRaises(ValueError):
            cmd.execute()
