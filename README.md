# Photovoltaik-Interconnection-Check

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
