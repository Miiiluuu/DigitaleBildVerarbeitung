# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 11:02:30 2018

@author: mieke
"""

import numpy as np


array = np.array([[1, 2, 3, 4], [7, 8, 9, 10]])
array_strich = array[1]
array_str = array_strich[:, np.newaxis]

print("aa")