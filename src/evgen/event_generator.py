# -*- coding: utf-8 -*-

from typing import Iterable, Tuple, Dict
from config import config, get_source_by_name
from .latency_sources import LatencySource, get_latency_source


class EventGenerator:
    def __init__(self, ev: Iterable[Tuple[str, float]]):
        '''
        :param ev: List of events may happen, with items being tuples of two, a
            name that can be found in `sources` in config, and its associated
            probability.
        '''
        self._events = {
            e[0]: (lambda s: get_latency_source(s['type'], s['name'], **s['parameters']))(get_source_by_name(e[0]))
            for e in ev
        }   # type: Dict[str, LatencySource]
        self._probs = {e[0]: e[1] for e in ev}  # type: Dict[str, float]

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
