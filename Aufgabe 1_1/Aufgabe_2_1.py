"""
    Aufgabe 2.1:
    Erstellt die Grauwertprofile fuer das Bild aus Aufgabe 1.1 laengs der
    Linien y = 60 mm und y = -60 mm.
    
    @author: Mieke Möller
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
    teil_array = array[y, :]
    return teil_array


def plot_vorbereitung_2sp(ueberschrift, unterueberschrift1, unterueberschrift2,
                          abszisse='', ordinate='', ticks=False):
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
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # zweiter Subplot
    ax2 = fig.add_subplot(122)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift2)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.9])
    # Position der Subplots untereinander veraendern:
    # vertikalen Abstand vergroeßern
    plt.subplots_adjust(wspace=0.3)
    # bei Bedarf Achsenbeschriftung mit Grid
    if ticks:
        ticks = np.linspace(-0.5, 0.5, 11)
        ax1.set_xticks(ticks)
        ax1.set_yticks(ticks)
        ax1.set_xticklabels(ticks, rotation=75)
        ax2.set_xticks(ticks)
        ax2.set_yticks(ticks)
        ax2.set_xticklabels(ticks, rotation=75)
    return ax1, ax2


def plot_2_1(xwerte1, grauwerte1, xwerte2, grauwerte2):
    """ Stellt Grauwertprofile fuer das Bild aus Aufgabe 1.1. längs
        bestimmter y- Linien dar.

        Parameter:
        ----------
        xwerte1, xwerte2: Abszissenwerte entlang bestimmter y- Linien.

        grauwerte1, grauwerte2: Grauwerte entlang bestimmter y- Linien.
    """
    ax1, ax2 = plot_vorbereitung_2sp('Grauwertprofile fuer das Bild aus ' +
                                 'Aufgabe 1.1', 'laengs y = 60',
                                 'laengs y = -60', r'$x/mm$',
                                 'Grauwert')
    ax1.plot(xwerte1, grauwerte1)
    ax2.plot(xwerte2, grauwerte2)
    plt.show()


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Extrahieren Grauwerte entlang von bestimmten y- Linien
    # (siehe Aufgabenstellung):
    # laengs y = 60, mit Umrechnung globales/lokales Koordinatensystem
    grauwertprofil_60 = extraktion_aus_array(szinti, pixel_quadrant - 60)
    # laengs y = -60, mit Umrechnung globales/lokales Koordinatensystem
    grauwertprofil_minus60 = extraktion_aus_array(szinti, pixel_quadrant + 60)
    # Plots: Erstellung Grauwertprofile
    plot_2_1(np.arange(-pixel_quadrant, pixel_quadrant), grauwertprofil_60,
             np.arange(-pixel_quadrant, pixel_quadrant),
             grauwertprofil_minus60)


if __name__ == "__main__":
    main()
