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
-- Tabellenstruktur für Tabelle `inverters`
--

CREATE TABLE `inverters` (
  `inverter_id` int(11) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `brand` varchar(20) DEFAULT NULL,
  `max_leistung` int(11) DEFAULT NULL,
  `max_spannung` int(11) DEFAULT NULL,
  `max_strom` decimal(4,2) DEFAULT NULL,
  `unterer_mpp_spannungsbereich` int(11) DEFAULT NULL,
  `oberer_mpp_spannungsbereich` int(11) DEFAULT NULL,
  `euro_wirkungsgrad` decimal(4,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `inverters`
--

INSERT INTO `inverters` (`inverter_id`, `name`, `brand`, `max_leistung`, `max_spannung`, `max_strom`, `unterer_mpp_spannungsbereich`, `oberer_mpp_spannungsbereich`, `euro_wirkungsgrad`) VALUES
(1, 'SB 4200TL HC', 'SMA', 4900, 750, '11.00', 125, 750, '95.40'),
(2, 'SB 5000TL HC', 'SMA', 6000, 750, '11.00', 125, 750, '95.50'),
(3, 'SB 5000TL', 'SMA', 6000, 750, '7.50', 125, 750, '94.50'),
(4, 'SB 3000TL-20', 'SMA', 3200, 550, '8.50', 125, 440, '96.30');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `inverters`
--
ALTER TABLE `inverters`
  ADD PRIMARY KEY (`inverter_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
