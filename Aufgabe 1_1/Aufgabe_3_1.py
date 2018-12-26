"""
    Aufgabe 3.1.
    Programmiert einen linearen Graukeil (mit 256 Grauwerten) und wendet die
    Kennlinien aus der Vorlesung, Folie 111 aus dem Modul MF-MRS_14 Digitale
    Bildverarbeitung darauf an.

    @author: Mieke Möller
"""

import numpy as np
import matplotlib.pyplot as plt


def make_graukeil(anz_pixel, anz_grauwerte):
    """ Erstellt einen linearen (quadratischen) Graukeil (mit bestimmter
        Anzahl Grauwerte).

        Parameter:
        ----------
        anz_pixel: Anzahl an Pixeln in 1D: bestimmt Groeße des Graukeils.

        anz_grauwerte: Anzahl der Grauwerte, die im Graukeil enthalten sein
        sollen.
    """
    graukeil = np.ones((anz_pixel, anz_pixel)) * np.arange(anz_grauwerte)
    return graukeil


def make_kennlinien(function_unten, function_oben, anz_grauwerte):
    """ Erstellt eine Look-up-Table mit verschiedenen Kennlinien aus der
        Vorlesung, Folie 111 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung,
        mit einer bestimmten Anzahl an Grauwerten.

        Parameter:
        ----------
        function_oben: obere Grenze der Grauwerte fuer binarisierte Kennlinie.

        function_unten: untere Grenze der Grauwerte fuer binarisierte
        Kennlinie.

        anz_grauwerte: Anzahl der Grauwerte, die in Transformation (Kennlinien)
        enthalten sein sollen.
    """
    # Funktion
    function = np.arange(anz_grauwerte)
    # Transformationsfunktion (Kennlinien erzeugen)
    # linear
    kennlinie_linear = function
    # negativ linear
    kennlinie_negativ = (anz_grauwerte - 1) - function
    # quadratisch
    kennlinie_quadr = function**2 / (anz_grauwerte - 1)
    # Wurzel
    kennlinie_sqrt = np.sqrt(anz_grauwerte * function)
    # binarisiert
    kennlinie_binaer = (function >= function_unten) * \
                       (function <= function_oben) * anz_grauwerte
    # Gauß:
    # Standardabweichung fuer Gaußverteilung
    std = 85
    # Mittelwert fuer Gaußverteilung
    mue = 0
    kennlinie_gauss = 258 - (54942 / (np.sqrt(2 * np.pi)) * std) * \
        np.exp(-(function - mue)**2 / (2 * std**2))
    return [kennlinie_linear, kennlinie_negativ, kennlinie_quadr,
            kennlinie_sqrt, kennlinie_binaer, kennlinie_gauss]


def use_kennlinien(graukeil, kennlinien):
    """ wendet Kennlinien auf linearen Graukeil (derselben Größe) an.

        Parameter:
        ----------
        graukeil: Graukeil, auf den jeweils Kennlinien angewendet werden.

        kennlinien: Transformationsfunktionen (Kennlinien), die auf linearen
        Graukeil angewendet werden.
        """
    # (jeweils fuer jede Kennlinie) jeden Pixel einzeln durchgehen
    graukeile = []
    for kennlinie in kennlinien:
        graukeil_kennlinie = np.zeros_like(graukeil)
        for x in range(len(graukeil)):
            for y in range(len(graukeil)):
                graukeil_kennlinie[y, x] = kennlinie[np.int
                                                    (round(graukeil[y, x]))]
        graukeile.append(graukeil_kennlinie)
    return graukeile


def plot_vorbereitung_6sp(ueberschrift):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        Ueberschrift, einzelnen Subplots etc. """
    # Erstellen von (sechs) Subplots:
    fig, axs = plt.subplots(2, 3, figsize=(13, 10), facecolor='w')
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    # TODO: Abstaende der Subplots besser machen
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.1, 0.9, 0.95])
    axs = axs.ravel()
    return axs


def plot_graukeile_transform(graukeile):
    """ Plot der einzelnen Graukeile nach Anwendung der einzelnen
        Kennlinien (= transformiert).
    """
    # Erstellung einzelner Subplots
    axs = plot_vorbereitung_6sp('Die Auswirkung verschiedener Kennlinien')
    # Ueberschriften der einzelnen Subplots
    # TODO: in Schleife?
    ax0 = axs[0]
    ax0.set_title("Linear")
    axs[1].set_title("Negativ linear")
    axs[2].set_title("Quadratisch")
    axs[3].set_title("Wurzel")
    axs[4].set_title("Binarisiert")
    axs[5].set_title("Gauss")
    for i in range(6):
        axs[i].imshow(graukeile[i], cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()


def main():
    # Graukeil erzeugen
    graukeil = make_graukeil(256, 256)
    # erzeuge Kennlinien
    kennlinien = make_kennlinien(100, 150, 256)
    # einzelnen Kennlinien auf den linearen Graukeil anwenden und einzelne
    # transformierten Graukeile abspeichern
    graukeile = use_kennlinien(graukeil, kennlinien)
    # Plot der einzelnen transformierten Graukeile
    plot_graukeile_transform(graukeile)


if __name__ == "__main__":
    main()
