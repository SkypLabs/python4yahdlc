import unittest
from yahdlc import *

class TestYahdlc(unittest.TestCase):
    def test_frame_data_invalid_inputs(self):
        with self.assertRaises(TypeError):
            frame_data(2)
        with self.assertRaises(TypeError):
            frame_data('test', 'test')
        with self.assertRaises(TypeError):
            frame_data('test', FRAME_DATA, 'test')
        with self.assertRaises(ValueError):
            frame_data('test', 12)
        with self.assertRaises(ValueError):
            frame_data('test', FRAME_DATA, 8)

    def test_get_data_invalid_inputs(self):
        with self.assertRaises(TypeError):
            get_data(12)
        with self.assertRaises(MessageError):
            get_data('')
        with self.assertRaises(MessageError):
            get_data('test')

    def test_get_data_corrupted_frame(self):
        data = bytearray(frame_data('test', FRAME_DATA, 0))
        data[7] ^= 0x01
        data = bytes(data)

        with self.assertRaises(FCSError):
            try:
                get_data(data)
            except FCSError as e:
                self.assertEqual(e.args[0], 0)
                raise

        data = bytearray(frame_data('test', FRAME_DATA, 2))
        data[7] ^= 0x01
        data = bytes(data)

        with self.assertRaises(FCSError):
            try:
                get_data(data)
            except FCSError as e:
                self.assertEqual(e.args[0], 2)
                raise

    def test_encode_and_decode_frame(self):
        frame = frame_data('test')
        data, type, seq_no = get_data(frame)

        self.assertEqual(b'test', data)
        self.assertEqual(FRAME_DATA, type)
        self.assertEqual(0, seq_no)

    def test_decode_frame_with_1B_buffer(self):
        frame = frame_data('test')

        for c in frame:
            try:
                data, type, seq_no = get_data(frame)
            except MessageError:
                pass

        self.assertEqual(b'test', data)
        self.assertEqual(FRAME_DATA, type)
        self.assertEqual(0, seq_no)

if __name__ == '__main__':
    unittest.main()
