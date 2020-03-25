# -*- coding: utf-8 -*-

import numpy as np
from .latency_source import LatencySource


class SamplingSource(LatencySource):
    def __init__(self, name: str, *_, **kwarg):
        super().__init__(name)


class NormalDistributionSource(SamplingSource):
    def __init__(self, name: str, *_, **kwarg):
        super().__init__(name)
        if not 'mu' in kwarg:
            raise RuntimeError(f'mu not parameterized for {name}')
        self._mu = kwarg['mu']
        if not 'sigma' in kwarg:
            raise RuntimeError(f'sigma not parameterized for {name}')
        self._sigma = kwarg['sigma']

    def __repr__(self) -> str:
        return (
            f'NormalDistributionSource(name: {self._name}, mu: {self._mu}, '
            f'sigma: {self._sigma})'
        )

    def __call__(self) -> float:
        return np.random.normal(self._mu, self._sigma)
