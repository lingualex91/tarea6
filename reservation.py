"""
This module defines the Reservation class and its associated methods.

The Reservation class is responsible for managing reservation information, including creating,
saving, loading, and canceling reservations. 
It interacts with a JSON file to persist reservation data.
"""

import json

class Reservation:
    """
    Represents a reservation, managing details such as reservation ID, customer ID,
    hotel ID, room ID, start date, and end date.
    """
    def __init__(self, reservation_details):
        """
        Initializes a new Reservation instance with details provided in a dictionary.

        Args:
            reservation_details (dict): A dictionary containing all necessary details 
            for the reservation.
        """
        self.reservation_id = reservation_details['reservation_id']
        self.customer_id = reservation_details['customer_id']
        self.hotel_id = reservation_details['hotel_id']
        self.room_id = reservation_details['room_id']
        self.start_date = reservation_details['start_date']
        self.end_date = reservation_details['end_date']

    @staticmethod
    def load_reservations():
        """Load reservations from a JSON file."""
        try:
            with open('reservations.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    @staticmethod
    def save_reservations(reservations):
        """Save reservations to a JSON file."""
        with open('reservations.json', 'w', encoding='utf-8') as file:
            json.dump(reservations, file, indent=4)

    def create_reservation(self):
        """Create and save a new reservation."""
        reservations = self.load_reservations()
        reservation = {
            "reservation_id": self.reservation_id,
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "room_id": self.room_id,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
        reservations.append(reservation)
        self.save_reservations(reservations)

    @staticmethod
    def cancel_reservation(reservation_id):
        """Cancel a reservation by removing it from the list and saving."""
        reservations = Reservation.load_reservations()
        reservations = [
                        reservation for reservation in reservations
                        if reservation['reservation_id'] != reservation_id
                        ]
        Reservation.save_reservations(reservations)
