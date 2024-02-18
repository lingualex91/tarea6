"""
This module contains unit tests for the Reservation class.
It tests the functionality of reservation creation, cancellation, 
and validation of reservation properties.
"""

import unittest
from reservation import Reservation

class TestReservation(unittest.TestCase):
    """Tests for the Reservation class."""

    def setUp(self):
        """
        Prepare environment for each test.
        Ensure the reservation list is empty before each test.
        """
        Reservation.save_reservations([])

    def test_create_reservation(self):
        """
        Test creating a reservation and verifying it's saved correctly.
        """
        reservation_details = {
            'reservation_id': "R001",
            'customer_id': "C001",
            'hotel_id': "H001",
            'room_id': "101",
            'start_date': "2024-01-01",
            'end_date': "2024-01-07"
        }

        reservation = Reservation(reservation_details)
        reservation.create_reservation()

        reservations = Reservation.load_reservations()
        found_reservation = next(
                            (r for r in reservations
                            if r['reservation_id'] == reservation_details['reservation_id']),
                            None
                            )

        self.assertIsNotNone(found_reservation, "Reservation should be in the list after creation")
        for key, value in reservation_details.items():
            self.assertEqual(
                found_reservation[key], value,
                f"{key} should match the created reservation detail."
            )

    def test_cancel_reservation(self):
        """
        Test canceling a reservation and verifying it's removed correctly.
        """
        reservation_details = {
            'reservation_id': "R002",
            'customer_id': "C002",
            'hotel_id': "H002",
            'room_id': "102",
            'start_date': "2024-02-01",
            'end_date': "2024-02-07"
        }

        reservation = Reservation(reservation_details)
        reservation.create_reservation()

        reservations_before_cancellation = Reservation.load_reservations()
        found_reservation_before = next(
                                      (r for r in reservations_before_cancellation
                                      if r['reservation_id'] == reservation_details['reservation_id'])
                                      , None
                                      )
        self.assertIsNotNone(
            found_reservation_before,
            "Reservation should exist before cancellation.\n"
            f"Reservation ID: {reservation_details['reservation_id']}"
        )

        Reservation.cancel_reservation(reservation_details['reservation_id'])

        reservations_after_cancellation = Reservation.load_reservations()
        found_reservation_after = next(
            (r for r in reservations_after_cancellation if r['reservation_id'] == reservation_details['reservation_id']),
            None
        )

        self.assertIsNone(found_reservation_after, "Reservation should be removed from the list after cancellation")

if __name__ == '__main__':
    unittest.main()
    