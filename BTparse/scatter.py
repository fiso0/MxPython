#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
N = 1000
x = np.random.randn(N)
y = np.random.randn(N)
plt.scatter(x, y,alpha=0.5)
plt.show()

if __name__ == '__main__':
	input()