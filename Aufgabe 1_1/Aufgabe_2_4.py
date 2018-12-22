"""
    Aufgabe 2.4:
    Berechnet den mittleren Informationsgehalt pro Pixel fuer das Bild aus
    Aufgabe 1.1.
    
    @author: Mieke Möller
"""

import numpy as np

import Aufgabe_1_1


def infogehalt(image):
    """ Berechnet den mittleren Informationsgehalt pro Pixel fuer ein
        Bild.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Histogrammverteilung (Ordinatenwerte des Histogramms) erstellen
    haufigkeiten, _ = np.histogram(image, bins=256)
    # Darstellung der relativen Haeufigkeitsverteilung
    # durch Normierung mit Anzahl der Bildpunkte
    haufigkeiten = haufigkeiten / np.sum(haufigkeiten)
    # Nullen aus relativer Histogrammverteilung entfernen
    haufigkeiten = haufigkeiten[haufigkeiten != 0]
    # Berechnung des Informationsgehaltes je Pixel entsprechend der Vorlesung,
    # Folie 39 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung
    info = np.sum(-haufigkeiten * np.log2(haufigkeiten))
    return info


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Informationsgehalt pro Pixel berechnen
    info = infogehalt(szinti)
    # Ausgabe des Informationsgehaltes pro Pixel fuer das Bild aus Aufgabe 1.1
    print(f'''Der mittlere Informationsgehalt pro ''' +
          f'''Pixel fuer das Bild aus Aufgabe 1.1 betraegt ''' +
          f'''{np.round(info, 3)} Bit/Pixel.''')


if __name__ == "__main__":
    main()
