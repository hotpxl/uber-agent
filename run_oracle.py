#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

import uber_agent.city
import uber_agent.simulation


class OracleAgent():
    def __init__(self, city):
        self._city = city

    def _reward(self, location, action):
        ALPHA = 1 / 150
        fare = self._city.fare_estimate(*action)
        travel_time = self._city.travel_time(
            location, action[0]) + self._city.travel_time(*action)
        reward = fare - ALPHA * travel_time
        return reward

    def forward(self, state, action):
        return self._reward(state, action)

    def backward(self, *args):
        pass


def main():
    agent = uber_agent.simulation.QLearningAgentWrapper(
        OracleAgent(uber_agent.city.City.load()))
    res = uber_agent.simulation.simulate(agent)
    np.savetxt('oracle.txt', res)


if __name__ == '__main__':
    main()
