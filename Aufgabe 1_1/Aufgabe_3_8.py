"""
    Aufgabe 3.6:
    Berechnung des geometrischen und den Massenschwerpunkt fuer ein Objekt,
    bestehend aus den Flaechenquellen B und C aus Aufgabe 1.1
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_3_4
import Aufgabe_3_3
import Aufgabe_3_7


def make_logic_image(image, schwelle_oben):
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
    koord_x, koord_y = np.meshgrid(np.arange(-center, center),
                                   np.arange(center, -center, step=-1))
    # Rausfilterung der Untergrundwerte nach einen bestimmten Wert 'value'
    koord_x = koord_x[image == value]
    koord_y = koord_y[image == value]
    return koord_x, koord_y


def hough_trafo(koord_x, koord_y):
    """ Anwenden der Hough-Transformation = Kantenorientierte Segmentierung.
        Mittels der Hesseschen Normalform fuer Geradengleichungen werden
        Geraden erkannt (siehe Vorlesung zu Modul MF-MRS_14 Digitale
        Bildverarbeitung, Folie 202f). Dafuer wird der Normalenvektor vom
        (virtuellen) Ursprung des Bildes und der zugehoerige Winkel
        parametrisiert.

        Parameter:
        ----------
        koord_x: (x-)Koordinaten einer Bildfunktion f(x, y), fuer die gilt:
            f(x, y) ungleich 0 .

        koord_y: (y-)Koordinaten einer Bildfunktion f(x, y), fuer die gilt:
            f(x, y) ungleich 0 .
    """
    winkel = []
    abstaende = []
    # verschiedene Winkel durchgehen
    for alpha in np.linspace(0, 180, 180, endpoint=False):
        # einzelne aktuelle Winkel abspeichern (Anzahl entsprechend Anzahl
        # der Koordinaten)
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
    # Darstellung der verketteten Kanten / durchgezogenen Linien des Dreieckes
    # als Häufungspunkte im 2D-Histogramm
    plot_2d_hist("Kantenorientierte Segmentierung \n"
                 "- Hough-Transformation zur Erkennung der Seiten des \n"
                 "Dreieckes aus Flaechenquelle D, Aufgabe 1.1 -",
                 r'Winkel $ϕ/°$', r'Abstand zum Mittelpunkt $d/mm$', winkel,
                 abstaende)


def plot_2d_hist(ueberschrift, abszisse, ordinate, werte1, werte2):
    """ Plot einer 2D-Histogramms mit entsprechender Ueberschrift,
        Achsenbeschriftung, Farbskala etc.
    """
    plt.figure(figsize=(10, 6))
    # Hinzufuegen der Ueberschrift zum Plot
    plt.suptitle(ueberschrift, fontsize=16)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    counts, xedges, yedges, image = plt.hist2d(werte1, werte2, bins=180,
                                               range=[[0, 180], [-64, 64]])
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.8])
    plt.colorbar(image)
    plt.show()


#def main():
# Bild- Array (aus Aufgabe 1.1) erstellen
szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
# Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
# Extraktion des rechten unteren Quadranten
szinti = Aufgabe_1_1.extract(szinti, 0, 256, 0, 128)
plt.imshow(szinti, cmap='gray')
# momente berechnen
m00 = np.sum(szinti)
m10 = 0
schleife = np.shape(szinti)[1]
for x in range(schleife):
    m10 += np.sum(szinti[:, x]) * x
szinti_t = np.transpose(szinti)
schleife_t = np.shape(szinti_t)[1]
m01 = 0
for x in range(schleife_t):
    m01 += np.sum(szinti_t[:, x]) * x
# Rechnung Schwerpunkte nach Vorlesung zu Modul MF-MRS_14 Digitale
# Bildverarbeitung Folie 213f
# Massenschwerpunkt in x-Richtung
x_s = m10 /m00
# Massenschwerpunkt in y-Richtung
y_s = m01 /m00
# Maskieren
# geometrischer Schwerpunkt wird entsprechend berechnet, aber zuvor wird Bild-
# funktion ueberall auf Eins gesetzt
# Schwellwertbedingung: in welchem Intervall liegen Objektpixel?
szinti_geo = Aufgabe_3_7.make_logic_image(szinti, 0)
# momente berechnen
m00_geo = np.sum(szinti_geo)
m10_geo = 0
schleife_geo = np.shape(szinti_geo)[1]
for x in range(schleife_geo):
    m10_geo += np.sum(szinti_geo[:, x]) * x
szinti_t_geo = np.transpose(szinti_geo)
schleife_t_geo = np.shape(szinti_t_geo)[1]
m01_geo = 0
for x in range(schleife_t_geo):
    m01_geo += np.sum(szinti_t_geo[:, x]) * x
# Rechnung Schwerpunkte nach Vorlesung zu Modul MF-MRS_14 Digitale
# Bildverarbeitung Folie 213f
# Massenschwerpunkt in x-Richtung
x_geo = m10_geo /m00_geo
# Massenschwerpunkt in y-Richtung
y_geo = m01_geo /m00_geo
   

#if __name__ == "__main__":
    #main()

# TDO: externe Console bzw Windowkonsole funktioniert nicht?
