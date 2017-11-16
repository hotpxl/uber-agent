#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import uber_agent.simulation


class RandomAgent():
    def forward(self, *args):
        return random.random()

    def backward(self, *args):
        pass


def main():
    agent = RandomAgent()
    print(uber_agent.simulation.simulate(agent))


if __name__ == '__main__':
    main()
