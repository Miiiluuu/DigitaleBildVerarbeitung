"""
    Aufgabe 2.3:
    Berechnet Mittelwert und Schiefe des Grauwert-Histogramms aus Aufgabe 2.2.

    @author: Mieke Möller
"""

import numpy as np

import Aufgabe_1_1


def mittelwert_grauwerthist(ordinate, abszisse):
    """ Berechnet den Mittelwert eines Grauwert-Histogramms.

        Parameter:
        ----------

        ordinate: relative Histogrammverteilung (Ordinatenwerte des
        Histogramms).

        abszisse: Grauwerte (Abszisse) des Grauwert-Histogramms.
    """
    # Berechnung vom  Mittelwertes des Grauwert-Histogramms entsprechend
    # der Vorlesung, Folie 33 aus dem Modul MF-MRS_14 Digitale
    # Bildverarbeitung
    avg_hist = np.sum(abszisse * ordinate)
    print(f'''Der Mittelwertes des Grauwert-Histogramms des Szintigramms ''' +
          f'''betraegt {np.round(avg_hist, 3)}.''')
    return avg_hist


def schiefe_grauwerthist(ordinate, abszisse, mittel):
    """ Berechnet die Schiefe eines Grauwert-Histogramms.

        Parameter:
        ----------

        ordinate: relative Histogrammverteilung (Ordinatenwerte des
        Histogramms).

        abszisse: Grauwerte (Abszisse) des Grauwert-Histogramms.

        mittel: Mittelwert des Grauwert-Histogramms.
    """
    # Berechnung der Schiefe des Grauwert-Histogramms entsprechend
    # der Vorlesung, Folie 34 aus dem Modul MF-MRS_14 Digitale
    # Bildverarbeitung:
    # Berechnen der Varianz des Grauwert-Histogramms
    varianz = np.sum(ordinate * (abszisse - mittel)**2)
    drittes_moment = np.sum(ordinate * (abszisse - mittel)**3)
    schiefe = drittes_moment / varianz**(3 / 2)
    print(f'''Die Schiefe des Grauwert-Histogramms aus dem Szintigramm''' +
          f'''betraegt {np.round(schiefe, 3)}.''')


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # relative Histogrammverteilung aus dem Bild aus Aufgabe 1.1
    # (Ordinatenwerte des Grauwerthistogramms) erstellen
    haufigkeit, _ = np.histogram(szinti, bins=256, density=True)
    # Grauwerte (Abszisse) des Grauwert-Histogramms
    grauwerte = np.arange(pixel)
    # Mittelwert des Grauwertdiagramms aus Aufgabe 2.2 berechnen
    avg_hist = mittelwert_grauwerthist(haufigkeit, grauwerte)
    # Schiefe des Grauwertdiagramms aus Aufgabe 2.2 berechnen
    schiefe_grauwerthist(haufigkeit, grauwerte, avg_hist)


if __name__ == "__main__":
    main()
