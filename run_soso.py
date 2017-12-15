#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections

import numpy as np

import uber_agent.simulation
import uber_agent.city


class SosoAgent():
    def __init__(self, city):
        self._city = city
        self._weights = collections.defaultdict(float)

    def feature_extractor(self, state, action):
        src, dest = action
        features = {}
        features['dist1'] = self._city.distance(state, src)
        features['dist2'] = self._city.distance(src, dest)
        features['cur_{}'.format(state)] = 1
        features['src_{}'.format(src)] = 1
        features['dest_{}'.format(dest)] = 1
        return features

    def forward(self, state, action):
        score = 0
        for f, v in self.feature_extractor(state, action).items():
            score += self._weights[f] * v
        return score

    def backward(self, state, action, reward, new_state):
        ETA = 0.1
        s = self.forward(state, action)
        for f, v in self.feature_extractor(state, action).items():
            self._weights[f] -= ETA * (s - reward) * v


def main():
    agent = uber_agent.simulation.QLearningAgentWrapper(
        SosoAgent(uber_agent.city.City.load()))
    res = uber_agent.simulation.simulate(agent)
    np.savetxt('soso.txt', res)


if __name__ == '__main__':
    main()
