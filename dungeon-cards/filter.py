#!/usr/bin/python3

def filter(ls, pred):
    res = []
    for it in ls:
        if pred(it): res.append(it)
    return res

