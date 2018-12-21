"""
    Aufgabe 2.2:
    Erstellt das Grauwerthistogramm des Bildes aus Aufgabe 1.1 und stellt es
    graphisch dar.
    
    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_1

def erstelle_grauwerthist(werte):
    """ Erstellung Grauwertprofil, Darstellung auf zwei Weisen:
        1. logarithmischer Skaleneinteilung,
        2. Zur besseren Darstellung kleinerer Werte ist Ordinatenachse bei
        bestimmten Wert abgeschnitten.

        Parameter:
        ----------
        werte: Array, Eingabewerte
    """
    ax1, ax2 = Aufgabe_2_1.plot_vorbereitung("Grauwerthistogramm fuer das " +
                                "Bild aus Aufgabe 1.1", 'logarithmische Skala',
                                'gekuerzte Ordinatenachse', r'$f$',
                                'Häufigkeitsverteilung $h(f)$', r'$f$',
                                'Häufigkeitsverteilung $h(f)$')
    ax1.hist(werte, bins=256, density=True, log=True)
    ordinate, _, _ = ax2.hist(werte, bins=256, density=True)
    # Ordinatenwerte sortieren
    ordinate_sort = np.sort(ordinate)
    # Ordinatenachse kuerzen
    plt.ylim(0, ordinate_sort[-2] * 1.1)
    # Position der Subplots untereinander veraendern:
    # vertikalen Abstand vergroeßern
    plt.subplots_adjust(wspace=0.3)
    plt.show()


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Grauwerthistogramm zeichnen:
    erstelle_grauwerthist(szinti.flatten())


if __name__ == "__main__":
    main()

