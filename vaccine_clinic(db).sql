-- MySQL dump 10.13  Distrib 8.0.41, for macos15 (x86_64)
--
-- Host: 65.0.103.152    Database: clinic_db
-- ------------------------------------------------------
-- Server version	8.0.44-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add clinic',7,'add_clinic'),(26,'Can change clinic',7,'change_clinic'),(27,'Can delete clinic',7,'delete_clinic'),(28,'Can view clinic',7,'view_clinic'),(29,'Can add parent',8,'add_parent'),(30,'Can change parent',8,'change_parent'),(31,'Can delete parent',8,'delete_parent'),(32,'Can view parent',8,'view_parent'),(33,'Can add child',9,'add_child'),(34,'Can change child',9,'change_child'),(35,'Can delete child',9,'delete_child'),(36,'Can view child',9,'view_child'),(37,'Can add schedule version',10,'add_scheduleversion'),(38,'Can change schedule version',10,'change_scheduleversion'),(39,'Can delete schedule version',10,'delete_scheduleversion'),(40,'Can view schedule version',10,'view_scheduleversion'),(41,'Can add vaccine',11,'add_vaccine'),(42,'Can change vaccine',11,'change_vaccine'),(43,'Can delete vaccine',11,'delete_vaccine'),(44,'Can view vaccine',11,'view_vaccine'),(45,'Can add vaccine dose',12,'add_vaccinedose'),(46,'Can change vaccine dose',12,'change_vaccinedose'),(47,'Can delete vaccine dose',12,'delete_vaccinedose'),(48,'Can view vaccine dose',12,'view_vaccinedose'),(49,'Can add child dose',13,'add_childdose'),(50,'Can change child dose',13,'change_childdose'),(51,'Can delete child dose',13,'delete_childdose'),(52,'Can view child dose',13,'view_childdose'),(53,'Can add partner',14,'add_partner'),(54,'Can change partner',14,'change_partner'),(55,'Can delete partner',14,'delete_partner'),(56,'Can view partner',14,'view_partner'),(57,'Can add field representative',15,'add_fieldrepresentative'),(58,'Can change field representative',15,'change_fieldrepresentative'),(59,'Can delete field representative',15,'delete_fieldrepresentative'),(60,'Can view field representative',15,'view_fieldrepresentative'),(61,'Can add doctor',16,'add_doctor'),(62,'Can change doctor',16,'change_doctor'),(63,'Can delete doctor',16,'delete_doctor'),(64,'Can view doctor',16,'view_doctor'),(65,'Can add o auth state',17,'add_oauthstate'),(66,'Can change o auth state',17,'change_oauthstate'),(67,'Can delete o auth state',17,'delete_oauthstate'),(68,'Can view o auth state',17,'view_oauthstate'),(69,'Can add doctor session token',18,'add_doctorsessiontoken'),(70,'Can change doctor session token',18,'change_doctorsessiontoken'),(71,'Can delete doctor session token',18,'delete_doctorsessiontoken'),(72,'Can view doctor session token',18,'view_doctorsessiontoken'),(73,'Can add child share link',19,'add_childsharelink'),(74,'Can change child share link',19,'change_childsharelink'),(75,'Can delete child share link',19,'delete_childsharelink'),(76,'Can view child share link',19,'view_childsharelink'),(77,'Can add vaccine education patient',20,'add_vaccineeducationpatient'),(78,'Can change vaccine education patient',20,'change_vaccineeducationpatient'),(79,'Can delete vaccine education patient',20,'delete_vaccineeducationpatient'),(80,'Can view vaccine education patient',20,'view_vaccineeducationpatient'),(81,'Can add vaccine education doctor',21,'add_vaccineeducationdoctor'),(82,'Can change vaccine education doctor',21,'change_vaccineeducationdoctor'),(83,'Can delete vaccine education doctor',21,'delete_vaccineeducationdoctor'),(84,'Can view vaccine education doctor',21,'view_vaccineeducationdoctor'),(85,'Can add ui string',22,'add_uistring'),(86,'Can change ui string',22,'change_uistring'),(87,'Can delete ui string',22,'delete_uistring'),(88,'Can view ui string',22,'view_uistring'),(89,'Can add ui string translation',23,'add_uistringtranslation'),(90,'Can change ui string translation',23,'change_uistringtranslation'),(91,'Can delete ui string translation',23,'delete_uistringtranslation'),(92,'Can view ui string translation',23,'view_uistringtranslation');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'','2025-10-27 06:16:26.778725',0,'doc:12','','','bhartidhote8@gmail.com',0,1,'2025-10-02 22:33:17.693697'),(2,'','2025-10-27 06:33:01.994433',0,'doc:13','','','bhartidhote8@gmail.com',0,1,'2025-10-02 23:05:28.754770'),(3,'pbkdf2_sha256$1000000$NMClg0ImPycBJYKRu6RMPS$VBfvtqdADmeWaetoyOGfpI0eq4I+AQSyWeF9qwmzoO4=','2025-10-31 07:24:07.086305',1,'Vaccine','','','bharti.dhote@inditech.co.in',1,1,'2025-10-02 23:19:08.635887'),(4,'','2025-10-27 13:26:16.601462',0,'doc:14','','','haterworld16@gmail.com',0,1,'2025-10-02 23:46:35.697501'),(5,'','2025-10-27 13:38:23.679746',0,'doc:15','','','bhartidhote8@gmail.com',0,1,'2025-10-03 13:48:03.497458'),(6,'','2025-10-06 17:46:19.501100',0,'doc:1','','','bhartidhote8@gmail.com',0,1,'2025-10-05 17:36:43.850842'),(7,'','2025-11-03 10:16:45.050750',0,'doc:16','','','bhartidhote8@gmail.com',0,1,'2025-10-05 18:17:24.483508'),(8,'','2025-10-07 09:25:15.890852',0,'doc:4','','','haterworld16@gmail.com',0,1,'2025-10-07 09:25:15.874723'),(9,'','2025-10-07 10:46:06.668938',0,'doc:5','','','bhartidhote8@gmail.com',0,1,'2025-10-07 10:46:06.660032'),(10,'','2025-10-07 10:53:55.585325',0,'doc:7','','','haterworld16@gmail.com',0,1,'2025-10-07 10:53:55.573913'),(11,'','2025-10-07 11:04:37.267581',0,'doc:8','','','bhartidhote8@gmail.com',0,1,'2025-10-07 11:04:37.254116'),(12,'','2025-10-07 12:27:31.872373',0,'doc:10','','','bhartidhote8@gmail.com',0,1,'2025-10-07 12:27:31.860782');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `child`
--

DROP TABLE IF EXISTS `child`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `child` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `parent_id` bigint NOT NULL,
  `clinic_id` bigint DEFAULT NULL,
  `full_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `date_of_birth` date DEFAULT NULL,
  `sex` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `state` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `child_name_enc` longblob,
  `date_of_birth_enc` longblob,
  `gender_enc` longblob,
  `state_enc` longblob,
  PRIMARY KEY (`id`),
  KEY `child_parent_id_72f601a8` (`parent_id`),
  KEY `child_clinic_id_8c3c1a2e` (`clinic_id`),
  KEY `idx_child_clinic` (`clinic_id`),
  KEY `idx_child_dob` (`date_of_birth`),
  KEY `idx_child_parent` (`parent_id`),
  CONSTRAINT `fk_child_clinic` FOREIGN KEY (`clinic_id`) REFERENCES `clinic` (`id`),
  CONSTRAINT `fk_child_parent` FOREIGN KEY (`parent_id`) REFERENCES `parent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child`
--

LOCK TABLES `child` WRITE;
/*!40000 ALTER TABLE `child` DISABLE KEYS */;
INSERT INTO `child` VALUES (25,1,NULL,'Test-1OCT','2025-01-01','M','2025-10-05 18:21:19.410584','2025-10-06 18:54:45.806299','Madhya Pradesh',NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `child` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `child_dose`
--

DROP TABLE IF EXISTS `child_dose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `child_dose` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `child_id` bigint NOT NULL,
  `dose_id` bigint NOT NULL,
  `given_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `due_until_date` date DEFAULT NULL,
  `status_override` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `updated_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
  `last_reminder_at` datetime(6) DEFAULT NULL,
  `last_reminder_by_id` bigint DEFAULT NULL,
  `last_reminder_for_date` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_cd_child_dose` (`child_id`,`dose_id`),
  KEY `idx_cd_child` (`child_id`),
  KEY `idx_cd_dose` (`dose_id`),
  KEY `idx_cd_due_date` (`due_date`),
  KEY `idx_cd_given_date` (`given_date`),
  KEY `child_dose_last_reminder_by_id_bb7c23f1_fk_doctor_id` (`last_reminder_by_id`),
  CONSTRAINT `child_dose_last_reminder_by_id_bb7c23f1_fk_doctor_id` FOREIGN KEY (`last_reminder_by_id`) REFERENCES `doctor` (`id`),
  CONSTRAINT `fk_cd_child` FOREIGN KEY (`child_id`) REFERENCES `child` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_cd_dose` FOREIGN KEY (`dose_id`) REFERENCES `vaccine_dose` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1069 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child_dose`
--

LOCK TABLES `child_dose` WRITE;
/*!40000 ALTER TABLE `child_dose` DISABLE KEYS */;
INSERT INTO `child_dose` VALUES (1024,25,85,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1025,25,86,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1026,25,87,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1027,25,88,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1028,25,44,NULL,'2025-01-01',NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1029,25,47,NULL,'2025-02-12',NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1030,25,53,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1031,25,59,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1032,25,73,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1033,25,78,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1034,25,45,NULL,'2025-01-01',NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1035,25,50,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1036,25,56,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1037,25,62,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1038,25,69,NULL,'2025-12-27',NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1039,25,90,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1040,25,76,NULL,'2025-12-27',NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1041,25,48,NULL,'2025-02-12',NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1042,25,54,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1043,25,60,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1044,25,74,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1045,25,81,NULL,'2033-12-30',NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1046,25,94,NULL,'2025-06-30',NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1047,25,95,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1048,25,49,NULL,'2025-02-12',NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1049,25,55,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1050,25,61,NULL,NULL,NULL,'','2025-10-05 18:21:19.415071','2025-10-05 18:21:19.415071',NULL,NULL,NULL),(1051,25,75,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1052,25,79,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1053,25,68,NULL,'2025-09-28',NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1054,25,71,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1055,25,80,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1056,25,46,NULL,'2025-01-01',NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1057,25,51,NULL,'2025-02-12',NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1058,25,57,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1059,25,63,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1060,25,70,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1061,25,52,NULL,'2025-02-12',NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1062,25,58,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1063,25,64,NULL,'2025-04-09',NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1064,25,89,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1065,25,82,NULL,'2034-12-30',NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1066,25,67,NULL,'2025-06-30',NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1067,25,72,NULL,'2026-03-27',NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL),(1068,25,77,NULL,NULL,NULL,'','2025-10-05 18:21:19.419752','2025-10-05 18:21:19.419752',NULL,NULL,NULL);
/*!40000 ALTER TABLE `child_dose` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `child_share_link`
--

DROP TABLE IF EXISTS `child_share_link`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `child_share_link` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expected_last10` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `child_id` bigint NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `child_share_child_i_a28a1d_idx` (`child_id`),
  KEY `child_share_expires_97186c_idx` (`expires_at`),
  KEY `child_share_link_created_by_id_7b23b4cb_fk_doctor_id` (`created_by_id`),
  CONSTRAINT `child_share_link_child_id_9d4968fb_fk_child_id` FOREIGN KEY (`child_id`) REFERENCES `child` (`id`),
  CONSTRAINT `child_share_link_created_by_id_7b23b4cb_fk_doctor_id` FOREIGN KEY (`created_by_id`) REFERENCES `doctor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child_share_link`
--

LOCK TABLES `child_share_link` WRITE;
/*!40000 ALTER TABLE `child_share_link` DISABLE KEYS */;
INSERT INTO `child_share_link` VALUES (6,'4gLZYRbAU4urcbaWPokUkMgs7nS2DCI_Otm9hBqU8yo','9827766106','2025-10-05 18:21:23.898330','2026-04-03 18:21:23.897327',1,25,NULL);
/*!40000 ALTER TABLE `child_share_link` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clinic`
--

DROP TABLE IF EXISTS `clinic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clinic` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `phone` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
  `state` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `headquarters` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `pincode` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `whatsapp_e164` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `receptionist_email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `languages_csv` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clinic`
--

LOCK TABLES `clinic` WRITE;
/*!40000 ALTER TABLE `clinic` DISABLE KEYS */;
/*!40000 ALTER TABLE `clinic` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(9,'vaccinations','child'),(13,'vaccinations','childdose'),(19,'vaccinations','childsharelink'),(7,'vaccinations','clinic'),(16,'vaccinations','doctor'),(18,'vaccinations','doctorsessiontoken'),(15,'vaccinations','fieldrepresentative'),(17,'vaccinations','oauthstate'),(8,'vaccinations','parent'),(14,'vaccinations','partner'),(10,'vaccinations','scheduleversion'),(22,'vaccinations','uistring'),(23,'vaccinations','uistringtranslation'),(11,'vaccinations','vaccine'),(12,'vaccinations','vaccinedose'),(21,'vaccinations','vaccineeducationdoctor'),(20,'vaccinations','vaccineeducationpatient');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=80 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-09-03 17:00:31.711581'),(2,'auth','0001_initial','2025-09-03 17:00:32.721175'),(3,'admin','0001_initial','2025-09-03 17:00:32.934724'),(4,'admin','0002_logentry_remove_auto_add','2025-09-03 17:00:32.937467'),(5,'admin','0003_logentry_add_action_flag_choices','2025-09-03 17:00:32.957904'),(6,'contenttypes','0002_remove_content_type_name','2025-09-03 17:00:33.116255'),(7,'auth','0002_alter_permission_name_max_length','2025-09-03 17:00:33.192115'),(8,'auth','0003_alter_user_email_max_length','2025-09-03 17:00:33.233450'),(9,'auth','0004_alter_user_username_opts','2025-09-03 17:00:33.248611'),(10,'auth','0005_alter_user_last_login_null','2025-09-03 17:00:33.320089'),(11,'auth','0006_require_contenttypes_0002','2025-09-03 17:00:33.320089'),(12,'auth','0007_alter_validators_add_error_messages','2025-09-03 17:00:33.336555'),(13,'auth','0008_alter_user_username_max_length','2025-09-03 17:00:33.419967'),(14,'auth','0009_alter_user_last_name_max_length','2025-09-03 17:00:33.507117'),(15,'auth','0010_alter_group_name_max_length','2025-09-03 17:00:33.526852'),(16,'auth','0011_update_proxy_permissions','2025-09-03 17:00:33.540318'),(17,'auth','0012_alter_user_first_name_max_length','2025-09-03 17:00:33.620533'),(18,'sessions','0001_initial','2025-09-03 17:00:33.671465'),(19,'vaccinations','0001_initial','2025-09-03 17:11:31.709867'),(21,'vaccinations','0002_child_state_alter_vaccine_code_alter_vaccine_name_and_more','2025-09-04 09:51:15.284442'),(22,'vaccinations','0003_phase2_whitelabel','2025-09-10 17:52:03.769186'),(23,'vaccinations','0004_doctor_google_login','2025-09-13 14:28:55.672913'),(24,'vaccinations','0005_oauthstate_and_more','2025-09-15 12:03:06.855693'),(25,'vaccinations','0006_oauthstate_redirect_uri','2025-09-15 12:51:43.883526'),(35,'vaccinations','0016_change_clinic_to_clinic_id','2025-10-05 17:32:39.759255'),(36,'vaccinations','0018_rename_sex_enc_to_gender_enc','2025-10-05 17:32:39.763764'),(45,'vaccinations','0019_child_idx_child_clinic_child_idx_child_dob_and_more','2025-10-06 13:27:21.941197'),(53,'vaccinations','0026_add_default_to_full_name','2025-10-06 17:39:46.877343'),(54,'vaccinations','0027_mysql_fix_full_name_not_null','2025-10-06 17:41:24.706990'),(55,'vaccinations','0028_fix_mysql_full_name_field','2025-10-06 17:48:43.730505'),(56,'vaccinations','0029_fix_mysql_full_name_field_direct','2025-10-06 17:50:22.832522'),(58,'vaccinations','0007_child_share_link','2025-10-06 18:21:04.445928'),(59,'vaccinations','0008_rename_idx_csl_child_child_share_child_i_a28a1d_idx_and_more','2025-10-06 18:21:44.889274'),(60,'vaccinations','0009_vaccineeducationdoctor_vaccineeducationpatient','2025-10-06 18:23:34.360139'),(61,'vaccinations','0010_childdose_last_reminder_at_and_more','2025-10-06 18:24:49.775014'),(62,'vaccinations','0011_uistring_uistringtranslation','2025-10-06 18:28:38.171259'),(63,'vaccinations','0012_vaccinedose_anchor_policy_and_more','2025-10-06 18:28:45.732764'),(64,'vaccinations','0013_vaccinedose_series_key_vaccinedose_series_seq','2025-10-06 18:28:50.893442'),(65,'vaccinations','0014_fix_influenza_series','2025-10-06 18:28:56.350163'),(66,'vaccinations','0015_patients_encryption','2025-10-06 18:29:00.985465'),(67,'vaccinations','0016_remove_child_child_parent__16983e_idx_and_more','2025-10-06 18:29:06.577662'),(68,'vaccinations','0017_rename_eligible_sex_vaccinedose_eligible_gender_and_more','2025-10-06 18:29:11.791682'),(69,'vaccinations','0018_remove_child_child_clinic__5e8bbe_idx_and_more','2025-10-06 18:29:17.273396'),(70,'vaccinations','0019_add_encrypted_columns','2025-10-06 18:29:22.290603'),(71,'vaccinations','0020_patient_encrypted_columns','2025-10-06 18:29:29.434884'),(72,'vaccinations','0021_merge_20251006_1959','2025-10-06 18:29:34.451836'),(73,'vaccinations','0022_child_idx_child_clinic_child_idx_child_dob_and_more','2025-10-06 18:29:42.865374'),(74,'vaccinations','0023_alter_doctor_options','2025-10-06 18:29:49.165038'),(75,'vaccinations','0024_alter_doctor_options','2025-10-06 18:30:04.867249'),(76,'vaccinations','0025_alter_doctor_options','2025-10-06 18:30:09.825669'),(77,'vaccinations','0026_parent_created_at_alter_child_created_at','2025-10-06 18:30:14.286863'),(78,'vaccinations','0027_auto','2025-10-06 18:30:18.549160'),(79,'vaccinations','0028_rename_vaccinations_child_id_idx_child_share_child_i_a28a1d_idx_and_more','2025-10-06 18:42:58.793074');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('14ocgnjbp49mi2ucksxuq6xx73ka9wxz','.eJxVj8tOwzAQRf_F6yhynJedFaqgC6TCByAUOZ5JbdraaeyA2qr_jg2VKMu5jzO6F9LLJeh-8Tj3BkhHGMnutUGqHdpkwIe0W5crZ8NshjxF8pvr840D3K9u2X8ALb2O7bphnFNAxhkWo2zLEVEpChI4FQCiqFVVNgOtOIyocEDWNmLktObQtJWqIhScCm7-QZPuQoKLzyL59Gk28jy8rHfn9XHpGT5aeHrVR_x6nixH9tdM-4oyI3iQZp8WaRdwMqfFa1o_bJMa5x3INSOTnNGG34a4Oz3p3grxfv0GlAtouQ:1vDGvj:M7Z8-ZFknUyOgIRX2BZpa_tLgfwiIOm7b0n1bvnz-N4','2025-11-10 06:42:11.217754'),('1qzb4hf2x6kpv6qbplk7z1rs8e9wy0e8','.eJxVj82OgjAUhd-la4cUhFJcqZlMZhZu1IVxQ257bymoNEKJJsZ3txgTne35-U7OjZUweFsOPXVljWzGBJt8agr0gdrRwAbaykXatb6rVTRGopfbRyuHdFy-sv8AFnob2plIpORIiUwoNpBPDZHWHAElLxCLONPpVCieSjSkSVGSi8JInkkUearTAEWnveueaDa7Me_CWCDTfhFXf7ufCjbNWVz2wJuvzdacf78PwxXW5bs5_osnjE5QH0NRWeh8jdZ5kvNqFMO5E7vfH9VJXLs:1v5pIG:j0pHQ1H4wrnrz16oj45acbluAUCVSByU8wCHfCRivhM','2025-10-20 17:46:40.723695'),('2k7t8n49whvnmyhnho75wx35gnb7uxma','.eJxVjMEOwiAQRP-Fs2lY6Crt0btfYAxZWJBqA6bUk_HfbU0T43HmvZmXeNAU8mwHFj10u1-soj9Dd9kJyj6VKbD1aRjZcqlhwwZx4Zaec7LPGqbvidDir3Pk7yGvgG-Ur6XxJc_T4JpVaTZam1PhMB439-8gUU3LOnZtC_4AGrQyTMZrMgGk04gSFLKT3EYk1NIheqVxb6QCFSVEUmEfxfsDYkhM_g:1vE9L0:V-S7xN3Wz-hIYInvKtNYmdGa4Vu8pRm3JcWW72vYfe4','2025-11-12 16:47:54.428611'),('48mf4v2zjo3jaug2d7wns8k93sl9i8ah','e30:1vCYFK:8O_oURr0XnNzBqoaYz_GkGOWgehGk0kqLDSpX6De9sE','2025-11-08 06:59:26.688065'),('4exub72ub9ugeyofzqxka6etanfi1jgb','.eJyFj7FuwjAURf_Fa0tsIkKIt4JaQKpKVMJAl8g8u9hKYqfOSyBC_HuN1L3bHc450r0RJ3rUZYcCFeE38jdIru3-q2rf3csy_978HMbtAVu_K47redHl44o8E-kAnS_RVcoGo2Gvb_o4ZB9Zdhm3Q2P0FTefswZOa0j3uz4YVl0xkFTS_2AqpKTB8EoarwDL3ptgasSWU2rVZRAAxqoIWmks1MYaiMBFxtLHH3p27lwrCqKuTwKqRwq7EIhZnEymbBKnBZvz6YLHWZQsZglLnxjjjJH7_RfJY1om:1vDGYn:XvkPlwuJEt57nSw4qZyGfvfGp_scghlMgRhgp_zsPDA','2025-11-10 06:18:29.635554'),('6gzjsiihn3zk81ikpbt9bamo3wwcak70','.eJyFj1FPwjAURv9LX3Xr7bAS-iZCYoKQGSE0vCzlrrK6ph3bRYmE_25JfPftezjnJN-FRXOiphrIkGXqwv4Gwx89fjuX7yCHbNM96-ML0KLVYbcyq1gsNbtndUSKfUWxtSEZ22a9h9fPYuonH7P5rIjky-XTot11043UxzIZwZ4pkbzm_8E80b2tXW-RqlPvktUQdYrzYL-_DKILNseudgG9Cw5zjLkL_PaFH2I8eMvReL832N5SNKRAAYXMhMhgtBagxESJcf4oH4QUdwAKgF2vv8aKVok:1vFref:-dQsF36sYDx-ChDeuAq5ofhz_Ne4pwWc5TvGd37hYhw','2025-11-17 10:19:17.706558'),('7jamg5lqyuiulqoaakhzv4ax97t1rvfu','.eJyrVipILErNK4nPTFGyMrTUQXCLlayiDS1jdZQS85Iz8otSU-KTMzJzUuJT8otTodIWlhaxtQD74Bbn:1vEL19:4jT-aHPtJZ9IgFr6QzuHl4BWgxnHMJz_sKXTU7ekZdg','2025-11-13 05:16:11.386949'),('7viy7dntes1zv88z9cofgsx7o03wt0jt','.eJyFj7FuwjAURf_FKyV-cVICXlOhMKC2NEIti2VeTGJh7MhxaFXEv9eRurPd4Zyre2_EyTF0YggyKMJv5D-Q07q-XD7aYV2vXsrqrR43Zenepbhud32fVQfyRBqHwXkR3FnZaLBWfH7Vxxxe9-kWh31nfxf5ziwPHgpzWlXRsOonRJI29BFMI-1Vo73CIEavo9WF0HNKrfq-SkRtVYJ9oy0abTUm6BJt6fSFts61RlGUxhwlnqeqMEwDgT3PU5izok4zzhYcigRYxvLlDIADkPv9D8QmVm0:1vDNEd:6rSWA8O5dE8qK5eieeq-bapt6nN8Xhuyq2yYF5PCTlI','2025-11-10 13:26:07.075624'),('8mqoc58zhj7urmft5iz5p5l818zjw4vy','e30:1vMW22:9Pa8nrgW_t1utE6HiLbN9tMg4BuHIAg7prD2GEHnKsI','2025-12-05 18:38:54.206711'),('8tz018bwwz4bio2b5bzq70fj07mai9wu','.eJyFj8tuwjAQRf_F20I8BEiwd636AFGViiK1XUVmYmGXxE7NJFAQ_46R2Hd3F-cc6Z6YVy2ZYkeKNJMndhvMj48L-9CsHt10-DWin_tXF_T83Xyq38lsMu9Yj5UeyYeC_Fa7aNTw9Gy-O_EmxP5v1tXWHGi6HNW4fsH8Y9FGw-kDRZKX_D-YRzro0gaNVLTBRssQNZJzp_edQrROJ9iU1mFlncUEfWIdv37hG-83leaoqmqtcHtN0S4GUkjH_QH003wFmRxkEvJkKEQG4g5AArDz-QLjx1hR:1vDGWV:PHzprmLdikVAGkkoJDzSmIngE_GR357ZES03KZQxlRk','2025-11-10 06:16:07.475433'),('97hsnp2o2zijq2y7zvko6kx3dkf3zvk0','.eJyFj02PgjAURf9Lt460VgXbfWfUGJkPFqMbUh8NNEJL4IFOjP99SjL72d3FuSf3PojXA1Z5jxoNkQ_yF0iVbs7qdG4P2Gd7pS3n32XWfGwHvlap2ryTF1J4QN_l6K_GhUbD1Gt1GsVRiNvPbmxsdcft56qByxskX-kQGs7cMZC0oP_BNNCdKWxnAPOhs9MixFZS6sxt1ADWmQjawjqorbMQgY-so9MXWnpf1oaCruuLhuukwj4IOOPr-YLNeZKxWC5iyZJoJZYijmeMScbI8_kLWRlXsg:1vDGWV:Tj8MuiLE28qDOInxhMHYzLTg6Efh_5qGpqBA4hykBmQ','2025-11-10 06:16:07.608982'),('9chr5l7vbp94u1jdazl7m8ef7u5wpee4','.eJwtjstOwzAURP_FW2h8676U7CqFAEKURwtSu4ncG6s2dezg3qSBqv-OIyHNYhZzZubCvGxJlyeSpFh2Yf-G6Y3tmk-dFsF9rIqvp-nv8vU7X-7e8rbPi_Uzu2WVR_KhJH9ULhI13BV626WrND3_PHa10T09vE9r3N_jYv3SRsKpnmKSRxtUZYJCKttghjmiJuPcqXMnEY1TCTaVcWiNM5igT4zjw1F-8P5gFUdp7V7icaiiUywQIGajMYzEYgPzTIioZDaB-WR8A5ABsOv1DzfOTGc:1vDGcY:atOhT_FnS7GXwtK_4X6y7WDbp_6Bzi8ALpSOO7s9pvE','2025-11-10 06:22:22.585077'),('9wpiwtnf16ic1b55d8lnwtrmbc8g828a','.eJxVjsEOwiAQRP-Fc9Ow0K3Uo3e_wDRkYUGqBkypJ-O_a00Pepx5M5N5CkuPJdlHDbOdWOyFFs2v58hfQ14BXyifS-tLXubJtWuk3Whtj4XD7bBl_wYS1fRpx6HrwO9Ag1aGyXhNJoB0GlGCQnaSu4iEWjpErzT2RipQUUIkFfr4Gb3THPLyfQnDj6xif4JhbARln8oc2Po03dhyqWHDBvvx9QZ3PEz_:1vELMM:jhvikcIvU089vxpCo8AGhl-HzmrYdJEsig3XhtHhQvY','2025-11-13 05:38:06.244967'),('9xzwumdepsg6t13qown5q63kp3ypxi2c','.eJyFj81SwjAURt8lW6W5DVYn2VHQhT8jQ0GETSe9TWlsJqnlgo4M726Yce_uW5xzZr4TC_pAbbknTYapE_sbbPEKP_Jhctds3gqT63I9Xcib7LEojra6baaGXbM6IIWhpNAZH411u6zg-UPkTjaz-5kI5OYvk6du2-er7P1zHg1vvimSvOb_wTzSg6ntYJDKw2Cj1RL1inNvvo4a0XqTYF9bj856iwmGxHp--cJ3Ieyc4aidqzR2lxTtY0CAyEZpOoLxMgWVSgUiARiDFFcACoCdz78yp1Xc:1vFreQ:4BGAoi0-uxwfKEzaFL058VhGx3OyhzYpVazz32X953Y','2025-11-17 10:19:02.055861'),('9y7yqxaqo7j289p51cs7qtvf60jfl9a5','.eJyFj8GKwjAURf8l25k2sTVWsxsZqMOAxTqKuxJfQ31tTSQ-HYv47xNh9u7u4pwD986cvtChOpMmw9Sd_Q-WFePyc6vz4_x7gUW7bW9d0xUl5n56tKnI2TurHZDzFbnO2GBsZrAaPsrrUNDuq4LML5u12CzacjXgfBklwbDmRoHkNX8F80B7U6M3QNXFY7AORCfFuTW_Vw2A1sRwqtFCjxYhBhej5c8vvHGu6Q0H3fd7Dd0zRecQSEQio5GIkuxnlKqxVGISSynT2fRNCCUEezz-ADEFVzc:1vEQso:Ba2rS2a4PMNUAtaOr6aLoKSo6WknC5khoaPqlSOWHYo','2025-11-13 11:31:58.915503'),('af6kygnzuede6610oorf6e9np1zriap0','.eJyFj71OwzAURt_FK03sWklDslUIShlAFIraKXKuTWwlsSPn5gdVfXdciZ3tG8450nchToyoywEFKlJcyN8g2_48vp9O31k9N4cHWe22_Cvde67Z8DIt0ZGsiHSAzpfoGmWD0bHHJ32e8tc8n3_2U2f0gs-HpINqB9nH2xgMqxYMJJX0P5gKKWkwvJLGK8By9CaYGrEvKLVqngSAsSqGXhoLrbEGYnCxsfT2h9bO1a2iINq2EtDcUjiEAGc8jdYs4tkn2xTr-yLN4k2WJ3lyx1jBGLlefwEpclmA:1vDGZF:cmrb_rR1oeVBQ-uFu8jEaTFywl0GZK-Ll9K3cVTHucE','2025-11-10 06:18:57.730630'),('b3uys3rxq3asx562wca77gyozudfnrf0','.eJyFj8tuwjAQRf_F2zbx2FEKeBcEoqhFAokCYhOZiUNMXDsNQx9C_HuN1H13d3HOke6VBX2hpjyTJsPUlf0NVsy82BjYberVqIZTMh8Mn1dDOS_8YCF_9u_skVUBKfQlhdb4aGyb9QFeT3LsRvVkOpGB3HJRvLT7bvyW7z6W0fDmmyLJK_4fzCPdm8r2Bqm89DZaDVGnOPfm61MjWm9S7Crr0VlvMcWQWs_vX_gxhKMzHLVzB43tPUXnGJAg80SIBLK1ACWelMhSIWSeiQcABcBut1-0w1VM:1vFrbh:n-E_GGFfP2hogt6b6bwabHhJEzUbswA0_YBX1B9i3l0','2025-11-17 10:16:13.167302'),('bg61dbsh7s5rktk3pzxn96nrfxtz626t','.eJyFj7FuwjAURf_FK03sBJxQb1SKYEGtEKItS-Q8m8TFshPnUSoQ_15H6t7tDudc3XsnXl6wq0eUqIm4k79AvjZVGPqhaPXL23o1rHZ8W94alVTV6bh-D1fyRJQH9KFGf9YuGnlbf3zumwV7PWRbGA-duxWLnV0eAyvt6XkTDad_MJJU0f9gGumglQkasL4EE60OsReUOn39lgDG6RR6ZRxY4wyk4FPj6PSFtt63VlOQ1jYSzlMVjtNAlvMkY0le7rO5yLngPF1mBcv4jDHBGHk8fgG9BlZo:1vDNER:8gTPgCf2mhZuiNIp0V3s56cYysRIXA-Hgpgvhi6d-6M','2025-11-10 13:25:55.959105'),('ea22c43j9vd37ztur9bvp72qcve3fl23','.eJxVjEEOwiAQRe_C2hCGYSq6dO8ZmoEBqRpISrsy3l2bdKHb_977LzXyupRx7WkeJ1FnherwuwWOj1Q3IHeut6Zjq8s8Bb0peqddX5uk52V3_w4K9_Kt88k5iEdAQOuFfUT2CUxAIgOWJBhxmZjQBKJokQZvLNhsILNNQ1bvD73ANus:1v5zh6:yij24w6Jq5sxLIPw7ZnSK7MtghANPy5H-3TbmyCMhkI','2025-10-21 04:53:00.712238'),('eupcsdqcyl62nt6yjmpgovba4zv626j9','eyJwYXJlbnRfaWQiOjE5LCJwYXJlbnRfaWRzIjpbMTldfQ:1vDM70:XN5PDD_Vu9o04zUrO0ffi9iPiXtTFFG_YTYf01op72k','2025-11-10 12:14:10.568169'),('gb0ttzru9xhjurumg4jr66qkbaxreitn','.eJyFj7FOwzAURf_FKzS2Q0yCRyZEVSghVIXFcl9MYsWyK-clRa367zgSO9sdzrm690KCnrBXI2o0RF7IXyD1Y32GqlHTaT1sRfgY41zM7-XLevNWF932mdySNgCGqDAMxicj79T-szkU7HXHNzDuen--L2pXfUVWuu-Hp2R484OJpC39D6aJjqa10QCqKdpk9YhHSak3p1kDWG8yOLbWg7PeQgYhs54uX2gXQucMBe3cQcOwVOG4DGS5WHG2ysuG38lcSCGyipcVFzeMScbI9foL0upWhQ:1vDNER:V3I45jPFwRWrAE0kyi2Cozvf3EWfd1RgIMpsMI8Xbb0','2025-11-10 13:25:55.961630'),('hroul2ilmd3uygkk1qw6lolgdkkt5wo5','.eJxVj8tOwzAQRf_F6yiyndckK9RdhQAJsSpCke0Z14EmRo6TBVX_HQcqUZZzH2d0z6xXS3T9MlPoB2QdE5Jlt6JW5oOmzcF3NR19bvwUw6DzLZJf3Tl_8Ein3TX7D-DU7FK7qiUAR5IgSVjVFJbIGI4KgbeIrahMWdSal4CWDGmSTd1a4BVg3ZSmTFD0Jvrwg2bdmUWfniXyPT7zw359CcW6Ph1487gasqBsWy0j33-Jv-Y2UPCM0aiGU2pqp0Ic0PlIcHfcxLRuZJeMfapAU_wtwM05s-5VwNvlG-zZZ2E:1vA8EA:vlurNlt1nZtJLSwSVXgYmdIYTN9yYD0VERdUomCGLB4','2025-11-01 14:48:14.876313'),('j9h5xii1wub4rsl5dx5ebaz1bqlwz5a6','e30:1vLQ9P:gd93P6mnNQfafVqdC3s1FdYnxTma9v7KG5A9fx8GS5w','2025-12-02 18:09:59.766608'),('k1v7gah8qzwx9g476zgl88l47jca2u5w','e30:1v8mKQ:5rywD01Ir_G_vozlMYHI60NA66nRMKDpDI-9De0-Yww','2025-10-28 21:13:06.454623'),('k5kuyfy8ixgyqwh6tqvskkzf19wcvp9q','e30:1vAlnX:Jlwp8IoeUFsQwfQXR4xqM-wOLkAajLQQUU1TqEZG2T8','2025-11-03 09:03:23.130819'),('l9nlhzkz2lqa0ofqlcs915wjcyyqfslp','.eJyFj71OwzAYRd_FKyT-oSaJN7ZKFQKhYgGL5XwxiVtjF9uFQNV3x5HYu93hnKt7TyjoY55UyjobJE7oPyAtk-s-5jb1cq1280_33CjvP6e7jaweKU_oGg0Bcogqh73xxWCjennd9ivyIOk9JDn539vVk2vfImnce7cuhjdzLiQe8CUYFzqawUYDWR2jLdaU80Fg7M33lwaw3tRwGKwHZ72FGkJtPV6-4DGE0RkM2rlew36pymkZSBivKKlYs6U3gnHBed3ShtH2ihBBCDqf_wATXVbG:1vDNER:tL9IpX7TTYFSbObkaWT7MmAcjfUVd9tvI49Bm8IjZBU','2025-11-10 13:25:55.961790'),('mbltozorb5rf3noguotnmp4f4c97vci8','.eJyFj8tOwzAURP_FW2h8Y-KUeAcbKhVEQaE8NpF74yYmlh0ltw9R9d_rSN2zm8U5o5kTC3pHbTWSJsPUiV0Dez4s--0blmRg3znZZrB6ehQPi-OHWOXLz192y-qAFIaKQmd8NERTfX2Xmwxe1-kLjuvW_-XZu7v_GWDutsUiGt4cKZK85v_BPNKDqe1gkKrdYKPVEvWKc28Oe41ovUmwr61HZ73FBENiPZ--8CaExhmO2rmNxm6qonEaCELOUpiJeZneKSGVlEmRF1KkNwAKgJ3PF2VKVgk:1vDNES:JlOuuldXFULNT8kfPxBKQviEJq_CoQyo3dth_lckFNs','2025-11-10 13:25:56.023801'),('mtbjr446y8spc3z5nrswzxcmnoxvjecr','.eJxVj01rg0AQhv_Lnq2sGz9WT2lOzSEpSQkUSpFxZ9TV6JZ1DUjIf6-GQNPjvB_P8F5ZDqOr83Egm2tkGYuY96wVoFrqFwMb6CvjK9M7qwt_ifgPd_B3Bum8eWT_AWoY6gUbCyk5kpCCghKSVUmkFEdAyVPENIhUuIoLHkosSVFBIonTUvJIYpyEKpyhaJQz9o5m2ZU5Mz-byadUHabX42V6d5_bXCV2X33w01tzPEx6s38Rf81lXxB5jDrQ57l50a2FroUexkZPECfranHmiR27eewHLPXu3hLB0zmw7EsE37df2T1pNQ:1vDNV0:BX5Z4s3QKIbNJcjWjE9TvtIHgD2wlbUJRIZxdmCCUyQ','2025-11-10 13:43:02.657462'),('orx92icd2paav64spr4dy5pafjsny89w','eyJwYXJlbnRfaWQiOjE5LCJwYXJlbnRfaWRzIjpbMTldfQ:1vDM1i:NxbOqWFtFdV8E-FpWZ9Bbrt_ICW1dHAPkCbp1rrP-Fc','2025-11-10 12:08:42.039371'),('oxza3h3m46g5x5qkrckvuf0er3we49y1','e30:1vQyk8:2hD1eAZoOahaHz9K0ALRMAtEn1u0eGVLNKOmc-M6XKM','2025-12-18 02:06:52.819074'),('pfk9c5ze731yjlpfey9ogblgh8ex2yvu','e30:1vDLKh:TjNKccG_MuVIPnCfQqLkJWSYx3ZUkJKHKR8oE5EGfUk','2025-11-10 11:24:15.975955'),('rdh9j543fhk5tjkfc5vs1eazp2cih7pq','.eJyFj8tuwjAQRf_F25L4QUoS79oFtEIi4iW1q8hMrDBNZFMzQAPi32uk7ru7i3OOdG_MmxPt6yMZskzf2N9gxRWn-Rw_s5Ar6We2-u7mWXkZZtV0h1mXsRFrPJAPNfnOumhsS1gOL6vzUNHHew15WLRrsX37Wi0HfF0kKhrO_lAkecP_g3mkg20wWKD6FDBae6KD5tzZy9kAoLMpHBp00KNDSMGn6PjjC2-9b3vLwfT9zkD3SNExBpRQz4kUico3cqzHhZYynchiIsonIbQQ7H7_BeH_VtY:1vDNQJ:fBPozLizZddaOzXIY2_wnWGjpCWj8wMUk7wuO0y6xik','2025-11-10 13:38:11.669629'),('rhtc7ppip067oiirvidpzp9maq1c0xdh','e30:1vDbpD:iG4uDqQZEJPgzLNcyza0fTioOR0-Q_C6EJBS3O77_Qo','2025-11-11 05:00:51.452500'),('sqx52w2j1hvqhg789pw4f3i9mrj1e4wb','e30:1vDGly:HyjLiARtKavMF5-8zsjFm4c-NI1QSe1rOoGRAWOoA6g','2025-11-10 06:32:06.451870'),('tt6ik4mifaxastkyy6v6wyzjaoy2h9qc','.eJyFj1FPwjAURv9LX5W1nXXL-maMwIyBREmIT8u4u66VrsVxt2EI_92S-M7b93DOSb4zC_VApjpSTcj0mf0P9lAO9Pq2Ktv5z2JTUfv9_JXh2rinabndgkJ2z5oAFPqKwh59NDrxMjefY7Eqium3HDtrTrR8Vx3sFpB_rIdoeDxRJHnDb8E80j02tkegauhttAzRQXPucRprAOsxgUNjPTjrLSQQEuv59QtvQ2gdcqid29Wwv6boGAOpSB9nUszSfCMyLTMt8kQpKZW8E0ILwS6XP_NeWFE:1vDGWV:SHduxjdWulW7QT__RzHQsWESHRNAY-3-72tB-d-UVPE','2025-11-10 06:16:07.585772'),('ujzyy2b75thbyaolp6638d1te23hhg3m','.eJyFj1FPgzAURv9LXxVaCIPQNxMVZ8xQpyZ7IuXSrA1wS7oLmy7773aJ7759D-ec5Dszp2YyzYEUaSbP7G-wFn1ttHqdnn_w862Ce_yqq7t-Z1bb6IXWG3bLOgfkfEOu1xiMUTw8mt1Sbsry-L1eRmtO9PSejdBWUGzrORioTxRI3vH_YB5orzvrNVAzexssQzRJzlEfFwVgUccwdRZhsGghBhdb5NcvfO_cftAc1DC0Cvprig4hkIp0FSUiSosPkcskl6KIsywp8_RGCCkEu1x-ARQNWHQ:1vDGWV:EY4jbBp7vd8eyPgDOfCSEVNxebx6niGiIZvx2kW-iv8','2025-11-10 06:16:07.587556'),('w5n23vw9x52u747rqf8srisnxudrwh2y','.eJyrVipILErNK4nPTFGyMrTUQXCLlayiDS1jdZQS85Iz8otSU-KTMzJzUuJT8otTodKWBoaxtQD7rBbY:1vDMeg:VOnjwFBNOCnTT60af7HnAQ6ORHSl-4D1-ta-tICxrgg','2025-11-10 12:48:58.740502'),('wl3q5198izz4oiebuirzbq0yucqwx24w','e30:1vGxwK:kP4tSHCWTgcYMAwMYlio9qy0q9h11iueLyH_aae5Kh0','2025-11-20 11:14:04.870956'),('zqcu2o2svqxv0vhonqe0g4pj032ax2zt','.eJxVj71OwzAUhd_FcxXZbuI4nWhUJqjUAQRiia59rxu3TgyJO1V9dxxUCVjPz3d0rqyDS-q7y0xT55FtWM1WfzUD9kzjYuAJxmMsbBzT5E2xRIq7Oxf7iBTae_YfoIe5z-1KSa05ktSShIN67Yis5QioeYPYiMqWa2V4qdGRJUOyVo3TvNKo6tKWGYrRpjj9oNnmylLMY5n81r8Y_nySbWjc7nEnYwqH_fbp_PHZvlbvX4ff5vJPqBWjAXzIzdkPU_4EAUYvxMNxkfO_gd1u37uhXNc:1vFrlW:DlpgEI9nHWnCTPqbI63ZBcpVyh32Jp7dswXIgH_nXOQ','2025-11-17 10:26:22.345418');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `whatsapp_e164` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `imc_number` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `photo` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `portal_token` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `clinic_id` bigint NOT NULL,
  `partner_id` bigint DEFAULT NULL,
  `field_rep_id` bigint DEFAULT NULL,
  `google_sub` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `last_login_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `imc_number` (`imc_number`),
  UNIQUE KEY `portal_token` (`portal_token`),
  UNIQUE KEY `google_sub` (`google_sub`),
  KEY `doctor_clinic__492837_idx` (`clinic_id`),
  KEY `doctor_partner_ca8c50_idx` (`partner_id`),
  KEY `doctor_field_r_49986a_idx` (`field_rep_id`),
  CONSTRAINT `doctor_clinic_id_310ac0ea_fk_clinic_id` FOREIGN KEY (`clinic_id`) REFERENCES `clinic` (`id`),
  CONSTRAINT `doctor_field_rep_id_9bb3d838_fk_field_representative_id` FOREIGN KEY (`field_rep_id`) REFERENCES `field_representative` (`id`),
  CONSTRAINT `doctor_partner_id_14377957_fk_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `partner` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor_session_token`
--

DROP TABLE IF EXISTS `doctor_session_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor_session_token` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `user_agent_hash` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `revoked` tinyint(1) NOT NULL,
  `doctor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`),
  KEY `doctor_sess_doctor__e7a0d8_idx` (`doctor_id`,`expires_at`),
  CONSTRAINT `doctor_session_token_doctor_id_93dba051_fk_doctor_id` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor_session_token`
--

LOCK TABLES `doctor_session_token` WRITE;
/*!40000 ALTER TABLE `doctor_session_token` DISABLE KEYS */;
/*!40000 ALTER TABLE `doctor_session_token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `field_representative`
--

DROP TABLE IF EXISTS `field_representative`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `field_representative` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rep_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `partner_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `field_representative_partner_id_rep_code_57bdb0bf_uniq` (`partner_id`,`rep_code`),
  KEY `field_repre_partner_e85b40_idx` (`partner_id`,`rep_code`),
  CONSTRAINT `field_representative_partner_id_6dca4029_fk_partner_id` FOREIGN KEY (`partner_id`) REFERENCES `partner` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `field_representative`
--

LOCK TABLES `field_representative` WRITE;
/*!40000 ALTER TABLE `field_representative` DISABLE KEYS */;
/*!40000 ALTER TABLE `field_representative` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oauth_state`
--

DROP TABLE IF EXISTS `oauth_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oauth_state` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `state` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `doctor_token` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `next_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `expires_at` datetime(6) NOT NULL,
  `redirect_uri` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `state` (`state`),
  KEY `oauth_state_state_0354d4_idx` (`state`,`expires_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oauth_state`
--

LOCK TABLES `oauth_state` WRITE;
/*!40000 ALTER TABLE `oauth_state` DISABLE KEYS */;
/*!40000 ALTER TABLE `oauth_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parent`
--

DROP TABLE IF EXISTS `parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `whatsapp_e164_enc` longblob,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parent`
--

LOCK TABLES `parent` WRITE;
/*!40000 ALTER TABLE `parent` DISABLE KEYS */;
INSERT INTO `parent` VALUES (1,NULL),(2,NULL),(3,NULL);
/*!40000 ALTER TABLE `parent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `partner`
--

DROP TABLE IF EXISTS `partner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `partner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `slug` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `registration_token` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `slug` (`slug`),
  UNIQUE KEY `registration_token` (`registration_token`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner`
--

LOCK TABLES `partner` WRITE;
/*!40000 ALTER TABLE `partner` DISABLE KEYS */;
/*!40000 ALTER TABLE `partner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule_version`
--

DROP TABLE IF EXISTS `schedule_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule_version` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `source_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `effective_from` date DEFAULT NULL,
  `is_current` tinyint(1) DEFAULT '0',
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_version`
--

LOCK TABLES `schedule_version` WRITE;
/*!40000 ALTER TABLE `schedule_version` DISABLE KEYS */;
INSERT INTO `schedule_version` VALUES (1,'IAP-2025-EXACT','Indian Academy of Pediatrics 2025 - Exact Schedule','https://iapindia.org/',NULL,1,'2025-10-07 05:59:15.158623');
/*!40000 ALTER TABLE `schedule_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ui_string`
--

DROP TABLE IF EXISTS `ui_string`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ui_string` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `key` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key` (`key`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ui_string`
--

LOCK TABLES `ui_string` WRITE;
/*!40000 ALTER TABLE `ui_string` DISABLE KEYS */;
INSERT INTO `ui_string` VALUES (1,'history.title','Page title'),(2,'history.note','Top note'),(3,'btn.update_due','Update button'),(4,'btn.add_child','Add child button'),(5,'btn.back','Back button'),(6,'th.vaccine','Table header'),(7,'th.status','Table header'),(8,'th.action','Table header'),(9,'btn.call_clinic','Call button'),(10,'lbl.given_on','Given label'),(11,'lbl.due_on','Due label'),(12,'status.given','Status given'),(13,'status.pending','Status pending'),(14,'edu.title','Education title'),(15,'edu.lead','Education lead'),(16,'csv.child_name','CSV header'),(17,'csv.date_of_birth','CSV header'),(18,'csv.gender','CSV header');
/*!40000 ALTER TABLE `ui_string` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ui_string_translation`
--

DROP TABLE IF EXISTS `ui_string_translation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ui_string_translation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `language` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `ui_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ui_string_translation_ui_id_language_a3db45a3_uniq` (`ui_id`,`language`),
  KEY `ui_string_translation_language_3cfcab59` (`language`),
  CONSTRAINT `ui_string_translation_ui_id_45d1e3b8_fk_ui_string_id` FOREIGN KEY (`ui_id`) REFERENCES `ui_string` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ui_string_translation`
--

LOCK TABLES `ui_string_translation` WRITE;
/*!40000 ALTER TABLE `ui_string_translation` DISABLE KEYS */;
INSERT INTO `ui_string_translation` VALUES (1,'en','Vaccination History',1),(2,'hi','αñƒαÑÇαñòαñ╛αñòαñ░αñú αñçαññαñ┐αñ╣αñ╛αñ╕',1),(3,'bn','αªƒαª┐αªòαª╛αªªαª╛αª¿ αªçαªñαª┐αª╣αª╛αª╕',1),(4,'ml','α┤╡α┤╛α┤òα╡ìα┤╕α┤┐α┤¿α╡çα┤╖α╡╗ α┤Üα┤░α┤┐α┤ñα╡ìα┤░α┤é',1),(5,'ta','α«ñα«ƒα»üα«¬α»ìα«¬α»éα«Üα«┐ α«╡α«░α«▓α«╛α«▒α»ü',1),(6,'te','α░╡α▒ìα░»α░╛α░òα▒ìα░╕α░┐α░¿α▒çα░╖α░¿α▒ì α░Üα░░α░┐α░ñα▒ìα░░',1),(7,'mr','αñ▓αñ╕αÑÇαñòαñ░αñú αñçαññαñ┐αñ╣αñ╛αñ╕',1),(8,'kn','α▓▓α▓╕α▓┐α▓òα│å α▓çα▓ñα▓┐α▓╣α▓╛α▓╕',1),(9,'en','If this is your first visit, click \"Update Due Date\" to enter the doses already given. Once done, only pending vaccines will remain.',2),(10,'hi','αñ»αñªαñ┐ αñ»αñ╣ αñåαñ¬αñòαÑÇ αñ¬αñ╣αñ▓αÑÇ αñ»αñ╛αññαÑìαñ░αñ╛ αñ╣αÑê, αññαÑï αñ¬αñ╣αñ▓αÑç αñ╕αÑç αñªαÑÇ αñùαñê αñûαÑüαñ░αñ╛αñò αñªαñ░αÑìαñ£ αñòαñ░αñ¿αÑç αñòαÑç αñ▓αñ┐αñÅ \"αñ¿αñ┐αñ»αññ αññαñ╛αñ░αÑÇαñû αñàαñ¬αñíαÑçαñƒ αñòαñ░αÑçαñé\" αñ¬αñ░ αñòαÑìαñ▓αñ┐αñò αñòαñ░αÑçαñéαÑñ αñÅαñò αñ¼αñ╛αñ░ αñ╣αÑï αñ£αñ╛αñ¿αÑç αñ¬αñ░, αñòαÑçαñ╡αñ▓ αñ▓αñéαñ¼αñ┐αññ αñƒαÑÇαñòαÑç αñ╣αÑÇ αñ░αñ╣ αñ£αñ╛αñÅαñéαñùαÑçαÑñ',2),(11,'bn','αªÅαªƒαª┐ αª»αªªαª┐ αªåαª¬αª¿αª╛αª░ αª¬αºìαª░αªÑαª« αª¡αª┐αª£αª┐αªƒ αª╣αª»αª╝, αªñαª╛αª╣αª▓αºç αªçαªñαª┐αª«αªºαºìαª»αºç αªªαºçαªôαª»αª╝αª╛ αªíαºïαª£αªùαºüαª▓αª┐ αª¬αºìαª░αª¼αºçαª╢ αªòαª░αªñαºç \"αª¿αª┐αª░αºìαªºαª╛αª░αª┐αªñ αªñαª╛αª░αª┐αªû αªåαª¬αªíαºçαªƒ αªòαª░αºüαª¿\" αªòαºìαª▓αª┐αªò αªòαª░αºüαª¿αÑñ αªÅαªòαª¼αª╛αª░ αª╕αª«αºìαª¬αª¿αºìαª¿ αª╣αª▓αºç, αª╢αºüαªºαºüαª«αª╛αªñαºìαª░ αª¼αª╛αªòαª┐ αªƒαª┐αªòαª╛αªùαºüαª▓αª┐ αªÑαª╛αªòαª¼αºçαÑñ',2),(12,'ml','α┤çα┤ñα╡ì α┤¿α┤┐α┤Öα╡ìα┤Öα┤│α╡üα┤ƒα╡å α┤åα┤ªα╡ìα┤» α┤╕α┤¿α╡ìα┤ªα╡╝α┤╢α┤¿α┤«α┤╛α┤úα╡åα┤Öα╡ìα┤òα┤┐α╡╜, α┤çα┤ñα┤┐α┤¿α┤òα┤é α┤¿α╡╜α┤òα┤┐α┤» α┤íα╡ïα┤╕α╡üα┤òα╡╛ α┤Äα╡╗α┤ƒα╡ìα┤░α┤┐ α┤Üα╡åα┤»α╡ìα┤»α┤╛α╡╗ \"α┤¿α┤┐α┤╢α╡ìα┤Üα┤┐α┤ñ α┤ñα╡Çα┤»α┤ñα┤┐ α┤àα┤¬α╡ìα┤íα╡çα┤▒α╡ìα┤▒α╡ì α┤Üα╡åα┤»α╡ìα┤»α╡üα┤ò\" α┤òα╡ìα┤▓α┤┐α┤òα╡ìα┤òα╡ì α┤Üα╡åα┤»α╡ìα┤»α╡üα┤ò. α┤¬α╡éα╡╝α┤ñα╡ìα┤ñα┤┐α┤»α┤╛α┤»α┤╛α╡╜, α┤¼α┤╛α┤òα╡ìα┤òα┤┐α┤»α╡üα┤│α╡ìα┤│ α┤╡α┤╛α┤òα╡ìα┤╕α┤┐α┤¿α╡üα┤òα╡╛ α┤«α┤╛α┤ñα╡ìα┤░α┤é α┤àα┤╡α┤╢α╡çα┤╖α┤┐α┤òα╡ìα┤òα╡üα┤éαÑñ',2),(13,'ta','α«çα«ñα»ü α«ëα«Öα»ìα«òα«│α»ì α««α»üα«ñα«▓α»ì α«╡α«░α»üα«òα»êα«»α«╛α«ò α«çα«░α»üα«¿α»ìα«ñα«╛α«▓α»ì, α«Åα«▒α»ìα«òα«⌐α«╡α»ç α«òα»èα«ƒα»üα«òα»ìα«òα«¬α»ìα«¬α«ƒα»ìα«ƒ α«ƒα»ïα«╕α»ìα«òα«│α»ê α«ëα«│α»ìα«│α«┐α«ƒ \"α«¿α«┐α«░α»ìαñºα«╛α«░αñ┐αññ α«ñα»çα«ñα«┐α«»α»ê α«¬α»üα«ñα»üα«¬α»ìα«¬α«┐α«òα»ìα«òα«╡α»üα««α»ì\" α«Äα«⌐α»ìα«¬α«ñα»ê α«òα«┐α«│α«┐α«òα»ì α«Üα»åα«»α»ìα«»α«╡α»üα««α»ì. α««α»üα«ƒα«┐α«¿α»ìα«ñα«ñα»üα««α»ì, α«¿α«┐α«▓α»üα«╡α»êα«»α«┐α«▓α»ì α«ëα«│α»ìα«│ α«ñα«ƒα»üα«¬α»ìα«¬α»éα«Üα«┐α«òα«│α»ì α««α«ƒα»ìα«ƒα»üα««α»ç α«çα«░α»üα«òα»ìα«òα»üα««α»ìαÑñ',2),(14,'te','α░çα░ªα░┐ α░«α▒Ç α░«α▒èα░ªα░ƒα░┐ α░╕α░éα░ªα░░α▒ìα░╢α░¿ α░àα░»α░┐α░ñα▒ç, α░çα░¬α▒ìα░¬α░ƒα░┐α░òα▒ç α░çα░Üα▒ìα░Üα░┐α░¿ α░íα▒ïα░╕α▒ìΓÇîα░▓α░¿α▒ü α░Äα░éα░ƒα░░α▒ì α░Üα▒çα░»α░íα░╛α░¿α░┐α░òα░┐ \"α░¿α░┐α░░α▒ìα░ºα░╛α░░α░┐α░ñ α░ñα▒çα░ªα▒Çα░¿α░┐ α░àα░¬α▒ìΓÇîα░íα▒çα░ƒα▒ì α░Üα▒çα░»α░éα░íα░┐\" α░òα▒ìα░▓α░┐α░òα▒ì α░Üα▒çα░»α░éα░íα░┐. α░¬α▒éα░░α▒ìα░ñα░»α░┐α░¿ α░ñα░░α▒ìα░╡α░╛α░ñ, α░¬α▒åα░éα░íα░┐α░éα░ùα▒ìΓÇîα░▓α▒ï α░ëα░¿α▒ìα░¿ α░╡α▒ìα░»α░╛α░òα▒ìα░╕α░┐α░¿α▒ìΓÇîα░▓α▒ü α░«α░╛α░ñα▒ìα░░α░«α▒ç α░«α░┐α░ùα░┐α░▓α░┐α░¬α▒ïα░ñα░╛α░»α░┐αÑñ',2),(15,'mr','αñ£αñ░ αñ╣αÑÇ αññαÑüαñ«αñÜαÑÇ αñ¬αñ╣αñ┐αñ▓αÑÇ αñ¡αÑçαñƒ αñàαñ╕αÑçαñ▓, αññαñ░ αñåαñºαÑÇαñÜ αñªαñ┐αñ▓αÑçαñ▓αÑç αñíαÑïαñ╕ αñÅαñéαñƒαñ░ αñòαñ░αñúαÑìαñ»αñ╛αñ╕αñ╛αñáαÑÇ \"αñ¿αñ┐αñ░αÑìαñºαñ╛αñ░αñ┐αññ αññαñ╛αñ░αÑÇαñû αñàαñ¬αñíαÑçαñƒ αñòαñ░αñ╛\" αñ╡αñ░ αñòαÑìαñ▓αñ┐αñò αñòαñ░αñ╛. αñ¬αÑéαñ░αÑìαñú αñ¥αñ╛αñ▓αÑìαñ»αñ╛αñ╡αñ░, αñ½αñòαÑìαññ αñ¬αÑìαñ░αñ▓αñéαñ¼αñ┐αññ αñ▓αñ╕αÑÇ αñ░αñ╛αñ╣αññαÑÇαñ▓αÑñ',2),(16,'kn','α▓çα▓ªα│ü α▓¿α▓┐α▓«α│ìα▓« α▓«α│èα▓ªα▓▓ α▓¡α│çα▓ƒα▓┐α▓»α▓╛α▓ùα▓┐α▓ªα│ìα▓ªα▓░α│å, α▓êα▓ùα▓╛α▓ùα▓▓α│ç α▓¿α│Çα▓íα▓┐α▓ª α▓íα│ïα▓╕α│ìΓÇîα▓ùα▓│α▓¿α│ìα▓¿α│ü α▓¿α▓«α│éα▓ªα▓┐α▓╕α▓▓α│ü \"α▓¿α▓┐α▓░α│ìα▓ºα▓╛α▓░α▓┐α▓ñ α▓ªα▓┐α▓¿α▓╛α▓éα▓òα▓╡α▓¿α│ìα▓¿α│ü α▓àα▓¬α│ìΓÇîα▓íα│çα▓ƒα│ì α▓«α▓╛α▓íα▓┐\" α▓òα│ìα▓▓α▓┐α▓òα│ì α▓«α▓╛α▓íα▓┐. α▓¬α│éα▓░α│ìα▓úα▓ùα│èα▓éα▓í α▓¿α▓éα▓ñα▓░, α▓¼α▓╛α▓òα▓┐ α▓çα▓░α│üα▓╡ α▓▓α▓╕α▓┐α▓òα│åα▓ùα▓│α│ü α▓«α▓╛α▓ñα│ìα▓░ α▓ëα▓│α▓┐α▓»α│üα▓ñα│ìα▓ñα▓╡α│åαÑñ',2),(17,'en','Update Due Date',3),(18,'hi','αñ¿αñ┐αñ»αññ αññαñ╛αñ░αÑÇαñû αñàαñ¬αñíαÑçαñƒ αñòαñ░αÑçαñé',3),(19,'bn','αª¿αª┐αª░αºìαªºαª╛αª░αª┐αªñ αªñαª╛αª░αª┐αªû αªåαª¬αªíαºçαªƒ αªòαª░αºüαª¿',3),(20,'ml','α┤¿α┤┐α┤╢α╡ìα┤Üα┤┐α┤ñ α┤ñα╡Çα┤»α┤ñα┤┐ α┤àα┤¬α╡ìα┤íα╡çα┤▒α╡ìα┤▒α╡ì α┤Üα╡åα┤»α╡ìα┤»α╡üα┤ò',3),(21,'ta','α«¿α«┐α«░α»ìαªºα«╛α«░αñ┐αññ α«ñα»çα«ñα«┐α«»α»ê α«¬α»üα«ñα»üα«¬α»ìα«¬α«┐α«òα»ìα«òα«╡α»üα««α»ì',3),(22,'te','α░¿α░┐α░░α▒ìα░ºα░╛α░░α░┐α░ñ α░ñα▒çα░ªα▒Çα░¿α░┐ α░àα░¬α▒ìΓÇîα░íα▒çα░ƒα▒ì α░Üα▒çα░»α░éα░íα░┐',3),(23,'mr','αñ¿αñ┐αñ░αÑìαñºαñ╛αñ░αñ┐αññ αññαñ╛αñ░αÑÇαñû αñàαñ¬αñíαÑçαñƒ αñòαñ░αñ╛',3),(24,'kn','α▓¿α▓┐α▓░α│ìα▓ºα▓╛α▓░α▓┐α▓ñ α▓ªα▓┐α▓¿α▓╛α▓éα▓òα▓╡α▓¿α│ìα▓¿α│ü α▓àα▓¬α│ìΓÇîα▓íα│çα▓ƒα│ì α▓«α▓╛α▓íα▓┐',3),(25,'en','Add Another Child',4),(26,'hi','αñªαÑéαñ╕αñ░αñ╛ αñ¼αñÜαÑìαñÜαñ╛ αñ£αÑïαñíαñ╝αÑçαñé',4),(27,'bn','αªåαª░αºçαªòαªƒαª┐ αª╢αª┐αª╢αºü αª»αºïαªù αªòαª░αºüαª¿',4),(28,'ml','α┤«α┤▒α╡ìα┤▒α╡èα┤░α╡ü α┤òα╡üα┤ƒα╡ìα┤ƒα┤┐α┤»α╡å α┤Üα╡çα╡╝α┤òα╡ìα┤òα╡üα┤ò',4),(29,'ta','α««α«▒α»ìα«▒α»èα«░α»ü α«òα»üα«┤α«¿α»ìα«ñα»êα«»α»ê α«Üα»çα«░α»ìα«òα»ìα«òα«╡α»üα««α»ì',4),(30,'te','α░«α░░α▒èα░ò α░¬α░┐α░▓α▒ìα░▓α░╡α░╛α░íα░┐α░¿α░┐ α░£α▒ïα░íα░┐α░éα░Üα░éα░íα░┐',4),(31,'mr','αñªαÑüαñ╕αñ░αÑç αñ«αÑéαñ▓ αñ£αÑïαñíαñ╛',4),(32,'kn','α▓«α▓ñα│ìα▓ñα│èα▓éα▓ªα│ü α▓«α▓ùα│üα▓╡α▓¿α│ìα▓¿α│ü α▓╕α│çα▓░α▓┐α▓╕α▓┐',4),(33,'en','Go Back',5),(34,'hi','αñ╡αñ╛αñ¬αñ╕ αñ£αñ╛αñÅαñé',5),(35,'bn','αª½αª┐αª░αºç αª»αª╛αª¿',5),(36,'ml','α┤ñα┤┐α┤░α┤┐α┤òα╡å α┤¬α╡ïα┤òα╡üα┤ò',5),(37,'ta','α«ñα«┐α«░α»üα««α»ìα«¬α«┐α«Üα»ì α«Üα»åα«▓α»ìα«▓α«╡α»üα««α»ì',5),(38,'te','α░╡α▒åα░¿α▒üα░òα░òα▒ü α░╡α▒åα░│α▒ìα░│α░éα░íα░┐',5),(39,'mr','αñ¬αñ░αññ αñ£αñ╛',5),(40,'kn','α▓╣α▓┐α▓éα▓ªα│å α▓╣α│ïα▓ùα▓┐',5),(41,'en','Vaccine',6),(42,'hi','αñƒαÑÇαñòαñ╛',6),(43,'bn','αªƒαª┐αªòαª╛',6),(44,'ml','α┤╡α┤╛α┤òα╡ìα┤╕α┤┐α╡╗',6),(45,'ta','α«ñα«ƒα»üα«¬α»ìα«¬α»éα«Üα«┐',6),(46,'te','α░╡α▒ìα░»α░╛α░òα▒ìα░╕α░┐α░¿α▒ì',6),(47,'mr','αñ▓αñ╕',6),(48,'kn','α▓▓α▓╕α▓┐α▓òα│å',6),(49,'en','Status',7),(50,'hi','αñ╕αÑìαñÑαñ┐αññαñ┐',7),(51,'bn','αªàαª¼αª╕αºìαªÑαª╛',7),(52,'ml','α┤¿α┤┐α┤▓',7),(53,'ta','α«¿α«┐α«▓α»ê',7),(54,'te','α░╕α▒ìα░Ñα░┐α░ñα░┐',7),(55,'mr','αñ╕αÑìαñÑαñ┐αññαÑÇ',7),(56,'kn','α▓╕α│ìα▓Ñα▓┐α▓ñα▓┐',7),(57,'en','Action',8),(58,'hi','αñòαñ╛αñ░αÑìαñ»',8),(59,'bn','αªòαª░αºìαª«',8),(60,'ml','α┤¬α╡ìα┤░α┤╡α╡╝α┤ñα╡ìα┤ñα┤¿α┤é',8),(61,'ta','α«Üα»åα«»α«▓α»ì',8),(62,'te','α░Üα░░α▒ìα░»',8),(63,'mr','αñòαÑâαññαÑÇ',8),(64,'kn','α▓òα│ìα▓░α▓┐α▓»α│å',8),(65,'en','Call Clinic',9),(66,'hi','αñòαÑìαñ▓αñ┐αñ¿αñ┐αñò αñòαÑï αñòαÑëαñ▓ αñòαñ░αÑçαñé',9),(67,'bn','αªòαºìαª▓αª┐αª¿αª┐αªòαºç αªòαª▓ αªòαª░αºüαª¿',9),(68,'ml','α┤òα╡ìα┤▓α┤┐α┤¿α┤┐α┤òα╡ìα┤òα┤┐α╡╜ α┤╡α┤┐α┤│α┤┐α┤òα╡ìα┤òα╡üα┤ò',9),(69,'ta','α««α«░α»üα«ñα»ìα«ñα»üα«╡α««α«⌐α»êα«»α»ê α«àα«┤α»êα«òα»ìα«òα«╡α»üα««α»ì',9),(70,'te','α░òα▒ìα░▓α░┐α░¿α░┐α░òα▒ìΓÇîα░òα▒ü α░òα░╛α░▓α▒ì α░Üα▒çα░»α░éα░íα░┐',9),(71,'mr','αñòαÑìαñ▓αñ┐αñ¿αñ┐αñòαñ▓αñ╛ αñòαÑëαñ▓ αñòαñ░αñ╛',9),(72,'kn','α▓òα│ìα▓▓α▓┐α▓¿α▓┐α▓òα│ìΓÇîα▓ùα│å α▓òα▓░α│å α▓«α▓╛α▓íα▓┐',9),(73,'en','Given on',10),(74,'hi','αñªαñ┐αñ»αñ╛ αñùαñ»αñ╛',10),(75,'bn','αªªαºçαªôαª»αª╝αª╛ αª╣αª»αª╝αºçαª¢αºç',10),(76,'ml','α┤¿α╡╜α┤òα┤┐α┤»α┤ñα╡ì',10),(77,'ta','α«òα»èα«ƒα»üα«òα»ìα«òα«¬α»ìα«¬α«ƒα»ìα«ƒα«ñα»ü',10),(78,'te','α░çα░╡α▒ìα░╡α░¼α░íα░┐α░éα░ªα░┐',10),(79,'mr','αñªαñ┐αñ▓αÑç αñùαÑçαñ▓αÑç',10),(80,'kn','α▓¿α│Çα▓íα▓▓α▓╛α▓ùα▓┐α▓ªα│å',10),(81,'en','Due on',11),(82,'hi','αñªαÑçαñ» αññαñ┐αñÑαñ┐',11),(83,'bn','αª¿αª┐αª░αºìαªºαª╛αª░αª┐αªñ αªñαª╛αª░αª┐αªû',11),(84,'ml','α┤¿α┤┐α┤╢α╡ìα┤Üα┤┐α┤ñ α┤ñα╡Çα┤»α┤ñα┤┐',11),(85,'ta','α«¿α«┐α«░α»ìαªºα«╛α«░α«┐α«ñα»ìα«ñ α«ñα»çα«ñα«┐',11),(86,'te','α░¿α░┐α░░α▒ìα░ºα░╛α░░α░┐α░ñ α░ñα▒çα░ªα▒Ç',11),(87,'mr','αñ¿αñ┐αñ░αÑìαñºαñ╛αñ░αñ┐αññ αññαñ╛αñ░αÑÇαñû',11),(88,'kn','α▓¿α▓┐α▓░α│ìα▓ºα▓╛α▓░α▓┐α▓ñ α▓ªα▓┐α▓¿α▓╛α▓éα▓ò',11),(89,'en','Given',12),(90,'hi','αñªαÑÇ αñùαñê',12),(91,'bn','αªªαºçαªôαª»αª╝αª╛ αª╣αª»αª╝αºçαª¢αºç',12),(92,'ml','α┤¿α╡╜α┤òα┤┐',12),(93,'ta','α«òα»èα«ƒα»üα«òα»ìα«òα«¬α»ìα«¬α«ƒα»ìα«ƒα«ñα»ü',12),(94,'te','α░çα░╡α▒ìα░╡α░¼α░íα░┐α░éα░ªα░┐',12),(95,'mr','αñªαñ┐αñ▓αÑÇ',12),(96,'kn','α▓¿α│Çα▓íα▓▓α▓╛α▓ùα▓┐α▓ªα│å',12),(97,'en','Pending',13),(98,'hi','αñ▓αñéαñ¼αñ┐αññ',13),(99,'bn','αª¼αª┐αª▓αª«αºìαª¼αª┐αªñ',13),(100,'ml','α┤¼α┤╛α┤òα╡ìα┤òα┤┐α┤»α╡üα┤úα╡ìα┤ƒα╡ì',13),(101,'ta','α«¿α«┐α«▓α»üα«╡α»êα«»α«┐α«▓α»ì',13),(102,'te','α░¬α▒åα░éα░íα░┐α░éα░ùα▒ìΓÇîα░▓α▒ï',13),(103,'mr','αñ¬αÑìαñ░αñ▓αñéαñ¼αñ┐αññ',13),(104,'kn','α▓¼α▓╛α▓òα▓┐ α▓çα▓ªα│å',13),(105,'en','Education',14),(106,'hi','αñ╢αñ┐αñòαÑìαñ╖αñ╛',14),(107,'bn','αª╢αª┐αªòαºìαª╖αª╛',14),(108,'ml','α┤╡α┤┐α┤ªα╡ìα┤»α┤╛α┤¡α╡ìα┤»α┤╛α┤╕α┤é',14),(109,'ta','α«òα«▓α»ìα«╡α«┐',14),(110,'te','α░╡α░┐α░ªα▒ìα░»',14),(111,'mr','αñ╢αñ┐αñòαÑìαñ╖αñú',14),(112,'kn','α▓╢α▓┐α▓òα│ìα▓╖α▓ú',14),(113,'en','Watch the short video(s) below to learn why this vaccine is important.',15),(114,'hi','αñçαñ╕ αñƒαÑÇαñòαÑç αñòαñ╛ αñ«αñ╣αññαÑìαñ╡ αñ£αñ╛αñ¿αñ¿αÑç αñòαÑç αñ▓αñ┐αñÅ αñ¿αÑÇαñÜαÑç αñªαñ┐αñÅ αñùαñÅ αñ¢αÑïαñƒαÑç αñ╡αÑÇαñíαñ┐αñ»αÑï αñªαÑçαñûαÑçαñéαÑñ',15),(115,'bn','αªÅαªç αªƒαª┐αªòαª╛ αªòαºçαª¿ αªùαºüαª░αºüαªñαºìαª¼αª¬αºéαª░αºìαªú αªñαª╛ αª£αª╛αª¿αªñαºç αª¿αª┐αªÜαºçαª░ αª¢αºïαªƒ αª¡αª┐αªíαª┐αªô(αªùαºüαª▓αª┐) αªªαºçαªûαºüαª¿αÑñ',15),(116,'ml','α┤ê α┤╡α┤╛α┤òα╡ìα┤╕α┤┐α╡╗ α┤Äα┤¿α╡ìα┤ñα╡üα┤òα╡èα┤úα╡ìα┤ƒα╡ì α┤¬α╡ìα┤░α┤ºα┤╛α┤¿α┤«α┤╛α┤úα╡åα┤¿α╡ìα┤¿α╡ì α┤àα┤▒α┤┐α┤»α┤╛α╡╗ α┤ñα┤╛α┤┤α╡åα┤»α╡üα┤│α╡ìα┤│ α┤Üα╡åα┤▒α┤┐α┤» α┤╡α╡Çα┤íα┤┐α┤»α╡ï(α┤òα╡╛) α┤òα┤╛α┤úα╡üα┤òαÑñ',15),(117,'ta','α«çα«¿α»ìα«ñ α«ñα«ƒα»üα«¬α»ìα«¬α»éα«Üα«┐ α«Åα«⌐α»ì α««α»üα«òα»ìα«òα«┐α«»α««α»ì α«Äα«⌐α»ìα«¬α«ñα»ê α«àα«▒α«┐α«» α«òα»Çα«┤α»ç α«ëα«│α»ìα«│ α«Üα«┐α«▒α«┐α«» α«╡α»Çα«ƒα«┐α«»α»ï(α«òα»ìα«òα«│α»ê) α«¬α«╛α«░α»ìα«òα»ìα«òα«╡α»üα««α»ìαÑñ',15),(118,'te','α░ê α░╡α▒ìα░»α░╛α░òα▒ìα░╕α░┐α░¿α▒ì α░Äα░éα░ªα▒üα░òα▒ü α░«α▒üα░ûα▒ìα░»α░«α▒ï α░ñα▒åα░▓α▒üα░╕α▒üα░òα▒ïα░╡α░íα░╛α░¿α░┐α░òα░┐ α░òα▒ìα░░α░┐α░éα░ª α░ëα░¿α▒ìα░¿ α░Üα░┐α░¿α▒ìα░¿ α░╡α▒Çα░íα░┐α░»α▒ï(α░▓α░¿α▒ü) α░Üα▒éα░íα░éα░íα░┐αÑñ',15),(119,'mr','αñ╣αÑÇ αñ▓αñ╕ αñòαñ╛ αñ«αñ╣αññαÑìαñ╡αñ╛αñÜαÑÇ αñåαñ╣αÑç αñ╣αÑç αñ£αñ╛αñúαÑéαñ¿ αñÿαÑçαñúαÑìαñ»αñ╛αñ╕αñ╛αñáαÑÇ αñûαñ╛αñ▓αÑÇαñ▓ αñ¢αÑïαñƒαÑç αñ╡αÑìαñ╣αñ┐αñíαñ┐αñô αñ¬αñ╣αñ╛αÑñ',15),(120,'kn','α▓ê α▓▓α▓╕α▓┐α▓òα│å α▓Åα▓òα│å α▓«α│üα▓ûα│ìα▓»α▓╡α▓╛α▓ùα▓┐α▓ªα│å α▓Äα▓éα▓¼α│üα▓ªα▓¿α│ìα▓¿α│ü α▓ñα▓┐α▓│α▓┐α▓»α▓▓α│ü α▓òα│åα▓│α▓ùα▓┐α▓¿ α▓Üα▓┐α▓òα│ìα▓ò α▓╡α│Çα▓íα▓┐α▓»α│ï(α▓ùα▓│α▓¿α│ìα▓¿α│ü) α▓¿α│ïα▓íα▓┐αÑñ',15),(121,'en','Child Name',16),(122,'hi','αñ¼αñÜαÑìαñÜαÑç αñòαñ╛ αñ¿αñ╛αñ«',16),(123,'bn','αª╢αª┐αª╢αºüαª░ αª¿αª╛αª«',16),(124,'ml','α┤òα╡üα┤ƒα╡ìα┤ƒα┤┐α┤»α╡üα┤ƒα╡å α┤¬α╡çα┤░α╡ì',16),(125,'ta','α«òα»üα«┤α«¿α»ìα«ñα»êα«»α«┐α«⌐α»ì α«¬α»åα«»α«░α»ì',16),(126,'te','α░¬α░┐α░▓α▒ìα░▓α░╡α░╛α░íα░┐ α░¬α▒çα░░α▒ü',16),(127,'mr','αñ«αÑüαñ▓αñ╛αñÜαÑç αñ¿αñ╛αñ╡',16),(128,'kn','α▓«α▓ùα│üα▓╡α▓┐α▓¿ α▓╣α│åα▓╕α▓░α│ü',16),(129,'en','Date of Birth',17),(130,'hi','αñ£αñ¿αÑìαñ« αññαñ┐αñÑαñ┐',17),(131,'bn','αª£αª¿αºìαª« αªñαª╛αª░αª┐αªû',17),(132,'ml','α┤£α┤¿α┤¿α┤ñα╡ìα┤ñα╡Çα┤»α┤ñα┤┐',17),(133,'ta','α«¬α«┐α«▒α«¿α»ìα«ñ α«ñα»çα«ñα«┐',17),(134,'te','α░¬α▒üα░ƒα▒ìα░ƒα░┐α░¿ α░ñα▒çα░ªα▒Ç',17),(135,'mr','αñ£αñ¿αÑìαñ« αññαñ╛αñ░αÑÇαñû',17),(136,'kn','α▓╣α│üα▓ƒα│ìα▓ƒα▓┐α▓ª α▓ªα▓┐α▓¿α▓╛α▓éα▓ò',17),(137,'en','Gender',18),(138,'hi','αñ▓αñ┐αñéαñù',18),(139,'bn','αª▓αª┐αªÖαºìαªù',18),(140,'ml','α┤▓α┤┐α┤éα┤ùα┤é',18),(141,'ta','α«¬α«╛α«▓α«┐α«⌐α««α»ì',18),(142,'te','α░▓α░┐α░éα░ùα░é',18),(143,'mr','αñ▓αñ┐αñéαñù',18),(144,'kn','α▓▓α▓┐α▓éα▓ù',18);
/*!40000 ALTER TABLE `ui_string_translation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vaccine`
--

DROP TABLE IF EXISTS `vaccine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vaccine` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `schedule_version_id` bigint NOT NULL,
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `aliases` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `education_parent_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '',
  `education_doctor_vimeo_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vaccine`
--

LOCK TABLES `vaccine` WRITE;
/*!40000 ALTER TABLE `vaccine` DISABLE KEYS */;
INSERT INTO `vaccine` VALUES (1,1,'bcg','BCG','',1,'','2025-10-07 05:59:15.164385','',''),(2,1,'hep_b1','Hep B1','',1,'','2025-10-07 05:59:15.174914','',''),(3,1,'opv','OPV','',1,'','2025-10-07 05:59:15.183738','',''),(4,1,'dtwp_dtap1','DTwP / DTaP1','',1,'','2025-10-07 05:59:15.191103','',''),(5,1,'hib-1','Hib-1','',1,'','2025-10-07 05:59:15.199128','',''),(6,1,'ipv-1','IPV-1','',1,'','2025-10-07 05:59:15.210951','',''),(7,1,'hep_b2','Hep B2','',1,'','2025-10-07 05:59:15.218914','',''),(8,1,'pcv_1','PCV 1','',1,'','2025-10-07 05:59:15.225798','',''),(9,1,'rota-1','Rota-1','',1,'','2025-10-07 05:59:15.232217','',''),(10,1,'dtwp_dtap2','DTwP / DTaP2','',1,'','2025-10-07 05:59:15.246216','',''),(11,1,'hib-2','Hib-2','',1,'','2025-10-07 05:59:15.253575','',''),(12,1,'ipv-2','IPV-2','',1,'','2025-10-07 05:59:15.262582','',''),(13,1,'hep_b3','Hep B3','',1,'','2025-10-07 05:59:15.273433','',''),(14,1,'pcv_2','PCV 2','',1,'','2025-10-07 05:59:15.280896','',''),(15,1,'rota-2','Rota-2','',1,'','2025-10-07 05:59:15.287827','',''),(16,1,'dtwp_dtap3','DTwP / DTaP3','',1,'','2025-10-07 05:59:15.299369','',''),(17,1,'hib-3','Hib-3','',1,'','2025-10-07 05:59:15.307934','',''),(18,1,'ipv-3','IPV-3','',1,'','2025-10-07 05:59:15.315560','',''),(19,1,'hep_b4','Hep B4','',1,'','2025-10-07 05:59:15.324696','',''),(20,1,'pcv_3','PCV 3','',1,'','2025-10-07 05:59:15.332665','',''),(21,1,'rota-3','Rota-3*','',1,'','2025-10-07 05:59:15.339313','',''),(22,1,'influenza-1','Influenza-1','',1,'','2025-10-07 05:59:15.349827','',''),(23,1,'influenza-2','Influenza-2','',1,'','2025-10-07 05:59:15.357762','',''),(24,1,'typhoid_conjugate_vaccine','Typhoid Conjugate Vaccine','',1,'','2025-10-07 05:59:15.365684','',''),(25,1,'mmr_1_measles_mumps_rubella','MMR 1 (Measles, Mumps, Rubella)','',1,'','2025-10-07 05:59:15.375214','',''),(26,1,'hepatitis_a-1','Hepatitis A-1','',1,'','2025-10-07 05:59:15.378566','',''),(27,1,'pcv_booster','PCV Booster','',1,'','2025-10-07 05:59:15.391902','',''),(28,1,'mmr_2','MMR 2','',1,'','2025-10-07 05:59:15.398906','',''),(29,1,'varicella','Varicella','',1,'','2025-10-07 05:59:15.407975','',''),(30,1,'dtwp_dtap','DTwP / DTaP','',1,'','2025-10-07 05:59:15.419312','',''),(31,1,'hib','Hib','',1,'','2025-10-07 05:59:15.426800','',''),(32,1,'ipv','IPV','',1,'','2025-10-07 05:59:15.436726','',''),(33,1,'hepatitis_a-2','Hepatitis A-2**','',1,'','2025-10-07 05:59:15.446528','',''),(34,1,'varicella_2','Varicella 2','',1,'','2025-10-07 05:59:15.454390','',''),(35,1,'mmr_3','MMR 3','',1,'','2025-10-07 05:59:15.468936','',''),(36,1,'hpv_2_doses','HPV (2 doses)','',1,'','2025-10-07 05:59:15.481807','',''),(37,1,'tdap_td','Tdap / Td','',1,'','2025-10-07 05:59:15.489187','',''),(38,1,'annual_influenza_vaccine','Annual Influenza Vaccine','',1,'','2025-10-07 05:59:15.499327','','');
/*!40000 ALTER TABLE `vaccine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vaccine_dose`
--

DROP TABLE IF EXISTS `vaccine_dose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vaccine_dose` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `schedule_version_id` bigint NOT NULL,
  `vaccine_id` bigint NOT NULL,
  `sequence_index` smallint unsigned NOT NULL,
  `dose_label` varchar(60) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `eligible_gender` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `min_offset_days` int unsigned NOT NULL,
  `max_offset_days` int unsigned DEFAULT NULL,
  `is_booster` tinyint(1) DEFAULT '0',
  `previous_dose_id` bigint DEFAULT NULL,
  `notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci,
  `created_at` datetime(6) NOT NULL,
  `anchor_policy` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT 'L',
  `series_key` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT '',
  `series_seq` smallint unsigned DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vaccine_dose`
--

LOCK TABLES `vaccine_dose` WRITE;
/*!40000 ALTER TABLE `vaccine_dose` DISABLE KEYS */;
INSERT INTO `vaccine_dose` VALUES (1,1,1,1,'BCG',NULL,0,30,0,NULL,'','2025-10-07 05:59:15.169781','L','',1),(2,1,2,1,'Hep B1',NULL,0,30,0,NULL,'','2025-10-07 05:59:15.177403','L','',1),(3,1,3,1,'OPV',NULL,0,30,0,NULL,'','2025-10-07 05:59:15.183738','L','',1),(4,1,4,1,'DTwP / DTaP1',NULL,42,72,0,NULL,'','2025-10-07 05:59:15.197221','L','',1),(5,1,5,1,'Hib-1',NULL,42,72,0,NULL,'','2025-10-07 05:59:15.205038','L','',1),(6,1,6,1,'IPV-1',NULL,42,72,0,NULL,'','2025-10-07 05:59:15.214038','L','',1),(7,1,7,1,'Hep B2',NULL,42,72,1,2,'','2025-10-07 05:59:15.223967','L','',1),(8,1,8,1,'PCV 1',NULL,42,72,0,NULL,'','2025-10-07 05:59:15.232217','L','',1),(9,1,9,1,'Rota-1',NULL,42,72,0,NULL,'','2025-10-07 05:59:15.239794','L','',1),(10,1,10,1,'DTwP / DTaP2',NULL,70,100,1,4,'','2025-10-07 05:59:15.251515','L','',1),(11,1,11,1,'Hib-2',NULL,70,100,1,5,'','2025-10-07 05:59:15.259555','L','',1),(12,1,12,1,'IPV-2',NULL,70,100,1,6,'','2025-10-07 05:59:15.266981','L','',1),(13,1,13,1,'Hep B3',NULL,70,100,1,7,'','2025-10-07 05:59:15.275577','L','',1),(14,1,14,1,'PCV 2',NULL,70,100,1,8,'','2025-10-07 05:59:15.280896','L','',1),(15,1,15,1,'Rota-2',NULL,70,100,1,9,'','2025-10-07 05:59:15.294662','L','',1),(16,1,16,1,'DTwP / DTaP3',NULL,98,128,1,10,'','2025-10-07 05:59:15.301709','L','',1),(17,1,17,1,'Hib-3',NULL,98,128,1,11,'','2025-10-07 05:59:15.310783','L','',1),(18,1,18,1,'IPV-3',NULL,98,128,1,12,'','2025-10-07 05:59:15.315560','L','',1),(19,1,19,1,'Hep B4',NULL,98,128,1,13,'','2025-10-07 05:59:15.328976','L','',1),(20,1,20,1,'PCV 3',NULL,98,128,1,14,'','2025-10-07 05:59:15.336332','L','',1),(21,1,21,1,'Rota-3*',NULL,98,128,1,15,'','2025-10-07 05:59:15.345323','L','',1),(22,1,22,1,'Influenza-1',NULL,180,210,0,NULL,'','2025-10-07 05:59:15.354178','L','',1),(23,1,23,1,'Influenza-2',NULL,210,240,1,22,'','2025-10-07 05:59:15.362789','L','',1),(24,1,24,1,'Typhoid Conjugate Vaccine',NULL,180,210,0,NULL,'','2025-10-07 05:59:15.371155','L','',1),(25,1,25,1,'MMR 1 (Measles, Mumps, Rubella)',NULL,270,300,0,NULL,'','2025-10-07 05:59:15.378566','L','',1),(26,1,26,1,'Hepatitis A-1',NULL,360,390,0,NULL,'','2025-10-07 05:59:15.384953','L','',1),(27,1,27,1,'PCV Booster',NULL,360,390,1,20,'','2025-10-07 05:59:15.395823','L','',1),(28,1,28,1,'MMR 2',NULL,450,480,1,25,'','2025-10-07 05:59:15.405906','L','',1),(29,1,29,1,'Varicella',NULL,450,480,0,NULL,'','2025-10-07 05:59:15.414219','L','',1),(30,1,30,1,'DTwP / DTaP',NULL,480,510,1,NULL,'','2025-10-07 05:59:15.421572','L','',1),(31,1,31,1,'Hib',NULL,480,510,1,17,'','2025-10-07 05:59:15.426800','L','',1),(32,1,32,1,'IPV',NULL,480,510,1,NULL,'','2025-10-07 05:59:15.440468','L','',1),(33,1,33,1,'Hepatitis A-2**',NULL,540,570,1,26,'','2025-10-07 05:59:15.449576','L','',1),(34,1,34,1,'Varicella 2',NULL,540,570,1,29,'','2025-10-07 05:59:15.457997','L','',1),(35,1,30,1,'DTwP / DTaP',NULL,1460,1490,1,35,'','2025-10-07 05:59:15.463144','L','',1),(36,1,32,1,'IPV',NULL,1460,1490,1,35,'','2025-10-07 05:59:15.464256','L','',1),(37,1,35,1,'MMR 3',NULL,1460,1490,1,28,'','2025-10-07 05:59:15.475317','L','',1),(38,1,36,1,'HPV (2 doses)',NULL,3285,3315,0,NULL,'','2025-10-07 05:59:15.482405','L','',1),(39,1,37,1,'Tdap / Td',NULL,3650,3680,1,35,'','2025-10-07 05:59:15.495198','L','',1),(40,1,38,1,'Annual Influenza Vaccine',NULL,365,395,1,23,'','2025-10-07 05:59:15.503605','L','',1),(41,1,38,1,'Annual Influenza Vaccine',NULL,730,760,1,40,'','2025-10-07 05:59:15.507747','L','',1),(42,1,38,1,'Annual Influenza Vaccine',NULL,1095,1125,1,41,'','2025-10-07 05:59:15.510188','L','',1),(43,1,38,1,'Annual Influenza Vaccine',NULL,1460,1490,1,42,'','2025-10-07 05:59:15.517105','L','',1);
/*!40000 ALTER TABLE `vaccine_dose` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vaccine_education_doctor`
--

DROP TABLE IF EXISTS `vaccine_education_doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vaccine_education_doctor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `language` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `video_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `platform` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `rank` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `vaccine_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vaccine_education_doctor_vaccine_id_video_url_99ab31b3_uniq` (`vaccine_id`,`video_url`),
  KEY `vaccine_education_doctor_language_9d7d65c4` (`language`),
  KEY `vaccine_edu_vaccine_f09e3c_idx` (`vaccine_id`,`rank`),
  KEY `vaccine_edu_is_acti_7524ff_idx` (`is_active`),
  CONSTRAINT `vaccine_education_doctor_vaccine_id_55d1f4a5_fk_vaccine_id` FOREIGN KEY (`vaccine_id`) REFERENCES `vaccine` (`id`),
  CONSTRAINT `vaccine_education_doctor_chk_1` CHECK ((`rank` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vaccine_education_doctor`
--

LOCK TABLES `vaccine_education_doctor` WRITE;
/*!40000 ALTER TABLE `vaccine_education_doctor` DISABLE KEYS */;
/*!40000 ALTER TABLE `vaccine_education_doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vaccine_education_patient`
--

DROP TABLE IF EXISTS `vaccine_education_patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vaccine_education_patient` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `language` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `video_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `platform` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `thumbnail_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `duration_seconds` int unsigned DEFAULT NULL,
  `rank` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `vaccine_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vaccine_education_patien_vaccine_id_language_vide_3eb0e922_uniq` (`vaccine_id`,`language`,`video_url`),
  KEY `vaccine_education_patient_language_a990bfc1` (`language`),
  KEY `vaccine_edu_vaccine_a5e22a_idx` (`vaccine_id`,`language`,`rank`),
  KEY `vaccine_edu_is_acti_14108b_idx` (`is_active`),
  CONSTRAINT `vaccine_education_patient_vaccine_id_a0631508_fk_vaccine_id` FOREIGN KEY (`vaccine_id`) REFERENCES `vaccine` (`id`),
  CONSTRAINT `vaccine_education_patient_chk_1` CHECK ((`duration_seconds` >= 0)),
  CONSTRAINT `vaccine_education_patient_chk_2` CHECK ((`rank` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vaccine_education_patient`
--

LOCK TABLES `vaccine_education_patient` WRITE;
/*!40000 ALTER TABLE `vaccine_education_patient` DISABLE KEYS */;
/*!40000 ALTER TABLE `vaccine_education_patient` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-18 12:49:25
