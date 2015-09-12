#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import math

def random_money(offset, limit):
    offset_f, offset_i = math.modf(offset)

    offset_i = int(offset_i)
    offset_f = int(offset_f * 10)

    value, intents = None, 0
    while value is None or intents < 100:
        value = random.randint(offset_i, limit) + random.random()
        intents += 1
    if value <= offset:
        value = random.randint(offset_i + 1, limit) + random.random()
    if value >= limit:
        value = float(limit)
    return value


if __name__ == "__main__":
    for idx in xrange(100000):
        offset = random.choice(range(0, 10))
        assert random_money(offset + random.random(), 10) <= 10
