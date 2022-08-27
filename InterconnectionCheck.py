"""AUTHOR: NILS WETHERINGTON

DESCRIPTION: Dieses Programm ist dazu da, um eine Verschaltungsprüfung durchzuführen.

Dies bedeutet, es wird ein Wechselrichter ausgewählt, ein bestimmtes Modul, sowie wie viele Module in Reihe geschaltet
werden sollen und wie viele Strings es in Parallel gibt. All dies geschieht über die Datenbank in PyMySQL. Falls Sie
einen anderen Modultyp, Wechselrichter, Anzahl der Module in Reihe oder Strings in Parallel ändern möchten, muss dies
durch Änderung der Werte in der Datenbank "Auslegungspruefung" geschehen, in der Tabelle "Pruefungstabelle". Um den
Modultyp zu wechseln muss eine Zahl in "Pruefungstabelle" unter "modul" geändert werden. Diese Zahl korreliert mit der
"modul_id" in der Tabelle pv_modules.
Das gleiche gilt für den Wechselrichter, die Zahl in der "Pruefungstabelle" unter "inverter" korreliert mit der
"inverter_id" aus der Tabelle "inverters".
Nach dem Sie eine Auswahl getroffen haben und mit der Datenbank verbunden sind, müssen Sie noch die Bibliotheken
pymysql, numpy, matplotlib.pyplot, pandas, sty und tabulate installieren. Hiernach kann das Programm zum Laufen gebracht
werden.
Die Verschaltungsprüfung untersucht, ob die gewählten Parameter des Solarmoduls, nach dem man diese x-mal in Reihe
schaltet und y-mal in Parallel, zusammen mit dem Wechselrichter fungieren würden, oder ob bei längerer Laufzeit
Schäden auftreten könnten. Dies wird anschaulich am Ende des Programms in einer Tabelle geprinted. Falls Sie überall
grüne Häkchen sehen, dann wird es keine Probleme mit der Verschaltung geben. Erscheint jedoch eine rotes Kreuz, dann
wird Ihnen das Programm eine Lösung vorschlagen, wie Sie dieses Problem beheben könnten.
Zu aller letzt wird Ihnen bei Durchführung des Programs noch eine IV-Kurve angezeigt. An dieser können Sie die unter
anderem den Short-Circuit Current und den Open-Circuit Voltage des ausgewählten Modules ablesen."""

import pymysql
import numpy as np
import matplotlib.pyplot as plt
import pandas
from sty import fg

def berechneMinimaleInverter(newLimit, maximum):
    """
    Berechnet minimale Inverteranzahl bei übergebenen Werten
    :param newLimit: Ein sich mit jeder Iteration erhöhendes Limit; stellt eine Vervielfachung der Inverter dar
    :param maximum: Ist das übergebene Maximum des vom Nutzer gewählten Systems, die es zu überschreiten gilt
    :return: Gibt Anzahl der Inverter zurück
    """
    i = 1
    while maximum > newLimit:
        newLimit += newLimit
        i = i + 1
    return i

def maxStringsInParallel(newPMax, maxLeistung, stringsInParallel, moduleInReihe):
    """
    Berechnung der maximalen Strings in Parallel für das System
    :param newPMax: Ist das pMax des Systems; wird bei jeder Iteration verniedrigt und somit ein String weniger
    :param maxLeistung: Ist die maximale Leistung die der Inverter hat
    :param stringsInParallel: Ist die Anzahl der Strings die übergeben werden und bei jeder Iteration verniedrigt wird
    :param moduleInReihe: Anzahl der Modulein Reihe für das System
    :return: Die errechnete Anzahl an Strings in Parallel, bei gleichbleibender anderer Parameter
    """
    i = stringsInParallel
    while newPMax > maxLeistung:
        i = i - 1
        newPMax = moduleInReihe * i * pmpp
    return i


def umppVorschlaegeInverter(umppWert, spannungsBereich):
    """
    Ermittelt Vorschläge, um die Umpp-Spannungsbereich bei der Zunahme von mehr Inverter zu berechnen
    :param umppWert: Wert des vom Nutzer gewählten Systems, diese muss überschritten werden
    :param spannungsBereich: Ein sich por Iteration veränderder Wert; ist abhängig von der Anzahl an Inverter
    :return: Ist die Anzahl an Inverter, bei gleichbleibender anderer Parameter
    """
    i = 0
    newSpannungsBereich = spannungsBereich
    while umppWert > newSpannungsBereich:
        newSpannungsBereich += newSpannungsBereich
        i = i + 1

    return i

def umppVorschlaegeModule(umppWert, spannungsBereich, oberUnterFlag, formelFlag):
    """
    Ermittelt Vorschläge, um die Umpp-Spannungsbereich bei der Veränderung von mehr (oder weniger) Module zu berechnen
    :param umppWert: Ein sich pro Iteration veränderder Wert; ist abhängig von der Anzahl an Module
    :param spannungsBereich: Wert des vom Nutzer gewählten Systems, diese muss überschritten (oder unterschritten) werden
    :param oberUnterFlag: Boolean; bestimmt ob mehr (false) oder weniger (true) Module genommen werden sollen
    :param formelFlag: Integer; bestimmt welche Formel genutzt werden soll; 0 (25 Grad), 1 (70 Grad), 2 (-10 Grad)
    :return: Gibt die minimale (oder maximale) Anzahl an Module zurück
    """
    if oberUnterFlag == True:  # Obererspannungsbreich prüfen wenn = True
        # Maximale Anzahl der der Module in Reihe für das System ermittlen
        if moduleInReihe > 1:
            i = moduleInReihe
            while umppWert > spannungsBereich:
                i = i - 1
                if formelFlag == 0:  # +25 Grad Formel
                    umppWert = i * umpp
                elif formelFlag == 1:  # +70 Grad Formel
                    umppWert = (45 * tempKoe_umpp * umpp + umpp) * i
                else:  # -10 Grad Formel
                    umppWert = (-35 * tempKoe_umpp * umpp + umpp) * i
                if i == 0:
                    break
            return i

    else:  # Sonst Untererspannungsbereich
        # Minimale Anzahl der der Module in Reihe für das System ermittlen
        if moduleInReihe > 1:
            i = moduleInReihe
            while umppWert < spannungsBereich:
                i = i + 1
                if formelFlag == 0:  # +25 Grad Formel
                    umppWert = i * umpp
                elif formelFlag == 1:  # +70 Grad Formel
                    umppWert = (45 * tempKoe_umpp * umpp + umpp) * i
                else:  # -10 Grad Formel
                    umppWert = (-35 * tempKoe_umpp * umpp + umpp) * i
            return i

# Initializing Variables
pmpp, umpp, impp, uoc, isc = 0, 0, 0, 0, 0
tempKoe_pmpp = 0
tempKoe_umpp = 0
tempKoe_impp = 0

maxLeistung, maxStrom, maxSpannung = 0, 0, 0
obererMppSpannungsbereich, untererMppSpannungsbereich = 0, 0

minimaleModuleWennMaxLeistungZuNiedrig = 0
maximaleModuleWennMaxLeistungZuNiedrig = 1000000
minimaleInverterWennMaxLeistungZuNiedrig = 0
maxStringsWennMaxLeistungZuNiedrig = 1000000

# Mit Datenbank verbinden
db = pymysql.connect(
    host="localhost",  # Host der Datenbank. Normalerweise localhost
    user="root",  # Benutzername für den Zugriff auf die Datenbank
    passwd="",  # Zugehöriges Passwort
    db="auslegungspruefung",  # Name der Datenbank, auf die zugegriffen werden soll.
    autocommit=True  # Einstellung, dass die SQL-Befehle automatisch ausgeführt werden.
)

cursor = db.cursor()  # Zeiger auf die Datenbank, um Abfragen ausführen zu können.

"""Nachfolgend SQL-Queries um auf die, vom Nutzer eingebene, Daten in der pruefungstabelle zuzugreifen"""
# Auswahl des Moduls/Inverters durch Nutzer
# Auswahl Modul aus Tabelle
sql = "SELECT modul FROM pruefungstabelle WHERE id = 1"  # Definition des SQL-Befehls
cursor.execute(sql)  # Ausführen des SQL-Befehls
sql_result = cursor.fetchall()  # Zuweisung aller resultierenden Zeilen aus der SQL-Abfrage
modulAuswahl = sql_result  # Enthält ein Int der zur Auswahl der modul_id in der Tabelle pv_modules dient

# Auswahl Inverter aus Tabelle
sql = "SELECT inverter FROM pruefungstabelle WHERE id = 1"  # Definition des SQL-Befehls
cursor.execute(sql)  # Ausführen des SQL-Befehls
sql_result = cursor.fetchall()  # Zuweisung aller resultierenden Zeilen aus der SQL-Abfrage
inverterAuswahl = sql_result  # Enthält ein Int der zur Auswahl der inverter_id in der Tabelle inverters dient

# Auswahl Module in Reihe / Strings in parallel
# Auswahl Module in Reihe aus Tabelle
sql = "SELECT module_in_reihe FROM pruefungstabelle WHERE id = 1"  # Definition des SQL-Befehls
cursor.execute(sql)  # Ausführen des SQL-Befehls
sql_result = cursor.fetchall()  # Zuweisung aller resultierenden Zeilen aus der SQL-Abfrage
moduleInReihe = sql_result[0][0] # Enthält ein Int der die Anzahl der Module in Reihe festhält

# Auswahl Strings in Parallel
sql = "SELECT strings_in_parallel FROM pruefungstabelle WHERE id = 1"  # Definition des SQL-Befehls
cursor.execute(sql)  # Ausführen des SQL-Befehls
sql_result = cursor.fetchall()  # Zuweisung aller resultierenden Zeilen aus der SQL-Abfrage
stringsInParallel = sql_result[0][0] # Enthält ein Int der die Anzahl der Strings in Parallel festhält

# Ermittlung der Tabellenwerte des Moduls
print("\nAusgabe der Werte des Moduls: \n")
sql = """SELECT pmpp, umpp, impp, uoc, isc, temperaturkoeffizient_pmpp, temperaturkoeffizient_umpp, 
temperaturkoeffizient_impp FROM pv_modules WHERE module_id = %s"""  # Definition des SQL-Befehls
cursor.execute(sql, modulAuswahl)  # Ausführen des SQL-Befehls
sql_result = cursor.fetchall()  # Zuweisung aller resultierenden Zeilen aus der SQL-Abfrage

for r in sql_result:  # Zeilenweise Ausgabe des Abfrageergebnisses
    pmpp = float(r[0])
    umpp = float(r[1])
    impp = float(r[2])
    uoc = float(r[3])
    isc = float(r[4])
    tempKoe_pmpp = float(r[5]) / 100
    tempKoe_umpp = float(r[6]) / 100
    tempKoe_impp = float(r[7]) / 100

sql = "SELECT name FROM pv_modules WHERE module_id = %s"  # Definition des SQL-Befehls
cursor.execute(sql, modulAuswahl)  # Ausführen des SQL-Befehls
sql_result = cursor.fetchall()  # Zuweisung aller resultierenden Zeilen aus der SQL-Abfrage
modulAuswahlName = sql_result

df1 = pandas.DataFrame(
    [[str(pmpp) + " W"], [str(umpp) + " V"],
     [str(impp) + " A"], [str(uoc) + " V"], [str(isc) + " A"],
     [str(tempKoe_pmpp) + " 1/K"], [str(tempKoe_umpp) + " 1/K"],
     [str(tempKoe_impp) + " 1/K"]], columns=["Parameter des " + modulAuswahlName[0][0] + " Moduls"],
    index=['Pmpp', 'Umpp', 'Impp', 'Uoc', 'Isc', 'Temp. Koeffizient Pmpp', 'Temp. Koeffizient Umpp',
           'Temp. Koeffizient Impp'])

print(df1.to_markdown(index=True))

print("\n###################################################################################################")
print("###################################################################################################")

# Nachfolgend Berechnung der Paramters aus dem Simplified One Diode Model um später die IV-Curve zu berechnen,
# sowie zur Berechnung der Verschaltung mit dem Wechselrichter.
M = uoc / isc * (-5.411 * ((impp * umpp) / (isc * uoc)) + 6.450 * (umpp / uoc) + 3.417 * (impp / isc) - 4.422)
print("\nGradient [M]: " + str(M) + " Ohm")

Rs = - M * (isc / impp) + (umpp / impp) * (1 - (isc / impp))
print("\nResistance [R\u209B]: " + str(Rs) + " Ohm")

ut = - (M + Rs) * isc
print("\nTemperature Voltage [U\u209C]: " + str(ut) + " Volt")

Is = isc * pow(np.e, -(uoc / ut))
print("\nReverse Current [I\u209B]: " + str(Is) + " Ampere")

iph = isc
print("\nPhoto current [I\u209A\u2095]: " + str(iph) + " Ampere")

pMax = moduleInReihe * stringsInParallel * pmpp
iMax = isc * stringsInParallel
uocAtMinus10 = (uoc * tempKoe_umpp * -35 + uoc) * moduleInReihe
umppAt25 = moduleInReihe * umpp
umppAt70 = (45 * tempKoe_umpp * umpp + umpp) * moduleInReihe
umppAtMinus10 = (-35 * tempKoe_umpp * umpp + umpp) * moduleInReihe

# Ermittlung der Inverterwerte für den Vergleich mit pMax, etc.
sql = """SELECT max_leistung, max_spannung, max_strom, unterer_mpp_spannungsbereich, oberer_mpp_spannungsbereich FROM 
inverters WHERE inverter_id = %s"""  # Definition des SQL-Befehls
cursor.execute(sql, inverterAuswahl)  # Ausführen des SQL-Befehls
sql_result = cursor.fetchall()  # Zuweisung aller resultierenden Zeilen aus der SQL-Abfrage

for r in sql_result:  # Zeilenweise Ausgabe des Abfrageergebnisses
    maxLeistung = float(r[0])
    maxSpannung = float(r[1])
    maxStrom = float(r[2])
    untererMppSpannungsbereich = float(r[3])
    obererMppSpannungsbereich = float(r[4])

# Vergleiche errechneten pMax aus den gewählten Parameter gegen die maximale Leistung des Inverters
if pMax > maxLeistung:
    # Berechnung der minimale Anzahl des baugleichen Inverters um Leistung zu kompensieren
    minimaleInverterWennMaxLeistungZuNiedrig = berechneMinimaleInverter(maxLeistung, pMax)

    # Maximale Anzahl der der Module in Reihe für das System ermittleln
    newPMax = pMax
    if moduleInReihe > 1:
        i = moduleInReihe
        while newPMax > maxLeistung:
            i = i - 1
            newPMax = i * stringsInParallel * pmpp
            if i == 0:
                break
        maximaleModuleWennMaxLeistungZuNiedrig = i

    # Berechnet Maximale String in parallel für das System
    maxStringsWennMaxLeistungZuNiedrig = maxStringsInParallel(pMax, maxLeistung, stringsInParallel, moduleInReihe)

# Isc mit des maximalen Stroms des Inverters vergleichen (Imax Vergleich)
if iMax > maxStrom:
    i = stringsInParallel
    # Berechne mindest Anzahl an baugleiche Inverter für das gewählte System
    if minimaleInverterWennMaxLeistungZuNiedrig < i:
        minimaleInverterWennMaxLeistungZuNiedrig = berechneMinimaleInverter(maxLeistung, pMax)

    # Berechnung der maximalen Strings in Parallel für das System
    newIMax = iMax
    while newIMax > maxStrom:
        i = i - 1
        newIMax = isc * i

    # Neue mindest Anzahl falls dieser Wert abweicht
    if maxStringsWennMaxLeistungZuNiedrig < i:
        maxStringsWennMaxLeistungZuNiedrig = i

# Uoc mit der maximalen Spannung des Inverters vergleichen
if uocAtMinus10 > maxSpannung:
    i = moduleInReihe
    # Berechne mindest Anzahl an baugleiche Inverter für das gewählte System
    if minimaleInverterWennMaxLeistungZuNiedrig < i:
        minimaleInverterWennMaxLeistungZuNiedrig = berechneMinimaleInverter(maxLeistung, pMax)

    # Maximale Anzahl der der Module in Reihe für das System ermittlen
    newUocAtMinus10 = uocAtMinus10
    if moduleInReihe > 1:
        while newUocAtMinus10 > maxSpannung:
            i = i - 1
            newUocAtMinus10 = (uoc * tempKoe_umpp * -35 + uoc) * i
            if i == 0:
                break

        if maximaleModuleWennMaxLeistungZuNiedrig > i:
            maximaleModuleWennMaxLeistungZuNiedrig = i

# Vmpp bei +25° Celsius mit dem mpp-Spannungsbereich des Inverters vergleichen
if (umppAt25 > obererMppSpannungsbereich):
    i = umppVorschlaegeModule(umppAt25, obererMppSpannungsbereich, True, 0)
    if maximaleModuleWennMaxLeistungZuNiedrig > i:
        maximaleModuleWennMaxLeistungZuNiedrig = i

    i = umppVorschlaegeInverter(umppAt25, obererMppSpannungsbereich)
    if minimaleInverterWennMaxLeistungZuNiedrig < i:
        minimaleInverterWennMaxLeistungZuNiedrig = i
elif (umppAt25 < untererMppSpannungsbereich):
    i = umppVorschlaegeModule(umppAt25, untererMppSpannungsbereich, False, 0)
    if minimaleModuleWennMaxLeistungZuNiedrig > i:
        minimaleModuleWennMaxLeistungZuNiedrig = i

    i = umppVorschlaegeInverter(umppAt25, obererMppSpannungsbereich)
    if minimaleInverterWennMaxLeistungZuNiedrig < i:
        minimaleInverterWennMaxLeistungZuNiedrig = i

# Vmpp bei +70° Celsius mit dem mpp-Spannungsbereich des Inverters vergleichen
if (umppAt70 > obererMppSpannungsbereich):
    i = umppVorschlaegeModule(umppAt70, obererMppSpannungsbereich, True, 1)
    if maximaleModuleWennMaxLeistungZuNiedrig > i:
        maximaleModuleWennMaxLeistungZuNiedrig = i

    i = umppVorschlaegeInverter(umppAt70, obererMppSpannungsbereich)
    if minimaleInverterWennMaxLeistungZuNiedrig < i:
        minimaleInverterWennMaxLeistungZuNiedrig = i
elif (umppAt70 < untererMppSpannungsbereich):
    i = umppVorschlaegeModule(umppAt70, untererMppSpannungsbereich, False, 1)
    if minimaleModuleWennMaxLeistungZuNiedrig > i:
        minimaleModuleWennMaxLeistungZuNiedrig = i

    i = umppVorschlaegeInverter(umppAt70, obererMppSpannungsbereich)
    if minimaleInverterWennMaxLeistungZuNiedrig < i:
        minimaleInverterWennMaxLeistungZuNiedrig = i

# Vmpp bei -10° Celsius mit dem mpp-Spannungsbereich des Inverters vergleichen
if (umppAtMinus10 > obererMppSpannungsbereich):
    i = umppVorschlaegeModule(umppAtMinus10, obererMppSpannungsbereich, True, 2)
    if maximaleModuleWennMaxLeistungZuNiedrig > i:
        maximaleModuleWennMaxLeistungZuNiedrig = i

    i = umppVorschlaegeInverter(umppAtMinus10, obererMppSpannungsbereich)
    if minimaleInverterWennMaxLeistungZuNiedrig < i:
        minimaleInverterWennMaxLeistungZuNiedrig = i
elif (umppAtMinus10 < untererMppSpannungsbereich):
    i = umppVorschlaegeModule(umppAtMinus10, untererMppSpannungsbereich, False, 2)
    if minimaleModuleWennMaxLeistungZuNiedrig > i:
        minimaleModuleWennMaxLeistungZuNiedrig = i

    i = umppVorschlaegeInverter(umppAtMinus10, obererMppSpannungsbereich)
    if minimaleInverterWennMaxLeistungZuNiedrig < i:
        minimaleInverterWennMaxLeistungZuNiedrig = i

print("\n###################################################################################################")
print("###################################################################################################\n")

# x bekommt die Farbe rot, das Häckchen die Farbe grün
red = fg.red + 'x' + fg.rs
green = fg.green + '\u2713' + fg.rs

# Flag der, wenn True gesetzt, mögliche Problembehebungsmöglichkeiten angibt
problemeFlag = False

"""Vergleich des ausgewählten Moduls im Verbindung mit der Anzahl in Reihe, sowie Strings in Parallel und anschließenden
vergleich mit dem ausgewählten Wechselrichter. Wenn alles in Ordnung geht, Ausgabe als grünes Häckchen, ansonsten
ein rotes Kreuz."""

if pMax > maxLeistung:
    b1 = red
    problemeFlag = True
else:
    b1 = green

if iMax > maxStrom:
    b2 = red
    problemeFlag = True
else:
    b2 = green

if uocAtMinus10 > maxSpannung:
    b3 = red
    problemeFlag = True
else:
    b3 = green

if umppAt25 > obererMppSpannungsbereich or umppAt25 < untererMppSpannungsbereich:
    b4 = red
    problemeFlag = True
else:
    b4 = green

if umppAt70 > obererMppSpannungsbereich or umppAt70 < untererMppSpannungsbereich:
    b5 = red
    problemeFlag = True
else:
    b5 = green

if umppAtMinus10 > obererMppSpannungsbereich or umppAtMinus10 < untererMppSpannungsbereich:
    b6 = red
    problemeFlag = True
else:
    b6 = green

print("If relation shows " + green + """, then there are no complications between the PV-Modules and the inverter,
otherwise the relation will show """ + red + ".\n")

df2 = pandas.DataFrame([[str(pMax) + " W", b1, str(maxLeistung) + " W"], [str(iMax) + " A", b2, str(maxStrom) + " A"],
        [str(uocAtMinus10) + " V", b3, str(maxSpannung) + " V"], [str(umppAt25) + " V", b4, " von " + str(
        untererMppSpannungsbereich) + " V bis " + str(obererMppSpannungsbereich) + " V"], [str(umppAt70) + " V", b5,
        " von " + str(untererMppSpannungsbereich) + " V bis " + str(obererMppSpannungsbereich) + " V"],
        [str(umppAtMinus10) + " V", b6, " von " + str(untererMppSpannungsbereich) + " V bis " + str(
        obererMppSpannungsbereich) + " V"]], columns=['PV-Modules', 'relation', 'Inverter'],
        index=['pMax', 'iMax', 'uocAtMinus10', 'umppAt25', 'umppAt70', 'umppAtMinus10'])

print(df2.to_markdown(index=True))

print("\n")

"""Falls Probleme bei der Verschaltung auftreten würden, wird in diesem Programmteil eine Lösungsmöglichkeit
vorgeschlagen."""

if problemeFlag:
    print("Hinweise um die möglichen Probleme zu beheben:\n")
    if minimaleModuleWennMaxLeistungZuNiedrig > 0:
        print("""Für das gewählte System bräuchte man mehr Module in Reihe, falls Sie die Anzahl an Strings
in Parallel beibehalten möchten. Nehmen Sie hierzu diese Anzahl an Module in Reihe: """
              + str(minimaleModuleWennMaxLeistungZuNiedrig))
    if maximaleModuleWennMaxLeistungZuNiedrig < 10000:
        print("""Für das gewählte System bräuchte man weniger Module in Reihe, falls Sie die Anzahl an Strings in 
Parallel beibehalten möchten, nehmen Sie diese Anzahl an Module in Reihe: """
              + str(maximaleModuleWennMaxLeistungZuNiedrig))
    if minimaleInverterWennMaxLeistungZuNiedrig > 0:
        print("Für das gewählte System bräuchte man mehr Inverter, nehmen Sie diese Anzahl an Inverter: "
              + str(minimaleInverterWennMaxLeistungZuNiedrig))
    if maxStringsWennMaxLeistungZuNiedrig < 10000:
        print("""Für das gewählte System bräuchte man weniger Strings in Parallel, falls Sie die Anzahl an Modulen
in Reihe beibehalten möchten. Nehmen Sie hierzu diese Anzahl an Strings in Parallel: """
              + str(maxStringsWennMaxLeistungZuNiedrig))

# Nutzung von Pandas um nachfolgend die IV-Curve zu printen
x = np.linspace(start=0, stop=isc, num=1000, dtype=float)  # Definition der Laufvariablen x in 100 Schritten
f = ut * np.log((isc - x + Is) / Is) - (x * Rs)  # Definition der IV-Kurve mit I als x

# Set the format of the curve
plt.plot(f, x, color="blue", linewidth=1.0, zorder=1)

# Set labels
plt.title("IV-Kennline des PV-Moduls " + str(modulAuswahlName[0][0]))
plt.xlabel('Spannung in V')
plt.ylabel('Strom in A')

# Set grid
plt.grid()

# Show the plot
plt.show()

# Schliessen der Datenbankverbindung
cursor.close()
db.close()
