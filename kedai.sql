-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 19, 2026 at 06:06 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kedai`
--

-- --------------------------------------------------------

--
-- Table structure for table `makanan`
--

CREATE TABLE `makanan` (
  `id_makanan` int(20) NOT NULL,
  `kodemakanan` char(50) NOT NULL,
  `namamakanan` varchar(100) NOT NULL,
  `harga` int(50) NOT NULL,
  `namafile` varchar(300) NOT NULL,
  `id_kategory` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `makanan`
--

INSERT INTO `makanan` (`id_makanan`, `kodemakanan`, `namamakanan`, `harga`, `namafile`, `id_kategory`) VALUES
(5, '1', 'Nasi Pecel', 13000, '5fa3f16d9c1cf.jpg', 1),
(7, '3', 'nasi goreng enakkk', 14000, '079979700_1587487794-Sajiku_1.jpg', 1),
(8, '4', 'Burger', 18000, 'resep-mini-cheese-burger_43.jpeg', 1),
(9, '4', 'Burger', 18000, 'es-cokelatjpg-20221120011930.jpg', 1);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'ade', 'scrypt:32768:8:1$R8tPbQnqxfuCSPvm$e932206f4cf59822442a2a84f7a58ab926bade9c27923495f2d428f0b76ff5bb82729256d8bd1d537f611c37a3bd761fe200e7855b7002c3d9721d3d4948cdbb'),
(3, 'akbar', 'scrypt:32768:8:1$SnRzzfUiKQVQzqAB$826c2c8b80d07d5184d2b629dc7f08c11f6c3dfd62ef6575c74a31752babdc81eb875ce840c435581ce1e77422b0768c74ee43dc2d8996a5d9723ecdea84298d'),
(4, 'ibnu', 'scrypt:32768:8:1$iMCUaopPV53Ymiko$9875c876527bb9c898999709380e98560098fe60626cb447e7030633f8ad3826ab0b759ba43ddabca0972d0ab0c128b2e1d9c346b166a1defd58123d9ec1d4dd');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `makanan`
--
ALTER TABLE `makanan`
  ADD PRIMARY KEY (`id_makanan`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `makanan`
--
ALTER TABLE `makanan`
  MODIFY `id_makanan` int(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
