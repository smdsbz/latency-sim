# -*- coding: utf-8 -*-

class LatencySource:
    def __init__(self, name: str, *_, **kwarg):
        self._name = name

    def __repr__(self):
        return f'LatencySource(name: {self._name})'

    def __call__(self) -> float:
        raise NotImplementedError('virtual function')
