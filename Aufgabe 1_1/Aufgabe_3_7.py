"""
    Aufgabe 3.6:
    Extrahieren des rechten unteren Quadranten des Bild aus Aufgabe 1.1
    (Flaechenquelle D, gleichseitiges Dreieck) als Teilbild. Dabei Durchführung
    einer Kantenextraktiion mit anschließender Hough-Transformation.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_3_4
import Aufgabe_2_2
import Aufgabe_3_3


def berechnung_flaeche_dreieck(hoehe):
    """ Berechnung der Flaeche eines Dreieckes 'objekt' in Pixeln.

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


def use_schwellwert(image, schwelle_oben):
    """ Funktion erzeugt aus einem Bild ein logisches Bild (Binaerbild), indem
        ein bestimmter Bereich mittels des Schwellwertverfahrens separiert
        wird. Dabei werden a priori Kenntnisse vorausgesetzt
        (Grauwerthistogramm u.Ä.). Beinhaltet Pixelklassifikation: Einteilung
        in Objekt- und Nichtobjektpixel.

        Parameter:
        ----------
        image: Array, Eingabewerte.
        
        schwelle_oben: oberer Schwellwert. Bis zu dieser Graustufe wird
        Grauwertverteilung als Objekt gezaehlt.
    """   
    # Anlegen eines Null-Arrays, welches Maske enthaelt:
    # Einsen: Pixel wird als Objekt klassifiziert
    # Nullen: Pixel wird als Nichtobjekt klassifiziert
    image_maske = np.zeros_like(image)
    image_maske[schwelle_oben <= image] = 1
    return image_maske
    
    
def extract_values(image, value):
    """ Funktion speichert aus einem Array die einander zugehoerigen (x- und
         y-)Koordinaten (als Meshgrid), welche einen bestimmten Wert 'value'
         enthalten. Dabei wird der (virtuelle) Ursprung in das Zentrum des
         Bildes gelegt.
         
        Parameter:
        ----------
        image: Array, Eingabewerte.
        
        value: bestimmter Wert, anhand dessen Filterung der Werte.
    """
    # Zentrum des Bildes
    center = len(image) // 2
    # Abspeichern der einander zugehoerigen Koordinaten 
    koord_x, koord_y = np.meshgrid(np.arange(-center, center ),
                                   np.arange(center, -center, step=-1))
    # Rausfilterung der Untergrundwerte nach einen bestimmten Wert 'value'
    koord_x = koord_x[image == value]
    koord_y = koord_y[image == value]
    return koord_x, koord_y


def hough_trafo():
    """ Anwenden der Hough-Transformation = Kantenorientierte Segmentierung.
        Mittels der Hesseschen Normalform fuer Geradengleichungen werden 
        Geraden erkannt (siehe Vorlesung zu Modul MF-MRS_14 Digitale
        Bildverarbeitung, Folie 202f). Dafuer wird der Normalenvektor vom (virtuellen)
        Ursprung des Bildes und der zugehrige Winkel parametrisiert
    
        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    winkel = []
    abstaende = []
    # verschiedene Winkel durchgehen
    for alpha in np.linspace(0, 180, 180, endpoint=False):
        # einzelne aktuelle Winkel abspeichern (so viele wie abstande)
        winkel.append(np.ones(len(koord_x))*alpha)
        # Winkel in Bogenmaß umrechen
        alpha = np.radians(alpha)
        # Hessesche Normalform der Geradengleichung
        abstand = koord_x * np.cos(alpha) + koord_y * np.sin(alpha)
        # zu aktuellen Winkel alle dazu berechneten Abstaende abspeichern
        abstaende.append(abstand)
    # Umwandeln der Listen in Arrays
    winkel = np.array(winkel).ravel()
    abstaende = np.array(abstaende).ravel()
    # 2D-Histogramm aus Abstaenden und Winkel darstellen
    plt.figure()
    counts, xedges, yedges, image = plt.hist2d(winkel, abstaende, bins=180)

def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
    # Extraktion des rechten unteren Quadranten
    quadrant_vier = Aufgabe_1_1.extract(szinti, 128, 256, 128, 256)
    # Medianfilter anwenden zur Erzeugung zusammenhaengender Gebiete,
    # Löcher in Flächen teilweise aufgefuellt
    quadrant_vier = Aufgabe_3_3.filter_image(quadrant_vier)
    # Anwendung Sobelfilter aufs Teilbild (Flaechenquelle D) aus Bild
    # Aufgabe 1.1 zur Kantenextraktion
    quadrant_vier = Aufgabe_3_4.filter_sobel_image(quadrant_vier) 
    # 2tes mal Medianfilter anwenden zur Erzeugung zusammenhaengender Gebiete,
    # Löcher in Flächen teilweise aufgefuellt
    quadrant_vier = Aufgabe_3_3.filter_image(quadrant_vier)
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    quadrant_vier = Aufgabe_1_1.make_scale(quadrant_vier)
#    # Kontrolldarstellung
#    plt.figure()
#    plt.imshow(quadrant_vier, cmap='gray')
    # logisches Bild (Binaerbild) aufbauen: mit Kanten Eins, Rest Null
    # dafür Histogramm anschauen
    plt.figure()
    Aufgabe_2_2.erstelle_grauwerthistogramm_abgeschnitten('Grauwerthistogramm',
                                'fuer Bild aus Aufgabe 1.1, ' +
                                'gekuerzte Ordinatenachse', r'$f$',
                                'Häufigkeitsverteilung $h(f)$',
                                quadrant_vier.flatten())
    # a priori werden Schwellwertgrenzen festgelegt, wodurch lediglich Kanten
    # extrahiert werden
    quadrant_vier_kanten = use_schwellwert(quadrant_vier, 160)
#    plt.figure()
#    plt.imshow(quadrant_vier_kanten, cmap='gray')
    # Extrahieren (nur) der (x- und y-) Koordinaten, bei denen Bildfunktion
    # f(x) ungleich 0
    # (d.h. in neuen Koordinaten-arrays sind lediglich Koordinaten der Kanten
    # (entsprechen Einsen im logischen Bild) enthalten)
    koord_x, koord_y = extract_values(quadrant_vier_kanten, 1)
    # Finden der Kantenpunkte, die zu einer (durchgehenden) Linie gehoeren
    # (sind also kein Rauschen)
    # Pruefen mit Hough-Transformation
    # (siehe Vorlesung zu Modul MF-MRS_14 Digitale Bildverarbeitung, Folie
    # 202f)
    # verschiedene Winkel durchgehen
    winkel = []
    abstaende = []
    for alpha in np.linspace(0, 180, 180, endpoint=False):
        # einzelne Winkel abspeichern (so viele wie abstande)
        winkel.append(np.ones(len(koord_x))*alpha)
        # Winkel in Bogenmaß umrechen
        alpha = np.radians(alpha)
        # Hessesche Normalform der Geradengleichung
        abstand = koord_x * np.cos(alpha) + koord_y * np.sin(alpha)
        # zu aktuellen Winkel alle dazu berechneten Abstaende abspeichern
        abstaende.append(abstand)
    # Umwandeln der Listen in Arrays
    winkel = np.array(winkel).ravel()
    abstaende = np.array(abstaende).ravel()
    # 2D-Histogramm aus Abstaenden und Winkel darstellen
    plt.figure()
    counts, xedges, yedges, image = plt.hist2d(winkel, abstaende, bins=180)
        
#    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
#    # Extraktion des rechten unteren Quadranten
#    quadrant_vier = szinti[128:256, 128:256]
#    # (virtueller) Ursprung des Bildes wird in das Zentrum des Teilbildes
#    # gelegt!
#    # nur Pixel durchgehen, indem auch Wert > Null gespeichert ist?
#    # ich kenne Seitenlaenge a
#    # alle Winkel in Bereich [0, pi] durchgehen:
##    for grad in range(np.pi):
##        # was fuer Koordinaten erhaelt man fuer dasselbe alpha?
##        # Berechnen der Koordinaten entsprechend der Hesse'schen Normalform
##        # der Geradengleichung, diese Koordinaten liegen auf einer Linie
##    # Anwendung Sobelfilter: logisches Binaerbild! Konturverkettung?


if __name__ == "__main__":
    main()

# TDO: externe Console bzw Windowkonsole funktioniert nicht?

# Interpretation:
    # Laplace: Hochpass zum Hervorheben strukturreicher Bildbereiche, da
    # diese kruemmungsempfindlich sind
    # Unterschiede zu Gradientenfiltern (aus Aufgabe 3.4): nutzen 2. Ableitung,
    # welche rauschanfaelliger ist als bei Nutzen erster Ableitung
