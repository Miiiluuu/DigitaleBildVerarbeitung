"""
    Aufgabe 3.4:
    Anwendung des Sobel- und Robertsfilters auf das Bild aus Aufgabe 1.1.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_1
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


def filter3x3_image(image, filter_art):
    """ Anwendung eines 3x3-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        filter_art: Beschreibt 3x3-Filter (-Array), welcher auf das Bild
        image angewendet wird. Falls Argument nicht angegeben, (es wird
        keine Filterart ausgewaehlt), wird fuer das image ein 3x3-Medianfilter
        benutzt. Bei Auswahl eines Argumentes filter_art wird dieser fuer das
        Filtern des Bildes verwendet.
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
    plt.tight_layout(rect=[0, 0.03, 1, 1.1])
    return ax1, ax2


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # ANwendung Sobelfilter aufs Bild aus Aufgabe 1.1
    szinti_sobel_ges = filter_sobel_image(szinti)
    ax1, ax2 = plot2_vorbereitung("_", "_", "_")
    ax1.imshow(szinti_sobel_ges, cmap='gray', extent=[-128, 128, -128, 128])

if __name__ == "__main__":
    main()

