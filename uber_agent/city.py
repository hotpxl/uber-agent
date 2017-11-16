#!/usr/bin/env
# -*- coding: utf-8 -*-
import pickle


class City():
    def __init__(self, locations, travel_times, fare_estimates):
        self._locations = locations
        self._travel_times = travel_times
        self._fare_estimates = fare_estimates

    def save(self, filename='city.p'):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename='city.p'):
        with open(filename, 'rb') as f:
            return pickle.load(f)