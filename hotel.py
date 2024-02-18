"""
This module defines the Hotel class and its associated methods.

The Hotel class is responsible for managing hotel information, including creating, deleting,
modifying, and displaying hotels. It also handles room reservations and cancellations by
interacting with the Reservation class.
"""

import json
from reservation import Reservation

class Hotel:
    """Represents a hotel, managing its properties and reservations."""

    def __init__(self, hotel_info):
        """
        Initializes a new Hotel instance with information provided in a dictionary.

        Args:
            hotel_info (dict): A dictionary containing all necessary information for the hotel.
                Expected keys are:
                - hotel_id (str): Unique identifier for the hotel.
                - name (str): Name of the hotel.
                - location (str): Location of the hotel.
                - rooms (list): A list of dictionaries, each representing a room.
                - amenities (list): A list of amenities offered by the hotel.
        """
        self.hotel_id = hotel_info['hotel_id']
        self.name = hotel_info['name']
        self.location = hotel_info['location']
        self.rooms = hotel_info['rooms']
        self.amenities = hotel_info['amenities']

    @staticmethod
    def load_hotels():
        """Loads the list of hotels from a JSON file."""
        try:
            with open('hotels.json', 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    @staticmethod
    def save_hotels(hotels):
        """Saves the list of hotels to a JSON file."""
        with open('hotels.json', 'w', encoding='utf-8') as file:
            json.dump(hotels, file, indent=4)

    def create_hotel(self):
        """Creates a new hotel entry and adds it to the JSON file."""
        hotels = self.load_hotels()
        hotel = {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "location": self.location,
            "rooms": self.rooms,
            "amenities": self.amenities
        }
        hotels.append(hotel)
        self.save_hotels(hotels)

    @staticmethod
    def delete_hotel(hotel_id):
        """Deletes a hotel entry from the JSON file."""
        hotels = Hotel.load_hotels()
        hotels = [hotel for hotel in hotels if hotel['hotel_id'] != hotel_id]
        Hotel.save_hotels(hotels)

    @staticmethod
    def display_hotel_info(hotel_id):
        """Prints information about a specific hotel."""
        hotels = Hotel.load_hotels()
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                print(json.dumps(hotel, indent=4))
                return
        print("Hotel not found.")

    @staticmethod
    def modify_hotel_info(hotel_id, **kwargs):
        """Modifies information for a specific hotel."""
        hotels = Hotel.load_hotels()
        for hotel in hotels:
            if hotel['hotel_id'] == hotel_id:
                hotel.update(kwargs)
                Hotel.save_hotels(hotels)
                print(f"Hotel {hotel_id} updated successfully.")
                return
        print("Hotel not found.")

    @staticmethod
    def reserve_room(hotel_id, customer_id, room_id, start_date, end_date):
        """Attempts to reserve a room for a given period."""
        reservations = Reservation.load_reservations()
        for reservation in reservations:
            if (reservation['hotel_id'] == hotel_id and reservation['room_id'] == room_id and
                not (end_date < reservation['start_date'] or start_date > reservation['end_date'])):
                print("Room is not available for the selected dates.")
                return

        # If room is available, create a new reservation
        reservation_details = {
            'reservation_id': f"R{len(reservations) + 1}",  # Simple way to generate a new ID
            'customer_id': customer_id,
            'hotel_id': hotel_id,
            'room_id': room_id,
            'start_date': start_date,
            'end_date': end_date
        }
        new_reservation = Reservation(reservation_details)
        new_reservation.create_reservation()
        print(f"Room {room_id} in Hotel {hotel_id} reserved successfully "
              f"from {start_date} to {end_date}.")

    @staticmethod
    def cancel_reservation(reservation_id):
        """Cancels an existing room reservation."""
        Reservation.cancel_reservation(reservation_id)
        print(f"Reservation {reservation_id} canceled successfully.")
        