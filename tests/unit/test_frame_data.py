"""
Unit tests for the 'frame_data' function.
"""

import unittest

from yahdlc import FRAME_DATA, frame_data


class TestFrameData(unittest.TestCase):
    """
    Unit tests for the 'frame_data' function.
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
