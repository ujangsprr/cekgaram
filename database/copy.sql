CREATE TABLE `user` (
  `id_user` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `role` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `garam` (
  `id_garam` varchar(20) NOT NULL,
  `id_user` int(11) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id_garam`),
  KEY `fk_garam_user` (`id_user`),
  CONSTRAINT `fk_garam_user` FOREIGN KEY (`id_user`) REFERENCES `user` (`id_user`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `garam_values` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_garam` varchar(20) NOT NULL,
  `kadar_air` decimal(5,2) DEFAULT NULL,
  `kadar_garam` decimal(5,2) DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `fk_garam_values_id_garam` (`id_garam`),
  CONSTRAINT `fk_garam_values_id_garam` FOREIGN KEY (`id_garam`) REFERENCES `garam` (`id_garam`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `hasil` (
  `id_hasil` int(11) NOT NULL AUTO_INCREMENT,
  `id_garam` varchar(20) DEFAULT NULL,
  `kualitas` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_hasil`),
  KEY `fk_hasil_garam` (`id_garam`),
  CONSTRAINT `fk_hasil_garam` FOREIGN KEY (`id_garam`) REFERENCES `garam` (`id_garam`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
