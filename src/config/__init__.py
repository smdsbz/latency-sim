# -*- coding: utf-8 -*-

_config = None

def init_config(path_: str):
    global _config
    import json
    with open(path_, 'r') as cf:
        _config = json.load(cf)

def has_config_init():
    return not _config is None

def get_source_by_name(name: str):
    '''
    :param name:
    :return: dict
    '''
    if not has_config_init():
        raise RuntimeError('config uninitialized')
    for source in _config['sources']:
        if source['name'] == name:
            return source
    return None
