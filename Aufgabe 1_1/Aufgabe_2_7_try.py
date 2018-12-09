"""
    Aufgabe 2.7:
    Berechnet 2D Fouriertransformierte und das Leistungsspektrum des Bildes
    aus Aufgabe 1.1
"""

import numpy as np
import matplotlib.pyplot as plt

import Aufgabe_1_1


def calculate_fourier(image):
    """ Ermittelt die 2D-dimensionale (diskrete) Fouriertransformierte sowie
        weitere Parameter (z.B. Leistungsspektrum, Amplituden- und Phasenbild
        etc., entsprechend der Vorlesung, Folie 78 aus dem Modul MF-MRS_14
        Digitale Bildverarbeitung).

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # 2D-Fouriertransformation
    fourier_image = np.fft.fft2(image)
    # Berechnung Imaginär- und Realteil der Fouriertransformierten
    imag = np.imag(fourier_image)
    real = np.real(fourier_image)
    # Ermittlung des Phasenbildes
    phase = np.arctan(imag / real)
    # Ermittlung des Leistungsspektrums
    power = real**2 + imag**2
    # Ermittlung des Amplitudenbildes
    amplitude = np.sqrt(power)
    return fourier_image, power, amplitude, phase


def umrechnung_koord_fourier(image_local, laenge_quadrant):
    """ Umrechnung der Koordinaten fuer die richtige Darstellung von
        Parametern der Fouriertransformation (siehe Vorlesung, Folie 78 aus
        dem Modul MF-MRS_14 Digitale Bildverarbeitung).

        Parameter:
        ----------
        laenge_quadrant: Anzahl an Pixeln, welche Bild in vier Quadranten
        einteilt: zur Erstellung eines globalen Koordinatensystem.
    """
    image_global = np.zeros((len(image_local), len(image_local)))
    for i in range(len(image_local)):
        image_global[image_local[i, :]] =+ laenge_quadrant
        image_global[image_local[:, i]] =- (laenge_quadrant) * -1
        #image_global[i, :] = image_local[i, :] + laenge_quadrant
        #image_global[:, i] = -1 * (image_local[:, i] - laenge_quadrant)
    return image_global


def plot_vorbereitung(ueberschrift, unterueberschrift1, unterueberschrift2,
                      unterueberschrift3):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Subplots, Ueberschriften etc.
    """
    fig = plt.figure(figsize=(7, 8))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    # erster Subplot
    ax1 = fig.add_subplot(221)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift1)
    # zweiter Subplot
    ax2 = fig.add_subplot(222)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift2)
    # dritter Subplot
    ax3 = fig.add_subplot(223)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift3)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.9])
    return ax1, ax2, ax3


def main():
    # Bild- Array (aus Aufgabe 1.1) erstellen
    szinti, pixel, pixel_quadrant = Aufgabe_1_1.make_szinti()
    # Fouriertransformation
    fourier_image, power, amplitude, phase = calculate_fourier(szinti)
    # Umrechnung in richtige Koordinaten
    power_global = umrechnung_koord_fourier(power, pixel_quadrant)
    amplitude_global = umrechnung_koord_fourier(amplitude, pixel_quadrant)
    phase_global = umrechnung_koord_fourier(phase, pixel_quadrant)
    # Plots:
    ax1, ax2, ax3 = plot_vorbereitung('Fouriertransformation des Bildes ' +
                                      'aus Aufgabe 1.1', 'Leistungsspektrum',
                                      'Amplitudenbild', 'Phasenbild')
    # Leistungsspektrum
    ax1.imshow(power_global, cmap='gray')
    # Amplitudenbild
    ax2.imshow(amplitude_global, cmap='gray')
    # Phasenbild
    ax3.imshow(phase_global, cmap='gray')


if __name__ == "__main__":
    main()

# Interpretation:
    # Phasenbild codiert raeumliche Info
    # Linien entsprechen Aenderungen in Grauwerten / Farbspruenge / Kanten
    # gar keine Linien hier? keine Farbaenderungen?   