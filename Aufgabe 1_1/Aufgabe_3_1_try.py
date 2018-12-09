"""
    Aufgabe 3.1.
    Programmiert einen linearen Graukeil (mit 256 Grauwerten) und wendet die
    Kennlinien aus der Vorlesung, Folie 111 aus dem Modul MF-MRS_14 Digitale
    Bildverarbeitung darauf an.
"""

import numpy as np
import matplotlib.pyplot as plt

# TODO: Plotfkt: (mit norm, extent usw...)


def make_graukeil(anz_pixel, anz_grauwerte):
    """ Erstellt einen linearen (quadratischen) Graukeil (mit bestimmten
        Anzahl Grauwerte).

        Parameter:
        ----------
        anz_pixel: Anzahl an Pixeln (in x- und y-Richtung).

        anz_grauwerte: Anzahl der Grauwerte, die im Graukeil enthalten sein
        sollen.
    """
    graukeil = np.ones((anz_pixel, anz_pixel)) * np.arange(anz_grauwerte)
    return graukeil


def make_kennlinien(function_unten, function_oben, anz_grauwerte):
    """ Erstellt eine Look-up-Table mit verschiedenen Kennlinien aus der
        Vorlesung, Folie 111 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung
        mit einer bestimmten Anzahl an Grauwerten

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


def kennlinie_anwenden(graukeil, kennlinien):
    """ wendet diese auf linearen Graukeil (derselben Größe) an.

        Parameter:
        ----------
        graukeil: Graukeil, auf den Kennlinie angewendet wird.

        kennlinien: Transformationsfunktionen (Kennlinien), die auf linearen
        Graukeil angewendet werden.
        """

    # Kennlinie auf Graukeil anwenden:
    # jeden Pixel einzeln durchgehen fuer jede Kennlinie
    # leere Liste zum Reinspeichern
    graukeile = []
    for kennlinie in kennlinien:
        graukeil_kennlinie = np.zeros_like(graukeil)
        for x in range(len(graukeil)):
            for y in range(len(graukeil)):
#                a = np.int(round(graukeil[y, x]))
#                b = kennlinie[a]
#                graukeil_kennlinie[y, x] = b
                graukeil_kennlinie[y, x] = kennlinie[np.int
                                                    (round(graukeil[y, x]))]
        graukeile.append(graukeil_kennlinie)
    return graukeile


def plot_vorbereitung(ueberschrift):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        Ueberschrift, einzelnen Subplots etc. """
    # Erstellen von (sechs) Subplots:
    fig, axs = plt.subplots(3, 2, figsize=(10, 10), facecolor='w')
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    axs = axs.ravel()
    return axs


def plot_graukeile_transform(graukeile):
    """ Plot der einzelnen Graukeile nach Anwendung der einzelnen
        Kennlinien.

        Parameter:
        ----------
        graukeile: Liste von linearen Graukeilen, auf den eine bestimmte
        Kennlinie angewendet wurde.
    """
    # Erstellung einzelner Subplots
    axs = plot_vorbereitung('Die Auswirkung verschiedener Kennlinien')
    for i in range(6):
        axs[i].set_title(f'''Kennlinie: {i}''')
        axs[i].imshow(graukeile[i], cmap='gray', extent=[-128, 128, -128, 128])


def main():
    # Graukeil erzeugen
    graukeil = make_graukeil(256, 256)
    # erzeuge Kennlinien
    kennlinien = make_kennlinien(100, 150, 256)
    # einzelnen Kennlinien auf den linearen Graukeil anwenden und abspeichern
    # der einzelnen transformierten Graukeile
    graukeile = kennlinie_anwenden(graukeil, kennlinien)
    # Plot der einzelnen transformierten Graukeile
    plot_graukeile_transform(graukeile)


if __name__ == "__main__":
    main()
