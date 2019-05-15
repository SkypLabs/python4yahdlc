"""
Unit tests written with the "unittest" module.
"""

import unittest

# pylint: disable=no-name-in-module
from yahdlc import FRAME_DATA, FCSError, MessageError, frame_data, get_data


class TestYahdlc(unittest.TestCase):
    """
    Unit tests for the yahdlc module.
    """

    def test_frame_data_invalid_inputs(self):
        """
        Call "frame_data" with invalid inputs.
        """

        with self.assertRaises(TypeError):
            frame_data(2)
        with self.assertRaises(TypeError):
            frame_data("test", "test")
        with self.assertRaises(TypeError):
            frame_data("test", FRAME_DATA, "test")
        with self.assertRaises(ValueError):
            frame_data("test", 12)
        with self.assertRaises(ValueError):
            frame_data("test", FRAME_DATA, 8)

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

    def test_encode_and_decode_frame(self):
        """
        Encode a frame using "frame_data" and then decode the same frame using
        "get_data".
        """

        frame = frame_data("test")
        data, ftype, seq_no = get_data(frame)

        self.assertEqual(b"test", data)
        self.assertEqual(FRAME_DATA, ftype)
        self.assertEqual(0, seq_no)

    def test_decode_frame_byte_per_byte(self):
        """
        Decode a frame byte per byte using "get_data".
        """

        frame = frame_data("test")

        for _ in frame:
            try:
                data, ftype, seq_no = get_data(frame)

                self.assertEqual(b"test", data)
                self.assertEqual(FRAME_DATA, ftype)
                self.assertEqual(0, seq_no)
            except MessageError:
                pass
