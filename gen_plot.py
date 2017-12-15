#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set()


def ema(arr):
    alpha = 0.05
    acc = arr[0]
    for i in range(1, len(arr)):
        acc = (1 - alpha) * acc + alpha * arr[i]
        arr[i] = acc
    return arr


baseline = np.loadtxt('baseline.txt')
soso = np.loadtxt('soso.txt')
oracle = np.loadtxt('oracle.txt')

plt.plot(ema(baseline[:100]), 'r', label='Baseline')
plt.plot(ema(soso[:100]), 'g', label='Our algorithm')
plt.plot(ema(oracle[:100]), 'b', label='Oracle')
plt.legend(loc=0)
plt.xlabel('Trial')
plt.ylabel('Total reward')
plt.savefig('reward.png')
