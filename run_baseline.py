#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random

import uber_agent.state


class RandomAgent():
    def interact(self, location, candidates):
        return random.choice(range(len(candidates)))


def main():
    map = uber_agent.state.load_map()
    evaluator = uber_agent.state.Evaluator(map, RandomAgent())
    evaluator.run_for(7200)
    print(evaluator.reward())


if __name__ == '__main__':
    main()
