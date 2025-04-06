-- MySQL dump 10.13  Distrib 9.2.0, for Win64 (x86_64)
--
-- Host: localhost    Database: trenes_db
-- ------------------------------------------------------
-- Server version	9.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `estaciones`
--

DROP TABLE IF EXISTS `estaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `operador` varchar(50) NOT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `nombre` varchar(100) NOT NULL,
  `horarios` text,
  `precio` float NOT NULL,
  `estado` varchar(20) DEFAULT 'Activo',
  `boletos_vendidos` int DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estaciones`
--

LOCK TABLES `estaciones` WRITE;
/*!40000 ALTER TABLE `estaciones` DISABLE KEYS */;
INSERT INTO `estaciones` VALUES (1,'admin','$2b$12$b.CGWjIJwchjODm5QYQVzepPUvEsJJFj7jevFbUZVBfQg4J2qGi8q','Administrador','00:00',0,'Activo',0),(2,'operador1','$2b$12$zBYPF23qay8ecatQZghRE.I6py7hyk4q2ME9Kovh9Y8OBKPXd6Km.','Estacion Central','08:00, 10:00, 12:00',10.5,'Activo',2),(6,'operador3','$2b$12$AMQjNc6YCqb1S2cZwaW0hux1WwJ/PqZlGjiKCeejVJx26UntZqvKG','Estacion Sur','08:00, 10:00, 12:00',12.5,'Activo',5),(8,'operador4','$2b$12$BGo1VmFBbQ7gvzqL0GXGW.7qFR5GG4oPfKj3dXOvT2pfYP2/1BPhG','pirineos','12:00, 13:00, 14:00',6,'activa',0),(10,'operador5','$2b$12$r5rvjcbTVfv3.ViDEQaW/.VZdOOpbUDNBzdQfwa/swhjmVDCV7TJG','pirineosII','10:00, 12:00, 14:00',7,'activo',0),(17,'Dominguez','$2b$12$e5gBPD25fw2bwHxb6.wwReqGdOaBOUuqkA0lF0XttxVO3.uWeQxfW','Táriba','10:00, 12:00, 14:00',3.5,'activo',0);
/*!40000 ALTER TABLE `estaciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trenes`
--

DROP TABLE IF EXISTS `trenes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trenes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trenes`
--

LOCK TABLES `trenes` WRITE;
/*!40000 ALTER TABLE `trenes` DISABLE KEYS */;
INSERT INTO `trenes` VALUES (1,'Tren Occidente'),(2,'Tren Sur'),(3,'Tren Norte');
/*!40000 ALTER TABLE `trenes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trenes_estaciones`
--

DROP TABLE IF EXISTS `trenes_estaciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trenes_estaciones` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tren_id` int NOT NULL,
  `estacion_id` int NOT NULL,
  `hora_aproximada` time NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tren_id` (`tren_id`),
  KEY `estacion_id` (`estacion_id`),
  CONSTRAINT `trenes_estaciones_ibfk_1` FOREIGN KEY (`tren_id`) REFERENCES `trenes` (`id`),
  CONSTRAINT `trenes_estaciones_ibfk_2` FOREIGN KEY (`estacion_id`) REFERENCES `estaciones` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trenes_estaciones`
--

LOCK TABLES `trenes_estaciones` WRITE;
/*!40000 ALTER TABLE `trenes_estaciones` DISABLE KEYS */;
/*!40000 ALTER TABLE `trenes_estaciones` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-21  1:17:42
