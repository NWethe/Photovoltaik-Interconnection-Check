-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 25. Feb 2022 um 19:26
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
-- Tabellenstruktur für Tabelle `pv_modules`
--

CREATE TABLE `pv_modules` (
  `module_id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `pmpp` decimal(5,2) DEFAULT NULL,
  `umpp` decimal(5,2) DEFAULT NULL,
  `impp` decimal(4,2) DEFAULT NULL,
  `uoc` decimal(5,2) DEFAULT NULL,
  `isc` decimal(8,4) DEFAULT NULL,
  `temperaturkoeffizient_pmpp` decimal(4,2) DEFAULT NULL,
  `temperaturkoeffizient_umpp` decimal(8,4) DEFAULT NULL,
  `temperaturkoeffizient_impp` decimal(8,4) DEFAULT NULL,
  `länge_in_m` decimal(8,4) DEFAULT NULL,
  `breite_in_m` decimal(8,4) DEFAULT NULL,
  `wirkungsgrad` decimal(4,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Daten für Tabelle `pv_modules`
--

INSERT INTO `pv_modules` (`module_id`, `name`, `brand`, `pmpp`, `umpp`, `impp`, `uoc`, `isc`, `temperaturkoeffizient_pmpp`, `temperaturkoeffizient_umpp`, `temperaturkoeffizient_impp`, `länge_in_m`, `breite_in_m`, `wirkungsgrad`) VALUES
(1, 'FS-270', 'First Solar', '70.00', '65.50', '1.07', '88.00', '1.2300', '-0.25', '-0.2500', '0.0400', '1.2000', '0.6000', '9.72'),
(2, 'FS-272', 'First Solar', '72.50', '66.60', '1.09', '88.70', '1.2300', '-0.25', '-0.2500', '0.0400', '1.2000', '0.6000', '10.07'),
(3, 'FS-275', 'First Solar', '75.00', '68.20', '1.10', '89.60', '1.2300', '-0.25', '-0.2500', '0.0400', '1.2000', '0.6000', '10.42'),
(4, 'FS-277', 'First Solar', '77.50', '69.90', '1.11', '90.50', '1.2200', '-0.25', '-0.2500', '0.0400', '1.2000', '0.6000', '10.76'),
(5, 'FS-280', 'First Solar', '80.00', '71.20', '1.12', '91.50', '1.2200', '-0.25', '-0.2500', '0.0400', '1.2000', '0.6000', '11.11'),
(6, 'E.ON Aura FM300', 'e.on', '300.00', '32.90', '9.12', '39.70', '9.5800', '-0.39', '-0.3000', '0.0500', '1.6400', '0.9900', '18.30');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `pv_modules`
--
ALTER TABLE `pv_modules`
  ADD PRIMARY KEY (`module_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
