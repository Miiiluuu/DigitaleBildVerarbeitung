# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 14:18:21 2018

@author: MOELLERMI
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1

# Bild- Array (aus Aufgabe 1.1) erstellen
szinti, pixel_quadrant = Aufgabe_1_1.make_szinti()

ebene = []
for i in range(7, -1, -1):
    bitebene = np.zeros((len(szinti), len(szinti)))
    bitebene[szinti >= 2**[i]] = 1
    szinti[szinti >= 2**[i]] -= 2**[i]
ebene.append(bitebene)
for i in range(7, -1, -1):
    plt.imshow(bitebene[i])
print("a")

