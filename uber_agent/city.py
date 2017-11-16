#!/usr/bin/env
# -*- coding: utf-8 -*-
import pickle
import math
import random


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
        weights = reversed(list(range(1, len(locations) + 1)))
        return self.start_from(random.choices(locations, weights=weights)[0])

    def start_from(self, l):
        locations = self._city.locations()
        assert l in locations, 'Invalid location.'
        locations.remove(l)
        destination = random.choice(locations)
        return (l, destination)
