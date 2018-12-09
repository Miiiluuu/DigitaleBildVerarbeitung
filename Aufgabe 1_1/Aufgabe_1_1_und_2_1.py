"""
    Darstellung eines aufgenommenen Szintigramms, bestehend aus 256x256 Pixel,
    aufgebaut aus vier Flaechenquellen (weitere Parameter siehe Vorlesung zu
    Modul MF-MRS_14 Digitale Bildverarbeitung)
"""

# Aufgabe 1.1.

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1


def extraktion_aus_array(array, y):
    """ Extrahiert für einen entsprechenden Ordinatenwert alle dazugehörigen
        Werte der Abszisse.

        Parameter:
        ----------
        y: Ordinatenwert, bei dem alle dazugehoerigen Abszissenwerte
        extrahiert werden.
    """
    # TODO: nur globalen Wert eintippen??
    teil_array = array[y, :]
    return teil_array


def plot_vorbereitung(ueberschrift, unterueberschrift1, unterueberschrift2,
                      abszisse1, ordinate1, abszisse2, ordinate2):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechender Achsenbeschriftung etc. """
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


def plot(xwerte1, ywerte1, xwerte2, ywerte2):
    """ Stellt Grauwertprofile fuer das Bild aus Aufgabe 1.1. längs
        bestimmter y- Linien dar.
    """
    ax1, ax2 = plot_vorbereitung('Grauwertprofile', 'laengs y = 60',
                                 'laengs y = -60', r'$x/mm$', r'$y/mm$',
                                 r'$x/mm$', r'$y/mm$')
    ax1.plot(xwerte1, ywerte1)
    ax2.plot(xwerte2, ywerte2)

    plt.show


def main():
    # Aufruf Aufgabe 1.1
    szinti, pixel_quadrant = Aufgabe_1_1.make_szinti()

    # Aufgabe 2.1.
    # Extrahieren Abszissenwerte entlang von bestimmten y- Linien
    # (siehe Aufgabenstellung)
    grauwertprofil_60 = extraktion_aus_array(szinti, pixel_quadrant - 60)
    grauwertprofil_minus60 = extraktion_aus_array(szinti, pixel_quadrant + 60)
    # Plots
    ordinate_60 = np.ones(len(grauwertprofil_60))*60
    ordinate_minus60 = np.ones(len(grauwertprofil_60))*-60
    plot(np.arange(-128, 128), grauwertprofil_60,
         np.arange(-128, 128), grauwertprofil_minus60)


main()

print("aaa")
