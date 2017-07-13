# -*- coding: utf-8 -*-


def to_int(value):
    try:
        res = int(value)
    except ValueError:
        res = int(float(value))
    return res


def to_float(value):
    return float(value)


def to_str(value):
    return str(value)
