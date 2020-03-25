# -*- coding: utf-8 -*-

from .latency_source import *
from .constant_sources import *
from .sampling_sources import *

def get_latency_source(type_: str, name: str, *_, **kwarg):
    if type_ == 'constant':
        return ConstantSource(name, **kwarg)
    if type_ == 'normal-distribution':
        return NormalDistributionSource(name, **kwarg)
    raise RuntimeError(f'unknown type {type_} for {name}')
