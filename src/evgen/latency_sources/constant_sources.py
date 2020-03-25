# -*- coding: utf-8 -*-

from .latency_source import LatencySource


class ConstantSource(LatencySource):
    def __init__(self, name: str, *_, **kwarg):
        '''
        :param name:
        :param value:
        '''
        super().__init__(name)
        if not 'value' in kwarg:
            raise RuntimeError('value not parameterized')
        self._value = kwarg['value']

    def __call__(self) -> float:
        return self._value
