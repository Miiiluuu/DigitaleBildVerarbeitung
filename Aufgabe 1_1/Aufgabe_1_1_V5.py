 # -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 13:20:08 2018

@author: MOELLERMI
"""

# Aufgabe 1.1.

import numpy as np
import matplotlib.pyplot as plt

# fuer Pixelgroeße von 256x256
pixel = 256
# fuer Erstellen Koordinatensystem Flaechenquelle A, B, C und D
pixel_quadrant = 128
# Anzahl an Pixel fuer jedes Objekt TODO???
n = 100


def get_image_A(laenge_quadrant, anz_pixel):
    """ Erzeugt Objekt A, ist Rechteck. """
#    # Mittelpunkt Flaechenquelle A
#    zentrum = 60                        # (x, y) = (60 mm, 60 mm)
#    delta_x = 100                       # mm
#    delta_y = 100                       # mm
    # mittlere flaechenbezogene Zahl der registrierten Ereignisse von Objekt A
    avg_a = 200                          # 1/mm²
    # erstelle 128x128- Array, in dem sich Flaechenquelle A befindet
    # ≙ lokales Koordinatensystem
    image_a = np.zeros((laenge_quadrant, laenge_quadrant))
    # Figur fuer Flaechenquelle A, Flaeche eingrenzen
    # ist Rechteck, beachte Indexierung von Arrays in numpy: beginnend mit Null
    quelle_a = image_a[18:118, 10:110]
    # auf jeden Pixel von Quelle A Poisson- Verteilung anwenden
    # dadurch Beachtung des statistischen Charakters des
    # radioaktiven Zerfalls
    for i in range(anz_pixel):
        for j in range(anz_pixel):
              quelle_a[i, j] = np.random.poisson(avg_a)
    return image_a
    
      

    
# Objekt A dem richtigen Platz des Szintigramms zuweisen
# Erstellung Szintigramm:
# erstelle ein 256x256- Array
# stellt Szintigramm-Flaeche dar
# ≙ globales Koordinatensystem
# beachte Indexierung von Arrays in numpy: beginnend mit Null
szinti = np.zeros((pixel, pixel))
# Einteilung des Szintigramms in vier Quadranten
# jedes Objekt befindet sich in jeweils einem Quadranten
quadrant_eins = szinti[0:128, 128:256]
quadrant_zwei = szinti[0:128, 0:128]
quadrant_drei = szinti[128:256, 0:128]
quadrant_vier = szinti[128:256, 128:256]

image_a = get_image_A(pixel_quadrant, n)
szinti[0:128, 128:256] = image_a


def get_image_B(laenge_quadrant,):
    """ Erzeugt Objekt B, ist Rechteck mit Streifen. """
    # mittlere flaechenbezogene Zahl der registrierten Ereignisse von
    # Objekt B, graue Streifen
    avg_b_g = 250                  # 1/mm²
    # mittlere flaechenbezogene Zahl der registrierten Ereignisse von
    # Objekt B, weiße Streifen
    avg_b_w = 300                  # 1/mm²
    # erstelle 128x128- Array, in dem sich Flaechenquelle B befindet
    image_b = np.zeros((laenge_quadrant, laenge_quadrant))
    # Figur fuer Flaechenquelle B, Flaeche eingrenzen
    # ist Rechteck, beachte Indexierung von Arrays in numpy: beginnend mit Null
    quelle_b = image_b[18:118, 18:118]
    # Streifen  
    i = 0
    while i < 100:
        quelle_b[:, i:i+5] = np.random.poisson(avg_b_g, (100, 5))
        i += 5
        quelle_b[:, i:i+5] = np.random.poisson(avg_b_w, (100, 5))
        i += 5
    return image_b
         
# Objekt B dem richtigen Platz des Szintigramms zuweisen
# Erstellung Szintigramm:
# erstelle ein 256x256- Array
# stellt Szintigramm-Flaeche dar
# beachte Indexierung von Arrays in numpy: beginnend mit Null
image_b = get_image_B(pixel_quadrant)
szinti[0:128, 0:128] = image_b


def get_image_C(laenge_quadrant):
    """ Erzeugt Objekt C, ist Kreis. """
    # erstelle 128x128- Array, in dem sich Flaechenquelle C befindet
    image_c = np.zeros((laenge_quadrant, laenge_quadrant))
    # Figur fuer Flaechenquelle A, Flaeche eingrenzen als Rechteck
    rechteck_c = image_c[10:110, 18:118]
    # Kreisformel
    # Satz des Pythagoras
    # Mittelpunkt vom Kreis
    mitte = 50              # (x, y) = (50 mm, 50 mm)
    # jeden Pixel einzeln durchgehen
    for i in range(n):
      for j in range(n):  
          deltax = mitte - i
          deltay = mitte - j
          if deltax**2 + deltay**2 <= mitte**2:
              rechteck_c[i, j] = np.random.poisson(50)
    return image_c

              
    # Objekt C dem richtigen Platz des Szintigramms zuweisen
    image_c = get_image_C(pixel_quadrant)
    szinti[128:256, 0:128] = image_c
    
    # Flaechenquelle D
    # erstelle 128x128- Array, in dem sich Flaechenquelle D befindet
    image_d = np.zeros((pixel_quadrant, pixel_quadrant))
    # Dreieck 
    # Formel zur Berechnung der gleichseitigen Kantenlaenge a
    # jeden Pixel einzeln durchgehen
    # Hoehe h
    # y Richtung
    h_y = 60
    # x Richtung
    h_x = 10
    # Laenge der Pixel
    m = len(image_d)
    for i in range(m):
      for j in range(m):  
          delta_ay = h_y + i
          delta_ax = h_x + j
          if delta_ax <= delta_ay / np.sqrt(3):
              image_d[i, j] = np.random.poisson(100)



# Objekt C dem richtigen Platz des Szintigramms zuweisen
szinti[128:256, 128:256] = image_d


def get_image_A():
    """ Erzeugt Objekt A. """


def get_image_B():
    """ Erzeugt Objekt B. """


def get_image_C():
    """ Erzeugt Objekt C. """


def get_image_D():
    """ Erzeugt Objekt D. """




def plot_vorbereitung(ueberschrift, abszisse, ordinate):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechender Achsenbeschriftung etc. """
    fig = plt.figure(figsize=(10, 5))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    # Achsenbeschriftungen
    fig.xlabel(abszisse)
    fig.ylabel(ordinate)
    # erster Subplot
    ax1 = fig.add_subplot(221)
    # zweiter Subplot
    ax2 = fig.add_subplot(222)
    # dritter Subplot
    ax3 = fig.add_subplot(223)
    # vierter Subplot
    ax4 = fig.add_subplot(224)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.8])
    return ax1, ax2, ax3, ax4

# radioaktiven Zerfall bzw. Poisson-Statistik auf Verteilung anwenden

## Pixel fuer Image A
#in_x = (data[:, 1] > y_koord_li) * \
#    (uebers_photonen_detektor[:, 1] < y_koord_re)
#in_y = (uebers_photonen_detektor[:, 2] > z_koord_li) * \
#    (uebers_photonen_detektor[:, 2] < z_koord_re)
#uebers_photonen_detektor = uebers_photonen_detektor[in_z * in_y]
#




plt.imshow(szinti)




