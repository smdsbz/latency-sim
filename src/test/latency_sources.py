# -*- coding: utf-8 -*-

import unittest

from evgen.latency_sources import get_latency_source


class TestGetLatencySource(unittest.TestCase):
    def test_helloworld(self):
        cd = get_latency_source('constant', 'constdist', value=12.0)
        from evgen.latency_sources import ConstantSource
        self.assertTrue(isinstance(cd, ConstantSource))
        self.assertEqual(cd(), 12.0)
        self.assertEqual(cd(), cd())

    def test_normal_distribution(self):
        nd = get_latency_source('normal-distribution', 'nvme-ssd-read',
            mu=2000.0, sigma=128.0)
        from evgen.latency_sources import NormalDistributionSource
        self.assertTrue(isinstance(nd, NormalDistributionSource))
        print(f'sampling from {nd} got {nd()}')

    def test_init_unknown_type(self):
        with self.assertRaises(RuntimeError):
            ud = get_latency_source('unkown-distribution', 'xxx')


if __name__ == '__main__':
    unittest.main()