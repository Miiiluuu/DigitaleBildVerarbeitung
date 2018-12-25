"""
    Programmierbeleg zum Modul MF-MRS_14 Digitale Bildverarbeitung, WS 18/19:
    Unter anderem Darstellung eines Szintigramms, anhand dessen
    verschiedene Bildmodifikatiotionen durchgefuehrt wird.

    @author: Mieke Möller
"""
# TODO: Fkt sortieren nach Berechnen, Plotten
# TODO: Style Code Analysis bei Karl angucken
# TODO: Fkt make.szinti() unnoetigerweise sehr oft aufgerufen?
# TODO: immer rescaled?
# TODO: Funktion in Windowskonsole schließt sich sofort?
# TODO: Ergebnisse vergleichen
# TODO: Fkt unnoetigerweise doppelt aufgerufen?
# TODO: welche Fkt sind wirklich nuetzlich?

import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import copy
from matplotlib.colors import LogNorm
import numba
import time


def make_scale(image):
    """ Skalieren der Zahlenwerte eines Arrays, sodass gesamter
        Grauwertebereich von 0...255 umfasst wird.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # niedrigster Wert soll sein: 0 ≙ schwarz
    if np.min(image) != 0:
        image -= np.min(image)
    # hoechster Wert soll sein: 255 ≙ weiß
    weiß = 255
    hoechster_grauwert = np.max(image)
    # Berechnung Skalierungsfaktor, sodass hoechster Grauwert erfasst wird
    skal = weiß / hoechster_grauwert
    # Skalierungsfaktor auf gesamtes Szintigramm anwenden
    image *= skal
    return image


def get_image_A(laenge_quadrant, kantenlaenge, avg_a, mittelpkt):
    """ Erzeugt Objekt A, ist Quadrat.

        Parameter:
        ----------
        laenge_quadrant: Anzahl an Pixeln des lokalen Koordinatensystems.

        kantenlaenge: Kantenlaenge des Quadrats (Flaechenquelle A) in mm.

        avg_a: mittlere flaechenbezogene Zahl der registrierten
        Ereignisse von Objekt A, in 1/mm².

        mittelpkt: Koordinaten des globalen Koordinatensystems als
        (x, y) in (mm, mm).
    """
    # erstelle Array, in dem sich Flaechenquelle A befindet
    # ≙ lokales Koordinatensystem
    image_a = np.zeros((laenge_quadrant, laenge_quadrant))
    # richtige Positionierung von Flaechenquelle A im Bezug zum Rand:
    # Abstand Quellenkante zum Rand in x- Richtung
    abstand_x = mittelpkt[0] - kantenlaenge // 2
    # Abstand Quellenkante zum Rand in y- Richtung
    abstand_y = laenge_quadrant - mittelpkt[1] - kantenlaenge // 2
    quelle_a = image_a[abstand_y:abstand_y + kantenlaenge,
                       abstand_x:abstand_x + kantenlaenge]
    # auf jeden Pixel von Quelle A Poisson- Statistik anwenden
    # dadurch Beachtung des statistischen Charakters des
    # radioaktiven Zerfalls
    for i in range(kantenlaenge):
        for j in range(kantenlaenge):
            quelle_a[i, j] = np.random.poisson(avg_a)
    return image_a


def get_image_B(laenge_quadrant, kantenlaenge, avg_b_g, avg_b_w,
                mittelpkt, deltax):
    """ Erzeugt Objekt B, ist Quadrat mit Streifen.

        Parameter:
        ----------
        laenge_quadrant: Anzahl an Pixeln des lokalen Koordinatensystems.

        kantenlaenge: Kantenlaenge des Quadrats (Flaechenquelle B) in mm.

        avg_b_g: mittlere flaechenbezogene Zahl der registrierten
        Ereignisse von Objekt B, graue Streifen, in 1/mm².

        avg_b_w: mittlere flaechenbezogene Zahl der registrierten
        Ereignisse von Objekt B, weiße Streifen, in 1/mm².

        mittelpkt: Koordinaten des globalen Koordinatensystems als
        (x, y) in (mm, mm).

        deltax: Breite der Streifen bzw. der einzelnen Flaechenquellenpaare
        in mm.
    """
    # erstelle Array, in dem sich Flaechenquelle B befindet
    image_b = np.zeros((laenge_quadrant, laenge_quadrant))
    # TODO: Erstellung dieses Quadrats doppelt sich, schlimm?
    # richtige Positionierung von Flaechenquelle B im Bezug zum Rand:
    # Abstand Quellenkante zum Rand in x- Richtung
    abstand_x = laenge_quadrant + mittelpkt[0] - kantenlaenge // 2
    # Abstand Quellenkante zum Rand in y- Richtung
    abstand_y = laenge_quadrant - mittelpkt[1] - kantenlaenge // 2
    quelle_b = image_b[abstand_y:abstand_y + kantenlaenge,
                       abstand_x:abstand_x + kantenlaenge]
    # Belegung der Flaeche mit zehn Paar Flaechenquellen (in Form von Streifen)
    # dafuer Anwendung Poisson- Statistik zur Charakterisierung der Streifen
    i = 0
    while i < kantenlaenge:
        quelle_b[:, i:i+deltax] = np.random.poisson(avg_b_g,
                                                    (kantenlaenge, deltax))
        i += deltax
        quelle_b[:, i:i+deltax] = np.random.poisson(avg_b_w,
                                                    (kantenlaenge, deltax))
        i += deltax
    return image_b


def get_image_C(laenge_quadrant, radius, avg_c, mittelpkt):
    """ Erzeugt Objekt C, ist Kreis.

        Parameter:
        ----------
        laenge_quadrant: Anzahl an Pixeln des lokalen Koordinatensystems.

        radius: Radius des Kreises in mm.

        avg_c: mittlere flaechenbezogene Zahl der registrierten Ereignisse
        von Objekt C, in 1/mm².

        mittelpkt: Koordinaten des globalen Koordinatensystems als
        (x, y) in (mm, mm).
    """
    # erstelle Array, in dem sich Flaechenquelle C befindet
    image_c = np.zeros((laenge_quadrant, laenge_quadrant))
    # lokaler Mittelpunkt (als (x, y)), von diesem aus Kreis mit Radius 50 mm
    # TODO: Berechnung Mittelpunkt lokal stimmt nur in diesem ganz speziellen
    # Fall? (ist nicht der Sinn von Parametern in Funktionen?)
    mitte_lokal = (laenge_quadrant + mittelpkt[0], -mittelpkt[1])
    # Kreisformel mit Satz des Pythagoras
    # jeden Pixel einzeln durchgehen
    for x in range(laenge_quadrant):
        for y in range(laenge_quadrant):
            deltax = mitte_lokal[0] - x
            deltay = mitte_lokal[1] - y
            if deltax**2 + deltay**2 <= radius**2:
                # Anwendung Poisson- Statistik fuer Beruecksichtigung
                # radioaktiver Zerfall
                image_c[y, x] = np.random.poisson(avg_c)
    return image_c


def get_image_D(laenge_quadrant, hoehe, avg_d, spitze):
    """ Erzeugt Objekt D, ist gleichseitiges Dreieck.

        Parameter:
        ----------
        laenge_quadrant: Anzahl an Pixeln des lokalen Koordinatensystems.

        hoehe: Hoehe des Dreiecks in mm.

        avg_d: mittlere flaechenbezogene Zahl der registrierten Ereignisse
        von Objekt D, in 1/mm².

        spitze: Koordinaten der Dreiecksspitze (x, y) in (mm, mm) im
        globalen Koordinatensystem.
    """
    # erstelle Array, in dem sich Flaechenquelle D befindet
    image_d = np.zeros((laenge_quadrant, laenge_quadrant))
    # Koordinaten der Spitze im lokalen Koordinatensystem:
    # TODO: Berechnung lokale Spitze stimmt nur in diesem ganz speziellen
    # Fall? (ist nicht der Sinn von Parametern in Funktionen?)
    spitze_lokal = (spitze[0], -spitze[1])
    # jeden Pixel der moeglichen Dreiecksflaeche einzeln durchgehen:
    # dabei wird y-Bereich von lokalen Spitze bis ... abgerastert:
    delta_y = spitze_lokal[1] + hoehe
    # jeden Pixel einzeln durchgehen
    for y in range(spitze_lokal[1], delta_y + 1):
        # aktuelle Hoehe
        akt_hoehe = np.absolute(spitze_lokal[1] - y)
        for x in range(laenge_quadrant):
            # Abstand zur Mitte ≙ aktueller x- Wert
            abstand_mitte = np.absolute(spitze_lokal[0] - x)
            # Formel zur Berechnung der Kantenlaenge des gleichseitigen
            # Dreiecks:
            # (falls Bedingung erfüllt ist, gehört Pixel zum Dreick
            # und es wird Poissonstatistik angewendet)
            if abstand_mitte <= akt_hoehe / np.sqrt(3):
                image_d[y, x] = np.random.poisson(avg_d)
    return image_d


def extract(image, y_begin, y_end, x_begin, x_end):
    """ Einteilung des Szintigramms in Quadranten und Extraktion.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        y_begin: Startpixel (in y-Richtung), welcher den Beginn des
        entsprechenden Quadranten bezeichnet. Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten.

        y_end: Pixel (in y-Richtung), welcher das Ende des
        entsprechenden Quadranten festlegt. Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten.

        x_begin: Startpixel (in x-Richtung), welcher den Beginn des
        entsprechenden Quadranten bezeichnet. Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten.

        x_end: Pixel (in x-Richtung), welcher das Ende des
        entsprechenden Quadranten festlegt. Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten.

        Zeichnung: TODO: ok?

                image:
                +-------------+--------------+
                |             |              |
                |             |              |
                |             |              |
                |             |              |
                |x_begin      |x_end         |
        y_begin +----------------------------+         +-------------+
                |             |              |         |             |
                |             |              |         |             |
                |       +-------------------------->   |             |
                |             |              |         |             |
                |             |              |         |             |
          y_end +-------------+--------------+         +-------------+

    """
    quadrant = image[y_begin:y_end, x_begin:x_end]
    return quadrant


def make_szinti():
    """ Erzeugung des Szintigramms aus Aufgabe 1.1. """
    # fuer Pixelgroeße von 256x256
    pixel = 256
    # Anzahl an Pixeln der Teilbilder (Flaechenquelle A, B, C und D, fuer
    # Erstellen (lokaler) Koordinatensysteme)
    # ≙ Mitte des globalen Koordinatensystems TODO: nicht immer?
    pixel_quadrant = pixel // 2
    # Erstellung Szintigramm = 256x256- Array
    # (Szintigramm-Flaeche ≙ globales Koordinatensystem)
    szinti = np.zeros((pixel, pixel))
    # Einteilung des Szintigramms in vier Quadranten
    # jedes Objekt befindet sich in jeweils einem Quadranten
    quadrant_eins = extract(szinti, 0, pixel_quadrant, pixel_quadrant, pixel)
    quadrant_zwei = extract(szinti, 0, pixel_quadrant, 0, pixel_quadrant)
    quadrant_drei = extract(szinti, pixel_quadrant, pixel, 0, pixel_quadrant)
    quadrant_vier = extract(szinti, pixel_quadrant, pixel,
                            pixel_quadrant, pixel)
    # Objekte dem richtigen Platz im Szintigramm zuweisen
    # (Parameter der einzelnen Flaechenquellen siehe Vorlesung zu Modul
    # MF-MRS_14 Digitale Bildverarbeitung Folie 17)
    image_a = get_image_A(pixel_quadrant, 100, 200, (60, 60))
    quadrant_eins[:, :] = image_a
    image_b = get_image_B(pixel_quadrant, 100, 250, 300, (-60, 60), 5)
    quadrant_zwei[:, :] = image_b
    image_c = get_image_C(pixel_quadrant, 50, 50, (-60, -60))
    quadrant_drei[:, :] = image_c
    image_d = get_image_D(pixel_quadrant, 100, 100, (60, -10))
    quadrant_vier[:, :] = image_d
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    szinti = make_scale(szinti)
    return szinti, pixel, pixel_quadrant


def extraktion_aus_array(array, y):
    """ Extrahiert für eine entsprechenden Ordinatenwertlinie alle
        dazugehörigen (Grau-)Werte.

        Parameter:
        ----------
        array: Array, Eingabewerte.

        y: Ordinatenwert, bei dem alle dazugehoerigen Abszissenwerte
        extrahiert werden.
    """
    teil_array = array[y, :]
    return teil_array


# TODO: plot_vorbereitungen 2, 3 oder 9 Subplots in einer Fkt?
def plot_vorbereitung_2sp(ueberschrift, unterueberschrift1, unterueberschrift2,
                          abszisse='', ordinate='', ticks=False):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        entsprechenden Ueberschriften, 2 Subplots, Achsenbeschriftung etc.
    """
    fig = plt.figure(figsize=(10, 5))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    # erster Subplot
    ax1 = fig.add_subplot(121)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift1)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # zweiter Subplot
    ax2 = fig.add_subplot(122)
    # Hinzufuegen einer Unterueberschrift
    plt.title(unterueberschrift2)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.9])
    # Position der Subplots untereinander veraendern:
    # vertikalen Abstand vergroeßern
    plt.subplots_adjust(wspace=0.3)
    # bei Bedarf Achsenbeschriftung mit Grid
    if ticks:
        ticks = np.linspace(-0.5, 0.5, 11)
        ax1.set_xticks(ticks)
        ax1.set_yticks(ticks)
        ax1.set_xticklabels(ticks, rotation=75)
        ax2.set_xticks(ticks)
        ax2.set_yticks(ticks)
        ax2.set_xticklabels(ticks, rotation=75)
    return ax1, ax2


# TODO: sehr speziell bezeichnete Fkt. Bloed?
def plot_profile(xwerte1, grauwerte1, xwerte2, grauwerte2):
    """ Stellt Grauwertprofile fuer das Bild aus Aufgabe 1.1. längs
        bestimmter y- Linien dar.

        Parameter:
        ----------
        xwerte1, xwerte2: Abszissenwerte entlang bestimmter y- Linien.

        grauwerte1, grauwerte2: Grauwerte entlang bestimmter y- Linien.
    """
    ax1, ax2 = plot_vorbereitung_2sp('Grauwertprofile fuer das Bild aus ' +
                                     'Aufgabe 1.1', 'laengs y = 60',
                                     'laengs y = -60', r'$x/mm$',
                                     'Grauwert')
    ax1.plot(xwerte1, grauwerte1)
    ax2.plot(xwerte2, grauwerte2)
    plt.show()


# TODO: ist relativ langsam. Numba?
def erstelle_grauwerthist(werte, herkunft):
    """ Erstellung Grauwertprofil, Darstellung auf zwei Weisen:
        1. logarithmischer Skaleneinteilung,
        2. Zur besseren Darstellung kleinerer Werte ist Ordinatenachse bei
        bestimmten Wert abgeschnitten.

        Parameter:
        ----------
        werte: Array, Eingabewerte.
        
        herkunft: bezeichnet jenes Bild, welches zur Erstellung des Grauwert-
        histogramms genutzt wird.
    """
    ax1, ax2 = plot_vorbereitung_2sp(f'''Grauwerthistogramm fuer ''' +
                    f'''{herkunft}''', 'logarithmische Skala',
                    f'''gekuerzte Ordinatenachse''', r'$f$',
                    f''''Häufigkeitsverteilung $h(f)$''')
    ax1.hist(werte, bins=256, density=True, log=True)
    ordinate, _, _ = ax2.hist(werte, bins=256, density=True)
    # Ordinatenwerte sortieren
    ordinate_sort = np.sort(ordinate)
    # Ordinatenachse kuerzen
    plt.ylim(0, ordinate_sort[-2] * 1.1)
    plt.show()


def mittelwert_grauwerthist(ordinate, abszisse):
    """ Berechnet den Mittelwert eines Grauwert-Histogramms.

        Parameter:
        ----------

        ordinate: relative Histogrammverteilung (Ordinatenwerte des
        Histogramms).

        abszisse: Grauwerte (Abszisse) des Grauwert-Histogramms.
    """
    # Berechnung vom  Mittelwertes des Grauwert-Histogramms entsprechend
    # der Vorlesung, Folie 33 aus dem Modul MF-MRS_14 Digitale
    # Bildverarbeitung
    avg_hist = np.sum(abszisse * ordinate)
    print(f'''Der Mittelwertes des Grauwert-Histogramms des Szintigramms ''' +
          f'''betraegt {np.round(avg_hist, 3)}.''')
    return avg_hist


def schiefe_grauwerthist(ordinate, abszisse, mittel):
    """ Berechnet die Schiefe eines Grauwert-Histogramms.

        Parameter:
        ----------

        ordinate: relative Histogrammverteilung (Ordinatenwerte des
        Histogramms).

        abszisse: Grauwerte (Abszisse) des Grauwert-Histogramms.

        mittel: Mittelwert des Grauwert-Histogramms.
    """
    # Berechnung der Schiefe des Grauwert-Histogramms entsprechend
    # der Vorlesung, Folie 34 aus dem Modul MF-MRS_14 Digitale
    # Bildverarbeitung:
    # Berechnen der Varianz des Grauwert-Histogramms
    varianz = np.sum(ordinate * (abszisse - mittel)**2)
    drittes_moment = np.sum(ordinate * (abszisse - mittel)**3)
    schiefe = drittes_moment / varianz**(3 / 2)
    print(f'''Die Schiefe des Grauwert-Histogramms aus dem Szintigramm''' +
          f'''betraegt {np.round(schiefe, 3)}.''')


def infogehalt(image):
    """ Berechnet den mittleren Informationsgehalt pro Pixel fuer ein
        Bild.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Histogrammverteilung (Ordinatenwerte des Histogramms) erstellen
    haufigkeiten, _ = np.histogram(image, bins=256)
    # Darstellung der relativen Haeufigkeitsverteilung
    # durch Normierung mit Anzahl der Bildpunkte
    haufigkeiten = haufigkeiten / np.sum(haufigkeiten)
    # Nullen aus relativer Histogrammverteilung entfernen
    haufigkeiten = haufigkeiten[haufigkeiten != 0]
    # Berechnung des Informationsgehaltes je Pixel entsprechend der Vorlesung,
    # Folie 39 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung
    info = np.sum(-haufigkeiten * np.log2(haufigkeiten))
    return info


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
        info = infogehalt(image[i])
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
    

def differenzbild(image):
    """ Funktion erstellt ein Differenzbild.
        
        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    differenz_image = np.zeros((len(image), len(image)))
    # Berechnung nach Differenzverfahren entsprechend der Vorlesung,
    # Folie 43f aus dem Modul MF-MRS_14 Digitale Bildverarbeitung
    for x in range(len(image)):
        for y in range(len(image)):
            differenz_image[y, x] = image[y, x] - image[y, x-1]
    # Addieren einer Konstanten auf alle Pixel, um negative Grauwerte zu
    # vermeiden
    konstante = np.absolute(np.amin(differenz_image))
    differenz_image += konstante
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    differenz_image = make_scale(differenz_image)
    return differenz_image


def vgl_infogehalt_differenz(bild1, bild2, info1, info2):
    """ Stellt den mittleren Informationsgehalt pro Pixel fuer 2 Bilder
        in einer Tabelle vergleichend gegenueber.

        Parameter:
        ----------
        bild1: Array, Eingabewerte fuer ein Bild1.
        
        bild2: Array, Eingabewerte fuer ein Bild2.
        
        info1: mittlerer Informationsgehalt je Pixel fuer ein Bild1.
        
        info2: mittlerer Informationsgehalt je Pixel fuer ein Bild2.
    """
    # Erstellung PrettyTable
    x = PrettyTable()
    x.field_names = ['Bild', 'mittlerer Informationsgehalt in ' +
                     'Bit/Pixel']
    x.add_row([bild1, info1])
    x.add_row([bild2, info2])
    print(x)


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
    fourier_image = np.fft.fftshift(fourier_image)
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


# TODO: warum ist Ueberschrift so weit oben?
def plot_vorbereitung_3sp(ueberschrift, unterueberschrift1, unterueberschrift2,
                          unterueberschrift3, abszisse, ordinate):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        drei Subplots, Ueberschriften, Achsenbeschriftungen etc.
    """
    # Erstellen von (drei) Subplots:
    fig, axs = plt.subplots(1, 3, figsize=(10, 10), facecolor='w')
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    axs = axs.ravel()
    # TODO: Schleife??
    # Unterueberschriften der Subplots
    axs[0].set_title(unterueberschrift1)
    axs[1].set_title(unterueberschrift2)
    axs[2].set_title(unterueberschrift3)
    fig.subplots_adjust(hspace=0.5, wspace=0.5)
    # Achsenbeschriftungen und Grid
    ticks = np.linspace(-0.5, 0.5, 11)
    for i in range(3):
        axs[i].set_xlabel(abszisse)
        axs[i].set_ylabel(ordinate)
        axs[i].set_xticks(ticks)
        axs[i].set_yticks(ticks)
        axs[i].set_xticklabels(ticks, rotation=75)
    return axs


# TODO: Fkt unsinnig da nur einmal verwendet?
def plot_fourier(power, amplitude, phase, herkunft):
    """"Darstellung des Leistungsspektrums, Phasen- und Amplitudenbild einer
        2D-Fouriertransformierten.

        Parameter:
        ----------
        herkunft: bezeichnet jenes Bild, welches zur Erstellung des Plottes
        genutzt wird.

        power: Leistungsspektrum einer 2D-Fouriertransformierten.

        amplitude: Amplitudenspektrum einer 2D-Fouriertransformierten.

        phase: Phasenbild einer 2D-Fouriertransformierten.
    """
    axs = plot_vorbereitung_3sp(f'''Fouriertransformation {herkunft}''',
                                'Leistungsspektrum',
                                'Amplitudenbild', 'Phasenbild',
                                '$ν_{x}/ν_{Sx}$', '$ν_{y}/ν_{Sy}$')
    # Leistungsspektrum
    axs[0].imshow(power, cmap='gray', norm=LogNorm(),
                  extent=[-0.5, 0.5, -0.5, 0.5])
    # Amplitudenbild
    axs[1].imshow(amplitude, cmap='gray', norm=LogNorm(),
                  extent=[-0.5, 0.5, -0.5, 0.5])
    # Phasenbild
    axs[2].imshow(phase, cmap='gray', norm=LogNorm(),
                  extent=[-0.5, 0.5, -0.5, 0.5])
    plt.show()
    
    
def drehmatrix(grad):
    """ Drehung eines Bildes in positivem Drehsinne (siehe Vorlesung,
        Folie 88, 131 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung).

        Parameter:
        ----------
        grad: Angabe der Drehung in Grad (im positivem Drehsinne), in Einheit
        Grad.
    """
    # Umrechnung Winkel in Bogenmaß
    grad_rad = np.radians(grad)
    # Drehmatrix in homogenen Koordinaten
    dreh = np.array([[np.cos(grad_rad), np.sin(grad_rad), 0],
                     [-np.sin(grad_rad), np.cos(grad_rad), 0], [0, 0, 1]])
    # Drehmatrix invertieren, da Transformation im positiven Sinn
    dreh = np.linalg.inv(dreh)
    return dreh


# TODO: Grauwertappromimation!
def transformation(image, pixel_mitte, transform):
    """ Transformation eines Bildes in positivem Drehsinne (siehe Vorlesung,
        Folie 88, 131 aus dem Modul MF-MRS_14 Digitale Bildverarbeitung).

        Parameter:
        ----------
        image: Array, Eingabewerte.

        pixel_mitte: Pixel, bei dem Mitte des Koordinaensystems liegt.
        TODO: nicht immer perfekt eingehalten?
        
        transform: Transformationsmatrix, die Transformation eines Bildes
        durchfuehrt.
    """
    image_transform = np.zeros_like(image)
    # Schleife:
    # jeden Pixel einzeln durchgehen, auf diesem Drehmatrix anwenden
    # und neue rotierte Koordinaten berechnen
    # Rotation mit Drehmatrix bezieht sich auf Nullpunkt des Koordinatensystems
    # das heißt fuer eine Drehung um die Mitte des Bildes muss der Nullpunkt
    # des Koordinatensystems in die Mitte des Bildes gelegt werden
    # (ansonsten Drehung um obere linke Ecke des Bildes)
    for x in range(-pixel_mitte, pixel_mitte):
        for y in range(-pixel_mitte, pixel_mitte):
            # Rotationsmatrix auf alle x-Werte anwenden
            koord_xy_transform = (transform @ np.array([x, y, 1]))
            x_transform = np.int_(np.round(koord_xy_transform[0]))
            y_transform = np.int_(np.round(koord_xy_transform[1]))
            # Pixel des Null-Arrays (image_transform) auffuellen:
            # Pruefen, ob rotierter Wert innerhalb Bereich Originalbild
            # vorkommt
            # wenn Bedingung erfuellt existieren Grauwerte im Originalbild,
            # die ins rotierte Bild an der richtigen Stelle uebernommen werden
            # (ansonsten Nullen an dieser Stelle)
            if (-pixel_mitte <= x_transform < pixel_mitte) and \
               (-pixel_mitte <= y_transform < pixel_mitte):
                # Addieren vom Zahlenwert des Pixels,von Mitte des 
                # Koordinatensystems, um Array nicht mit negativen Indices
                # anzusprechen (wuerde falsche Werte liefern)
                image_transform[y + pixel_mitte, x + pixel_mitte] = \
                    image[y_transform + pixel_mitte, x_transform + pixel_mitte]
    return image_transform
       

def aufgabe_1_1(szinti, pixel, pixel_quadrant):
    """ Darstellung eines aufgenommenen Szintigramms, bestehend aus 256x256
        Pixel, aufgebaut aus vier Flaechenquellen (weitere Parameter siehe
        Vorlesung zu Modul MF-MRS_14 Digitale Bildverarbeitung)
    """
    print("")
    print("Aufgabe 1.1:")
    print("")
    # Szintigramm als Plot zeichnen
    plt.figure()
    plt.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    plt.show()


def aufgabe_2_1(szinti, pixel, pixel_quadrant):
    """
        Erstellt die Grauwertprofile fuer das Bild aus Aufgabe 1.1 laengs der
        Linien y = 60 mm und y = -60 mm.
    """
    print("")
    print("Aufgabe 2.1:")
    print("")
    # Extrahieren Grauwerte entlang von bestimmten y- Linien
    # (siehe Aufgabenstellung):
    # laengs y = 60, mit Umrechnung globales/lokales Koordinatensystem
    grauwertprofil_60 = extraktion_aus_array(szinti, pixel_quadrant - 60)
    # laengs y = -60, mit Umrechnung globales/lokales Koordinatensystem
    grauwertprofil_minus60 = extraktion_aus_array(szinti, pixel_quadrant + 60)
    # Plots: Erstellung Grauwertprofile
    plot_profile(np.arange(-pixel_quadrant, pixel_quadrant), grauwertprofil_60,
                 np.arange(-pixel_quadrant, pixel_quadrant),
                 grauwertprofil_minus60)


def aufgabe_2_2(szinti, pixel, pixel_quadrant):
    """ Erstellt das Grauwerthistogramm des Bildes aus Aufgabe 1.1 und stellt
        es graphisch dar. """
    print("")
    print("Aufgabe 2.2:")
    print("")
    # Grauwerthistogramm zeichnen:
    erstelle_grauwerthist(szinti.flatten(), "das Bild aus Aufgabe 1.1")


def aufgabe_2_3(szinti, pixel, pixel_quadrant):
    """ Berechnet Mittelwert und Schiefe des Grauwert-Histogramms aus Aufgabe
        2.2.
    """
    print("")
    print("Aufgabe 2.3:")
    print("")
    # relative Histogrammverteilung aus dem Bild aus Aufgabe 1.1
    # (Ordinatenwerte des Grauwerthistogramms) erstellen
    haufigkeit, _ = np.histogram(szinti, bins=256, density=True)
    # Grauwerte (Abszisse) des Grauwert-Histogramms
    grauwerte = np.arange(pixel)
    # Mittelwert des Grauwertdiagramms aus Aufgabe 2.2 berechnen
    avg_hist = mittelwert_grauwerthist(haufigkeit, grauwerte)
    # Schiefe des Grauwertdiagramms aus Aufgabe 2.2 berechnen
    schiefe_grauwerthist(haufigkeit, grauwerte, avg_hist)


def aufgabe_2_4(szinti, pixel, pixel_quadrant):
    """ Berechnet den mittleren Informationsgehalt pro Pixel fuer das Bild aus
        Aufgabe 1.1.
    """
    print("")
    print("Aufgabe 2.4:")
    print("")
    # Informationsgehalt pro Pixel berechnen
    info = infogehalt(szinti)
    # Ausgabe des Informationsgehaltes pro Pixel fuer das Bild aus Aufgabe 1.1
    print(f'''Der mittlere Informationsgehalt pro ''' +
          f'''Pixel fuer das Bild aus Aufgabe 1.1 betraegt ''' +
          f'''{np.round(info, 3)} Bit/Pixel.''')


# TODO:  Ergebnisse vergleichen
def aufgabe_2_5(szinti, pixel, pixel_quadrant):
    """ Erstellt die Bitebenen aller Bilder aus Aufgabe 1.1 und berechnet fuer
        jede Ebene den mittleren Informationsgehalt je Pixel.
    """
    print("")
    print("Aufgabe 2.5:")
    print("")
    # Erstellung Bitebenen
    ebene = erstellung_bitebenen(szinti)
    # Berechnung mittlerer Informationsgehalt pro Pixel
    infogehalt_einzelne_bitebenen(ebene)
    # Interpretation!!!
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
    

# TODO: ist relativ langsam. Numba?
def aufgabe_2_6(szinti, pixel, pixel_quadrant):
    """ Berechnet aus Aufgabe 1.1 ein Differenzbild. Von diesem Differenzbild
        wird ein Histogramm erzeugt sowie dessen mittlerer Informationsgehalt
        ermittelt und dem Originalbild vergleichend gegenuebergestellt.
    """
    print("")
    print("Aufgabe 2.6:")
    print("")
    # Plot Histogramm fuer Originalbild aus Aufgabe 1.1
    erstelle_grauwerthist(szinti.flatten(), "das Bild aus Aufgabe 1.1")
    # Erstellung Differenzbild
    differenz = differenzbild(szinti)
    # Plot Histogramm des Differenzbildes
    erstelle_grauwerthist(differenz.flatten(), "das Differenzbild")
    # Berechnung mittlerer Informationsgehalt pro Pixel fuer das Originalbild
    info_original = infogehalt(szinti)
    # Berechnung mittlerer Informationsgehalt pro Pixel fuer das
    # Differenzbild
    info_differenz = infogehalt(differenz)
    # Gegenueberstellung der beiden Informationsgehalte in einer Tabelle
    vgl_infogehalt_differenz('Original', 'Differenz',
                             np.round(info_original, 3),
                             np.round(info_differenz, 3))
    # Interpretation!!!
        # Differenz entspricht Kompression: eigentlich verlustfrei
        # das heißt Infogehalt muesste derselbe sein?
        # Eliminierung redundanter Bildinformationen
        # Wiederherstellung des Originalbildes i.a. moeglich
        # Sinn: durch Bildung der Differenz muessen nur noch kleine Zahlenwerte
        # abgespeichert werden
        # aber laut Tabelle: Differenzbild weißt weniger Infogehalt auf
        # laut Formel: bei benachbarten Pixeln mit denselben Grauwerten
        # ergibt sich als Differenz Null
        # das heißt wirkliche Bildinformationen treten nur an Kanten/ starken
        # Bildkontrasten auf
        # auf spitze Form des Histogramms eingehen:
        # viele relativ kleine/ mittlere Werte werden abgespeichert im
        # Differenzbild, keine hohen Farbwerte (da Differenzbildung)
        # Infogehalt ist pro Pixel
        # bei Differenzbild ist zwischen einzelnen Pixeln eine mathematische
        # Abhaengigkeit, bei Originalbild sind Pixel voneinander unabhaengig.
        # das heißt PRO Pixel ist es bei Differenz niedriger
    

def aufgabe_2_7(szinti, pixel, pixel_quadrant):
    """ Berechnet 2D Fouriertransformierte und das Leistungsspektrum des
        Bildes aus Aufgabe 1.1:
    """
    # Fouriertransformation
    fourier_image, power, amplitude, phase = calculate_fourier(szinti)
    # graphische Darstellung der Fouriertransformierten
    plot_fourier(power, amplitude, phase, "des Bildes aus Aufgabe 1.1")  
    # Interpretation!!!
        # Phasenbild codiert raeumliche Info
        # Linien entsprechen Aenderungen in Grauwerten / Farbspruenge / Kanten
        # gar keine Linien hier? keine Farbaenderungen?
    
    
def aufgabe_2_8(szinti, pixel, pixel_quadrant):
    """ Dreht das Bild aus Aufgabe 1.1 um 30° im positiven Drehsinne,
        berechnet die Fouriertransformierte und vergleicht das Ergebnis mit
        dem aus Aufgabe 2.7.
    """
    # Plots fuer Ortsraum Originalbild und gedrehtes Bild erstellen:
    ax1, ax2 = plot_vorbereitung_2sp('Ortsraum', 'Originalbild aus ' +
                                     'Aufgabe 1.1', 'um 30° gedrehtes Bild')
    # Plot Originalbild Ortsraum
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Drehmatrix erstellen (um 30° im positivem Sinne)
    dreh = drehmatrix(30)
    # Erstellung gedrehtes Originalbild Ortsraum
    szinti_transform = transformation(szinti, pixel_quadrant, dreh)
    # Plot gedrehtes Originalbild Ortsraum
    ax2.imshow(szinti_transform, cmap='gray', extent=[-128, 128, -128, 128])
    
    # Plots fuer Frequenzraum Originalbild und gedrehtes Bild erstellen:
    ax3, ax4 = plot_vorbereitung_2sp('Frequenzraum - Leistungsspektrum',
                                     'Originalbild aus Aufgabe 1.1',
                                     'um 30° gedrehtes Bild',
                                     '$ν_{x}/ν_{Sx}$', '$ν_{y}/ν_{Sy}$',
                                     ticks=True)
    # Fouriertransformation: Erstellung Leistungsspektrum
    _, power, _, _ = calculate_fourier(szinti)
    # Plot Leistungsspektrum
    ax3.imshow(power, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    # Erstellung gedrehtes Leistungsspektrum
    power_transform = transformation(power, pixel_quadrant, dreh)
    # Plot Leistungsspektrum gedrehtes Bild
    ax4.imshow(power_transform, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    plt.show()
    # Interpretation!!!
          # eine Drehung der Ortsfunktion um den Winkel alpha fuehrt zu einer
          # gleichartigen Drehung der entsprechenden Frequenzfunktion im
          # Frequenzraum


def main():
    # Szintigramm (beschrieben in Vorlesung zu Modul MF-MRS_14 Digitale
    # Bildverarbeitung, siehe Folie 17)  erstellen
    szinti, pixel, pixel_quadrant = make_szinti()
    # Aufruf Aufgabe 1.1
    aufgabe_1_1(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.1
    aufgabe_2_1(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.2
    aufgabe_2_2(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.3
    aufgabe_2_3(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.4
    aufgabe_2_4(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.5
    aufgabe_2_5(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.6
    aufgabe_2_6(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.7
    aufgabe_2_7(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.8
    aufgabe_2_8(szinti, pixel, pixel_quadrant)

#    # Zeit messen:
#    # fuer Zeitmessung:
#    t1 = time.time()
#    # fuer Zeitmessung:
#    t2 = time.time()
#    # Ausgabe Zeitanspruch des Programms
#    print("Die Zeit dieses Programmes lautet:", t2 - t1)


if __name__ == "__main__":
    main()
