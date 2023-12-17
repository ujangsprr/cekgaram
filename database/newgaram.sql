-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 15 Des 2023 pada 05.02
-- Versi server: 10.4.19-MariaDB
-- Versi PHP: 8.0.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `newgaram`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `garam`
--

CREATE TABLE `garam` (
  `id_garam` int(11) NOT NULL,
  `id_petani` int(11) DEFAULT NULL,
  `kadar_air` decimal(5,2) DEFAULT NULL,
  `kadar_garam` decimal(5,2) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `garam`
--

INSERT INTO `garam` (`id_garam`, `id_petani`, `kadar_air`, `kadar_garam`, `timestamp`) VALUES
(1, 1, '5.20', '86.90', '2023-12-14 20:55:56'),
(2, 1, '5.20', '86.90', '2023-12-14 20:55:56'),
(3, 1, '0.20', '98.20', '2023-12-14 20:55:56'),
(4, 1, '2.40', '30.50', '2023-12-14 20:56:48'),
(5, 1, '8.30', '10.00', '2023-12-14 21:22:28'),
(6, 2, '1.00', '50.00', '2023-12-14 21:23:25'),
(7, 1, '1.20', '95.80', '2023-12-14 21:37:44'),
(8, 3, '1.20', '95.80', '2023-12-15 02:02:17'),
(9, 3, '5.10', '90.20', '2023-12-15 02:07:39'),
(10, 3, '6.20', '89.20', '2023-12-15 02:08:28'),
(11, 3, '9.20', '23.20', '2023-12-15 02:12:02'),
(12, 2, '2.80', '73.80', '2023-12-15 02:52:26');

-- --------------------------------------------------------

--
-- Struktur dari tabel `hasil`
--

CREATE TABLE `hasil` (
  `id_hasil` int(11) NOT NULL,
  `id_garam` int(11) DEFAULT NULL,
  `kualitas` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `hasil`
--

INSERT INTO `hasil` (`id_hasil`, `id_garam`, `kualitas`) VALUES
(1, 1, 'K3'),
(2, 2, 'K3'),
(3, 3, 'K1'),
(4, 4, 'K3'),
(5, 5, 'K3'),
(6, 6, 'K3'),
(7, 7, 'K1'),
(8, 8, 'K1'),
(9, 9, 'K2'),
(10, 10, 'K3'),
(11, 11, 'K3'),
(12, 12, 'K3');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pengguna`
--

CREATE TABLE `pengguna` (
  `id_petani` int(11) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data untuk tabel `pengguna`
--

INSERT INTO `pengguna` (`id_petani`, `nama`, `email`, `password`) VALUES
(1, 'Fatimah Nurul Izzah', 'nurul@gmail.com', '123'),
(2, 'Fasya', 'fasya@gmail.com', '123'),
(3, 'Bambang Sudiro', 'bambang@gmail.com', '123'),
(4, 'Herman Santoso', 'herman@gmail.com', '123');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `garam`
--
ALTER TABLE `garam`
  ADD PRIMARY KEY (`id_garam`),
  ADD KEY `fk_garam_pengguna` (`id_petani`);

--
-- Indeks untuk tabel `hasil`
--
ALTER TABLE `hasil`
  ADD PRIMARY KEY (`id_hasil`),
  ADD KEY `fk_hasil_garam` (`id_garam`);

--
-- Indeks untuk tabel `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`id_petani`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `garam`
--
ALTER TABLE `garam`
  MODIFY `id_garam` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT untuk tabel `hasil`
--
ALTER TABLE `hasil`
  MODIFY `id_hasil` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT untuk tabel `pengguna`
--
ALTER TABLE `pengguna`
  MODIFY `id_petani` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `garam`
--
ALTER TABLE `garam`
  ADD CONSTRAINT `fk_garam_pengguna` FOREIGN KEY (`id_petani`) REFERENCES `pengguna` (`id_petani`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Ketidakleluasaan untuk tabel `hasil`
--
ALTER TABLE `hasil`
  ADD CONSTRAINT `fk_hasil_garam` FOREIGN KEY (`id_garam`) REFERENCES `garam` (`id_garam`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
