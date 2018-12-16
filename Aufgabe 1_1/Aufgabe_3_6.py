"""
    Aufgabe 3.6:
    Separierung der Flaechenquelle D im Bild aus Aufgabe 1.1 (mittels
    Schwellwertverfahren).
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_3_3
# TODO: doppelte Plot-Funktion? Figuresize


def use_schwellwert(image, schwelle_unten, schwelle_oben):
    """ Funktion segmentiert mittels Schwellwertverfahren und a priori
        Kenntnisse einen bestimmten Bereich.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        schwelle_unten: unterer Schwellwert. Bis zu dieser Graustufe wird
        Grauwertverteilung als Objekt gezaehlt.

        schwelle_oben: oberer Schwellwert. Bis zu dieser Graustufe wird
        Grauwertverteilung als Objekt gezaehlt.
    """
    # Anlegen eines Null-Arrays, welches Maske enthaelt:
    # Nullen: Pixel wird als Nichtobjekt klassifiziert
    # andere Grauwerte: Pixel wird als Objekt klassifiziert
    image_maske = np.zeros_like(image)
    # reinspeichern der Ursprungsgrauwerte in diese Pixel, welche unter der
    # Schwelle liegen
    # Schwellwertbedingung: in welchem Intervall liegen Objektpixel?
    intervall_schwellen = (image >= schwelle_unten) * (image <= schwelle_oben)
    image_maske[intervall_schwellen] = image[intervall_schwellen]
    return image_maske


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # vor Anwendung Schwellwertverfahren (a priori) Glaettung mit
    # Medianfilter zur Erzeugung zusammenhaengender Gebiete, Löcher in
    # Flächen teilweise aufgefuellt
    szinti_bearbeitet = Aufgabe_3_3.filter_image(szinti)
    # aus der a priori Kenntnis von Flaechenquelle D (mittlere flaechenbezogene
    # Zahl der registrierten Ereignisse 100 mm², siehe Vorlesung zu
    # Modul MF-MRS_14 Digitale Bildverarbeitung, Aufgabe 1.1 (Folie 17))
    # werden aus (geglaetteten) Grauwerthistogramm Schwellwerte visuell
    # entnommen (sodass Gesamt-segmentierungsfehler möglichst gering)
    szinti_bearbeitet = use_schwellwert(szinti_bearbeitet, 50, 100)
    # Darstellung der separierten Flaechenquelle D (Dreieck)
    plt.figure()
    plt.imshow(szinti_bearbeitet, cmap='gray', extent=[-128, 128, -128, 128],
               vmax=255)


if __name__ == "__main__":
    main()
