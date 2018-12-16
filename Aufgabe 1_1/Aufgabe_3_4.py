"""
    Aufgabe 3.4:
    Anwendung des Sobel- und Robertsfilters auf das Bild aus Aufgabe 1.1.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
# TODO: doppelte Plot-Funktion? Figuresize


def make_sobelfilter_x_y():
    """ Erstellung eines Sobelfilters, einzeln zur Kantenextraktion in x- und
        in y-Richtung.
    """
    # in x-Richtung
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    # in x-Richtung
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    return sobel_x, sobel_y


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


def filter_sobel_image(image):
    """ Anwendung eines Sobel-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Erstellen der Sobelfilter in x- und y-Richtung
    sobel_x, sobel_y = make_sobelfilter_x_y()
    # Anwendung der Sobelfilter in x- und y-Richtung auf das 'image'
    image_sobel_x = filter3x3_image(image, sobel_x)
    image_sobel_y = filter3x3_image(image, sobel_y)
    # Wirkung des gesamten Filters (sowohl x- als auch y-Richtung),
    # entsprechend Vorlesung Folien 154f des Modul
    # MF-MRS_14 Digitale Bildverarbeitung)
    image_sobel_ges = np.abs(image_sobel_x) + np.abs(image_sobel_y)
    return image_sobel_ges


def robertsfilter(image):
    """ Anwendung eines Roberts-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Nullarray anlegen, TODO: Annahme das quadratisches Eingangsarray...
    # Aendern?
    image_robert = np.zeros((len(image), len(image)))
    # Berechnung nach Differenzverfahren entsprechend der Vorlesung,
    # Folie 43f aus dem Modul MF-MRS_14 Digitale Bildverarbeitung
    for x in range(len(image)-1):
        for y in range(len(image)-1):
            image_robert[y, x] = np.abs(image[y, x] - image[y+1, x+1]) + \
                                 np.abs(image[y, x+1] - image[y+1, x])
    return image_robert

# TODO: Grenzen richtig?


def plot2_vorbereitung(ueberschrift, unterueberschrift1, unterueberschrift2):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Subplots, Ueberschriften etc. """
    fig = plt.figure(figsize=(9, 10))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    # erster Subplot
    ax1 = fig.add_subplot(121)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift1)
    # zweiter Subplot
    ax2 = fig.add_subplot(122)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift2)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 1.35])
    return ax1, ax2


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Anwendung Sobelfilter aufs Bild aus Aufgabe 1.1
    szinti_sobel_ges = filter_sobel_image(szinti)
    # Anwendung Roberts-Filter aufs Bild aus Aufgabe 1.1
    szinti_robert = robertsfilter(szinti)
    # Plots
    ax1, ax2 = plot2_vorbereitung("verschiedene Filter zur Kantenextraktion",
                                  "Sobel-Filter", "Roberts-Filter")
    ax1.imshow(szinti_sobel_ges, cmap='gray', extent=[-128, 128, -128, 128])
    ax2.imshow(szinti_robert, cmap='gray', extent=[-128, 128, -128, 128])


if __name__ == "__main__":
    main()

# TDO: externe Console bzw Windowkonsole funktioniert nicht?
    
# Interpretation:
    # Kantenextraktion:
    # Bildung der ersten Ableitung aus zwei orthogonalen Richtungen
    # und damit Gradientenbildbestimmung (siehe Vorlesung)
    # Sobel drei Zeilen: Gradient ueber 3 Zeilen, damit rauschunempfindlicher
    # Robertsfilter besitzt kleinere Matrix (2x2),
    # Robert bildet Differenzen in Richtungen 45° und 135° (diagonal)
    # bezieht fuer
    # Kantenextraktion
    # kleineren Bereich mit ein, d.h. Sobel rauschunempfindlicher
    # fuer Kantenfiilter gilt Isotropie: Filterantwort soll nicht von der
    # Richtung der Kante abhaengen: beide Filter sehen in etwa gleich aus
    # Sobel bildet Differenzen in horizontaler und vertikaler Richtungen
    # d.h. wirkt am staerksten auf horizontale und vertikale Grauwertkanten
    # Sobel und Robert haben Richtungsabhaengigkeit


