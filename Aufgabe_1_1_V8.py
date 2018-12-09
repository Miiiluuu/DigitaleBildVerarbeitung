"""
    Darstellung eines aufgenommenen Szintigramms, bestehend aus 256x256 Pixel,
    aufgebaut aus vier Flaechenquellen (weitere Parameter siehe Vorlesung zu
    Modul MF-MRS_14 Digitale Bildverarbeitung)
"""

# Aufgabe 1.1.

import numpy as np
import matplotlib.pyplot as plt


# TODO: Parameter Definitionen erklären


def get_image_A(laenge_quadrant, kantenlaenge, avg_a, mittelpkt):
    """ Erzeugt Objekt A, ist Rechteck. """   
    # TODO: avg_a erklären!                    
    # erstelle Array, in dem sich Flaechenquelle A befindet
    # ≙ lokales Koordinatensystem
    image_a = np.zeros((laenge_quadrant, laenge_quadrant))
    # Figur fuer Flaechenquelle A, Flaeche eingrenzen
    # ist Rechteck, beachte Indexierung von Arrays in numpy:
    # beginnend mit Null
    # Abstand Quellenkante zum Rand in x- Richtung
    abstand_x = mittelpkt[0] - kantenlaenge // 2
    # Abstand Quellenkante zum Rand in y- Richtung
    abstand_y = laenge_quadrant - mittelpkt[1] - kantenlaenge // 2
    quelle_a = image_a[abstand_y:abstand_y + kantenlaenge, abstand_x:abstand_x + kantenlaenge]
    # auf jeden Pixel von Quelle A Poisson- Verteilung anwenden
    # dadurch Beachtung des statistischen Charakters des
    # radioaktiven Zerfalls
    for i in range(kantenlaenge):
        for j in range(kantenlaenge):
              quelle_a[i, j] = np.random.poisson(avg_a)
    return image_a


def get_image_B(laenge_quadrant, kantenlaenge, avg_b_g, avg_b_w, mittelpkt, deltax):
    """ Erzeugt Objekt B, ist Rechteck mit Streifen. 
    
        Parameter:
        ----------
        avg_b_g: mittlere flaechenbezogene Zahl der registrierten
        Ereignisse von Objekt B, graue Streifen, in 1/mm².
        
        avg_b_w: mittlere flaechenbezogene Zahl der registrierten
        Ereignisse von Objekt B, weiße Streifen, in 1/mm².
        
        deltax: Breite der Streifen bzw. der einzelnen Flaechenquellen in mm. """
    # erstelle Array, in dem sich Flaechenquelle B befindet
    image_b = np.zeros((laenge_quadrant, laenge_quadrant))
    # Figur fuer Flaechenquelle B, Flaeche eingrenzen
    # ist Rechteck, beachte Indexierung von Arrays in numpy: beginnend mit Null
    # Abstand Quellenkante zum Rand in x- Richtung
    abstand_x = laenge_quadrant + mittelpkt[0] - kantenlaenge // 2
    # Abstand Quellenkante zum Rand in y- Richtung
    abstand_y = laenge_quadrant - mittelpkt[1] - kantenlaenge // 2
    quelle_b = image_b[abstand_y:abstand_y + kantenlaenge, abstand_x:abstand_x + kantenlaenge]
    # Streifen
    i = 0
    while i < kantenlaenge:
        quelle_b[:, i:i+deltax] = np.random.poisson(avg_b_g, (kantenlaenge, deltax))
        i += deltax
        quelle_b[:, i:i+deltax] = np.random.poisson(avg_b_w, (kantenlaenge, deltax))
        i += deltax
    return image_b


def get_image_C(laenge_quadrant, anz_pixel):
    """ Erzeugt Objekt C, ist Kreis. """
    # mittlere flaechenbezogene Zahl der registrierten Ereignisse von
    # Objekt C
    avg_c = 50
    # erstelle 128x128- Array, in dem sich Flaechenquelle C befindet
    image_c = np.zeros((laenge_quadrant, laenge_quadrant))
    # Figur fuer Flaechenquelle A, Flaeche eingrenzen als Rechteck
    rechteck_c = image_c[10:110, 18:118]
    # Kreisformel
    # Satz des Pythagoras
    # Mittelpunkt vom Kreis
    mitte = 50              # (x, y) = (50 mm, 50 mm)
    # jeden Pixel einzeln durchgehen
    for i in range(anz_pixel):
      for j in range(anz_pixel):
          deltax = mitte - i
          deltay = mitte - j
          if deltax**2 + deltay**2 <= mitte**2:
              rechteck_c[i, j] = np.random.poisson(avg_c)
    return image_c


def get_image_D(laenge_quadrant):
    """ Erzeugt Objekt D, ist gleichseitiges Dreieck. """
    # mittlere flaechenbezogene Zahl der registrierten Ereignisse von
    # Objekt D
    avg_d = 100
    # erstelle 128x128- Array, in dem sich Flaechenquelle D befindet
    image_d = np.zeros((laenge_quadrant, laenge_quadrant))
    # gleichseitiges Dreieck mit Parametern: 
    # Koordinaten der Dreiecksspitze
    # x- Richtung
    spitze_x = 60
    # y- Richtung
    spitze_y = 10
    # Hoehe des Dreicks
    hoehe = 100         # mm
    # jedes Pixel der moeglichen Dreiecksflaeche einzeln durchgehen:
    # abgerasteter y- Bereich von der spitze_y bis:
    delta_y = spitze_y + hoehe
    for y in range(spitze_y, delta_y + 1):
        # aktueller Hoehe
        akt_hoehe = np.absolute(spitze_y - y)
        for x in range(laenge_quadrant):
            # Abstand zur Mitte: aktueller x- Wert
            abstand_mitte = np.absolute(spitze_x - x)
            # Formel zur Berechnung der gleichseitigen Kantenlaenge a
            # falls Bedingung erfüllt ist, gehört Pixel zum Dreick
            # und es wird Poissonstatistik angewendet
            if abstand_mitte <= akt_hoehe / np.sqrt(3):
                image_d[y, x] = np.random.poisson(avg_d)
    return image_d


def main():
    """ Erzeugung des Szintigramms. """
    # fuer Pixelgroeße von 256x256
    pixel = 256
    # fuer Erstellen Koordinatensystem Flaechenquelle A, B, C und D
    pixel_quadrant = pixel // 2
    # Kantenlaenge fuer Objekt A, B
    n = 100
    # Erstellung Szintigramm = 256x256- Array
    # stellt Szintigramm-Flaeche dar ≙ globales Koordinatensystem
    # beachte Indexierung von Arrays in numpy:
    # beginnend mit Null
    szinti = np.zeros((pixel, pixel))
    # Einteilung des Szintigramms in vier Quadranten
    # jedes Objekt befindet sich in jeweils einem Quadranten
    quadrant_eins = szinti[0:128, 128:256]
    quadrant_zwei = szinti[0:128, 0:128]
    quadrant_drei = szinti[128:256, 0:128]
    quadrant_vier = szinti[128:256, 128:256]
    # Objekte dem richtigen Platz im Szintigramm zuweisen
    image_a = get_image_A(pixel_quadrant, n, 200, (60, 60))
    quadrant_eins[:,:] = image_a
    image_b = get_image_B(pixel_quadrant, n, 250, 300, (-60, 60), 5)
    quadrant_zwei[:,:] = image_b
    image_c = get_image_C(pixel_quadrant, n)
    quadrant_drei[:,:] = image_c
    image_d = get_image_D(pixel_quadrant)
    quadrant_vier[:,:] = image_d
    # Skalieren der Zahlenwerte, sodass Glauwerte von 0...255 umfasst werden
    # hoechster Wert: 255 ≙ weiß
    weiß = 255
    # niedrigester Wert: 0 ≙ schwarz
    schwarz = 0
    hoechster_grauwert = np.max(szinti)
    # Berechnung Skalierungsfaktor, sodass hoechsten Grauwert entspricht
    skal = weiß / hoechster_grauwert
    # Skalierungsfaktor auf gesamtes Szintigramm anwenden
    szinti = skal * szinti
    # Plot zeichnen
    plt.imshow(szinti, cmap='gray')
    

main()

