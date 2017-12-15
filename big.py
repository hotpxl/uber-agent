#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
import pickle
import collections
import math
import random
import pickle

import numpy as np


class City():
    def __init__(self, locations, travel_times, fare_estimates, coordinates):
        self._locations = locations
        self._travel_times = travel_times
        self._fare_estimates = fare_estimates
        self._coordinates = coordinates

    def save(self, filename='city.p'):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename='city.p'):
        with open(filename, 'rb') as f:
            return pickle.load(f)

    def locations(self):
        return self._locations[:]

    def travel_time(self, a, b):
        return self._travel_times[a][b]

    def fare_estimate(self, a, b):
        return self._fare_estimates[a][b]

    def coordinate(self, a):
        return self._coordinates[a]

    def distance(self, a, b):
        return math.sqrt(
            sum(
                map(lambda i, j: (i - j)**2, self._coordinates[a],
                    self._coordinates[b])))


class TripGenerator():
    def __init__(self, city):
        self._city = city

    def driver_at(self, l):
        locations = self._city.locations()
        assert l in locations, 'Invalid location.'
        weights = np.arange(1, len(locations) + 1)[::-1].astype(np.float)
        weights /= np.sum(weights)
        return self.start_from(np.random.choice(locations, p=weights))

    def start_from(self, l):
        locations = self._city.locations()
        assert l in locations, 'Invalid location.'
        locations.remove(l)
        destination = random.choice(locations)
        return (l, destination)


def simulate(city, agent, num_trials=2000, time_limit=12 * 3600,
             training=True):
    trip_generator = TripGenerator(city)
    reward_history = []
    for i in range(num_trials):
        simulator = Simulator(city, trip_generator, agent)
        time = 0
        total_reward = 0
        total_trips = 0
        while time < time_limit:
            old_state, action, reward, new_state, travel_time = simulator.step(
            )
            if training:
                agent.feedback(old_state, action, reward, new_state)
            time += travel_time
            total_reward += reward
            total_trips += 1
        print('Trial {} finished with total reward {} and {} trips.'.format(
            i, total_reward, total_trips))
        reward_history.append(total_reward)
    return reward_history


class Simulator():
    def __init__(self,
                 city,
                 trip_generator,
                 agent,
                 start_location=None,
                 num_choices=5):
        self._city = city
        self._trip_generator = trip_generator
        self._agent = agent
        if start_location is not None:
            assert start_location in self._city.locations(
            ), 'Invalid start state.'
            self._location = start_location
        else:
            self._location = self._city.locations()[0]
        self._num_choices = num_choices

    def step(self):
        ALPHA = 1 / 150
        candidates = [
            self._trip_generator.driver_at(self._location)
            for _ in range(self._num_choices)
        ]
        action = self._agent.get_action(self._location, candidates)
        fare = self._city.fare_estimate(*action)
        travel_time = self._city.travel_time(
            self._location, action[0]) + self._city.travel_time(*action)
        reward = fare - ALPHA * travel_time
        old_state = self._location
        new_state = action[1]
        self._location = new_state
        return old_state, action, reward, new_state, travel_time


class QLearningAgentWrapper():
    def __init__(self, agent):
        self._agent = agent

    def get_action(self, state, actions):
        predictions = [(self._agent.forward(state, i), i) for i in actions]
        predictions.sort(reverse=True)
        return predictions[0][1]

    def feedback(self, old_state, action, reward, new_state):
        self._agent.backward(old_state, action, reward, new_state)


class RandomAgent():
    def get_action(self, _, actions):
        return random.choice(actions)

    def feedback(self, *args):
        pass


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
    with open('data.p', 'rb') as f:
        data = pickle.load(f)
    city = City(data['locations'], data['travel_times'],
                data['fare_estimates'], data['coordinates'])
    agent = RandomAgent()
    res = simulate(city, agent)
    np.savetxt('baseline.txt', res)
    agent = QLearningAgentWrapper(OracleAgent(city))
    res = simulate(city, agent)
    np.savetxt('oracle.txt', res)
    agent = QLearningAgentWrapper(SosoAgent(city))
    res = simulate(city, agent)
    np.savetxt('soso.txt', res)


if __name__ == '__main__':
    main()
