import unittest
import client


class TestGetMove(unittest.TestCase):
    def test_get_move_returns_a_valid_move(self):
        board = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 1, 0, 0, 0], [
            0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
        self.assertEqual(client.get_move(1, board), [4, 2])


class TestPrepareResponse(unittest.TestCase):
    def test_prepare_response_returns_a_valid_response(self):
        self.assertEqual(client.prepare_response([4, 2]), b'[4, 2]\n')


if __name__ == '__main__':
    unittest.main()
