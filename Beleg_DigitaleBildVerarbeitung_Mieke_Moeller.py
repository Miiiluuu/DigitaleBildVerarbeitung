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
# TODO: Plotfkt: (mit norm, extent usw...)
# TODO: Tritt irgendwo was doppelt auf?
# funktion mit der aktuellen Aufgabenstellung?

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
    # TODO: funktioniert nicht wenn image int32-Werte, nur float
    image *= skal
    # Zuordnung auf 255 Grauwerte
    image = np.int_(image)
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

        y_begin: Startpixel (in y-Richtung). Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten. Dieser Pixel ist in 
        extrahiertem Quadranten enthalten.

        y_end: Endpixel (in y-Richtung). Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten. Dieser Pixel ist in 
        extrahiertem Quadranten nicht mehr enthalten.

        x_begin: Startpixel (in x-Richtung). Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten. Dieser Pixel ist in 
        extrahiertem Quadranten enthalten.

        x_end: Endpixel (in x-Richtung). Zur Festlegung der
        Intervallgrenzen des entsprechenden Quadranten. Dieser Pixel ist in 
        extrahiertem Quadranten nicht mehr enthalten.

        Zeichnung:

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
    print(f'''Die Schiefe des Grauwert-Histogramms aus dem Szintigramm ''' +
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
    axs[0].set_xlabel(r'$x/mm$')
    axs[0].set_ylabel(r'$y/mm$')
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
        # Achsenbeschriftungen
        axs[i+1].set_xlabel(r'$x/mm$')
        axs[i+1].set_ylabel(r'$y/mm$')
        axs[i+1].imshow(ebene[i], cmap='gray', extent=[-128, 128, -128, 128])
    return ebene


def infogehalt_einzelne_bitebenen(image, herkunft):
    """ Berechnet fuer alle Bitebenen (fuer ein Bild) den mittleren
        Informationsgehalt pro Pixel.

        Parameter:
        ----------
        image: Liste der einzelnen Bitebenen, Eingabewerte.
        
        herkunft: bezeichnet jenes Bild, welches fuer Aufgabenstellung
        genutzt wird.
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
    print(f'''Der mittlere Informationsgehalt pro Pixel fuer das Bild ''' +
          f'''aus {herkunft} betraegt:''')
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
    phase = np.arctan2(imag, real)
    # Ermittlung des Leistungsspektrums
    power = real**2 + imag**2
    # Ermittlung des Amplitudenbildes
    amplitude = np.sqrt(power)
    return fourier_image, power, amplitude, phase


def plot_vorbereitung_3sp(ueberschrift, sub_ueberschriften, abszisse, ordinate):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        drei Subplots, Ueberschriften, Achsenbeschriftungen etc.
    """
    # Erstellen von (drei) Subplots:
    fig, axs = plt.subplots(1, 3, figsize=(10, 8), facecolor='w')
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    axs = axs.ravel()
    # entsprechende Unterueberschriften der Subplots
    for i in range(3):
        axs[i].set_title(sub_ueberschriften[i])
    # Ueberlappungen vermeiden
    plt.tight_layout(w_pad=3.5, rect=[0, 0, 1, 1.4])
    # Achsenbeschriftungen und Grid
    ticks = np.linspace(-0.5, 0.5, 11)
    for i in range(3):
        axs[i].set_xlabel(abszisse)
        axs[i].set_ylabel(ordinate)
        axs[i].set_xticks(ticks)
        axs[i].set_yticks(ticks)
        axs[i].set_xticklabels(ticks, rotation=75)
    return axs


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
                                ['Leistungsspektrum',
                                 'Amplitudenbild', 'Phasenbild'],
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
       

def transformationsmatrix(dreh):
    """ Transformation eines Bildes:
        Diese Matrix fuehrt zunaechst eine Drehung (im positivem Drehsinne)
        und anschließend eine Scherung (entsprechend Vorlesung, Folie 136 aus
        dem Modul MF-MRS_14 Digitale Bildverarbeitung) durch.

        Parameter:
        ----------
        dreh: Drehmatrix, welche zuerst auf das Bild angewendet werden soll.
        Danach erfolgt eine Scherung.
    """
    # Schermatrix in homogenen Koordinaten
    scherung = np.array([[1, -(np.sqrt(2) / 2), 0],
                         [0, (np.sqrt(2) / 2), 0], [0, 0, 1]])
    # Schermatrix invertieren, da Transformation im positiven Sinn
    scherung = np.linalg.inv(scherung)
    # Transformationsmatrix:
    # Hintereinander-Ausfuehrung von Drehung und Scherung durch einfaches
    # Multiplizieren der einzelnen Transformationsmatrizen
    transform = (dreh @ scherung)
    return transform


def make_kreisfilter(image, anteil, pixel_mitte,):
    """ Erstellt Filter (in Groeße eines Bildes 'image', Filterform Kreis)
        mit einer oberen Grenzfrequenz: hat Form eines Kreises mit einem
        bestimmten Radius.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        anteil: Anteil der Nyquistfrequenz, welche obere Grenzfrequenz des
        Tiefpassfilters bestimmt.

        pixel_mitte: Pixel, bei dem hier Mitte des Koordinaensystems liegt.
    """
    filter_kreis = np.zeros_like(image)
    # TODO: pixel_mitte (128) ≙ Nyquist-Frequenz. warum?
    # Radius eines Kreises berechnen, welcher tiefe Frequenzen durchlässt
    # (definiert obere Grenzfrequenz des Tiefpassfilters)
    radius = pixel_mitte * anteil       # TODO: pixel_mitte = 128 = ν_Nvquist?
                                        # nur in diesem Fall: Allgemein?
    for x in range(len(image)):
        for y in range(len(image)):
            deltax = pixel_mitte - x
            deltay = pixel_mitte - y
            if deltax**2 + deltay**2 <= radius**2:
                filter_kreis[y, x] = 1
    return filter_kreis


def use_filter(image, filter_image):
    """ Anwendung des Filters auf ein Bild. Dafuer wird Fouriertransformation
        des Eingabebildes berechnet. Die Fouriertransformierte wird
        anschließend gefiltert (durch eine Multiplikation der Filtermaske, im
        Frequenzraum).

        Parameter:
        ----------
        image: Array, Eingabewerte.

        filter_image: Filter, der auf ein Eingabebild angewendet wird.
    """
    # Fouriertransformation des Eingabebildes
    fourier_image, _, _, _ = calculate_fourier(image)
    # Multiplikation im Frequenzraum
    fourier_gefiltert = fourier_image * filter_image
    # Bild zurueckshiften
    fourier_gefiltert = np.fft.ifftshift(fourier_gefiltert)
    # Ruecktransformation Frequenz- in Ortsraum
    image_gefiltert = np.fft.ifft2(fourier_gefiltert)
    # Realteil vom Bild zur spaeteren graphischen Darstellung extrahieren
    image_gefiltert = np.real(image_gefiltert)
    return image_gefiltert


def bandpassfilter(image, anteil_up, anteil_down, pixel_mitte):
    """ Erstellt Bandpassfilter mit einem bestimmten erlaubten Frequenzbereich.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        anteil_up: Anteil der Nyquistfrequenz, welche obere Grenzfrequenz des
        Bandpassfilters bestimmt.

        anteil_down: Anteil der Nyquistfrequenz, welche untere Grenzfrequenz
        des Bandpassfilters bestimmt.

        pixel_mitte: Pixel, bei dem hier Mitte des Koordinaensystems liegt.
    """
    # Teilkreis / -filter 1:
    filter_kreis1 = make_kreisfilter(image, anteil_up, pixel_mitte)
    # Teilkreis / -filter 2:
    filter_kreis2 = make_kreisfilter(image, anteil_down, pixel_mitte)
    # Teilfilter 1 und 2 zusammensetzen zu Gesamtfilter (entspricht
    # Bandpassfilter, siehe Vorlesung zu Modul MF-MRS_14 Digitale
    # Bildverarbeitung, Folie 107)
    filter_band = filter_kreis1 - filter_kreis2
    return filter_band


def make_hochpassfilter(image, anteil, pixel_mitte):
    """ Erstellt Hochpassfilter (in Groeße eines Bildes 'image',
        Filterform Kreis), welcher nur hohe Frequenzen durchlaesst.
    """
    # Erstellung Kreisfilter
    filter_kreis = make_kreisfilter(image, anteil, pixel_mitte)
    # inverser Kreis- ist Hochpassfilter
    filter_hochpass = 1 - filter_kreis
    return filter_hochpass


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
    axs[0].set_title("Linear")
    axs[1].set_title("Negativ linear")
    axs[2].set_title("Quadratisch")
    axs[3].set_title("Wurzel")
    axs[4].set_title("Binarisiert")
    axs[5].set_title("Gauss")
    for i in range(6):
        axs[i].imshow(graukeile[i], cmap='gray', extent=[-128, 128, -128, 128])
    
    
def make_mittelwertfilter():
    """ Erstellung eines 3x3-Mittelwertfilters mit entsprechender Normierung
        (1 / 9).
    """
    mittelwertfilter = (1 / 9) * np.ones((3, 3))
    return mittelwertfilter


def make_binfilter():
    """ Erstellung eines 3x3-Binomialfilters mit entsprechender Normierung
        (1 / 16). Werte sind entnommen aus Pascalschen Dreieck.
    """
    binfilter = (1 / 16) * np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]])
    return binfilter


def use_filter3x3_image(image, filter_art=None):
    """ Anwendung eines 3x3-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        filter_art: Beschreibt 3x3-Filter (-Array), welcher auf das Bild
        'image' angewendet wird. Bei Auswahl eines naeher spezifizierten
        Argumentes wird dieser fuer das Filtern des Bildes verwendet.
        Falls Argument nicht angegeben, (es wird keine Filterart ausgewaehlt),
        wird fuer das 'image' ein 3x3-Medianfilter benutzt.
    """
    # Schleife: jeden Pixel einzeln durchgehen (bis auf aeußere Pixel
    # (-Randbereich)), da diese von Filter nicht beruecksichtigt wird:
    # (aeußere Rand-Pixel werden auf Null gesetzt)
    image_gefiltert = np.zeros((len(image), len(image)))
    for x in range(1, len(image)-1):
        for y in range(1, len(image)-1):
            # Filterbereich, der einzeln (fuer jeden Pixel) wirksam wird (3x3)
            bereich = image[y-1:y+2, x-1:x+2]
            # Anwenden eines Medianfilters auf das Bild, falls fuer filter_art
            # kein Argument ausgewaehlt ist
            if filter_art is None:
                image_gefiltert[y, x] = np.median(bereich)
            # ansonsten Anwenden eines anderen 3x3-Filters auf das Bild
            # (je nachdem, welches Argument der Funktion beim Aufruf gegeben
            # wird)
            else:
                # Anwendung Filter auf Filterbereich
                bereich_filter = bereich * filter_art
                # Fuellen des entsprechenden Pixels mit neuem gefilterten Wert
                image_gefiltert[y, x] = np.sum(bereich_filter)
    return image_gefiltert


def plot_vorbereitung_8sp(ueberschrift, sub_ueberschriften,
                          sub_ueberschrift_grau, abszisse,
                          ordinate):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Diagramm mit
        Ueberschrift, einzelnen Subplots etc.

        Parameter:
        ----------
        ueberschrift: Ueberschrift der Figure.

        sub_ueberschriften: Liste an Ueberschriften fuer die ersten
        Subplots.

        sub_ueberschrift_grau: Ueberschrift der Subplots, welche ein Grauwert-
        profil enthalten.

        abszisse: Beschriftung der Abszisse von den Subplots, die ein Grauwert-
        profil enthalten.

        ordinate: Beschriftung der Ordinate von den Subplots, die ein Grauwert-
        profil enthalten.
    """
    # Erstellen von (acht) Subplots:
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


def make_sobelfilter_x_y():
    """ Erstellung eines 3x3-Sobelfilters, einzeln zur Kantenextraktion in x-
        und in y-Richtung.
    """
    # in x-Richtung
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    # in y-Richtung
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    return sobel_x, sobel_y


def filter_sobel_image(image):
    """ Anwendung eines 3x3-Sobel-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    # Erstellen der Sobelfilter in x- und y-Richtung
    sobel_x, sobel_y = make_sobelfilter_x_y()
    # Anwendung der Sobelfilter in x- und y-Richtung auf das 'image'
    image_sobel_x = use_filter3x3_image(image, sobel_x)
    image_sobel_y = use_filter3x3_image(image, sobel_y)
    # Bildung des Gradienten: Wirkung des gesamten Filters (sowohl x- als auch
    # y-Richtung), entsprechend Vorlesung Folien 154f des Modul
    # MF-MRS_14 Digitale Bildverarbeitung)
    image_sobel_ges = np.abs(image_sobel_x) + np.abs(image_sobel_y)
    return image_sobel_ges


# TODO: Richtig?
def robertsfilter(image):
    """ Anwendung eines Roberts-Filters auf ein Bild 'image'.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    image_robert = np.zeros((len(image), len(image)))
    # Berechnung nach Differenzverfahren entsprechend der Vorlesung,
    # Folie 43f aus dem Modul MF-MRS_14 Digitale Bildverarbeitung
    for x in range(len(image)-1):
        for y in range(len(image)-1):
            image_robert[y, x] = np.abs(image[y, x] - image[y+1, x+1]) + \
                                 np.abs(image[y, x+1] - image[y+1, x])
    return image_robert


def make_laplacefilter():
    """ Erstellung eines Laplacefilters mit einer 8er-Nachbarschaft.
    """
    laplace = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    return laplace


# oefter verwendet?
def plot(ueberschrift, image):
    """ Vorbereitung fuer anschließenden Plot: Erstellung Figure mit
        Ueberschriften etc.

        Parameter:
        ----------
        image: Array, Eingabewerte, welche im Plot dargestellt werden.
    """
    fig = plt.figure(figsize=(6, 7))
    # Hinzufuegen der Ueberschrift zum Plot
    fig.suptitle(ueberschrift, fontsize=16)
    plt.imshow(image, cmap='gray', extent=[-128, 128, -128, 128])


def use_schwellwert(image, schwelle_unten, schwelle_oben):
    """ Funktion segmentiert mittels Schwellwertverfahren und a priori
        Kenntnisse einen bestimmten Bereich.
        Es wird eine Maske erstellt, diese enthaelt:
        Nullen: dieser Pixel wird als Nichtobjekt klassifiziert.
        Andere Grauwerte: dieser Pixel wird als Objekt klassifiziert.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        schwelle_unten: unterer Schwellwert. Ab dieser Graustufe wird
        Grauwertverteilung als Objekt gezaehlt.

        schwelle_oben: oberer Schwellwert. Bis zu dieser Graustufe wird
        Grauwertverteilung als Objekt gezaehlt.
    """
    # Anlegen eines Null-Arrays, welches Maske enthaelt:
    image_maske = np.zeros_like(image)
    # Schwellwertbedingung: innerhalb dieses Intervalls werden entsprechende
    # Pixel als Objekt gezaehlt und in die Maske uebernommen
    intervall_schwellen = (image >= schwelle_unten) * (image <= schwelle_oben)
    image_maske[intervall_schwellen] = image[intervall_schwellen]
    return image_maske


def make_logic_image(image, schwelle):
    """ Funktion erzeugt aus einem Bild ein logisches Bild (Binaerbild), indem
        ein bestimmter Bereich mittels des Schwellwertverfahrens separiert
        wird. Dabei werden a priori Kenntnisse vorausgesetzt
        (Grauwerthistogramm u.Ä.).
        Beinhaltet Pixelklassifikation: Einteilung in Objekt- (enthaelt Einsen)
        und Nichtobjektpixel (enthaelt Nullen).

        Parameter:
        ----------
        image: Array, Eingabewerte.

        schwelle: Schwellwert. Ab naechstgroeßeren Graustufe wird
        Grauwertverteilung als Objekt gezaehlt.
    """
    image_maske = np.zeros_like(image)
    image_maske[schwelle < image] = 1
    return image_maske


def extract_values(image, value):
    """ Funktion speichert aus einem Array die einander zugehoerigen (x- und
         y-) Koordinaten (als Meshgrid), welche einen bestimmten Wert 'value'
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


def szinti_vorverarbeitung_3_7(szinti, pixel, pixel_quadrant):
    """ Funktion leistet Vorverarbeitung des Bildes aus Aufgabe 1.1 fuer
        anschließende Kantenorientierte Segmentierung (Hough-Transformation).
        Kanten werden extrahiert durch Anwendung verschiedener Filter und
        Aehnliches.
    """
    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
    # Extraktion des rechten unteren Quadranten
    quadrant_vier = extract(szinti, pixel_quadrant, pixel, pixel_quadrant,
                            pixel)
    # Medianfilter anwenden zur Erzeugung zusammenhaengender Gebiete, sodass
    # Löcher in Flächen teilweise aufgefuellt
    quadrant_vier = use_filter3x3_image(quadrant_vier)
    # Anwendung Sobelfilter aufs Teilbild (Flaechenquelle D) aus Bild
    # Aufgabe 1.1 zur Kantenextraktion
    quadrant_vier = filter_sobel_image(quadrant_vier)
    # 2tes mal Medianfilter anwenden zur Erzeugung zusammenhaengender Gebiete,
    # sodass Löcher in Flächen teilweise aufgefuellt
    quadrant_vier = use_filter3x3_image(quadrant_vier)
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    quadrant_vier = make_scale(quadrant_vier)
    # a priori werden Schwellwertgrenzen festgelegt, wodurch lediglich Kanten
    # extrahiert werden
    quadrant_vier_kanten = make_logic_image(quadrant_vier, 160)
    # Extrahieren (nur) der (x- und y-) Koordinaten, bei denen Bildfunktion
    # f(x) ungleich 0
    # (d.h. in neuen Koordinaten-arrays sind lediglich Koordinaten der Kanten
    # (entsprechen Einsen im logischen Bild) enthalten)
    koord_x, koord_y = extract_values(quadrant_vier_kanten, 1)
    return koord_x, koord_y


def plot_2d_hist(ueberschrift, abszisse, ordinate, werte1, werte2):
    """ Plot eines 2D-Histogramms mit entsprechender Ueberschrift,
        Achsenbeschriftung, Farbskala etc.
    """
    plt.figure(figsize=(10, 6))
    # Hinzufuegen der Ueberschrift zum Plot
    plt.suptitle(ueberschrift, fontsize=16)
    # Achsenbeschriftungen
    plt.xlabel(abszisse)
    plt.ylabel(ordinate)
    counts, xedges, yedges, image = plt.hist2d(werte1, werte2, bins=180)
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.8])
    plt.colorbar(image, label="bla")


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
        winkel.append(np.ones(len(koord_x)) * alpha)
        # Winkel in Bogenmaß umrechen
        alpha = np.radians(alpha)
        # Hessesche Normalform der Geradengleichung: Abstaende berechnen
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
    
    
def calc_schwerpkt_1d(image):
    """ Funktion berechnet bestimmte Momente von Bildern und darauf aufbauend
        (in einer Dimension) den Schwerpunkt dieses Bildes entsprechend
        Vorlesung zum Modul MF-MRS_14 Digitale Bildverarbeitung, Folie 213f.

        Parameter:
        ----------
        image: Array, Eingabewerte.
    """
    moment0 = np.sum(image)
    x_koord = np.arange(np.shape(image)[1])
    moment = np.sum(image, axis=0) * x_koord
    moment = np.sum(moment)
    # Schwerpunkt in 1D
    schwerpkt = moment / moment0
    return schwerpkt


def calc_schwerpkt(image, calc_geometric=False):
    """ Funktion berechnet den Schwerpunkt eines Bildes (in x- und y-Richtung)
        entsprechend Vorlesung zum Modul MF-MRS_14 Digitale Bildverarbeitung,
        Folie 213f.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        calc_geometric: Falls dieser Parameter angegeben wird, wird anstatt des
        geometrischen der Massenschwerpunktes ermittelt.
    """
    # falls Berechnung vom geometrischen Schwerpunkt:
    if calc_geometric:
        # dafuer wird zuvor zunaechst logisches Bild erzeugt:
        # Bildfunktion wird auf Eins gesetzt
        image = make_logic_image(image, 0)
    # Berechnung vom Schwerpunkt in x-Richtung
    schwerpkt_x = calc_schwerpkt_1d(image)
    # Berechnung vom Schwerpunkt in y-Richtung
    image_t = np.transpose(image)
    schwerpkt_y = calc_schwerpkt_1d(image_t)
    return schwerpkt_x, schwerpkt_y


def plot_schnittpkt(ueberschrift, image, schnittpkt):
    """ Funktion erstellt einen Plot mit Ueberschriften, Achsenbeschriftungen
        und Ähnliches. Es wird ein Bild geplottet mit einem Schnittpunkt
        bestimmter Geraden.

        Parameter:
        ----------
        image: Array, Eingabewerte.

        schnittpkt: enthält Koordinaten (in x- und y-Richtung), die einen
        Schnittpunkt im geplotten Bild darstellen.
    """
    plt.figure(figsize=(10, 7))
    # Hinzufuegen der Ueberschrift zum Plot
    plt.suptitle(ueberschrift, fontsize=16)
    plt.imshow(image, cmap='gray')
    # x-Koordinate als Vertikale plotten
    plt.axvline(schnittpkt[0], color="deeppink")
    # y-Koordinate als Horizontale plotten
    plt.axhline(schnittpkt[1], color="deeppink")
    # Ueberlappungen vermeiden
    plt.tight_layout(rect=[0, 0.03, 1, 0.85])


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
    szinti = extract(szinti, 0, pixel_quadrant, 0, pixel_quadrant)
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
        szinti = use_filter3x3_image(szinti)
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    szinti = make_scale(szinti)
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
    image = plt.imshow(ubergange, norm=LogNorm())
    plt.colorbar(image, shrink=0.6, label="bla")
    plt.tight_layout(rect=[0, 0, 1, 1.1])


def aufgabe_1_1(szinti, pixel, pixel_quadrant):
    """ Darstellung eines aufgenommenen Szintigramms, bestehend aus 256x256
        Pixel, aufgebaut aus vier Flaechenquellen (weitere Parameter siehe
        Vorlesung zu Modul MF-MRS_14 Digitale Bildverarbeitung)
    """
    print("")
    print("Aufgabe 1.1:")
    print("")
    # Szintigramm als Plot zeichnen
    # TODO: ist dieser Plot haufiger?
    plt.figure()
    # Hinzufuegen der Ueberschrift zum Plot
    plt.suptitle("Szintigramm aus Aufgabe 1.1", fontsize=16)
    # Achsenbeschriftungen
    plt.xlabel(r'$x/mm$')
    plt.ylabel(r'$y/mm$')
    plt.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    plt.savefig("Aufgabe_1_1", dpi=300)
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
    ax1, ax2 = plot_vorbereitung_2sp('Grauwertprofile fuer das Bild aus ' +
                                     'Aufgabe 1.1', 'laengs y = 60',
                                     'laengs y = -60', r'$x/mm$',
                                     'Grauwert')
    ax1.plot(np.arange(-pixel_quadrant, pixel_quadrant), grauwertprofil_60)
    ax2.plot(np.arange(-pixel_quadrant, pixel_quadrant),
             grauwertprofil_minus60)
    plt.savefig("Aufgabe_2_1", dpi=300)
    plt.show()
    

def aufgabe_2_2(szinti, pixel, pixel_quadrant):
    """ Erstellt das Grauwerthistogramm des Bildes aus Aufgabe 1.1 und stellt
        es graphisch dar. """
    print("")
    print("Aufgabe 2.2:")
    print("")
    # Grauwerthistogramm zeichnen:
    erstelle_grauwerthist(szinti.flatten(), "das Bild aus Aufgabe 1.1")
    plt.savefig("Aufgabe_2_2", dpi=300)
    plt.show()


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


def aufgabe_2_5(szinti, pixel, pixel_quadrant):
    """ Erstellt die Bitebenen aller Bilder aus Aufgabe 1.1 und berechnet fuer
        jede Ebene den mittleren Informationsgehalt je Pixel.
    """
    print("")
    print("Aufgabe 2.5:")
    print("")
    # Erstellung Bitebenen
    ebene = erstellung_bitebenen(szinti)
    plt.savefig("Aufgabe_2_5", dpi=300)
    plt.show()
    # Berechnung mittlerer Informationsgehalt pro Pixel
    infogehalt_einzelne_bitebenen(ebene, "Aufgabe 1.1")
    

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
    plt.savefig("Aufgabe_2_6_Original", dpi=300)
    plt.show()
    # Erstellung Differenzbild
    differenz = differenzbild(szinti)
    # Plot Histogramm des Differenzbildes
    erstelle_grauwerthist(differenz.flatten(), "das Differenzbild")
    plt.savefig("Aufgabe_2_6_Differenz", dpi=300)
    plt.show()
    # Berechnung mittlerer Informationsgehalt pro Pixel fuer das Originalbild
    info_original = infogehalt(szinti)
    # Berechnung mittlerer Informationsgehalt pro Pixel fuer das
    # Differenzbild
    info_differenz = infogehalt(differenz)
    # Gegenueberstellung der beiden Informationsgehalte in einer Tabelle
    vgl_infogehalt_differenz('Original', 'Differenz',
                             np.round(info_original, 3),
                             np.round(info_differenz, 3))
    

def aufgabe_2_7(szinti, pixel, pixel_quadrant):
    """ Berechnet 2D Fouriertransformierte und das Leistungsspektrum des
        Bildes aus Aufgabe 1.1:
    """
    print("")
    print("Aufgabe 2.7:")
    print("")
    # Fouriertransformation
    fourier_image, power, amplitude, phase = calculate_fourier(szinti)
    # graphische Darstellung der Fouriertransformierten
    plot_fourier(power, amplitude, phase, "des Bildes aus Aufgabe 1.1")
    plt.savefig("Aufgabe_2_7", dpi=300)
    plt.show()
    # Interpretation!!!
        # Phasenbild codiert raeumliche Info
        # Linien entsprechen Aenderungen in Grauwerten / Farbspruenge / Kanten
        # gar keine Linien hier? keine Farbaenderungen?
    

def aufgabe_2_8(szinti, pixel, pixel_quadrant):
    """ Dreht das Bild aus Aufgabe 1.1 um 30° im positiven Drehsinne,
        berechnet die Fouriertransformierte und vergleicht das Ergebnis mit
        dem aus Aufgabe 2.7.
    """
    print("")
    print("Aufgabe 2.8:")
    print("")
    # Plots fuer Ortsraum Originalbild und gedrehtes Bild erstellen:
    ax1, ax2 = plot_vorbereitung_2sp('Ortsraum', 'Originalbild aus ' +
                                     'Aufgabe 1.1', 'um 30° gedrehtes Bild')
    # Plot Originalbild Ortsraum
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Drehmatrix erstellen (um 30° im positivem Sinne)
    dreh = drehmatrix(30)
    # Erstellung gedrehtes Originalbild Ortsraum
    szinti_transform = transformation(szinti, pixel_quadrant, dreh)
    # TODO: manchmal ist szinti_transform nicht 255: scale??
    # aber 255 Wert ist einfach rausgedreht, kann man nichts machen
    # (funktioniert gar nicht)
    # Plot gedrehtes Originalbild Ortsraum
    ax2.imshow(szinti_transform, cmap='gray', extent=[-128, 128, -128, 128])
    plt.savefig("Aufgabe_2_8_original", dpi=300)
    
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
    # TODO: hier auch scale da Transformation???
    # Plot Leistungsspektrum gedrehtes Bild
    ax4.imshow(power_transform, cmap='gray', norm=LogNorm(),
               extent=[-0.5, 0.5, -0.5, 0.5])
    plt.savefig("Aufgabe_2_8_power", dpi=300)
    plt.show()
          
          
def aufgabe_2_9(szinti, pixel, pixel_quadrant):
    """ Anwendung eines Tiefpassfilters mit einer oberen Grenzfrequenz von
        |ν_lim| = 0.25 ∙ ν_Nvquist auf das Bild aus Aufgabe 1.1.
    """
    print("")
    print("Aufgabe 2.9:")
    print("")
    # Erzeugung Tiefpassfilter (in Groeße des Originalbildes)
    filter_tief = make_kreisfilter(szinti, 0.25, pixel_quadrant)
    # Anwendung des Tiefpassfilters auf Originalbild
    szinti_gefiltert = use_filter(szinti, filter_tief)
    # Skalieren der Zahlenwerte, sodass Grauwerte von 0...255 umfasst werden
    # TODO: ist gar nicht der Sinn eines Tiefpassfilters, da hohe Frequenzen
    # ja gerade eliminiert werden sollen, die gefilterten Werte sind teilweise
    # auch negativ, dabei muessten sie sich doch von Null an verteilen?
#    szinti_gefiltert = make_scale(szinti_gefiltert)
    # Erstellung Plots fuer graphische Darstellung Originalbild und
    # gefiltertes Bild
    ax1, ax2 = plot_vorbereitung_2sp('Tiefpassfilterung \n'
                                     '(obere Grenzfrequenz: ' +
                                     '|ν_lim| = 0.25 ∙ ν_Nvquist)',
                                     'Originalbild', 'gefiltertes Bild')
    # Plot Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Plot gefiltertes Bild
    ax2.imshow(szinti_gefiltert, cmap='gray', extent=[-128, 128, -128, 128])
    plt.savefig("Aufgabe_2_9", dpi=300)
    plt.show()
    # Interpretation:
        # Schaerfe ist weggenommen vom Originalbild, da hohe Frequenzen
        # rausgeschnitten wurden (hohe Frequenzen sind fuer Kanten, Abbildung
        # Details zustaendig)
        # periodisches Muster in Funktion reingebracht durch Anwenden einer
        # Kastenfunktion mit Kreis im Frequenzraum, die im Ortsraum wiederum
        # eine periodische sinc-Funktion ergibt?
        
    
def aufgabe_2_10(szinti, pixel, pixel_quadrant):
    """ Anwendung eines Bandpassfilters mit einem erlaubten Frequenzbereich von
        3/8 ∙ ν_Nvquist < |ν| < 5/8 ∙ ν_Nvquist auf das Bild aus Aufgabe 1.1.
    """
    print("")
    print("Aufgabe 2.10:")
    print("")
    # Erzeugung Bandpassfilter (in Groeße des Originalbildes)
    filter_band = bandpassfilter(szinti, (5 / 8),  (3 / 8), pixel_quadrant)
    # Anwendung des Bandpassfilters auf Originalbild
    szinti_gefiltert = use_filter(szinti, filter_band)
    # Erstellung Plots fuer graphische Darstellung Originalbild und
    # gefiltertes Bild
    ax1, ax2 = plot_vorbereitung_2sp('Bandpassfilterung \n'
                                    '(erlaubter Frequenzbereich: ' +
                                    '3/8 ∙ ν_Nvquist < |ν| < 5/8 ∙ ν_Nvquist)',
                                    'Originalbild', 'gefiltertes Bild')
    # Plot Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Plot gefiltertes Bild
    ax2.imshow(szinti_gefiltert, cmap='gray', extent=[-128, 128, -128, 128])
    plt.savefig("Aufgabe_2_10", dpi=300)
    plt.show()
    # Interpretation!!!
        # mittleren Frequenzen passieren Filter, sind noch in Originalbild
        # vorhanden,übrigen Frequenzen (hohe und tiefe) werden gesperrt
        # Kanten (durch hohe Frequenzen) nur noch geringfügig drin, es lassen
        # sich nur noch Tendenzen erkennen
        # ist frequenzselektiver Filter (laesst einzelne Teile des Frequenzbandes
        # durch und sperrt andere )
        
        
def aufgabe_2_11(szinti, pixel, pixel_quadrant):
    """ Anwendung eines Hochpassfilters mit einem erlaubten Frequenzbereich
        von 3/4 ∙ ν_Nvquist < |ν| < ν_Nvquist auf das Bild aus Aufgabe 1.1.
    """
    print("")
    print("Aufgabe 2.11:")
    print("")
    # Erzeugung Tiefpassfilter (in Groeße des Originalbildes)
    filter_hochpass = make_hochpassfilter(szinti, (3 / 4), pixel_quadrant)
    # Anwendung des Hochpassfilters auf Originalbild
    szinti_gefiltert = use_filter(szinti, filter_hochpass)
    # Erstellung Plots fuer graphische Darstellung Originalbild und
    # gefiltertes Bild
    ax1, ax2 = plot_vorbereitung_2sp('Hochpassfilterung \n'
                                     '(erlaubter Frequenzbereich: ' +
                                     '3/4 ∙ ν_Nvquist < |ν| < ν_Nvquist',
                                     'Originalbild', 'gefiltertes Bild')
    # Plot Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Plot gefiltertes Bild
    ax2.imshow(szinti_gefiltert, cmap='gray', extent=[-128, 128, -128, 128])
    plt.savefig("Aufgabe_2_11", dpi=300)
    plt.show()
    # Interpretation:
        # hohe Frequenzen des Originalbildes noch vorhanden
        # (sind fuer Kanten, Abbildung Details zustaendig)
        # d.h. strukturreiche/detailreiche Elemente gut zu sehen
        # aber dafuer sind niedrige Frequenzen, welche homogene Bereiche des
        # Bildes, kontinuierliche (Grauwert)uebergaenge darstellen, weg
        

def aufgabe_3_1():
    """ Programmiert einen linearen Graukeil (mit 256 Grauwerten) und wendet
        die Kennlinien aus der Vorlesung, Folie 111 aus dem Modul MF-MRS_14
        Digitale Bildverarbeitung darauf an.
    """
    print("")
    print("Aufgabe 3.1:")
    print("")
    # Graukeil erzeugen
    graukeil = make_graukeil(256, 256)
    # erzeuge Kennlinien
    kennlinien = make_kennlinien(100, 150, 256)
    # einzelnen Kennlinien auf den linearen Graukeil anwenden und einzelne
    # transformierten Graukeile abspeichern
    graukeile = use_kennlinien(graukeil, kennlinien)
    # Plot der einzelnen transformierten Graukeile
    plot_graukeile_transform(graukeile)
    plt.savefig("Aufgabe_3_1", dpi=300)
    plt.show()
    

def aufgabe_3_2(szinti, pixel, pixel_quadrant):
    """ Fuehrt nacheinander zunaechst eine Rotation um 90° (im positiven
        Drehsinne) und anschließend eine Scherung auf das Bild aus
        Aufgabe 1.1 durch.
    """
    print("")
    print("Aufgabe 3.2:")
    print("")
    # Plots:
    # Plots (fuer Originalbild und transformiertes Bild aus Aufgabe 1.1)
    # erstellen
    ax1, ax2 = plot_vorbereitung_2sp('Ortsraum', 'Originalbild ' +
                                     'aus Aufgabe 1.1',
                                     'transformiertes Bild')
    # Plot Originalbild
    ax1.imshow(szinti, cmap='gray', extent=[-128, 128, -128, 128])
    # Drehmatrix mit 30° als Winkel erstellen
    dreh = drehmatrix(90)
    # Transformationmatrix erstellen
    transform = transformationsmatrix(dreh)
    # Transformationsmatrix auf Bild aus Aufgabe 1.1 anwenden
    # (positive Drehung um 90°, Scherung)
    szinti_transform = transformation(szinti, pixel_quadrant, transform)
    # Plot transformiertes Bild aus Aufgabe 1.1
    ax2.imshow(szinti_transform, cmap='gray', extent=[-128, 128, -128, 128])
    plt.savefig("Aufgabe_3_2", dpi=300)
    plt.show()
    

def aufgabe_3_3(szinti, pixel, pixel_quadrant):
    """ Anwendung eines 3x3- Mittelwert-, 3x3- Median- und einem
        3x3-Bionomialfilter am Bild aus Aufgabe 1.1.
    """
    print("")
    print("Aufgabe 3.3:")
    print("")
    # Erstellung der Filter
    mittelwertfilter = make_mittelwertfilter()
    binfilter = make_binfilter()
    # Anwendung Filter auf das Bild aus Aufgabe 1.1:
    # Mittelwertfilter
    szinti_filter_avg = use_filter3x3_image(szinti, mittelwertfilter)
    # Medianfilter
    szinti_filter_med = use_filter3x3_image(szinti)
    # Binomialfilter
    szinti_filter_bin = use_filter3x3_image(szinti, binfilter)
    # Erstellung Grauwertprofile entlang y-Linie = 60:
    # fuer Originalbild aus Aufgabe 1.1
    grauprofil_60_szinti = extraktion_aus_array(szinti, pixel_quadrant - 60)
    # fuer angewendeten 3x3-Mittelwertsfilter
    grauprofil_60_avg = extraktion_aus_array(szinti_filter_avg,
                                             pixel_quadrant - 60)
    # fuer angewendeten 3x3-Medianfilter
    grauprofil_60_med = extraktion_aus_array(szinti_filter_med,
                                             pixel_quadrant - 60)
    # fuer angewendeten 3x3-Binomialfilter
    grauprofil_60_bin = extraktion_aus_array(szinti_filter_bin,
                                             pixel_quadrant - 60)
    # einzelne Subplots erstellen:
    axs = plot_vorbereitung_8sp('Vergleich verschiedener Glaettungsverfahren',
                                ['Originalbild aus Aufgabe 1.1',
                                 '3x3-Mittelwertfilter', '3x3-Medianfilter',
                                 '3x3-Binomialfilter'],
                                'entsprechendes Grauwertprofile \n'
                                '- laengs y = 60 - ',
                                r'$x/mm$', 'Grauwert')
    # Anlegen einer Liste, welche einzelnen (gefilterten) Bilder und die
    # entsprechenden Grauwertprofile enthaelt
    bilder = [szinti, szinti_filter_avg, szinti_filter_med,
              szinti_filter_bin, grauprofil_60_szinti, grauprofil_60_avg,
              grauprofil_60_med, grauprofil_60_bin]
    # Plot der (verschieden) gefilterten Bilder (aus Aufgabe 1.1)
    for i in range(4):
        axs[i].imshow(bilder[i], cmap='gray', extent=[-128, 128, -128, 128])
    # Plot der Grauwertprofile (entlang y = 60) fuer die entsprechenden
    # Filterungen
    for i in range(4, 8):
        axs[i].plot((np.arange(-pixel_quadrant, pixel_quadrant)), bilder[i])
    plt.savefig("Aufgabe_3_3", dpi=300)
    plt.show()
    # Vergleich
        # alle sind Glättungsverfahren: Reduzieren des Bildrauschens,
        # Unebenheiten in den Grauwerten des Bildes (teilweise "hohe
        # Bildfrequenzen" beseitigen, siehe auch entsprechende Grauwertprofile)
        # Mittelwert: Elimination hoher Bildfrequenzen, damit sind Kanten
        # (Darstellung mit hohen Frequenzen) abgeflacht, Bild wird
        # "verschmiert"
        # Median hat sowohl Glättungswirkung und kann auch Kantensteilheit
        # erhalten
        # dafür aber Artefakte in spitzwinkligen Strukturen, die vorher nicht
        # da
        # waren (z.B. siehe abgebrochene Ecken in Rechtecken/Flaechenquelle
        # A & B)
        # allg. Robustheit gegen Ausreisser, effektiv gegen Salt-und-Pepper
        # Rauschen gegenüber Mittelwert
        # (hier wird Helligkeitsrauschen geglaettet)
        # Binomial ist spezielle Form des Mittelwertfilters, dabei liegt mehr
        # Gewicht auf mittleren Pixel waehrend hier verwendeter
        # Mittelwertfilter jedem Pixel das
        # selbe Gewicht Eins gibt (dadurch nicht mehr so verschmiert? bzw keine
        # Artefakte)
        

def aufgabe_3_4(szinti, pixel, pixel_quadrant):
    """ Anwendung des Sobel- und Robertsfilters auf das Bild aus Aufgabe 1.1.
    """
    print("")
    print("Aufgabe 3.4:")
    print("")
    # Anwendung Sobelfilter aufs Bild aus Aufgabe 1.1
    szinti_sobel_ges = filter_sobel_image(szinti)
    # Anwendung Roberts-Filter aufs Bild aus Aufgabe 1.1
    szinti_robert = robertsfilter(szinti)
    # Subplots erstellen fuer graphische Darstellung
    ax1, ax2 = plot_vorbereitung_2sp("verschiedene Filter zur " +
                                     "Kantenextraktion",
                                     "Sobel-Filter", "Roberts-Filter")
    # Plot Sobelfilter
    ax1.imshow(szinti_sobel_ges, cmap='gray', extent=[-128, 128, -128, 128])
    # Plot Robertsfilter
    ax2.imshow(szinti_robert, cmap='gray', extent=[-128, 128, -128, 128])
    plt.savefig("Aufgabe_3_4", dpi=300)
    plt.show()
    # Interpretation:
        # Kantenextraktion:
        # dafuer Bildung der ersten Ableitung aus zwei orthogonalen Richtungen
        # und Gradientenbildbestimmung (siehe Vorlesung)
        # Sobel drei Zeilen: Gradient ueber 3 Zeilen
        # Robertsfilter besitzt kleinere Matrix (2x2),
        # bezieht fuer
        # Kantenextraktion
        # kleineren Bereich mit ein, d.h. Sobel rauschunempfindlicher
        # Robert bildet Differenzen in Richtungen 45° und 135° (diagonal)
        # Sobel bildet Differenzen in horizontaler und vertikaler Richtungen
        # Sobel und Robert haben Richtungsabhaengigkeit
        # aber: fuer Kantenfilter gilt Isotropie: Filterantwort soll nicht von
        # der Richtung der Kante abhaengen: beide Filter sehen in etwa gleich
        # aus
        # Sobel mehr Mittelung daher Robert schaerfer
    
    
def aufgabe_3_5(szinti, pixel, pixel_quadrant):
    """ Anwendung des Laplace-Filters (mit einer 8er Nachbarschaft) auf das
        Bild aus Aufgabe 1.1.
    """
    print("")
    print("Aufgabe 3.5:")
    print("")
    # Erstellung Laplace-Filter mit 8er Nachbarschaft
    laplacefilter = make_laplacefilter()
    # Anwendung Laplacefilter aufs Bild aus Aufgabe 1.1
    szinti_laplace = use_filter3x3_image(szinti, laplacefilter)
    # Plot des Bildes aus Aufgabe 1.1 nach Anwendung eines Laplacefilters
    # mit einer 8er Nachbarschaft
    plot('Anwendung eines Laplacefilters (8er Nachbarschaft) \n'
         'auf das Bild aus Aufgabe 1.1', szinti_laplace)
    plt.savefig("Aufgabe_3_5", dpi=300)
    plt.show()
    # Interpretation:
        # Laplace: Summe partielle zweite Ableitungen nach x und y Richtung
        # strukturreiche Bereiche werden hervorgehoben
        # (da krümmungsempfindlicher), weniger strukturreiche
        # Bereiche unterdrueckt
        # Hochpasseigenschaften (niedrige Frequenzen unterdrueckt)
        # Unterschiede zu Gradientenfiltern (aus Aufgabe 3.4): nutzen 2.
        # Ableitung statt erster,
        # welche rauschanfaelliger ist als bei Nutzen erster Ableitung


def aufgabe_3_6(szinti, pixel, pixel_quadrant):
    """ Separierung der Flaechenquelle D im Bild aus Aufgabe 1.1 (mittels
        Schwellwertverfahren).
    """
    print("")
    print("Aufgabe 3.6:")
    print("")
    # vor Anwendung Schwellwertverfahren (a priori) Glaettung mit
    # Medianfilter zur Erzeugung zusammenhaengender Gebiete, sodass Loecher in
    # Flächen teilweise aufgefuellt
    szinti_bearbeitet = use_filter3x3_image(szinti)
    # aus der a priori Kenntnis von Flaechenquelle D (Parameter siehe
    # Vorlesung zu Modul MF-MRS_14 Digitale Bildverarbeitung, Aufgabe 1.1
    # (Folie 17)) werden aus (geglaetteten) Grauwerthistogramm Schwellwerte
    # visuell entnommen (sodass Gesamt-segmentierungsfehler möglichst gering)
    # und so Schwellwertgrenzen festgelegt
    szinti_bearbeitet = use_schwellwert(szinti_bearbeitet, 50, 100)
    # Darstellung der separierten Flaechenquelle D (Dreieck)
    plt.figure()
    plt.imshow(szinti_bearbeitet, cmap='gray', extent=[-128, 128, -128, 128],
               vmax=255)
    plt.savefig("Aufgabe_3_6", dpi=300)
    plt.show()


def aufgabe_3_7(szinti, pixel, pixel_quadrant):
    """ Extrahieren des rechten unteren Quadranten des Bild aus Aufgabe 1.1
        (Flaechenquelle D, gleichseitiges Dreieck) als Teilbild. Dabei Durchführung
        einer Kantenextraktiion mit anschließender Hough-Transformation.
    """
    print("")
    print("Aufgabe 3.7:")
    print("")
    # Vorverarbeitung des Bildes: Voraussetzung fuer Hough-Transformation
    # ist Kantenextraktion
    koord_x, koord_y = szinti_vorverarbeitung_3_7(szinti, pixel,
                                                  pixel_quadrant)
    # Finden der Kantenpunkte, die zu einer (durchgehenden) Linie gehoeren
    # (und demnach kein Rauschen sind) mittels Hough-Transformation
    # (siehe Vorlesung zu Modul MF-MRS_14 Digitale Bildverarbeitung, Folie
    # 202f):
    # Finden der Kantenpunkte, die zu einer (durchgehenden) Linie gehoeren
    # (und demnach kein Rauschen sind)
    hough_trafo(koord_x, koord_y)
    plt.savefig("Aufgabe_3_7", dpi=300)
    plt.show()
    

def aufgabe_3_8(szinti, pixel, pixel_quadrant):
    """ Berechnung des geometrischen und den Massenschwerpunkt fuer ein Objekt,
        bestehend aus den Flaechenquellen B und C aus Aufgabe 1.1.
    """
    print("")
    print("Aufgabe 3.8:")
    print("")
    # Einteilung Bild aus Aufgabe 1.1 in Teilbilder:
    # Extraktion von Flaechenquelle B und C
    szinti = extract(szinti, 0, pixel, 0, pixel_quadrant)
    # Berechnung vom geometrischen Schwerpunkt (in x- und y-Richtung)
    schwerpkt_geo = calc_schwerpkt(szinti, calc_geometric=True)
    # Einzeichnen des geometrischen Schwerpunktes
    plot_schnittpkt("geometrischer Schwerpunkt \n"
                "- innerhalb Bild aus Aufgabe 1.1 -", szinti, schwerpkt_geo)
    plt.savefig("Aufgabe_3_8_geometric", dpi=300)
    plt.show()
    # Berechnung vom Massenschwerpunkt (in x- und y-Richtung)
    schwerpkt_mass = calc_schwerpkt(szinti)
    # Einzeichnen des Massenschwerpunktes
    plot_schnittpkt("Massenschwerpunkt \n"
                "- innerhalb Bild aus Aufgabe 1.1 -", szinti, schwerpkt_mass)
    plt.savefig("Aufgabe_3_8_mass", dpi=300)
    plt.show()
    
    
def aufgabe_3_9(szinti, pixel, pixel_quadrant):
    """ Extraktion von Flaechenquelle B aus Szintigramm Aufgabe 1.1,
        Bestimmung der Grauwertuebergangsmatrix C(δ=(1,0)), C(δ=(0,1)) und
        Interpretation.
    """
    print("")
    print("Aufgabe 3.8:")
    print("")
    szinti = szinti_vorbereitung_3_9(szinti, pixel, pixel_quadrant)
    # Erzeugen der Uebergangsmatrizen:
    # mit Vektor C(δ=(1,0))
    make_uebergangsmatrix(szinti)
    plt.savefig("Aufgabe_3_9_10", dpi=300)
    plt.show()
    # mit Vektor C(δ=(0,1))
    szinti_t = np.transpose(szinti)
    make_uebergangsmatrix(szinti_t)
    plt.savefig("Aufgabe_3_9_01", dpi=300)
    plt.show()


def main():
    # Zeit messen:
    # fuer Zeitmessung:
    t1 = time.time()
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
    # Aufruf Aufgabe 2.9
    aufgabe_2_9(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.10
    aufgabe_2_10(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 2.11
    aufgabe_2_11(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 3.1
    aufgabe_3_1()
    # Aufruf Aufgabe 3.2
    aufgabe_3_2(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 3.3
    aufgabe_3_3(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 3.4
    aufgabe_3_4(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 3.5
    aufgabe_3_5(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 3.6
    aufgabe_3_6(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 3.7
    aufgabe_3_7(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 3.8
    aufgabe_3_8(szinti, pixel, pixel_quadrant)
    # Aufruf Aufgabe 3.9
    aufgabe_3_9(szinti, pixel, pixel_quadrant)
    # fuer Zeitmessung:
    t2 = time.time()

#    # Zeit messen:
#    # fuer Zeitmessung:
#    t1 = time.time()
#    # fuer Zeitmessung:
#    t2 = time.time()
    # Ausgabe Zeitanspruch des Programms
    print("Die Zeit dieses Programmes lautet:", t2 - t1, "s")
#    input("Bitte Enter druecken zum Beenden!")


if __name__ == "__main__":
    main()
