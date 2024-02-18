"""
This module contains unit tests for the Customer class.
It tests the functionality of customer creation, deletion, and validation of customer properties.
"""

import unittest
from customer import Customer

class TestCustomer(unittest.TestCase):
    """Tests for the Customer class."""

    def setUp(self):
        """
        Prepare environment for each test.
        Ensure the customer list is empty before each test.
        """
        Customer.save_customers([])

    def test_create_customer(self):
        """
        Test creating a customer and verifying it's saved correctly.
        """
        customer_id = "C001"
        name = "John Doe"
        email = "john.doe@example.com"
        phone = "123-456-7890"

        customer = Customer(customer_id, name, email, phone)
        customer.create_customer()

        customers = Customer.load_customers()
        found_customer = next((c for c in customers if c['customer_id'] == customer_id), None)

        self.assertIsNotNone(found_customer, "Customer should be in the list after creation")
        self.assertEqual(found_customer['name'], name)
        self.assertEqual(found_customer['email'], email)
        self.assertEqual(found_customer['phone'], phone)

    def test_delete_customer(self):
        """
        Test deleting a customer and verifying it's removed correctly.
        """
        customer_id = "C002"
        customer = Customer(customer_id, "Jane Doe", "jane.doe@example.com", "098-765-4321")
        customer.create_customer()

        customers_before_deletion = Customer.load_customers()
        found_customer_before = next(
                                (c for c in customers_before_deletion
                                if c['customer_id'] == customer_id),
                                None
                                )
        self.assertIsNotNone(found_customer_before, "Customer should exist before deletion")

        Customer.delete_customer(customer_id)

        customers_after_deletion = Customer.load_customers()
        found_customer_after = next(
                                   (c for c in customers_after_deletion
                                   if c['customer_id'] == customer_id), None
                                   )

        self.assertIsNone(found_customer_after, "Customer should be removed from the list")

    # Additional tests for display_customer_info and modify_customer_info can be added here.

if __name__ == '__main__':
    unittest.main()
