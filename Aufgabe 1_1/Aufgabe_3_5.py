"""
    Aufgabe 3.5:
    Anwendung des Laplace-Filters (mit einer 8er Nachbarschaft) auf das
    Bild aus Aufgabe 1.1.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_3_3


def make_laplacefilter():
    """ Erstellung eines Laplacefilters mit einer 8er-Nachbarschaft.
    """
    laplace = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    return laplace


def plot(ueberschrift, image):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Figure mit
        Ueberschriften etc.

        Parameter:
        ----------
        image: Array, Eingabewerte, welche im Plot dargestellt werden.
    """
    fig = plt.figure(figsize=(6, 7))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    plt.imshow(image, cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Erstellung Laplace-Filter mit 8er Nachbarschaft
    laplacefilter = make_laplacefilter()
    # Anwendung Laplacefilter aufs Bild aus Aufgabe 1.1
    szinti_laplace = Aufgabe_3_3.use_filter3x3_image(szinti, laplacefilter)
    # Plot des Bildes aus Aufgabe 1.1 nach Anwendung eines Laplacefilters
    # mit einer 8er Nachbarschaft
    plot('Anwendung eines Laplacefilters (8er Nachbarschaft) \n'
         'auf das Bild aus Aufgabe 1.1', szinti_laplace)


if __name__ == "__main__":
    main()

# Interpretation:
    # Laplace: Summe partielle zweite Ableitungen nach x und y Richtung
    # strukturreiche Bereiche werden hervorgehoben (da krümmungsempfindlicher),
    # weniger strukturreiche
    # Bereiche unterdrueckt
    # Hochpasseigenschaften (niedrige Frequenzen unterdrueckt)
    # Unterschiede zu Gradientenfiltern (aus Aufgabe 3.4): nutzen 2. Ableitung
    # statt erster,
    # welche rauschanfaelliger ist als bei Nutzen erster Ableitung
