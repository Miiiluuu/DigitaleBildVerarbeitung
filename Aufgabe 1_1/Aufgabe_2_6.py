"""
    Aufgabe 2.6:
    Berechnet aus Aufgabe 1.1 ein Differenzbild. Von diesem Differenzbild
    wird ein Histogramm erzeugt sowie dessen mittlerer Informationsgehalt
    ermittelt und dem Originalbild vergleichend gegenuebergestellt.
"""

import numpy as np
from prettytable import PrettyTable

import Aufgabe_1_1
import Aufgabe_2_2
import Aufgabe_2_4


def differenzbild(image):
    """ Funktion erstellt ein Differenzbild.
        
        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    differenz_image = np.zeros((len(image), len(image)))
    # Berechnung nach Differenzverfahren entsprechend der Vorlesung,
    # Folie 43f aus dem Modul MF-MRS_14 Digitale Bildverarbeitung
    for x in range(len(image)):
        for y in range(len(image)):
            differenz_image[y, x] = image[y, x] - image[y, x-1]
    # Addieren einer Konstanten auf alle Pixel, um negative Grauwerte zu
    # vermeiden
    konstante = np.absolute(np.amin(differenz_image))
    differenz_image += konstante
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    differenz_image = Aufgabe_1_1.make_scale(differenz_image)
    return differenz_image


def vgl_infogehalt_differenz(bild1, bild2, info1, info2):
    """ Stellt den mittleren Informationsgehalt pro Pixel fuer 2 Bilder
        in einer Tabelle vergleichend gegenueber.

        Parameter:
        ----------
        bild1: Array, Eingabewerte fuer ein Bild1.
        
        bild2: Array, Eingabewerte fuer ein Bild2.
        
        info1: mittlerer Informationsgehalt je Pixel fuer ein Bild1.
        
        info2: mittlerer Informationsgehalt je Pixel fuer ein Bild2.
    """
    # Erstellung PrettyTable
    x = PrettyTable()
    x.field_names = ['Bild', 'mittlerer Informationsgehalt in ' +
                     'Bit/Pixel']
    x.add_row([bild1, info1])
    x.add_row([bild2, info2])
    print(x)        
    

def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Plot Histogramm fuer Originalbild aus Aufgabe 1.1
    Aufgabe_2_2.erstelle_grauwerthist(szinti.flatten(),
                                      "das Bild aus Aufgabe 1.1")
    # Erstellung Differenzbild
    differenz = differenzbild(szinti)
    # Plot Histogramm des Differenzbildes
    Aufgabe_2_2.erstelle_grauwerthist(differenz.flatten(),
                                      "das Differenzbild")
    # Berechnung mittlerer Informationsgehalt pro Pixel fuer das Originalbild
    info_original = Aufgabe_2_4.infogehalt(szinti)
    # Berechnung mittlerer Informationsgehalt pro Pixel fuer das
    # Differenzbild
    info_differenz = Aufgabe_2_4.infogehalt(differenz)
    # Gegenueberstellung der beiden Informationsgehalte in einer Tabelle
    vgl_infogehalt_differenz('Original', 'Differenz',
                             np.round(info_original, 3),
                             np.round(info_differenz, 3))


if __name__ == "__main__":
    main()
    
    # Interpretation:
    # Differenz entspricht Kompression: eigentlich verlustfrei
    # das heißt Infogehalt muesste derselbe sein?
    # Eliminierung redundanter Bildinformationen
    # Wiederherstellung des Originalbildes i.a. moeglich
    # Sinn: durch Bildung der Differenz muessen nur noch kleine Zahlenwerte
    # abgespeichert werden
    # aber laut Tabelle: Differenzbild weißt weniger Infogehalt auf
    # laut Formel: bei benachbarten Pixeln mit denselben Grauwerten
    # ergibt sich als Differenz Null
    # das heißt wirkliche Bildinformationen treten nur an Kanten/ starken
    # Bildkontrasten auf
    # auf spitze Form des Histogramms eingehen:
    # viele relativ kleine/ mittlere Werte werden abgespeichert im
    # Differenzbild, keine hohen Farbwerte (da Differenzbildung)
    # Infogehalt ist pro Pixel
    # bei Differenzbild ist zwischen einzelnen Pixeln eine mathematische
    # Abhaengigkeit, bei Originalbild sind Pixel voneinander unabhaengig.
    # das heißt PRO Pixel ist es bei Differenz niedriger