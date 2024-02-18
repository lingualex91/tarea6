"""
This module defines the Customer class and its associated methods.

The Customer class is responsible for managing customer information, including creating, deleting,
modifying, and displaying customer details. It interacts with a JSON file to persist customer data.
"""

import json

class Customer:
    """
    Represents a customer, managing their information such as ID, name, email, and phone number.
    """
    def __init__(self, customer_id, name, email, phone):
        """
        Initializes a new Customer instance.

        Args:
            customer_id (str): Unique identifier for the customer.
            name (str): Name of the customer.
            email (str): Email address of the customer.
            phone (str): Phone number of the customer.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    @staticmethod
    def load_customers():
        """Load the list of customers from the JSON file."""
        try:
            with open('customers.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    @staticmethod
    def save_customers(customers):
        """Save the list of customers to the JSON file."""
        with open('customers.json', 'w', encoding='utf-8') as file:
            json.dump(customers, file, indent=4)

    def create_customer(self):
        """Create a new customer and add it to the JSON file."""
        customers = self.load_customers()
        customer = {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }
        if any(cust['customer_id'] == self.customer_id for cust in customers):
            print(f"Customer with ID {self.customer_id} already exists.")
            return
        customers.append(customer)
        self.save_customers(customers)
        print(f"Customer {self.name} created successfully.")

    @staticmethod
    def delete_customer(customer_id):
        """Delete a customer from the JSON file."""
        customers = Customer.load_customers()
        customers = [customer for customer in customers if customer['customer_id'] != customer_id]
        Customer.save_customers(customers)
        print(f"Customer {customer_id} deleted successfully.")

    @staticmethod
    def display_customer_info(customer_id):
        """Display information for a specific customer."""
        customers = Customer.load_customers()
        for customer in customers:
            if customer['customer_id'] == customer_id:
                print(json.dumps(customer, indent=4))
                return
        print("Customer not found.")

    @staticmethod
    def modify_customer_info(customer_id, **kwargs):
        """Modify information for a specific customer."""
        customers = Customer.load_customers()
        for customer in customers:
            if customer['customer_id'] == customer_id:
                for key, value in kwargs.items():
                    if key in customer:
                        customer[key] = value
                Customer.save_customers(customers)
                print(f"Customer {customer_id} updated successfully.")
                return
        print("Customer not found.")
