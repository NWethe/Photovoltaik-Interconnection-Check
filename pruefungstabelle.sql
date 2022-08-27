-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 25. Feb 2022 um 19:02
-- Server-Version: 10.4.22-MariaDB
-- PHP-Version: 7.3.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `auslegungspruefung`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `pruefungstabelle`
--

CREATE TABLE `pruefungstabelle` (
  `id` int(11) NOT NULL,
  `modul` int(11) NOT NULL,
  `module_in_reihe` int(11) NOT NULL,
  `strings_in_parallel` int(11) NOT NULL,
  `inverter` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `pruefungstabelle`
--

INSERT INTO `pruefungstabelle` (`id`, `modul`, `module_in_reihe`, `strings_in_parallel`, `inverter`) VALUES
(1, 5, 16, 16, 2);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `pruefungstabelle`
--
ALTER TABLE `pruefungstabelle`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
