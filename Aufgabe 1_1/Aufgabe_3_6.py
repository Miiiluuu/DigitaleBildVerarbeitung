"""
    Aufgabe 3.6:
    Separierung der Flaechenquelle D im Bild aus Aufgabe 1.1 (mittels
    Schwellwertverfahren).
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_2
import Aufgabe_3_3
# TODO: doppelte Plot-Funktion? Figuresize


def berechnung_flaeche_dreieck(hoehe):
    """ Berechnung der Flaeche eines Dreieckes 'dreieck' in Pixeln.

        Parameter:
        ----------
        hoehe: Hoehe des gleicheitigen Dreiecks in mm.
    """
    # Berechnung der Seitenlaenge a eines gleichseitigen Dreiecks aus der Hoehe
    a = 2 * hoehe / np.sqrt(3)
    # Berechnung des Flaecheninhaltes eines gleichseitigen Dreiecks aus der
    # Seitenlaenge a
    flaeche = np.sqrt(3) * a**2 / 4     # Einheit: in mm² bzw Anzahl Pixel, da
                                        # 1 Pixel 1 mm² entspricht
    return flaeche


def berechnung_flaeche_rechteck(deltax, deltay):
    """ Berechnung der Flaeche eines Rechteckes 'rechteck' in Pixeln.

        Parameter:
        ----------
        hoehe: Hoehe des gleicheitigen Dreiecks in mm.
    """
    flaeche = deltax * deltay           # Einheit: in mm² bzw Anzahl Pixel, da
                                        # 1 Pixel 1 mm² entspricht
    return flaeche


def seek_schwellwert(flaeche):
    """ Funktion bestimmt Schwellwert zur Extraktion bestimmter zu
        segmentierender Objekte, ausgehend von deren (bekannter) Flaeche.
    
    sucht in einem Bild 'image', ob dessen Haufigkeitsverteilung
        einen Bereich desselben Grauwertes besitzt, wobei dieser Bereich einem
        bestimmten Flaecheninhalt entspricht und separiert dieses Objekt. 

        Parameter:
        ----------
        image: Array, Eingabewerte.
        
        flaeche: Flaecheninhalt in Anzahl an Pixeln eines bestimmten Objektes.
    """





#def separiere_objekt(image, flaeche):
#    """ Funktion sucht in einem Bild 'image', ob dessen Haufigkeitsverteilung
#        einen Bereich desselben Grauwertes besitzt, wobei dieser Bereich einem
#        bestimmten Flaecheninhalt entspricht und separiert dieses Objekt. 
#
#        Parameter:
#        ----------
#        image: Array, Eingabewerte.
#        
#        flaeche: Flaecheninhalt in Anzahl an Pixeln eines bestimmten Objektes.
#    """
#    # Berechnung der Haeufigkeitsverteilung
#    ordinate, _, _ = plt.hist(image.flatten(), bins=256, density=True)
#    # Bereich finden, der denselben Grauwert  bzw lamda 100 von
#    # Poissonverteilung besitzt und gleichzeitig bestimmter Flaeche in Anzahl
#    # Pixeln eines gleichseitigen Dreieck entspricht
#    # TODO: Derselbe Grauwert, ohne dessen Kenntniss vorauszusetzen?
#    if (... lambda richtig mit Abweichung < np.exp(-17)) and
#        np.sum(DIESER ordinaten-Werte) = flaeche (mit geringem Fehler):
#            # Wenn Bedingung zutrifft, wird dieser Ordinatenwert beibehalten,
#            # alle anderen Ordinatenwerte werden auf Null gesetzt
#            # Umkehrfunktion von hist, um Bild wieder darzustellen
#            # aus Histgramm?
#    # Look-Up-Table
#    return objekt_separiert
   
    
def plot(ueberschrift, image):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Subplots, Ueberschriften etc.

        Parameter:
        ----------
        image: Array, Eingabewerte, welche im Plot dargestellt werden.
    """
    fig = plt.figure(figsize=(6, 7))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    plt.imshow(image, cmap='gray', extent=[-128, 128, -128, 128])


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
#    # Berechnung des Flaecheninhaltes des zu separierenden Objektes
#    # (≙ Flaechenquelle D aus Aufgabe 1.1, gleichseitiges Dreieck)
#    flaeche_quelleD = berechnung_flaeche_dreieck(100)
#    # Separiere diese Flaechenquelle D aus dem Bild aus Aufgabe 1.1
#    quelleD_separiert = separiere_objekt(szinti, flaeche_quelleD)
#    # Plot
#    plot('Schwellwertverfahren \n'
#         '-Separierung von Flaechenquelle D des Bildes aus Aufgabe 1.1-', 
#         quelleD_separiert)
    # vor Anwendung Schwellwertverfahren (a priori) Glaettung mit 
    # Medianfilter zur Erzeugung zusammenhaengender Gebiete, Löcher in
    # Flächen teilweise aufgefuellt
    szinti_filter_med = Aufgabe_3_3.filter_image(szinti)
    # Darstellung des Grauwerthistogramms
    Aufgabe_2_2.erstelle_grauwerthistogramm_abgeschnitten('Grauwerthistogramm',
                                'fuer Bild aus Aufgabe 1.1, ' +
                                'gekuerzte Ordinatenachse', r'$f$',
                                'Häufigkeitsverteilung $h(f)$',
                                szinti_filter_med.flatten())
    # aus der a priori Kenntnis von Flaechenquelle D (mittlere flaechenbezogene
    # Zahl der registrierten Ereignisse 100 mm², siehe Vorlesung zu
    # Modul MF-MRS_14 Digitale Bildverarbeitung, Aufgabe 1.1 (Folie 17))
    # werden aus (geglaetteten) Grauwerthistogramm Schwellwerte visuell
    # entnommen (sodass Gesamt-segmentierungsfehler möglichst gering)
    szinti_filter_med[50 <= ]
    


if __name__ == "__main__":
    main()

# TDO: externe Console bzw Windowkonsole funktioniert nicht?

# Interpretation:
    # Laplace: Hochpass zum Hervorheben strukturreicher Bildbereiche, da
    # diese kruemmungsempfindlich sind
    # Unterschiede zu Gradientenfiltern (aus Aufgabe 3.4): nutzen 2. Ableitung,
    # welche rauschanfaelliger ist als bei Nutzen erster Ableitung
