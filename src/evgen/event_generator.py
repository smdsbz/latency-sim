# -*- coding: utf-8 -*-

from typing import List, Tuple, Dict
from .latency_sources import LatencySource, get_latency_source


class EventGenerator:
    def __init__(self, ev: List[Tuple[str, float]]):
        '''
        :param ev: List of events may happen, with items being tuples of two, a
            name that can be found in `sources` in config, and an associated
            probability.
        '''
        self._events = {    # type: Dict[str, LatencySource]
            e[0]: None  # TODO
            for e in ev
        }

    def sample(self) -> LatencySource:
        '''
        Sample from 
        '''
        pass

    def step(self):
        '''
        Take a step forward and change latency source states.
        Since .LatencySource.StochasticProcessSource is not implemented, this
        method is left as no-op.
        '''
        pass
