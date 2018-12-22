"""
    Aufgabe 2.5:
    Erstellt die Bitebenen aller Bilder aus Aufgabe 1.1 und berechnet fuer
    jede Ebene den mittleren Informationsgehalt je Pixel.
"""

import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import copy

import Aufgabe_1_1
import Aufgabe_2_4


def plot_vorbereitung_9sp(ueberschrift):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        Ueberschrift, neun Subplots etc. """
    # Erstellen von (neun) Subplots:
    fig, axs = plt.subplots(3, 3, figsize=(10, 10), facecolor='w')
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    axs = axs.ravel()
    return axs


# TODO: Trennung von Berechnung und Plot?
def erstellung_bitebenen(image):
    """ Erstellt und plottet Bitebenen Null bis Sieben eines Bildes sowie
        das Ursprungsbild mit entsprechender Beschriftung.
        
        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    axs = plot_vorbereitung_9sp('Der Informationsgehalt von Bildern \n'
                                '- verschiedene Bitebenen -')

    # Plot des Ursprungsbildes mit Unterueberschrift
    axs[0].imshow(image, cmap='gray', extent=[-128, 128, -128, 128])
    axs[0].set_title('Ursprungsbild')
    # einzelne Bitebenen erstellen
    ebene = []
    # Kopie des Eingabe-Arrays, um Originalbild unveraendert zu lassen!
    image_copy = copy.copy(image)
    for i in range(7, -1, -1):
        bitebene = np.zeros((len(image_copy), len(image_copy)))
        bitebene[image_copy >= 2**(i)] = 1
        image_copy[image_copy >= 2**(i)] -= 2**(i)
        ebene.append(bitebene)
    # Plots der einzelnen Bitebenen mit Unterueberschriften
    for i in range(7, -1, -1):
        axs[i+1].set_title(f'''Bitebene {7-i}''')
        axs[i+1].imshow(ebene[i], cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()
    return ebene


# TODO: fuer das Bild aus Aufgabe 1.1 als Bezeichnung ok? 
# (lieber {aufgabe} als Variable?)
def infogehalt_einzelne_bitebenen(image):
    """ Berechnet fuer alle Bitebenen (des Bildes aus Aufgabe 1.1) den
         mittleren Informationsgehalt pro Pixel.

        Parameter:
        ----------
        image: Liste der einzelnen Bitebenen, Eingabewerte.
    """
    info_bit = []
    for i in range(7, -1, -1):
        info = Aufgabe_2_4.infogehalt(image[i])
        # Runden des Informationsgehaltes
        info = np.round(info, 3)
        # Abspeichern des Informationsgehaltes der einzelnen Bitebenen:
        # Anhaengen an eine Liste
        info_bit.append(info)
    # Ausgabe des Informationsgehaltes pro Pixel fuer die einzelnen
    # Bitebenen des Bildes aus Aufgabe 1.1 mit PrettyTable
    print('Der mittlere Informationsgehalt pro Pixel fuer das Bild aus ' +
          'Aufgabe 1.1 betraegt:')
    # Erstellung PrettyTable
    x = PrettyTable()
    x.field_names = ['Bitebene', 'mittlerer Informationsgehalt in ' +
                     'Bit/Pixel']
    for i in range(8):
        # Hinzufuegen einzelner Zeilen zur PrettyTable
        x.add_row([(i), info_bit[i]])
    print(x)


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Erstellung Bitebenen
    ebene = erstellung_bitebenen(szinti)
    # Berechnung mittlerer Informationsgehalt pro Pixel
    infogehalt_einzelne_bitebenen(ebene)


if __name__ == "__main__":
    main()

    # TODO: Ergebnisse vergleichen
    
    # Interpretation:
    # einzelne Bitebenen entspricht Zahlencodierung
    # es werden nur Farbkontraste wirklich sichtbar in oberen Bitebenen?
    # in unteren Bitebenen nur Rauschen, keine Infos
    # Arrays der einzelnen Bitebenen bestehen nur aus Einsen und Nullen:
    # Nullen werden weggeschmissen
    # daraus folgt Negativer Infogehalt? = sehr gering?
    # wann besten Infogehalt:laut Bildern bei Bitebene 5, aber laut Tabelle
    # größter Infogehalt bei Bitebene Null? 
    # ist kein gutes Maß fuer Bitebenen,da Einsen und Nullen
    # 7 ist relativ wichtig (most signifikant), unt. weiß / schwarz
    # Histogramm enthaelt keine raumlichen Infos