#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uber_agent.city


def simulate(agent, num_trials=500, time_limit=3 * 3600, training=True):
    city = uber_agent.city.City.load()
    trip_generator = uber_agent.city.TripGenerator(city)
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
                agent.backward(old_state, action, reward, new_state)
            time += travel_time
            total_reward += reward
            total_trips += 1
        print('Trial {} finished with total reward {} and {} trips.'.format(
            i, total_reward, total_trips))
        reward_history.append(total_reward)
    return reward_history


# TODO(yutian): Make this Q-learning specific simulator? Factor out problem MDP?
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
        predictions = [(self._agent.forward(self._location, i), i)
                       for i in candidates]
        predictions.sort(reverse=True)
        action = predictions[0][1]
        fare = self._city.fare_estimate(*action)
        travel_time = self._city.travel_time(
            self._location, action[0]) + self._city.travel_time(*action)
        reward = fare - ALPHA * travel_time
        old_state = self._location
        new_state = action[1]
        self._location = new_state
        return old_state, action, reward, new_state, travel_time
