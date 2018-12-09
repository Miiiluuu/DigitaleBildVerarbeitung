"""
    Aufgabe 3.3:
    Anwendung eines 3x3- Mittelwert-, 3x3- Median- und einem 3x3-Bionomial-
    filter am Bild aus Aufgabe 1.1.
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1
import Aufgabe_2_1
# TODO: doppelte Plot-Funktion? Figuresize


def make_mittelwertfilter():
    """ Erstellung eines 3x3-Mittelwertfilters mit entsprechender Normierung
        (1 /9).
    """
    mittelwertfilter = (1 / 9) * np.ones((3, 3))
    return mittelwertfilter


def make_binfilter():
    """ Erstellung eines 3x3-Binomialfilters mit entsprechender Normierung
        (1 / 16). Werte sind entnommen aus Pascalschen Dreieck.
    """
    binfilter = (1 / 16) * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    return binfilter


def filter_image(image, filter_art=None):
    """ Anwendung eines 3x3-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        filter_art: Beschreibt 3x3-Filter (-Array), welcher auf das Bild
        image angewendet wird. Falls Argument nicht angegeben, (es wird
        keine Filterart ausgewaehlt), wird fuer das image ein 3x3-Medianfilter
        benutzt. Bei Auswahl eines Argumentes filter_art wird dieser fuer das
        Filtern des Bildes verwendet.
    """
    # Schleife: jeden Pixel einzeln durchgehen (bis auf aeußersten Pixel
    # (-Rand)), da dieser von Filter nicht beruecksichtigt wird:
    # aeußeren Rand-Pixel werden auf Null gesetzt
    image_gefiltert = np.zeros((len(image), len(image)))
    for x in range(1, len(image)-1):
        for y in range(1, len(image)-1):
            # Filterbereich, der einzeln (fuer jeden Pixel) wirksam wird (3x3)
            bereich = image[y-1:y+2, x-1:x+2]
            # Anwenden eines Medianfilters auf das Bild
            if filter_art is None:
                image_gefiltert[y, x] = np.median(bereich)
            # Anwenden eines anderen 3x3-Filters auf das Bild
            # (je nachdem, welches Argument der Funktion beim Aufruf gegeben
            # wird)
            else:
                # Anwendung Filter auf Filterbereich
                bereich_filter = bereich * filter_art
                # Fuellen des entsprechenden Pixels mit neuem gefilterten Wert
                image_gefiltert[y, x] = np.sum(bereich_filter)
    return image_gefiltert


def plot_vorbereitung(ueberschrift, sub_ueberschriften,
                      sub_ueberschrift_grau, abszisse,
                      ordinate):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        Ueberschrift, einzelnen Subplots etc.

        Parameter:
        ----------
        ueberschrift: Ueberschrift der Figure.

        sub_ueberschriften: Liste an Ueberschriften fuer die einzelnen
        Subplots.

        sub_ueberschrift_grau: Ueberschrift der Subplots, welche ein Grauwert-
        profil enthalten.

        abszisse: Beschriftung der Abszisse von den Subplots, die ein Grauwert-
        profil enthalten.

        ordinate: Beschriftung der Ordinate von den Subplots, die ein Grauwert-
        profil enthalten.
    """
    # Erstellen von (vier) Subplots:
    fig, axs = plt.subplots(2, 4, figsize=(20, 10), facecolor='w')
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    axs = axs.ravel()
    # entsprechende Unterueberschriften der Subplots
    for i in range(4):
        axs[i].set_title(sub_ueberschriften[i])
    for i in range(4, 8):
        axs[i].set_title(sub_ueberschrift_grau)
        axs[i].set_xlabel(abszisse)
        axs[i].set_ylabel(ordinate)
    return axs


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Erstellung der Filter
    mittelwertfilter = make_mittelwertfilter()
    binfilter = make_binfilter()
    # Anwendung Filter auf das Bild aus Aufgabe 1.1:
    # Mittelwertfilter
    szinti_filter_avg = filter_image(szinti, mittelwertfilter)
    # Medianfilter
    szinti_filter_med = filter_image(szinti)
    # Binomialfilter
    szinti_filter_bin = filter_image(szinti, binfilter)
    # Erstellung Grauwertprofile entlang y-Linie = 60:
    # fuer Originalbild aus Aufgabe 1.1
    grauprofil_60_szinti = Aufgabe_2_1.extraktion_aus_array(szinti,
                            pixel_quadrant - 60)
    # fuer angewendeten 3x3-Mittelwertsfilter
    grauprofil_60_avg = Aufgabe_2_1.extraktion_aus_array(szinti_filter_avg,
                            pixel_quadrant - 60)
    # fuer angewendeten 3x3-Medianfilter
    grauprofil_60_med = Aufgabe_2_1.extraktion_aus_array(szinti_filter_med,
                            pixel_quadrant - 60)
    # fuer angewendeten 3x3-Binomialfilter
    grauprofil_60_bin = Aufgabe_2_1.extraktion_aus_array(szinti_filter_bin,
                            pixel_quadrant - 60)
    # Plots:
    axs = plot_vorbereitung('Vergleich verschiedener Glaettungsverfahren',
                            ['Originalbild aus Aufgabe 1.1',
                             '3x3-Mittelwertfilter', '3x3-Medianfilter',
                             '3x3-Binomialfilter'],
                            'entsprechendes Grauwertprofile \n'
                            '- laengs y = 60 - ',
                            r'$x/mm$', 'Grauwert')
    # Anlegen einer Liste, welche einzelten (gefilterten) Bilder und die
    # entsprechenden Grauwertprofile enthaelt
    bilder = [szinti, szinti_filter_avg, szinti_filter_med,
              szinti_filter_bin, grauprofil_60_szinti, grauprofil_60_avg,
              grauprofil_60_med, grauprofil_60_bin]
    for i in range(4):
        axs[i].imshow(bilder[i], cmap='gray', extent=[-128, 128, -128, 128])
    for i in range(4, 8):
        axs[i].plot((np.arange(-pixel_quadrant, pixel_quadrant)), bilder[i])


if __name__ == "__main__":
    main()

# Vergleich
    # alle sind Glättungsverfahren: Reduzieren des Bildrauschens,
    # Unebenheiten in den Grauwerten des Bildes (teilweise "hohe
    # Bildfrequenzen" beseitigen, siehe auch entsprechende Grauwertprofile)
    # Mittelwert: Elimination hoher Bildfrequenzen, damit sind Kanten
    # (Darstellung mit hohen Frequenzen) abgeflacht, Bild wird "verschmiert"
    # Median hat sowohl Glättungswirkung und kann auch Kantensteilheit erhalten
    # dafür aber Artefakte in spitzwinkligen Strukturen, die vorher nicht da
    # waren (z.B. siehe abgebrochene Ecken in Rechtecken/Flaechenquelle A & B)
    # allg. Robustheit gegen Ausreisser, effektiv gegen Salt-und-Pepper
    # Rauschen gegenüber Mittelwert
    # (hier wird Helligkeitsrauschen geglaettet)
    # Binomial ist spezielle Form des Mittelwertfilters, dabei liegt mehr 
    # Gewicht auf mittleren Pixel waehrend hier verwendeter 
    # Mittelwertfilter jedem Pixel das 
    # selbe Gewicht Eins gibt (dadurch nicht mehr so verschmiert? bzw keine 
    # Artefakte)
