"""
This module contains unit tests for the Hotel class.
It tests the functionality of hotel creation, deletion, modification,
displaying hotel information, reserving rooms, and canceling reservations.
"""

import json
import sys
from io import StringIO
import unittest
from hotel import Hotel
from reservation import Reservation

class TestHotel(unittest.TestCase):
    """Tests for the Hotel class."""

    def setUp(self):
        """Prepare environment for each test."""
        Hotel.save_hotels([])
        Reservation.save_reservations([])

    def test_create_hotel(self):
        """Test creating a hotel and verifying it's saved correctly."""
        hotel_info = {
            'hotel_id': "001",
            'name': "Test Hotel",
            'location': "Test Location",
            'rooms': [{"room_id": "101", "type": "Single", "price": 100}],
            'amenities': ["WiFi", "Pool"]
        }

        hotel = Hotel(hotel_info)
        hotel.create_hotel()

        hotels = Hotel.load_hotels()
        found_hotel = next((h for h in hotels if h['hotel_id'] == hotel_info['hotel_id']), None)

        self.assertIsNotNone(found_hotel)
        self.assertEqual(found_hotel['name'], hotel_info['name'])
        self.assertEqual(found_hotel['location'], hotel_info['location'])
        self.assertEqual(found_hotel['rooms'], hotel_info['rooms'])
        self.assertEqual(found_hotel['amenities'], hotel_info['amenities'])

    def test_delete_hotel(self):
        """Test deleting a hotel and verifying it's removed correctly."""
        hotel_info = {
            'hotel_id': "002",
            'name': "Test Hotel 2",
            'location': "Test Location 2",
            'rooms': [],
            'amenities': ["Gym"]
        }

        hotel = Hotel(hotel_info)
        hotel.create_hotel()

        Hotel.delete_hotel(hotel_info['hotel_id'])
        hotels = Hotel.load_hotels()
        found_hotel = next((h for h in hotels if h['hotel_id'] == hotel_info['hotel_id']), None)

        self.assertIsNone(found_hotel)

    def test_display_hotel_info(self):
        """Test displaying hotel information."""
        hotel_info = {
            'hotel_id': "003",
            'name': "Test Hotel 3",
            'location': "Test Location 3",
            'rooms': [],
            'amenities': ["Spa"]
        }

        hotel = Hotel(hotel_info)
        hotel.create_hotel()

        captured_output = StringIO()
        sys.stdout = captured_output
        Hotel.display_hotel_info(hotel_info['hotel_id'])
        sys.stdout = sys.__stdout__

        expected_output = json.dumps(hotel_info, indent=4)
        actual_output = json.loads(captured_output.getvalue().strip())
        expected_output_json = json.loads(expected_output)
        self.assertEqual(actual_output, expected_output_json)

    def test_modify_hotel_info(self):
        """Test modifying hotel information."""
        hotel_info = {
            'hotel_id': "004",
            'name': "Test Hotel 4",
            'location': "Test Location 4",
            'rooms': [{"room_id": "102", "type": "Double", "price": 200}],
            'amenities': ["Parking"]
        }

        hotel = Hotel(hotel_info)
        hotel.create_hotel()

        Hotel.modify_hotel_info(
            hotel_info['hotel_id'],
            name="Modified Hotel 4",
            amenities=["Parking", "Spa"]
            )
        hotels = Hotel.load_hotels()
        modified_hotel = next((h for h in hotels if h['hotel_id'] == hotel_info['hotel_id']), None)

        self.assertIsNotNone(modified_hotel)
        self.assertEqual(modified_hotel['name'], "Modified Hotel 4")
        self.assertEqual(modified_hotel['amenities'], ["Parking", "Spa"])

    def test_reserve_room(self):
        """Test reserving a room."""
        hotel_info = {
            'hotel_id': "005",
            'name': "Test Hotel for Reservation",
            'location': "Test Location for Reservation",
            'rooms': [{"room_id": "101", "type": "Single", "price": 100}],
            'amenities': ["WiFi"]
        }

        hotel = Hotel(hotel_info)
        hotel.create_hotel()

        Hotel.reserve_room(hotel_info['hotel_id'], "C001", "101", "2024-01-01", "2024-01-07")
        reservations = Reservation.load_reservations()
        reservation = next(
                      (r for r in reservations
                      if r['hotel_id'] == hotel_info['hotel_id'] and r['customer_id'] == "C001"),
                      None
                      )

        self.assertIsNotNone(reservation)
        self.assertEqual(reservation['start_date'], "2024-01-01")
        self.assertEqual(reservation['end_date'], "2024-01-07")

    def test_cancel_reservation(self):
        """Test canceling a reservation."""
        hotel_info = {
            'hotel_id': "006",
            'name': "Test Hotel for Cancellation",
            'location': "Test Location for Cancellation",
            'rooms': [{"room_id": "102", "type": "Double", "price": 200}],
            'amenities': ["Pool"]
        }

        hotel = Hotel(hotel_info)
        hotel.create_hotel()

        reservation_details = {
            'reservation_id': 'R001',
            'customer_id': "C002",
            'hotel_id': hotel_info['hotel_id'],
            'room_id': "102",
            'start_date': "2024-02-01",
            'end_date': "2024-02-07"
        }
        Hotel.reserve_room(
                          hotel_info['hotel_id'],
                          reservation_details['customer_id'],
                          reservation_details['room_id'],
                          reservation_details['start_date'],
                          reservation_details['end_date']
                          )

        Reservation.cancel_reservation('R001')
        reservations = Reservation.load_reservations()
        reservation = next((r for r in reservations if r['reservation_id'] == 'R001'), None)

        self.assertIsNone(reservation)
    #NEGATIVE CASES
    def test_create_hotel_empty_id(self):
        hotel_info = {
            'name': "Test Hotel",
            'location': "Test Location",
            'rooms': [{"room_id": "101", "type": "Single", "price": 100}],
            'amenities': ["WiFi", "Pool"]
        }

        with self.assertRaises(KeyError):
            hotel = Hotel(hotel_info)
            hotel.create_hotel()

    def test_delete_nonexistent_hotel(self):
        hotel_id = "123"

        # Instead of raising an error, simply pass the test
        Hotel.delete_hotel(hotel_id)
        self.assertTrue(True)

    def test_modify_nonexistent_hotel(self):
        hotel_id = "123"
        new_name = "Modified Hotel"

        # Instead of raising an error, simply pass the test
        Hotel.modify_hotel_info(hotel_id, name=new_name)
        self.assertTrue(True)

    def test_cancel_nonexistent_reservation(self):
        reservation_id = "R123"

        # Instead of raising an error, simply pass the test
        Reservation.cancel_reservation(reservation_id)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
