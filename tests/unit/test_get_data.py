"""
Unit tests for the 'get_data' function.
"""

import unittest

from yahdlc import FRAME_DATA, FCSError, MessageError, frame_data, get_data


class TestGetData(unittest.TestCase):
    """
    Unit tests for the 'get_data' function.
    """

    def test_get_data_invalid_inputs(self):
        """
        Call "get_data" with invalid inputs.
        """

        with self.assertRaises(TypeError):
            get_data(12)
        with self.assertRaises(MessageError):
            get_data("")
        with self.assertRaises(MessageError):
            get_data("test")

    def test_get_data_corrupted_frame(self):
        """
        Call "get_data" with a corrupted frame as input.
        """

        data = bytearray(frame_data("test", FRAME_DATA, 0))
        data[7] ^= 0x01
        data = bytes(data)

        with self.assertRaises(FCSError):
            try:
                get_data(data)
            except FCSError as err:
                self.assertEqual(err.args[0], 0)
                raise

        data = bytearray(frame_data("test", FRAME_DATA, 2))
        data[7] ^= 0x01
        data = bytes(data)

        with self.assertRaises(FCSError):
            try:
                get_data(data)
            except FCSError as err:
                self.assertEqual(err.args[0], 2)
                raise
