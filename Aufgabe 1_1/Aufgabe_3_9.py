"""
    Aufgabe 3.9:
    Extraktion von Flaechenquelle B aus Szintigramm Aufgabe 1.1,
    Bestimmung der Grauwertuebergangsmatrix C(δ=(1,0)) und C(δ=(0,1)) und
    Interpretation.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

import Aufgabe_1_1
import Aufgabe_3_3


def medianfilter_5x5(image):
    """ Anwendung eines 5x5-Medianfilters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Schleife: jeden Pixel einzeln durchgehen (bis auf aeußeren (Rand-)
    # Pixel, da dieser von Filter nicht beruecksichtigt werden:
    # aeußeren Rand-Pixel werden auf Null gesetzt
    image_gefiltert = np.zeros((len(image), len(image)))
    for x in range(2, len(image)-2):
        for y in range(2, len(image)-2):
            # Filterbereich, der einzeln (fuer jeden Pixel) wirksam wird (5x5)
            bereich = image[y-2:y+3, x-2:x+3]
            # Anwenden eines Medianfilters auf das Bild
            image_gefiltert[y, x] = np.median(bereich)
    return image_gefiltert


def szinti_vorbereitung_3_9(szinti, pixel, pixel_quadrant):
    """ Funktion leistet Vorverarbeitung des Bildes aus Aufgabe 1.1 fuer
        anschließende Bestimmung von Grauwertuebergangsmatrizen. Dabei
        Anwendung verschiedener Filter und Aehnliches.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
    # Extraktion des linken oberen Quadranten (Flaechenquelle B)
    szinti = Aufgabe_1_1.extract(szinti, 0, pixel_quadrant, 0, pixel_quadrant)
#    # Kontrolldarstellung
#    plt.figure()
#    # Hinzufuegen der Ueberschrift zum Plot
#    plt.suptitle("Originalbild", fontsize=16)
#    plt.imshow(szinti, cmap='gray')
    # mehrmalige Anwendung von Medianfiltern (verschiedener Groeße), um
    # Bildrauschen (durch radioaktivem Zerfall) zu reduzieren, aber Lage
    # und Steilheit vom Bild erhalten! (Kombination durch Ausprobieren):
    # zweimaliges Anwenden eines 5x5 Medianfilters
    for i in range(2):
        szinti = medianfilter_5x5(szinti)
    # zweimaliges Anwenden eines 3x3 Medianfilters
    for i in range(2):
        szinti = Aufgabe_3_3.use_filter3x3_image(szinti)
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    szinti = Aufgabe_1_1.make_scale(szinti)
#    # Kontrolldarstellung
#    plt.figure()
#    # Hinzufuegen der Ueberschrift zum Plot
#    plt.suptitle("gefiltertes Bild", fontsize=16)
#    plt.imshow(szinti, cmap='gray')
    return szinti
    
    
def make_uebergangsmatrix(image):
    """ Erzeugt eine Uebergangsmatrix mit den C(δ=(1,0)) und C(δ=(0,1))
        fuer ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Erzeugen der Uebergangsmatrix
    ubergange = np.zeros((256, 256)) 
    # Pixel einzeln durchgehen
    for y in range(len(image)):
        for x in range(len(image)-1):
                ubergange[image[y, x], image[y, x+1]] += 1
    # Plot der Uebergangsmatix
    fig = plt.figure(figsize=(6, 7))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle("Uebergangsmatrix", fontsize=16)
    plt.imshow(ubergange, cmap='gray', norm=LogNorm())
    plt.tight_layout(rect=[0, 0, 1, 1.1])
#    # TODO: colorbar?
#    # TODO: Colorbarbeschriftung
#    plt.colorbar(ubergange)
    plt.show()
    

def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    
    szinti = szinti_vorbereitung_3_9(szinti, pixel, pixel_quadrant)
    
    # Erzeugen der Uebergangsmatrizen:
    # mit Vektor C(δ=(1,0))
    make_uebergangsmatrix(szinti)
    # mit Vektor C(δ=(0,1))
    szinti_t = np.transpose(szinti)
    make_uebergangsmatrix(szinti_t)


if __name__ == "__main__":
    main()

