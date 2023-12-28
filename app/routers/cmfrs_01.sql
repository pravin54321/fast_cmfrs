-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: cmfrs
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cast`
--

DROP TABLE IF EXISTS `cast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cast` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Cast` varchar(200) NOT NULL,
  `Religion_id` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Cast` (`Cast`),
  KEY `Religion_id` (`Religion_id`),
  KEY `ix_cast_id` (`id`),
  CONSTRAINT `cast_ibfk_1` FOREIGN KEY (`Religion_id`) REFERENCES `religion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cast`
--

LOCK TABLES `cast` WRITE;
/*!40000 ALTER TABLE `cast` DISABLE KEYS */;
INSERT INTO `cast` VALUES (1,'Kunabi',1,'2023-12-27 05:24:20','2023-12-27 05:24:20'),(2,'SC',1,'2023-12-27 05:26:20','2023-12-27 05:27:01'),(3,'Muslim_cast',1,'2023-12-27 05:28:07','2023-12-27 05:28:07'),(4,'Christian_cast',1,'2023-12-27 05:28:39','2023-12-27 05:28:39'),(5,'Parsi_cast',1,'2023-12-27 05:29:36','2023-12-27 05:29:36');
/*!40000 ALTER TABLE `cast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `distric`
--

DROP TABLE IF EXISTS `distric`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `distric` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Distric` varchar(200) NOT NULL,
  `State_id` int(11) NOT NULL,
  `Region_id` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Distric` (`Distric`),
  KEY `State_id` (`State_id`),
  KEY `Region_id` (`Region_id`),
  CONSTRAINT `distric_ibfk_1` FOREIGN KEY (`State_id`) REFERENCES `state` (`id`),
  CONSTRAINT `distric_ibfk_2` FOREIGN KEY (`Region_id`) REFERENCES `region` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `distric`
--

LOCK TABLES `distric` WRITE;
/*!40000 ALTER TABLE `distric` DISABLE KEYS */;
INSERT INTO `distric` VALUES (1,'District_01',2,2,'2023-12-26 12:11:19','2023-12-26 12:14:30'),(2,'District_03',3,3,'2023-12-26 12:12:26','2023-12-26 12:12:26'),(3,'District_04',4,4,'2023-12-26 12:12:42','2023-12-26 12:12:42'),(4,'District_05',5,5,'2023-12-26 12:13:03','2023-12-26 12:13:03');
/*!40000 ALTER TABLE `distric` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groupimg`
--

DROP TABLE IF EXISTS `groupimg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groupimg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ImgPath` varchar(200) NOT NULL,
  `original_img` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_groupimg_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groupimg`
--

LOCK TABLES `groupimg` WRITE;
/*!40000 ALTER TABLE `groupimg` DISABLE KEYS */;
/*!40000 ALTER TABLE `groupimg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `headoffice`
--

DROP TABLE IF EXISTS `headoffice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `headoffice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `HeadOffice` varchar(200) NOT NULL,
  `State_id` int(11) NOT NULL,
  `Region_id` int(11) NOT NULL,
  `Distric_id` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `HeadOffice` (`HeadOffice`),
  KEY `State_id` (`State_id`),
  KEY `Region_id` (`Region_id`),
  KEY `Distric_id` (`Distric_id`),
  KEY `ix_headoffice_id` (`id`),
  CONSTRAINT `headoffice_ibfk_1` FOREIGN KEY (`State_id`) REFERENCES `state` (`id`),
  CONSTRAINT `headoffice_ibfk_2` FOREIGN KEY (`Region_id`) REFERENCES `region` (`id`),
  CONSTRAINT `headoffice_ibfk_3` FOREIGN KEY (`Distric_id`) REFERENCES `distric` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `headoffice`
--

LOCK TABLES `headoffice` WRITE;
/*!40000 ALTER TABLE `headoffice` DISABLE KEYS */;
INSERT INTO `headoffice` VALUES (1,'head_01',1,1,2,'2023-12-26 12:16:23','2023-12-26 12:16:23'),(2,'head_02',2,2,2,'2023-12-26 12:16:47','2023-12-26 12:31:21'),(3,'head_03',3,3,3,'2023-12-26 12:17:11','2023-12-26 12:17:11'),(4,'head_04',4,4,4,'2023-12-26 12:17:29','2023-12-26 12:17:29');
/*!40000 ALTER TABLE `headoffice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kalam`
--

DROP TABLE IF EXISTS `kalam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kalam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Kalam` varchar(200) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Kalam` (`Kalam`),
  UNIQUE KEY `ix_kalam_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kalam`
--

LOCK TABLES `kalam` WRITE;
/*!40000 ALTER TABLE `kalam` DISABLE KEYS */;
INSERT INTO `kalam` VALUES (3,'kalam_03','2023-12-22 07:35:18','2023-12-22 07:35:18'),(4,'kalam_04','2023-12-22 07:35:28','2023-12-22 07:35:28'),(5,'kalam_05','2023-12-22 07:35:37','2023-12-22 07:35:37'),(6,'kalam_06','2023-12-22 07:35:56','2023-12-22 07:35:56'),(7,'Act-C','2023-12-22 07:36:13','2023-12-25 05:30:49'),(8,'Act-B','2023-12-25 05:20:20','2023-12-25 05:29:08');
/*!40000 ALTER TABLE `kalam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `langues`
--

DROP TABLE IF EXISTS `langues`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `langues` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Langues` varchar(200) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Langues` (`Langues`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `langues`
--

LOCK TABLES `langues` WRITE;
/*!40000 ALTER TABLE `langues` DISABLE KEYS */;
/*!40000 ALTER TABLE `langues` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `occupation`
--

DROP TABLE IF EXISTS `occupation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `occupation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Occupation` varchar(200) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Occupation` (`Occupation`),
  KEY `ix_Occupation_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `occupation`
--

LOCK TABLES `occupation` WRITE;
/*!40000 ALTER TABLE `occupation` DISABLE KEYS */;
/*!40000 ALTER TABLE `occupation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `outhperson`
--

DROP TABLE IF EXISTS `outhperson`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `outhperson` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `OuthPerson` varchar(200) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `OuthPerson` (`OuthPerson`),
  KEY `ix_outhperson_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `outhperson`
--

LOCK TABLES `outhperson` WRITE;
/*!40000 ALTER TABLE `outhperson` DISABLE KEYS */;
/*!40000 ALTER TABLE `outhperson` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `person`
--

DROP TABLE IF EXISTS `person`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `person` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) DEFAULT NULL,
  `Mobile_Number` varchar(12) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Age` int(11) DEFAULT NULL,
  `Gender` varchar(50) DEFAULT NULL,
  `Address` text DEFAULT NULL,
  `Status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Email` (`Email`),
  KEY `ix_person_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `person`
--

LOCK TABLES `person` WRITE;
/*!40000 ALTER TABLE `person` DISABLE KEYS */;
/*!40000 ALTER TABLE `person` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `personimg`
--

DROP TABLE IF EXISTS `personimg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `personimg` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file_path` varchar(255) DEFAULT NULL,
  `face_encoding` text DEFAULT NULL,
  `Person_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `Person_id` (`Person_id`),
  KEY `ix_personimg_id` (`id`),
  CONSTRAINT `personimg_ibfk_1` FOREIGN KEY (`Person_id`) REFERENCES `person` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `personimg`
--

LOCK TABLES `personimg` WRITE;
/*!40000 ALTER TABLE `personimg` DISABLE KEYS */;
/*!40000 ALTER TABLE `personimg` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `policestation`
--

DROP TABLE IF EXISTS `policestation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `policestation` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `PoliceStation` varchar(200) NOT NULL,
  `State_id` int(11) NOT NULL,
  `Region_id` int(11) NOT NULL,
  `Distric_id` int(11) NOT NULL,
  `HeadOffice_id` int(11) NOT NULL,
  `Subdivision_id` int(11) NOT NULL,
  `Taluka_id` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `PoliceStation` (`PoliceStation`),
  KEY `State_id` (`State_id`),
  KEY `Region_id` (`Region_id`),
  KEY `Distric_id` (`Distric_id`),
  KEY `HeadOffice_id` (`HeadOffice_id`),
  KEY `Subdivision_id` (`Subdivision_id`),
  KEY `Taluka_id` (`Taluka_id`),
  KEY `ix_policestation_id` (`id`),
  CONSTRAINT `policestation_ibfk_1` FOREIGN KEY (`State_id`) REFERENCES `state` (`id`),
  CONSTRAINT `policestation_ibfk_2` FOREIGN KEY (`Region_id`) REFERENCES `region` (`id`),
  CONSTRAINT `policestation_ibfk_3` FOREIGN KEY (`Distric_id`) REFERENCES `distric` (`id`),
  CONSTRAINT `policestation_ibfk_4` FOREIGN KEY (`HeadOffice_id`) REFERENCES `headoffice` (`id`),
  CONSTRAINT `policestation_ibfk_5` FOREIGN KEY (`Subdivision_id`) REFERENCES `subdivision` (`id`),
  CONSTRAINT `policestation_ibfk_6` FOREIGN KEY (`Taluka_id`) REFERENCES `taluka` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policestation`
--

LOCK TABLES `policestation` WRITE;
/*!40000 ALTER TABLE `policestation` DISABLE KEYS */;
INSERT INTO `policestation` VALUES (1,'station_01',2,3,2,2,2,2,'2023-12-26 12:47:14','2023-12-26 12:52:44'),(2,'station_02',2,2,2,2,2,2,'2023-12-26 12:48:08','2023-12-26 12:48:08'),(3,'station_03',3,3,3,3,3,3,'2023-12-26 12:48:33','2023-12-26 12:48:33'),(4,'station_04',4,4,4,4,4,4,'2023-12-26 12:48:59','2023-12-26 12:48:59');
/*!40000 ALTER TABLE `policestation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `policestation_new`
--

DROP TABLE IF EXISTS `policestation_new`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `policestation_new` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `PoliceStation` varchar(200) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  `db_name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `PoliceStation` (`PoliceStation`),
  UNIQUE KEY `db_name` (`db_name`),
  KEY `ix_policestation_new_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `policestation_new`
--

LOCK TABLES `policestation_new` WRITE;
/*!40000 ALTER TABLE `policestation_new` DISABLE KEYS */;
INSERT INTO `policestation_new` VALUES (3,'lakhandur','2023-12-25 09:12:47','2023-12-25 09:12:47','lakhandur_db'),(4,'Sakoli_policestation','2023-12-27 06:52:54','2023-12-27 06:52:54','Sakoli_policestation_db'),(5,'sakoli','2023-12-27 10:00:15','2023-12-27 10:00:15','sakoli_db'),(7,'sakoli_new','2023-12-27 10:02:12','2023-12-27 10:02:12','sakoli_new_db');
/*!40000 ALTER TABLE `policestation_new` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `post`
--

DROP TABLE IF EXISTS `post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `post` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Post` varchar(200) NOT NULL,
  `State_id` int(11) NOT NULL,
  `Region_id` int(11) NOT NULL,
  `Distric_id` int(11) NOT NULL,
  `HeadOffice_id` int(11) NOT NULL,
  `Subdivision_id` int(11) NOT NULL,
  `Taluka_id` int(11) NOT NULL,
  `PoliceStation_id` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Post` (`Post`),
  KEY `State_id` (`State_id`),
  KEY `Region_id` (`Region_id`),
  KEY `Distric_id` (`Distric_id`),
  KEY `HeadOffice_id` (`HeadOffice_id`),
  KEY `Subdivision_id` (`Subdivision_id`),
  KEY `Taluka_id` (`Taluka_id`),
  KEY `PoliceStation_id` (`PoliceStation_id`),
  CONSTRAINT `post_ibfk_1` FOREIGN KEY (`State_id`) REFERENCES `state` (`id`),
  CONSTRAINT `post_ibfk_2` FOREIGN KEY (`Region_id`) REFERENCES `region` (`id`),
  CONSTRAINT `post_ibfk_3` FOREIGN KEY (`Distric_id`) REFERENCES `distric` (`id`),
  CONSTRAINT `post_ibfk_4` FOREIGN KEY (`HeadOffice_id`) REFERENCES `headoffice` (`id`),
  CONSTRAINT `post_ibfk_5` FOREIGN KEY (`Subdivision_id`) REFERENCES `subdivision` (`id`),
  CONSTRAINT `post_ibfk_6` FOREIGN KEY (`Taluka_id`) REFERENCES `taluka` (`id`),
  CONSTRAINT `post_ibfk_7` FOREIGN KEY (`PoliceStation_id`) REFERENCES `policestation` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `post`
--

LOCK TABLES `post` WRITE;
/*!40000 ALTER TABLE `post` DISABLE KEYS */;
INSERT INTO `post` VALUES (1,'post_01',2,4,2,4,2,2,2,'2023-12-26 12:54:12','2023-12-26 12:59:19'),(2,'post_02',2,2,2,2,2,2,2,'2023-12-26 12:55:29','2023-12-26 12:55:29'),(3,'post_03',3,3,3,3,3,3,3,'2023-12-26 12:56:18','2023-12-26 12:56:18'),(4,'post_04',4,4,4,4,4,4,4,'2023-12-26 12:57:07','2023-12-26 12:57:07');
/*!40000 ALTER TABLE `post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `region`
--

DROP TABLE IF EXISTS `region`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `region` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Region` varchar(200) NOT NULL,
  `State_id` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Region` (`Region`),
  KEY `State_id` (`State_id`),
  CONSTRAINT `region_ibfk_1` FOREIGN KEY (`State_id`) REFERENCES `state` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `region`
--

LOCK TABLES `region` WRITE;
/*!40000 ALTER TABLE `region` DISABLE KEYS */;
INSERT INTO `region` VALUES (1,'Amarawati',1,'2023-12-26 11:28:15','2023-12-26 11:28:15'),(2,'Amara_01',1,'2023-12-26 11:28:34','2023-12-26 11:42:13'),(3,'Amara_03',3,'2023-12-26 11:28:46','2023-12-26 11:28:46'),(4,'Amara_04',4,'2023-12-26 11:29:09','2023-12-26 11:29:09'),(5,'Amara_05',5,'2023-12-26 11:29:20','2023-12-26 11:29:20');
/*!40000 ALTER TABLE `region` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `religion`
--

DROP TABLE IF EXISTS `religion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `religion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Religion` varchar(200) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Religion` (`Religion`),
  KEY `ix_religion_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `religion`
--

LOCK TABLES `religion` WRITE;
/*!40000 ALTER TABLE `religion` DISABLE KEYS */;
INSERT INTO `religion` VALUES (1,'Hindu','2023-12-27 05:22:06','2023-12-27 05:22:06'),(2,'Muslim','2023-12-27 05:22:20','2023-12-27 05:22:20'),(3,'Bhudh','2023-12-27 05:22:30','2023-12-27 05:22:30'),(4,'Christian','2023-12-27 05:23:05','2023-12-27 05:23:05'),(5,'Parsi','2023-12-27 05:23:20','2023-12-27 05:23:20');
/*!40000 ALTER TABLE `religion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `state`
--

DROP TABLE IF EXISTS `state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `State` varchar(200) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `State` (`State`),
  KEY `ix_state_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `state`
--

LOCK TABLES `state` WRITE;
/*!40000 ALTER TABLE `state` DISABLE KEYS */;
INSERT INTO `state` VALUES (1,'Maharastra','2023-12-26 11:25:29','2023-12-26 11:25:29'),(2,'Tamilnadu','2023-12-26 11:25:45','2023-12-26 11:25:45'),(3,'Keral','2023-12-26 11:25:59','2023-12-26 11:25:59'),(4,'Goa','2023-12-26 11:26:10','2023-12-26 11:26:10'),(5,'Gujarath','2023-12-26 11:26:46','2023-12-26 11:26:46');
/*!40000 ALTER TABLE `state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subcast`
--

DROP TABLE IF EXISTS `subcast`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subcast` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Subcast` varchar(200) NOT NULL,
  `Religion_id` int(11) NOT NULL,
  `Cast_id` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Subcast` (`Subcast`),
  KEY `Religion_id` (`Religion_id`),
  KEY `Cast_id` (`Cast_id`),
  CONSTRAINT `subcast_ibfk_1` FOREIGN KEY (`Religion_id`) REFERENCES `religion` (`id`),
  CONSTRAINT `subcast_ibfk_2` FOREIGN KEY (`Cast_id`) REFERENCES `cast` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subcast`
--

LOCK TABLES `subcast` WRITE;
/*!40000 ALTER TABLE `subcast` DISABLE KEYS */;
INSERT INTO `subcast` VALUES (1,'Hindu_Subcast',2,2,'2023-12-27 05:39:02','2023-12-27 05:44:29'),(2,'Muslim_subcast',2,2,'2023-12-27 05:39:46','2023-12-27 05:39:46'),(3,'Budh_subcast',3,3,'2023-12-27 05:40:13','2023-12-27 05:40:13'),(4,'Christian_subcast',4,4,'2023-12-27 05:40:47','2023-12-27 05:40:47'),(5,'Parsi_subcast',5,5,'2023-12-27 05:41:08','2023-12-27 05:41:08');
/*!40000 ALTER TABLE `subcast` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subdivision`
--

DROP TABLE IF EXISTS `subdivision`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subdivision` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Subdivision` varchar(200) NOT NULL,
  `State_id` int(11) NOT NULL,
  `Region_id` int(11) NOT NULL,
  `Distric_id` int(11) NOT NULL,
  `HeadOffice_id` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Subdivision` (`Subdivision`),
  KEY `State_id` (`State_id`),
  KEY `Region_id` (`Region_id`),
  KEY `Distric_id` (`Distric_id`),
  KEY `HeadOffice_id` (`HeadOffice_id`),
  CONSTRAINT `subdivision_ibfk_1` FOREIGN KEY (`State_id`) REFERENCES `state` (`id`),
  CONSTRAINT `subdivision_ibfk_2` FOREIGN KEY (`Region_id`) REFERENCES `region` (`id`),
  CONSTRAINT `subdivision_ibfk_3` FOREIGN KEY (`Distric_id`) REFERENCES `distric` (`id`),
  CONSTRAINT `subdivision_ibfk_4` FOREIGN KEY (`HeadOffice_id`) REFERENCES `headoffice` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subdivision`
--

LOCK TABLES `subdivision` WRITE;
/*!40000 ALTER TABLE `subdivision` DISABLE KEYS */;
INSERT INTO `subdivision` VALUES (1,' subdivision_01',2,2,2,2,'2023-12-26 12:32:30','2023-12-26 12:35:36'),(2,'subdivision_02',2,2,2,2,'2023-12-26 12:32:53','2023-12-26 12:32:53'),(3,'subdivision_03',3,3,3,3,'2023-12-26 12:33:14','2023-12-26 12:33:14'),(4,'subdivision_04',4,4,4,4,'2023-12-26 12:33:34','2023-12-26 12:33:34');
/*!40000 ALTER TABLE `subdivision` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taluka`
--

DROP TABLE IF EXISTS `taluka`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taluka` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Taluka` varchar(200) NOT NULL,
  `State_id` int(11) NOT NULL,
  `Region_id` int(11) NOT NULL,
  `Distric_id` int(11) NOT NULL,
  `HeadOffice_id` int(11) NOT NULL,
  `Subdivision_id` int(11) NOT NULL,
  `create_date` datetime DEFAULT NULL,
  `update_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Taluka` (`Taluka`),
  KEY `State_id` (`State_id`),
  KEY `Region_id` (`Region_id`),
  KEY `Distric_id` (`Distric_id`),
  KEY `HeadOffice_id` (`HeadOffice_id`),
  KEY `Subdivision_id` (`Subdivision_id`),
  KEY `ix_taluka_id` (`id`),
  CONSTRAINT `taluka_ibfk_1` FOREIGN KEY (`State_id`) REFERENCES `state` (`id`),
  CONSTRAINT `taluka_ibfk_2` FOREIGN KEY (`Region_id`) REFERENCES `region` (`id`),
  CONSTRAINT `taluka_ibfk_3` FOREIGN KEY (`Distric_id`) REFERENCES `distric` (`id`),
  CONSTRAINT `taluka_ibfk_4` FOREIGN KEY (`HeadOffice_id`) REFERENCES `headoffice` (`id`),
  CONSTRAINT `taluka_ibfk_5` FOREIGN KEY (`Subdivision_id`) REFERENCES `subdivision` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taluka`
--

LOCK TABLES `taluka` WRITE;
/*!40000 ALTER TABLE `taluka` DISABLE KEYS */;
INSERT INTO `taluka` VALUES (1,'Taluka_01',1,1,1,1,1,'2023-12-26 12:37:47','2023-12-26 12:37:47'),(2,'Taluka_02',1,1,1,1,1,'2023-12-26 12:38:41','2023-12-26 12:46:10'),(3,'Taluka_03',3,3,2,3,3,'2023-12-26 12:39:05','2023-12-26 12:39:05'),(4,'Taluka_04',4,4,4,4,4,'2023-12-26 12:40:06','2023-12-26 12:40:06');
/*!40000 ALTER TABLE `taluka` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `UserName` varchar(50) NOT NULL,
  `UserEmail` varchar(200) NOT NULL,
  `UserPassword` varchar(200) DEFAULT NULL,
  `disabled` tinyint(1) DEFAULT NULL,
  `PoliceStation` varchar(200) DEFAULT 'Null',
  `Db_Name` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `UserEmail` (`UserEmail`),
  KEY `ix_user_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'vip4','vip4@gmail.com.com','$2b$12$eKvqRzkuTiuFFnDlnjz81OUehlwMjbydDKDO.F0f6vf0.XEiWtpVm',1,'Lakhandur','Lakhandur_db');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-28 14:18:42
