-- phpMyAdmin SQL Dump
-- version 4.9.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 15. Feb 2020 um 10:24
-- Server-Version: 10.4.11-MariaDB
-- PHP-Version: 7.4.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `pps`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Daten für Tabelle `orders`
--

INSERT INTO `orders` (`order_id`, `status`) VALUES
(1, 999),
(2, 143),
(3, 3463),
(4, 3982),
(5, 1946),
(6, 173),
(7, 1738),
(8, 3941),
(9, 3299),
(10, 515),
(11, 2613),
(12, 2716),
(13, 4005),
(14, 3654),
(15, 3540),
(16, 2483),
(17, 2380),
(18, 4469),
(19, 3284),
(20, 4375),
(21, 3744),
(22, 3055),
(23, 57),
(24, 3018),
(25, 73),
(26, 2077),
(27, 903),
(28, 2928),
(29, 1615),
(30, 2253),
(31, 3308),
(32, 191),
(33, 733),
(34, 2834),
(35, 511),
(36, 3152),
(37, 3650),
(38, 2433),
(39, 4312),
(40, 3579),
(41, 440),
(42, 4692),
(43, 4045),
(44, 3435),
(45, 130),
(46, 330),
(47, 3398),
(48, 2113),
(49, 2038),
(50, 3666),
(51, 915),
(52, 1614),
(53, 4389),
(54, 2696),
(55, 3848),
(56, 1801),
(57, 2179),
(58, 3330),
(59, 2148),
(60, 89),
(61, 4537),
(62, 1206),
(63, 480),
(64, 3653),
(65, 1272),
(66, 4828),
(67, 1374),
(68, 1170),
(69, 2031),
(70, 578),
(71, 154),
(72, 2559),
(73, 2085),
(74, 1450),
(75, 1378),
(76, 855),
(77, 1745),
(78, 2519),
(79, 3964),
(80, 397),
(81, 4406),
(82, 2722),
(83, 4311),
(84, 2652),
(85, 1067),
(86, 2889),
(87, 3830),
(88, 1702),
(89, 4026),
(90, 2591),
(91, 1258),
(92, 4615),
(93, 3370),
(94, 1410),
(95, 1834),
(96, 669),
(97, 2441),
(98, 1944),
(99, 4195);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
