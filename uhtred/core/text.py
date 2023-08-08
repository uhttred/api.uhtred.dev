import random

DEFATAUL_STR: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTWUXYZ0123456789'

def get_random_string_code (length: int = 6, sequence: str = ''):
    return ''.join([random.choice(sequence or DEFATAUL_STR) for i in range(length)])
    