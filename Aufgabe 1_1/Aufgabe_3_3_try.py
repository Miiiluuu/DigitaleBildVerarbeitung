"""
    Aufgabe 3.3:
    Anwendung eines 3x3- Mittelwert-, 3x3- Median- und einem 3x3-Bionomial-
    filter am Bild aus Aufgabe 1.1.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_1
# TODO: doppelte Plot-Funktion?


def make_mittelwertfilter():
    """ Erstellung eines 3x3-Mittelwertfilters mit entsprechender Normierung
        (1 /9).
    """
    mittelwertfilter = (1 / 9) * np.ones((3, 3))
    return mittelwertfilter


def make_binfilter():
    """ Erstellung eines 3x3-Binomialfilters mit entsprechender Normierung
        (1 /16). Werte sind entnommen aus Pascalschen Dreieck.
    """
    binfilter = (1 / 16) * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    return binfilter


def filter_image(image, filter_art):
    """ Anwendung eines 3x3-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        filter_art: 3x3-Filter (-Array), welcher aufs Bild angewendet wird.
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
      

def medianfilter_image(image):
    """ Anwendung eines 3x3-Medianfilters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Schleife: jeden Pixel einzeln durchgehen (bis auf aeußersten Pixel
    # (-Rand)), da dieser von Filter nicht beruecksichtigt wird:
    # aeußeren Rand-Pixel werden auf Null gesetzt
    image_filter_median = np.zeros((len(image), len(image)))
    for x in range(1, len(image)-1):
        for y in range(1, len(image)-1):
            # Filterbereich, der einzeln (fuer jeden Pixel) wirksam wird (3x3)
            bereich = image[y-1:y+2, x-1:x+2]
            # Berechnung Medianwert in Filterbereich, Fuellen des
            # entsprechenden Pixels mit diesem medianen Wert
            image_filter_median[y, x] = np.median(bereich)
    return image_filter_median


def plot_vorbereitung(ueberschrift, sub_ueberschriften,
                      sub_ueberschrift_grau, abszisse,
                      ordinate):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        Ueberschrift, einzelnen Subplots etc. """
    # Erstellen von (vier) Subplots:
    fig, axs = plt.subplots(2, 4, figsize=(20, 10), facecolor='w')
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    axs = axs.ravel()
    # entsprechende Unterueberschriften der Subplots
    for i in range(4):
        axs[i].set_title(sub_ueberschriften[i])
    for i in range(4, 8):
        axs[i].set_title(sub_ueberschrift_grau)
        axs[i].set_xlabel(abszisse)
        axs[i].set_ylabel(ordinate)
    return axs


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Erstellung der Filter
    mittelwertfilter = make_mittelwertfilter(3)
    binfilter = make_binfilter()
    # Anwendung Filter aufs Bild aus Aufgabe 1.1:
    # Mittelwertfilter
    szinti_gefiltert_mittel = filter_image(szinti, mittelwertfilter)
    # Medianfilter
    szinti_filter_median = medianfilter_image(szinti)
    # Binomialfilter
    szinti_gefiltert_bin = filter_image(szinti, binfilter)
    # Plots:
    axs = plot_vorbereitung('Vergleich verschiedener Glaettungsverfahren',
                            ['Originalbild aus Aufgabe 1.1',
                            '3x3-Mittelwertfilter', '3x3-Medianfilter',
                            '3x3-Binomialfilter'],
                            'entsprechendes Grauwertprofile \n'
                            '- laengs y = 60 - ',
                            r'$x/mm$', 'Grauwert')
    # Plot (gefilterten) Bilder
    # Anlegen einer Liste
    bilder = [szinti, szinti_gefiltert_mittel, szinti_filter_median,
              szinti_gefiltert_bin]
    for i in range(4):
        axs[i].imshow(bilder[i], cmap='gray', extent=[-128, 128, -128, 128])
    # Erstellung Grauwertprofile entlang y-Linie = 60
    grauwertprofil_60_szinti = Aufgabe_2_1.extraktion_aus_array(szinti,
                                                    pixel_quadrant - 60)
    grauwertprofil_60_mittel = Aufgabe_2_1.extraktion_aus_array(szinti_gefiltert_mittel,
                                                    pixel_quadrant - 60)
    grauwertprofil_60_median = Aufgabe_2_1.extraktion_aus_array(szinti_filter_median,
                                                    pixel_quadrant - 60)
    grauwertprofil_60_bin = Aufgabe_2_1.extraktion_aus_array(szinti_gefiltert_bin,
                                                    pixel_quadrant - 60)
    # Plot Grauwertprofile
    # Anlegen einer Liste
    grauwertprofile = [grauwertprofil_60_szinti, grauwertprofil_60_mittel,
                       grauwertprofil_60_median, grauwertprofil_60_bin]
    for i in range(4):
        axs[i+4].plot((np.arange(-pixel_quadrant, pixel_quadrant)), grauwertprofile[i])


if __name__ == "__main__":
    main()

# Vergleich
    # Median Vgl Mittel: erhaelt Kanten, Artefakte in spitzwinkligen,
    # Robustheit gegen Ausreisser, effektiv gegen Salt-und-Pepper Rauschen
    # (hier eher Helligkeitsrauschen, auch ganz ok)
    # VGl allgemeine Eigenschaften von Glaettungsfiltern
    # Mittelwert: Reduzieren des Bildrauschens, Reduzieren der Kantensteilheit!
    # Grauwerthistogramme entlang bestimmter Linien darstellen?
    # um zu sehen, dass Kanten nicht mehr sooo bzw Glaetten
    # Binomial nicht so matschig da Gewicht auf mittleren Pixel hoeher, Mittel-
    # wert gibt jedem Pixel das Gewicht Eins
