"""
    Aufgabe 3.9:
    Extraktion von Flaechenquelle B aus Szintigramm Aufgabe 1.1,
    Bestimmung der Grauwertuebergangsmatrix C(δ=(1,0)) und C(δ=(0,1)) und
    Interpretation.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_3_7
import Aufgabe_3_3

def medianfilter_5x5(image):
    """ Anwendung eines 5x5-Medianfilters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Schleife: jeden Pixel einzeln durchgehen (bis auf aeußersten Pixel
    # (-Rand)), da dieser von Filter nicht beruecksichtigt wird:
    # aeußeren Rand-Pixel werden auf Null gesetzt
    image_gefiltert = np.zeros((len(image), len(image)))
    for x in range(2, len(image)-2):
        for y in range(2, len(image)-2):
            # Filterbereich, der einzeln (fuer jeden Pixel) wirksam wird (5x5)
            bereich = image[y-2:y+3, x-2:x+3]
            # Anwenden eines Medianfilters auf das Bild
            image_gefiltert[y, x] = np.median(bereich)
    return image_gefiltert


#def main():
# Bild- Array (aus Aufgabe 1.1) erstellen
szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
# Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
# Extraktion des linken oberen Quadranten (Flaechenquelle B)
szinti = Aufgabe_1_1.extract(szinti, 0, 128, 0, 128)
# Kontrolldarstellung
plt.figure()
# Hinzufuegen der Ueberschrift zum Plot
plt.suptitle("Originalbild", fontsize=16)
plt.imshow(szinti, cmap='gray')
# mehrmalige Anwendung von Medianfiltern (verschiedener Groeße), um
# Bildrauschen (durch radioaktivem Zerfall) zu reduzieren, aber Lage
# und Steilheit vom Bild erhalten!
# zweimaliges Anwenden eines 5x5 Medianfilters
for i in range(2):
    szinti = medianfilter_5x5(szinti)
# zweimaliges Anwenden eines 3x3 Medianfilters
for i in range(2):
    szinti = Aufgabe_3_3.filter_image(szinti)
# Kontrolldarstellung
plt.figure()
# Hinzufuegen der Ueberschrift zum Plot
plt.suptitle("gefiltertes Bild", fontsize=16)
plt.imshow(szinti, cmap='gray')

  
    
    
#if __name__ == "__main__":
#    main()

# TDO: externe Console bzw Windowkonsole funktioniert nicht?
