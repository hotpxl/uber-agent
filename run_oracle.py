#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uber_agent.state


class OracleAgent():
    def __init__(self, map):
        self._map = map

    def interact(self, location, candidates):
        return sorted(enumerate(candidates), key=lambda i: self._map.travel_time(location, i[1][0]) + self._map.travel_time(*i[1]))[0][0]


def main():
    map = uber_agent.state.load_map()
    evaluator = uber_agent.state.Evaluator(map, OracleAgent(map))
    evaluator.run_for(7200)
    print(evaluator.reward())


if __name__ == '__main__':
    main()
