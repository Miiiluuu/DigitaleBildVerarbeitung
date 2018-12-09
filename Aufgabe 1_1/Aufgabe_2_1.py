"""
    Aufgabe 2.1:
    Erstellt die Grauwertprofile fuer das Bild aus Aufgabe 1.1 laengs
    bestimmter y- Linien.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1


def extraktion_aus_array(array, y):
    """ Extrahiert für eine entsprechenden Ordinatenwertlinie alle
        dazugehörigen (Grau-)Werte.

        Parameter:
        ----------
        array: Array, Eingabewerte.

        y: Ordinatenwert, bei dem alle dazugehoerigen Abszissenwerte
        extrahiert werden.
    """
    # TODO: nur globalen Wert eintippen??
    teil_array = array[y, :]
    return teil_array


def plot_vorbereitung(ueberschrift, unterueberschrift1, unterueberschrift2,
                      abszisse1, ordinate1, abszisse2, ordinate2):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Ueberschriften, Achsenbeschriftung etc.
    """
    fig = plt.figure(figsize=(10, 5))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    # erster Subplot
    ax1 = fig.add_subplot(121)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift1)
    # Achsenbeschriftungen
    plt.xlabel(abszisse1)
    plt.ylabel(ordinate1)
    # zweiter Subplot
    ax2 = fig.add_subplot(122)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift2)
    # Achsenbeschriftungen
    plt.xlabel(abszisse2)
    plt.ylabel(ordinate2)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.9])
    return ax1, ax2


def plot(xwerte1, grauwerte1, xwerte2, grauwerte2):
    """ Stellt Grauwertprofile fuer das Bild aus Aufgabe 1.1. längs
        bestimmter y- Linien dar.

        Parameter:
        ----------
        xwerte1, xwerte2: Abszissenwerte entlang bestimmter y- Linien.

        grauwerte1, grauwerte2: Grauwerte entlang bestimmter y- Linien.
    """
    # TODO: Achsenbeschriftungen allgemeiner machen bzw was mit {}
    # reinschreiben!!!
    ax1, ax2 = plot_vorbereitung('Grauwertprofile fuer das Bild aus ' +
                                 'Aufgabe 1.1', 'laengs y = 60',
                                 'laengs y = -60', r'$x/mm$',
                                 'Grauwert', r'$x/mm$',
                                 'Grauwert')
    ax1.plot(xwerte1, grauwerte1)
    ax2.plot(xwerte2, grauwerte2)

    plt.show


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Extrahieren Grauwerte entlang von bestimmten y- Linien
    # (siehe Aufgabenstellung)
    # laengs y = 60, mit Umrechnung Koordinaten
    grauwertprofil_60 = extraktion_aus_array(szinti, pixel_quadrant - 60)
    # laengs y = -60, mit Umrechnung Koordinaten
    grauwertprofil_minus60 = extraktion_aus_array(szinti, pixel_quadrant + 60)
    # Plots: Erstellung Grauwertprofile
    plot(np.arange(-pixel_quadrant, pixel_quadrant), grauwertprofil_60,
         np.arange(-pixel_quadrant, pixel_quadrant), grauwertprofil_minus60)


if __name__ == "__main__":
    main()
