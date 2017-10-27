#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import random
import pickle


class Map():
    def __init__(self, locations, travel_times):
        self._locations = locations
        self._travel_times = travel_times

    def locations(self):
        return self._locations

    def travel_time(self, src, dst):
        return self._travel_times[src][dst]


class Evaluator():
    def __init__(self, map, agent):
        self._map = map
        locations = self._map.locations()
        self._candidates = []
        for _ in range(100):
            self._candidates.append(random.sample(locations, 2))
        self._agent = agent
        self._agent_location = locations[0]
        self._time_elapsed = 0
        self._reward = 0

    def step(self):
        candidates = sorted(
            self._candidates,
            key=lambda c: self._map.travel_time(self._agent_location, c[0]))
        index = self._agent.interact(self._agent_location, candidates[:5])
        choice = candidates[index]
        self._time_elapsed += self._map.travel_time(self._agent_location,
                                                    choice[0])
        self._time_elapsed += self._map.travel_time(*choice)
        self._candidates.remove(choice)
        self._agent_location = choice[1]
        self._reward += 1

    def run_for(self, t):
        while self._time_elapsed < t and 0 < len(self._candidates):
            self.step()

    def reward(self):
        return self._reward


def load_map():
    with open(os.path.join(os.path.dirname(__file__), 'map.p'), 'rb') as f:
        travel_times = pickle.load(f)
    return Map(
        locations=list(range(len(travel_times))), travel_times=travel_times)
