"""
    Aufgabe 3.4:
    Anwendung des Sobel- und Robertsfilters auf das Bild aus Aufgabe 1.1.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_1
import Aufgabe_3_3


def make_sobelfilter_x_y():
    """ Erstellung eines 3x3-Sobelfilters, einzeln zur Kantenextraktion in x-
        und in y-Richtung.
    """
    # in x-Richtung
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    # in y-Richtung
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    return sobel_x, sobel_y


def filter_sobel_image(image):
    """ Anwendung eines 3x3-Sobel-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Erstellen der Sobelfilter in x- und y-Richtung
    sobel_x, sobel_y = make_sobelfilter_x_y()
    # Anwendung der Sobelfilter in x- und y-Richtung auf das 'image'
    image_sobel_x = Aufgabe_3_3.use_filter3x3_image(image, sobel_x)
    image_sobel_y = Aufgabe_3_3.use_filter3x3_image(image, sobel_y)
    # Bildung des Gradienten: Wirkung des gesamten Filters (sowohl x- als auch
    # y-Richtung), entsprechend Vorlesung Folien 154f des Modul
    # MF-MRS_14 Digitale Bildverarbeitung)
    image_sobel_ges = np.abs(image_sobel_x) + np.abs(image_sobel_y)
    return image_sobel_ges


# TODO: Richtig?
def robertsfilter(image):
    """ Anwendung eines Roberts-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    image_robert = np.zeros((len(image), len(image)))
    # Berechnung nach Differenzverfahren entsprechend der Vorlesung,
    # Folie 43f aus dem Modul MF-MRS_14 Digitale Bildverarbeitung
    for x in range(len(image)-1):
        for y in range(len(image)-1):
            image_robert[y, x] = np.abs(image[y, x] - image[y+1, x+1]) + \
                                 np.abs(image[y, x+1] - image[y+1, x])
    return image_robert


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Anwendung Sobelfilter aufs Bild aus Aufgabe 1.1
    szinti_sobel_ges = filter_sobel_image(szinti)
    # Anwendung Roberts-Filter aufs Bild aus Aufgabe 1.1
    szinti_robert = robertsfilter(szinti)
    # Subplots erstellen fuer graphische Darstellung
    ax1, ax2 = Aufgabe_2_1.plot_vorbereitung_2sp("verschiedene Filter zur " +
                                                 "Kantenextraktion",
                                                 "Sobel-Filter",
                                                 "Roberts-Filter")
    # Plot Sobelfilter
    ax1.imshow(szinti_sobel_ges, cmap='gray', extent=[-128, 128, -128, 128])
    # Plot Robertsfilter
    ax2.imshow(szinti_robert, cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()


if __name__ == "__main__":
    main()

# Interpretation:
    # Kantenextraktion:
    # dafuer Bildung der ersten Ableitung aus zwei orthogonalen Richtungen
    # und Gradientenbildbestimmung (siehe Vorlesung)
    # Sobel drei Zeilen: Gradient ueber 3 Zeilen
    # Robertsfilter besitzt kleinere Matrix (2x2),
    # bezieht fuer
    # Kantenextraktion
    # kleineren Bereich mit ein, d.h. Sobel rauschunempfindlicher
    # Robert bildet Differenzen in Richtungen 45° und 135° (diagonal)
    # Sobel bildet Differenzen in horizontaler und vertikaler Richtungen
    # Sobel und Robert haben Richtungsabhaengigkeit
    # aber: fuer Kantenfilter gilt Isotropie: Filterantwort soll nicht von der
    # Richtung der Kante abhaengen: beide Filter sehen in etwa gleich aus
    # Sobel mehr Mittelung daher Robert schaerfer
