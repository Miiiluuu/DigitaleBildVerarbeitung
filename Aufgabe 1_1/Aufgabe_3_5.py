"""
    Aufgabe 3.5:
    Anwendung des Laplace-Filters (mit einer 8er Nachbarschaft) auf das
    Bild aus Aufgabe 1.1.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
# TODO: doppelte Plot-Funktion? Figuresize


def make_laplacefilter():
    """ Erstellung eines Laplacefilters mit einer 8er-Nachbarschaft.
    """
    laplace = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    return laplace


def filter3x3_image(image, filter_art):
    """ Anwendung eines 3x3-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        filter_art: Beschreibt 3x3-Filter (-Array), welcher auf das Bild
        image angewendet wird.
    """
    # Schleife: jeden Pixel einzeln durchgehen (bis auf aeußersten Pixel
    # (-Rand)), da dieser von Filter nicht beruecksichtigt wird:
    # aeußeren Rand-Pixel werden auf Null gesetzt
    image_gefiltert = np.zeros((len(image), len(image)))
    for x in range(1, len(image)-1):
        for y in range(1, len(image)-1):
            # Filterbereich, der einzeln (fuer jeden Pixel) wirksam wird (3x3)
            bereich = image[y-1:y+2, x-1:x+2]
            # Anwendung Filter auf Filterbereich
            bereich_filter = bereich * filter_art
            # Fuellen des entsprechenden Pixels mit neuem gefilterten Wert
            image_gefiltert[y, x] = np.sum(bereich_filter)
    return image_gefiltert


def plot(ueberschrift, image):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Subplots, Ueberschriften etc.

        Parameter:
        ----------
        image: Array, Eingabewerte, welche im Plot dargestellt werden.
    """
    fig = plt.figure(figsize=(6, 7))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    plt.imshow(image, cmap='gray', extent=[-128, 128, -128, 128])


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Erstellung Laplace-Filter mit 8er Nachbarschaft
    laplacefilter = make_laplacefilter()
    # Anwendung Laplacefilter aufs Bild aus Aufgabe 1.1
    szinti_laplace = filter3x3_image(szinti, laplacefilter)
    # Plot des Bildes aus Aufgabe 1.1 nach Anwendung eines Laplacefilters
    # mit einer 8er Nachbarschaft
    plot('Anwendung eines Laplacefilters (8er Nachbarschaft) \n'
         'auf das Bild aus Aufgabe 1.1', szinti_laplace)


if __name__ == "__main__":
    main()

# TDO: externe Console bzw Windowkonsole funktioniert nicht?

# Interpretation:
    # Laplace: Summe partielle zweite Ableitungen nach x und y Richtung
    # strukturreiche Bereiche werden hervorgehoben (da krümmungsempfindlicher),
    # weniger strukturreiche
    # Bereiche unterdrueckt
    # Hochpasseigenschaften (niedrige Frequenzen unterdrueckt)
    # Unterschiede zu Gradientenfiltern (aus Aufgabe 3.4): nutzen 2. Ableitung
    # statt erster,
    # welche rauschanfaelliger ist als bei Nutzen erster Ableitung
