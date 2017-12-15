#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import numpy as np

import uber_agent.simulation


class RandomAgent():
    def get_action(self, _, actions):
        return random.choice(actions)

    def feedback(self, *args):
        pass


def main():
    agent = RandomAgent()
    res = uber_agent.simulation.simulate(agent)
    np.savetxt('baseline.txt', res)


if __name__ == '__main__':
    main()
