"""
Integration tests for both encoding and decoding HDLC frames.
"""

import unittest

from yahdlc import FRAME_DATA, MessageError, frame_data, get_data


class TestEncodeDecode(unittest.TestCase):
    """
    Integration tests for both encoding and decoding HDLC frames.
    """

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
                # No HDLC frame detected.
                pass
