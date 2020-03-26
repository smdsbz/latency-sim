# -*- coding: utf-8 -*-

import unittest

from config import init_config
from evgen import EventGenerator


class TestEventGenerator(unittest.TestCase):
    def test_init_evgen(self):
        init_config('../configs/testuse/test.json')
        # TODO:
        pass


if __name__ == '__main__':
    unittest.main()