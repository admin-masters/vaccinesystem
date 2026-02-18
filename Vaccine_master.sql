-- MySQL dump 10.13  Distrib 8.0.41, for macos15 (x86_64)
--
-- Host: 65.0.103.152    Database: vacc_masters
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
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add clinic',7,'add_clinic'),(26,'Can change clinic',7,'change_clinic'),(27,'Can delete clinic',7,'delete_clinic'),(28,'Can view clinic',7,'view_clinic'),(29,'Can add schedule version',8,'add_scheduleversion'),(30,'Can change schedule version',8,'change_scheduleversion'),(31,'Can delete schedule version',8,'delete_scheduleversion'),(32,'Can view schedule version',8,'view_scheduleversion'),(33,'Can add parent',9,'add_parent'),(34,'Can change parent',9,'change_parent'),(35,'Can delete parent',9,'delete_parent'),(36,'Can view parent',9,'view_parent'),(37,'Can add child',10,'add_child'),(38,'Can change child',10,'change_child'),(39,'Can delete child',10,'delete_child'),(40,'Can view child',10,'view_child'),(41,'Can add vaccine',11,'add_vaccine'),(42,'Can change vaccine',11,'change_vaccine'),(43,'Can delete vaccine',11,'delete_vaccine'),(44,'Can view vaccine',11,'view_vaccine'),(45,'Can add vaccine dose',12,'add_vaccinedose'),(46,'Can change vaccine dose',12,'change_vaccinedose'),(47,'Can delete vaccine dose',12,'delete_vaccinedose'),(48,'Can view vaccine dose',12,'view_vaccinedose'),(49,'Can add child dose',13,'add_childdose'),(50,'Can change child dose',13,'change_childdose'),(51,'Can delete child dose',13,'delete_childdose'),(52,'Can view child dose',13,'view_childdose'),(53,'Can add partner',14,'add_partner'),(54,'Can change partner',14,'change_partner'),(55,'Can delete partner',14,'delete_partner'),(56,'Can view partner',14,'view_partner'),(57,'Can add field representative',15,'add_fieldrepresentative'),(58,'Can change field representative',15,'change_fieldrepresentative'),(59,'Can delete field representative',15,'delete_fieldrepresentative'),(60,'Can view field representative',15,'view_fieldrepresentative'),(61,'Can add doctor',16,'add_doctor'),(62,'Can change doctor',16,'change_doctor'),(63,'Can delete doctor',16,'delete_doctor'),(64,'Can view doctor',16,'view_doctor'),(65,'Can add doctor session token',17,'add_doctorsessiontoken'),(66,'Can change doctor session token',17,'change_doctorsessiontoken'),(67,'Can delete doctor session token',17,'delete_doctorsessiontoken'),(68,'Can view doctor session token',17,'view_doctorsessiontoken'),(69,'Can add o auth state',18,'add_oauthstate'),(70,'Can change o auth state',18,'change_oauthstate'),(71,'Can delete o auth state',18,'delete_oauthstate'),(72,'Can view o auth state',18,'view_oauthstate'),(73,'Can add child share link',19,'add_childsharelink'),(74,'Can change child share link',19,'change_childsharelink'),(75,'Can delete child share link',19,'delete_childsharelink'),(76,'Can view child share link',19,'view_childsharelink'),(77,'Can add vaccine education doctor',20,'add_vaccineeducationdoctor'),(78,'Can change vaccine education doctor',20,'change_vaccineeducationdoctor'),(79,'Can delete vaccine education doctor',20,'delete_vaccineeducationdoctor'),(80,'Can view vaccine education doctor',20,'view_vaccineeducationdoctor'),(81,'Can add vaccine education patient',21,'add_vaccineeducationpatient'),(82,'Can change vaccine education patient',21,'change_vaccineeducationpatient'),(83,'Can delete vaccine education patient',21,'delete_vaccineeducationpatient'),(84,'Can view vaccine education patient',21,'view_vaccineeducationpatient'),(85,'Can add ui string',22,'add_uistring'),(86,'Can change ui string',22,'change_uistring'),(87,'Can delete ui string',22,'delete_uistring'),(88,'Can view ui string',22,'view_uistring'),(89,'Can add ui string translation',23,'add_uistringtranslation'),(90,'Can change ui string translation',23,'change_uistringtranslation'),(91,'Can delete ui string translation',23,'delete_uistringtranslation'),(92,'Can view ui string translation',23,'view_uistringtranslation');
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
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `full_name` varchar(120) NOT NULL,
  `date_of_birth` date NOT NULL,
  `sex` varchar(1) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `clinic_id` bigint DEFAULT NULL,
  `parent_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `child_parent__16983e_idx` (`parent_id`),
  KEY `child_clinic__5e8bbe_idx` (`clinic_id`),
  KEY `child_date_of_670404_idx` (`date_of_birth`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child`
--

LOCK TABLES `child` WRITE;
/*!40000 ALTER TABLE `child` DISABLE KEYS */;
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
  `given_date` date DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `due_until_date` date DEFAULT NULL,
  `status_override` varchar(32) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `child_id` bigint NOT NULL,
  `dose_id` bigint NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child_dose`
--

LOCK TABLES `child_dose` WRITE;
/*!40000 ALTER TABLE `child_dose` DISABLE KEYS */;
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
  `token` varchar(64) NOT NULL,
  `expected_last10` varchar(10) NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `child_share_link`
--

LOCK TABLES `child_share_link` WRITE;
/*!40000 ALTER TABLE `child_share_link` DISABLE KEYS */;
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
  `name` varchar(150) NOT NULL,
  `address` longtext NOT NULL,
  `phone` varchar(30) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `state` varchar(100) DEFAULT NULL,
  `headquarters` varchar(255) DEFAULT NULL,
  `pincode` varchar(20) DEFAULT NULL,
  `whatsapp_e164` varchar(20) DEFAULT NULL,
  `receptionist_email` varchar(255) DEFAULT NULL,
  `languages_csv` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clinic`
--

LOCK TABLES `clinic` WRITE;
/*!40000 ALTER TABLE `clinic` DISABLE KEYS */;
INSERT INTO `clinic` VALUES (1,'Bharti','','','2025-10-06 14:45:45.212893','Madhya Pradesh','Bhopal','455001','+918269966106','','en,hi'),(2,'Bharti','','','2025-10-06 14:49:35.116803','Madhya Pradesh','Bhopal','455001','+918269966106','','en,hi'),(3,'Bharti','','','2025-10-06 14:50:11.929232','Madhya Pradesh','Bhopal','455001','+918269966106','','en,hi'),(4,'Bharti','','','2025-10-06 14:58:08.263729','Madhya Pradesh','Bhopal','455001','+918269966106','','en,hi,mr'),(5,'Sanyam','','','2025-10-07 09:20:33.984676','Maharashtra','','','+918103422926','','en,hi'),(6,'Sanyam','','','2025-10-07 09:23:15.016344','Maharashtra','','','+918103422926','','en,hi'),(7,'Sanyam','','','2025-10-07 09:23:29.046366','Maharashtra','','','+918103422926','','en,hi'),(8,'Bharti Dhote','EWS 649 Vikas Nagar Dewas Madhya Pradesh','','2025-10-07 10:45:44.699339','Madhya Pradesh','','455001','+918269966106','','en,hi'),(9,'Test Clinic','','1234567890','2025-10-07 10:48:52.030117','Test State','','','','',''),(10,'Niomi','','','2025-10-07 10:53:28.824212','Maharashtra','','','+918103422926','','en,hi'),(11,'Bharti Dhote','EWS 649 Vikas Nagar Dewas Madhya Pradesh','','2025-10-07 11:04:16.882350','Madhya Pradesh','','455001','+918269966106','',''),(12,'Bharti Dhote','EWS 649 Vikas Nagar Dewas Madhya Pradesh','','2025-10-07 12:24:38.448316','Madhya Pradesh','','455001','+918269966106','',''),(13,'Bharti Dhote','EWS 649 Vikas Nagar Dewas Madhya Pradesh','','2025-10-07 12:27:16.817784','Madhya Pradesh','','455001','+918269966106','',''),(14,'Khushan Poptani','9084712373','','2025-10-27 05:59:20.487226','Uttar Pradesh','9084712373','282005','+919084712373','poptanikhushan@gmail.com','en,hi,mr'),(15,'Niomi','','','2025-10-27 06:15:59.677397','Madhya Pradesh','','','+918269966106','','en,hi'),(16,'Rakshit','','','2025-10-27 06:32:06.194407','Madhya Pradesh','','','+918269966106','','en,hi'),(17,'Piyush','','','2025-10-27 13:25:51.214448','Madhya Pradesh','','','+918269966106','','en,hi'),(18,'Vikram','Xyz','','2025-10-27 13:38:10.426317','Maharashtra','Mumbai','400604','+918591196243','vikramkanaujiya67@gmail.com','en'),(19,'Simran Galani','Tender Care Clinic, Mumbai, 421001','','2025-11-03 10:16:08.042316','Maharashtra','','421001','+919657961017','tarunagalani23@gmail.com','en,hi,mr');
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
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(10,'vaccinations','child'),(13,'vaccinations','childdose'),(19,'vaccinations','childsharelink'),(7,'vaccinations','clinic'),(16,'vaccinations','doctor'),(17,'vaccinations','doctorsessiontoken'),(15,'vaccinations','fieldrepresentative'),(18,'vaccinations','oauthstate'),(9,'vaccinations','parent'),(14,'vaccinations','partner'),(8,'vaccinations','scheduleversion'),(22,'vaccinations','uistring'),(23,'vaccinations','uistringtranslation'),(11,'vaccinations','vaccine'),(12,'vaccinations','vaccinedose'),(20,'vaccinations','vaccineeducationdoctor'),(21,'vaccinations','vaccineeducationpatient');
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
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-05 19:25:36.886462'),(2,'auth','0001_initial','2025-10-05 19:25:37.789631'),(3,'admin','0001_initial','2025-10-05 19:25:37.994930'),(4,'admin','0002_logentry_remove_auto_add','2025-10-05 19:25:38.004942'),(5,'admin','0003_logentry_add_action_flag_choices','2025-10-05 19:25:38.015110'),(6,'contenttypes','0002_remove_content_type_name','2025-10-05 19:25:38.174397'),(7,'auth','0002_alter_permission_name_max_length','2025-10-05 19:25:38.279251'),(8,'auth','0003_alter_user_email_max_length','2025-10-05 19:25:38.305416'),(9,'auth','0004_alter_user_username_opts','2025-10-05 19:25:38.316200'),(10,'auth','0005_alter_user_last_login_null','2025-10-05 19:25:38.400985'),(11,'auth','0006_require_contenttypes_0002','2025-10-05 19:25:38.403945'),(12,'auth','0007_alter_validators_add_error_messages','2025-10-05 19:25:38.415196'),(13,'auth','0008_alter_user_username_max_length','2025-10-05 19:25:38.512924'),(14,'auth','0009_alter_user_last_name_max_length','2025-10-05 19:25:38.616717'),(15,'auth','0010_alter_group_name_max_length','2025-10-05 19:25:38.639606'),(16,'auth','0011_update_proxy_permissions','2025-10-05 19:25:38.650870'),(17,'auth','0012_alter_user_first_name_max_length','2025-10-05 19:25:38.740768'),(18,'sessions','0001_initial','2025-10-05 19:25:38.797456'),(19,'vaccinations','0001_initial','2025-10-05 19:27:34.265320'),(20,'vaccinations','0002_child_state_alter_vaccine_code_alter_vaccine_name_and_more','2025-10-05 19:27:34.272147'),(21,'vaccinations','0003_phase2_whitelabel','2025-10-05 19:27:34.279434'),(22,'vaccinations','0004_doctor_google_login','2025-10-05 19:27:34.283545'),(23,'vaccinations','0005_oauthstate_and_more','2025-10-05 19:27:34.285891'),(24,'vaccinations','0006_oauthstate_redirect_uri','2025-10-05 19:27:34.292997'),(25,'vaccinations','0007_child_share_link','2025-10-05 19:27:34.297985'),(26,'vaccinations','0008_rename_idx_csl_child_child_share_child_i_a28a1d_idx_and_more','2025-10-05 19:27:34.302467'),(27,'vaccinations','0009_vaccineeducationdoctor_vaccineeducationpatient','2025-10-05 19:27:34.306308'),(28,'vaccinations','0010_childdose_last_reminder_at_and_more','2025-10-05 19:27:34.309117'),(29,'vaccinations','0011_uistring_uistringtranslation','2025-10-05 19:27:34.315199'),(30,'vaccinations','0012_vaccinedose_anchor_policy_and_more','2025-10-05 19:27:34.321243'),(31,'vaccinations','0013_vaccinedose_series_key_vaccinedose_series_seq','2025-10-05 19:27:34.323844'),(32,'vaccinations','0014_fix_influenza_series','2025-10-05 19:27:34.329761'),(33,'vaccinations','0015_patients_encryption','2025-10-05 19:27:34.334727'),(34,'vaccinations','0016_remove_child_child_parent__16983e_idx_and_more','2025-10-05 19:27:34.337088'),(35,'vaccinations','0017_rename_eligible_sex_vaccinedose_eligible_gender_and_more','2025-10-05 19:27:34.342969'),(36,'vaccinations','0018_remove_child_child_clinic__5e8bbe_idx_and_more','2025-10-06 14:31:12.727470'),(37,'vaccinations','0020_patient_encrypted_columns','2025-10-06 14:31:12.749872'),(38,'vaccinations','0019_add_encrypted_columns','2025-10-06 14:31:12.770080'),(39,'vaccinations','0021_merge_20251006_1959','2025-10-06 14:31:12.774644'),(40,'vaccinations','0022_child_idx_child_clinic_child_idx_child_dob_and_more','2025-10-06 14:31:12.791978'),(41,'vaccinations','0023_alter_doctor_options','2025-10-06 14:49:55.217897'),(42,'vaccinations','0024_alter_doctor_options','2025-10-06 14:52:30.230236'),(43,'vaccinations','0025_alter_doctor_options','2025-10-06 14:54:33.867885'),(44,'vaccinations','0026_parent_created_at_alter_child_created_at','2025-10-07 07:32:10.691313'),(45,'vaccinations','0027_auto','2025-10-07 07:32:11.029402'),(46,'vaccinations','0028_rename_vaccinations_child_id_idx_child_share_child_i_a28a1d_idx_and_more','2025-10-07 07:32:11.100398');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
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
  `clinic_id` bigint NOT NULL,
  `full_name` varchar(120) NOT NULL,
  `whatsapp_e164` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `imc_number` varchar(30) NOT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `partner_id` bigint DEFAULT NULL,
  `field_rep_id` bigint DEFAULT NULL,
  `portal_token` varchar(64) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `google_sub` varchar(64) DEFAULT NULL,
  `last_login_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `imc_number` (`imc_number`),
  UNIQUE KEY `portal_token` (`portal_token`),
  UNIQUE KEY `google_sub` (`google_sub`),
  KEY `idx_doctor_clinic` (`clinic_id`),
  KEY `idx_doctor_partner` (`partner_id`),
  KEY `idx_doctor_field_rep` (`field_rep_id`),
  CONSTRAINT `doctor_ibfk_1` FOREIGN KEY (`clinic_id`) REFERENCES `clinic` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (10,13,'Bharti Dhote','+918269966106','bhartidhote8@gmail.com','89754123','',NULL,NULL,'KdR0ZIvTr3vvOZ07Nvcef8af95um0Iz1',1,'2025-10-07 12:27:17','2025-10-07 17:57:31','102724152428071937183',NULL),(11,14,'Khushan Poptani','+919084712373','poptanikhushan@gmail.com','9084712373','',NULL,NULL,'hCanToi8Jf7PaCss7affcooWou0zmEqs',1,'2025-10-27 05:59:21','2025-10-27 05:59:21',NULL,NULL),(12,15,'Niomi','+919827766106','haterworld16@gmail.com','22222','',NULL,NULL,'m0EFhYv9N99wyIvmihxtHR4mcbGc7SOu',1,'2025-10-27 06:16:00','2025-10-27 06:16:26','100404728320280613265',NULL),(13,16,'Rakshit','+919310897212','dhotepiyush05@gmail.com','256666','',NULL,NULL,'yviMazbNFkzFqu_2eDndEOhqewJpn8e2',1,'2025-10-27 06:32:06','2025-10-27 06:33:02','104625351863567886525',NULL),(14,17,'Piyush','+918306304550','rmdhote3@gmail.com','88996655','',NULL,NULL,'2g_XYTb40OV1McsVhnz64Rl8Zr07lf9H',1,'2025-10-27 13:25:51','2025-10-27 13:26:16','109892512723241426130',NULL),(15,18,'Vikram','+918591196243','vikramkanaujiya67@gmail.com','112233','doctor_photos/1000069209.jpg',NULL,NULL,'U9cQyARvyOtXI_c7rNgS0UHjRQyiBN-2',1,'2025-10-27 13:38:10','2025-10-27 13:38:23','101542516497255841944',NULL),(16,19,'Simran Galani','+917798493048','simrangalani11@gmail.com','82929','doctor_photos/3da64a0c-ac9e-4f48-88a9-128bad0ace38.jpeg',NULL,NULL,'WhTb0Lj2Bl9fDED2otlPMAKkZpBU5XqP',1,'2025-11-03 10:16:08','2025-11-03 10:16:45','101252746157957167386',NULL);
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `field_representative`
--

DROP TABLE IF EXISTS `field_representative`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `field_representative` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `partner_id` bigint NOT NULL,
  `rep_code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `full_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `field_representative_partner_rep_code_unique` (`partner_id`,`rep_code`),
  KEY `field_representative_partner_id_idx` (`partner_id`),
  CONSTRAINT `field_representative_partner_id_fk` FOREIGN KEY (`partner_id`) REFERENCES `partner` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `field_representative`
--

LOCK TABLES `field_representative` WRITE;
/*!40000 ALTER TABLE `field_representative` DISABLE KEYS */;
INSERT INTO `field_representative` VALUES (1,1,'MUM-001','Anita Desai',1,'2025-10-07 09:19:25.373285'),(2,1,'MUM-002','Ravi Patil',1,'2025-10-07 09:19:25.382382'),(3,1,'BLR-101','Meera Krishnan',1,'2025-10-07 09:19:25.390724'),(4,2,'MUM-001','Anita Desai',1,'2025-10-07 10:52:46.607423'),(5,2,'MUM-002','Ravi Patil',1,'2025-10-07 10:52:46.614959'),(6,2,'BLR-101','Meera Krishnan',1,'2025-10-07 10:52:46.622006'),(7,3,'MUM-001','Anita Desai',1,'2025-10-30 05:29:13.382606'),(8,3,'MUM-002','Ravi Patil',1,'2025-10-30 05:29:13.592115'),(9,3,'BLR-101','Meera Krishnan',1,'2025-10-30 05:29:13.805717');
/*!40000 ALTER TABLE `field_representative` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parent`
--

DROP TABLE IF EXISTS `parent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parent` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(120) NOT NULL,
  `whatsapp_e164` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `clinic_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `whatsapp_e164` (`whatsapp_e164`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parent`
--

LOCK TABLES `parent` WRITE;
/*!40000 ALTER TABLE `parent` DISABLE KEYS */;
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
  UNIQUE KEY `registration_token` (`registration_token`),
  KEY `partner_slug_idx` (`slug`),
  KEY `partner_registration_token_idx` (`registration_token`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `partner`
--

LOCK TABLES `partner` WRITE;
/*!40000 ALTER TABLE `partner` DISABLE KEYS */;
INSERT INTO `partner` VALUES (1,'Niomi','niomi','O2Qqa0CFHC85trS-R8vs3DqDRTe-thhb','2025-10-07 09:19:25.361811'),(2,'Khushan','khushan','cXf3GU7P8yHq89zMQO9odbXtd7kQ70NJ','2025-10-07 10:52:46.597326'),(3,'Niomi','niomi-1','AOTQzT1YnW9ISxyVkOZbEtata56dMgko','2025-10-30 05:29:13.257047');
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
  `code` varchar(50) NOT NULL,
  `name` varchar(120) NOT NULL,
  `source_url` varchar(200) NOT NULL,
  `effective_from` date DEFAULT NULL,
  `is_current` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule_version`
--

LOCK TABLES `schedule_version` WRITE;
/*!40000 ALTER TABLE `schedule_version` DISABLE KEYS */;
INSERT INTO `schedule_version` VALUES (2,'IAP-2025','IAP Schedule 2025','',NULL,1,'2025-10-02 22:07:23.500576');
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
  `key_name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `context` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `key` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `key_name` (`key_name`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ui_string`
--

LOCK TABLES `ui_string` WRITE;
/*!40000 ALTER TABLE `ui_string` DISABLE KEYS */;
INSERT INTO `ui_string` VALUES (4,'history.title','Page title','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','history.title','Page title'),(5,'history.note','Top note','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','history.note','Top note'),(6,'btn.update_due','Update button','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','btn.update_due','Update button'),(7,'btn.add_child','Add child button','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','btn.add_child','Add child button'),(8,'btn.back','Back button','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','btn.back','Back button'),(9,'th.vaccine','Table header','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','th.vaccine','Table header'),(10,'th.status','Table header','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','th.status','Table header'),(11,'th.action','Table header','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','th.action','Table header'),(12,'btn.call_clinic','Call button','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','btn.call_clinic','Call button'),(13,'lbl.given_on','Given label','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','lbl.given_on','Given label'),(14,'lbl.due_on','Due label','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','lbl.due_on','Due label'),(15,'status.given','Status given','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','status.given','Status given'),(16,'status.pending','Status pending','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','status.pending','Status pending'),(17,'edu.title','Education title','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','edu.title','Education title'),(18,'edu.lead','Education lead','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','edu.lead','Education lead'),(19,'csv.child_name','CSV header','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','csv.child_name','CSV header'),(20,'csv.date_of_birth','CSV header','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','csv.date_of_birth','CSV header'),(21,'csv.gender','CSV header','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','csv.gender','CSV header');
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
  `ui_string_id` bigint NOT NULL,
  `language_code` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `language` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ui_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_string_language` (`ui_string_id`,`language_code`),
  CONSTRAINT `ui_string_translation_ibfk_1` FOREIGN KEY (`ui_string_id`) REFERENCES `ui_string` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ui_string_translation`
--

LOCK TABLES `ui_string_translation` WRITE;
/*!40000 ALTER TABLE `ui_string_translation` DISABLE KEYS */;
INSERT INTO `ui_string_translation` VALUES (1,4,'en','Vaccination History','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',4),(2,4,'hi','टीकाकरण इतिहास','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',4),(3,4,'bn','টিকাদান ইতিহাস','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',4),(4,4,'ml','വാക്സിനേഷൻ ചരിത്രം','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',4),(5,4,'ta','தடுப்பூசி வரலாறு','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',4),(6,4,'te','వ్యాక్సినేషన్ చరిత్ర','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',4),(7,4,'mr','लसीकरण इतिहास','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',4),(8,4,'kn','ಲಸಿಕೆ ಇತಿಹಾಸ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',4),(9,5,'en','If this is your first visit, click \"Update Due Date\" to enter the doses already given. Once done, only pending vaccines will remain.','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',5),(10,5,'hi','यदि यह आपकी पहली यात्रा है, तो पहले से दी गई खुराक दर्ज करने के लिए \"नियत तारीख अपडेट करें\" पर क्लिक करें। एक बार हो जाने पर, केवल लंबित टीके ही रह जाएंगे।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',5),(11,5,'bn','এটি যদি আপনার প্রথম ভিজিট হয়, তাহলে ইতিমধ্যে দেওয়া ডোজগুলি প্রবেশ করতে \"নির্ধারিত তারিখ আপডেট করুন\" ক্লিক করুন। একবার সম্পন্ন হলে, শুধুমাত্র বাকি টিকাগুলি থাকবে।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',5),(12,5,'ml','ഇത് നിങ്ങളുടെ ആദ്യ സന്ദർശനമാണെങ്കിൽ, ഇതിനകം നൽകിയ ഡോസുകൾ എൻട്രി ചെയ്യാൻ \"നിശ്ചിത തീയതി അപ്ഡേറ്റ് ചെയ്യുക\" ക്ലിക്ക് ചെയ്യുക. പൂർത്തിയായാൽ, ബാക്കിയുള്ള വാക്സിനുകൾ മാത്രം അവശേഷിക്കും।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',5),(13,5,'ta','இது உங்கள் முதல் வருகையாக இருந்தால், ஏற்கனவே கொடுக்கப்பட்ட டோஸ்களை உள்ளிட \"நிர்धாரित தேதியை புதுப்பிக்கவும்\" என்பதை கிளிக் செய்யவும். முடிந்ததும், நிலுவையில் உள்ள தடுப்பூசிகள் மட்டுமே இருக்கும்।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',5),(14,5,'te','ఇది మీ మొదటి సందర్శన అయితే, ఇప్పటికే ఇచ్చిన డోస్‌లను ఎంటర్ చేయడానికి \"నిర్ధారిత తేదీని అప్‌డేట్ చేయండి\" క్లిక్ చేయండి. పూర్తయిన తర్వాత, పెండింగ్‌లో ఉన్న వ్యాక్సిన్‌లు మాత్రమే మిగిలిపోతాయి।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',5),(15,5,'mr','जर ही तुमची पहिली भेट असेल, तर आधीच दिलेले डोस एंटर करण्यासाठी \"निर्धारित तारीख अपडेट करा\" वर क्लिक करा. पूर्ण झाल्यावर, फक्त प्रलंबित लसी राहतील।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',5),(16,5,'kn','ಇದು ನಿಮ್ಮ ಮೊದಲ ಭೇಟಿಯಾಗಿದ್ದರೆ, ಈಗಾಗಲೇ ನೀಡಿದ ಡೋಸ್‌ಗಳನ್ನು ನಮೂದಿಸಲು \"ನಿರ್ಧಾರಿತ ದಿನಾಂಕವನ್ನು ಅಪ್‌ಡೇಟ್ ಮಾಡಿ\" ಕ್ಲಿಕ್ ಮಾಡಿ. ಪೂರ್ಣಗೊಂಡ ನಂತರ, ಬಾಕಿ ಇರುವ ಲಸಿಕೆಗಳು ಮಾತ್ರ ಉಳಿಯುತ್ತವೆ।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',5),(17,6,'en','Update Due Date','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',6),(18,6,'hi','नियत तारीख अपडेट करें','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',6),(19,6,'bn','নির্ধারিত তারিখ আপডেট করুন','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',6),(20,6,'ml','നിശ്ചിത തീയതി അപ്ഡേറ്റ് ചെയ്യുക','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',6),(21,6,'ta','நிர்ধாரित தேதியை புதுப்பிக்கவும்','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',6),(22,6,'te','నిర్ధారిత తేదీని అప్‌డేట్ చేయండి','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',6),(23,6,'mr','निर्धारित तारीख अपडेट करा','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',6),(24,6,'kn','ನಿರ್ಧಾರಿತ ದಿನಾಂಕವನ್ನು ಅಪ್‌ಡೇಟ್ ಮಾಡಿ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',6),(25,7,'en','Add Another Child','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',7),(26,7,'hi','दूसरा बच्चा जोड़ें','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',7),(27,7,'bn','আরেকটি শিশু যোগ করুন','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',7),(28,7,'ml','മറ്റൊരു കുട്ടിയെ ചേർക്കുക','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',7),(29,7,'ta','மற்றொரு குழந்தையை சேர்க்கவும்','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',7),(30,7,'te','మరొక పిల్లవాడిని జోడించండి','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',7),(31,7,'mr','दुसरे मूल जोडा','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',7),(32,7,'kn','ಮತ್ತೊಂದು ಮಗುವನ್ನು ಸೇರಿಸಿ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',7),(33,8,'en','Go Back','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',8),(34,8,'hi','वापस जाएं','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',8),(35,8,'bn','ফিরে যান','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',8),(36,8,'ml','തിരികെ പോകുക','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',8),(37,8,'ta','திரும்பிச் செல்லவும்','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',8),(38,8,'te','వెనుకకు వెళ్ళండి','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',8),(39,8,'mr','परत जा','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',8),(40,8,'kn','ಹಿಂದೆ ಹೋಗಿ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',8),(41,9,'en','Vaccine','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',9),(42,9,'hi','टीका','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',9),(43,9,'bn','টিকা','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',9),(44,9,'ml','വാക്സിൻ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',9),(45,9,'ta','தடுப்பூசி','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',9),(46,9,'te','వ్యాక్సిన్','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',9),(47,9,'mr','लस','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',9),(48,9,'kn','ಲಸಿಕೆ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',9),(49,10,'en','Status','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',10),(50,10,'hi','स्थिति','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',10),(51,10,'bn','অবস্থা','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',10),(52,10,'ml','നില','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',10),(53,10,'ta','நிலை','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',10),(54,10,'te','స్థితి','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',10),(55,10,'mr','स्थिती','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',10),(56,10,'kn','ಸ್ಥಿತಿ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',10),(57,11,'en','Action','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',11),(58,11,'hi','कार्य','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',11),(59,11,'bn','কর্ম','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',11),(60,11,'ml','പ്രവർത്തനം','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',11),(61,11,'ta','செயல்','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',11),(62,11,'te','చర్య','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',11),(63,11,'mr','कृती','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',11),(64,11,'kn','ಕ್ರಿಯೆ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',11),(65,12,'en','Call Clinic','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',12),(66,12,'hi','क्लिनिक को कॉल करें','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',12),(67,12,'bn','ক্লিনিকে কল করুন','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',12),(68,12,'ml','ക്ലിനിക്കിൽ വിളിക്കുക','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',12),(69,12,'ta','மருத்துவமனையை அழைக்கவும்','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',12),(70,12,'te','క్లినిక్‌కు కాల్ చేయండి','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',12),(71,12,'mr','क्लिनिकला कॉल करा','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',12),(72,12,'kn','ಕ್ಲಿನಿಕ್‌ಗೆ ಕರೆ ಮಾಡಿ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',12),(73,13,'en','Given on','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',13),(74,13,'hi','दिया गया','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',13),(75,13,'bn','দেওয়া হয়েছে','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',13),(76,13,'ml','നൽകിയത്','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',13),(77,13,'ta','கொடுக்கப்பட்டது','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',13),(78,13,'te','ఇవ్వబడింది','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',13),(79,13,'mr','दिले गेले','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',13),(80,13,'kn','ನೀಡಲಾಗಿದೆ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',13),(81,14,'en','Due on','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',14),(82,14,'hi','देय तिथि','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',14),(83,14,'bn','নির্ধারিত তারিখ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',14),(84,14,'ml','നിശ്ചിത തീയതി','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',14),(85,14,'ta','நிர்ধாரித்த தேதி','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',14),(86,14,'te','నిర్ధారిత తేదీ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',14),(87,14,'mr','निर्धारित तारीख','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',14),(88,14,'kn','ನಿರ್ಧಾರಿತ ದಿನಾಂಕ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',14),(89,15,'en','Given','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',15),(90,15,'hi','दी गई','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',15),(91,15,'bn','দেওয়া হয়েছে','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',15),(92,15,'ml','നൽകി','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',15),(93,15,'ta','கொடுக்கப்பட்டது','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',15),(94,15,'te','ఇవ్వబడింది','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',15),(95,15,'mr','दिली','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',15),(96,15,'kn','ನೀಡಲಾಗಿದೆ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',15),(97,16,'en','Pending','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',16),(98,16,'hi','लंबित','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',16),(99,16,'bn','বিলম্বিত','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',16),(100,16,'ml','ബാക്കിയുണ്ട്','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',16),(101,16,'ta','நிலுவையில்','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',16),(102,16,'te','పెండింగ్‌లో','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',16),(103,16,'mr','प्रलंबित','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',16),(104,16,'kn','ಬಾಕಿ ಇದೆ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',16),(105,17,'en','Education','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',17),(106,17,'hi','शिक्षा','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',17),(107,17,'bn','শিক্ষা','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',17),(108,17,'ml','വിദ്യാഭ്യാസം','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',17),(109,17,'ta','கல்வி','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',17),(110,17,'te','విద్య','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',17),(111,17,'mr','शिक्षण','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',17),(112,17,'kn','ಶಿಕ್ಷಣ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',17),(113,18,'en','Watch the short video(s) below to learn why this vaccine is important.','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',18),(114,18,'hi','इस टीके का महत्व जानने के लिए नीचे दिए गए छोटे वीडियो देखें।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',18),(115,18,'bn','এই টিকা কেন গুরুত্বপূর্ণ তা জানতে নিচের ছোট ভিডিও(গুলি) দেখুন।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',18),(116,18,'ml','ഈ വാക്സിൻ എന്തുകൊണ്ട് പ്രധാനമാണെന്ന് അറിയാൻ താഴെയുള്ള ചെറിയ വീഡിയോ(കൾ) കാണുക।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',18),(117,18,'ta','இந்த தடுப்பூசி ஏன் முக்கியம் என்பதை அறிய கீழே உள்ள சிறிய வீடியோ(க்களை) பார்க்கவும்।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',18),(118,18,'te','ఈ వ్యాక్సిన్ ఎందుకు ముఖ్యమో తెలుసుకోవడానికి క్రింద ఉన్న చిన్న వీడియో(లను) చూడండి।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',18),(119,18,'mr','ही लस का महत्वाची आहे हे जाणून घेण्यासाठी खालील छोटे व्हिडिओ पहा।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',18),(120,18,'kn','ಈ ಲಸಿಕೆ ಏಕೆ ಮುಖ್ಯವಾಗಿದೆ ಎಂಬುದನ್ನು ತಿಳಿಯಲು ಕೆಳಗಿನ ಚಿಕ್ಕ ವೀಡಿಯೋ(ಗಳನ್ನು) ನೋಡಿ।','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',18),(121,19,'en','Child Name','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',19),(122,19,'hi','बच्चे का नाम','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',19),(123,19,'bn','শিশুর নাম','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',19),(124,19,'ml','കുട്ടിയുടെ പേര്','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',19),(125,19,'ta','குழந்தையின் பெயர்','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',19),(126,19,'te','పిల్లవాడి పేరు','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',19),(127,19,'mr','मुलाचे नाव','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',19),(128,19,'kn','ಮಗುವಿನ ಹೆಸರು','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',19),(129,20,'en','Date of Birth','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',20),(130,20,'hi','जन्म तिथि','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',20),(131,20,'bn','জন্ম তারিখ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',20),(132,20,'ml','ജനനത്തീയതി','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',20),(133,20,'ta','பிறந்த தேதி','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',20),(134,20,'te','పుట్టిన తేదీ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',20),(135,20,'mr','जन्म तारीख','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',20),(136,20,'kn','ಹುಟ್ಟಿದ ದಿನಾಂಕ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',20),(137,21,'en','Gender','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','en',21),(138,21,'hi','लिंग','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','hi',21),(139,21,'bn','লিঙ্গ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','bn',21),(140,21,'ml','ലിംഗം','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ml',21),(141,21,'ta','பாலினம்','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','ta',21),(142,21,'te','లింగం','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','te',21),(143,21,'mr','लिंग','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','mr',21),(144,21,'kn','ಲಿಂಗ','2025-10-07 12:20:24.577676','2025-10-07 12:20:24.577676','kn',21);
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
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `aliases` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `schedule_version_id` bigint NOT NULL,
  `education_parent_url` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `education_doctor_vimeo_url` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `vaccine_schedule_version_id_code_80ed188e_uniq` (`schedule_version_id`,`code`),
  KEY `vaccine_schedul_e962e1_idx` (`schedule_version_id`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vaccine`
--

LOCK TABLES `vaccine` WRITE;
/*!40000 ALTER TABLE `vaccine` DISABLE KEYS */;
INSERT INTO `vaccine` VALUES (19,'bcg','BCG','',1,'','2025-10-02 22:07:23.508503',2,'',''),(20,'hep-b','Hep B','',1,'','2025-10-02 22:07:23.518119',2,'',''),(21,'opv','OPV','',1,'','2025-10-02 22:07:23.525995',2,'',''),(22,'dtwp-dtap','DTwP / DTaP','',1,'','2025-10-02 22:07:23.527774',2,'',''),(23,'hib','Hib','',1,'','2025-10-02 22:07:23.535658',2,'',''),(24,'ipv','IPV','',1,'','2025-10-02 22:07:23.544365',2,'',''),(25,'pcv','PCV','',1,'','2025-10-02 22:07:23.555530',2,'',''),(26,'rota','Rota','',1,'','2025-10-02 22:07:23.562670',2,'',''),(27,'rota-3','Rota-3*','',1,'','2025-10-02 22:07:23.569848',2,'',''),(28,'influenza','Influenza','',1,'','2025-10-02 22:07:23.571127',2,'',''),(29,'typhoid-conjugate-vaccine','Typhoid Conjugate Vaccine','',1,'','2025-10-02 22:07:23.584921',2,'',''),(30,'mmr','MMR','',1,'','2025-10-02 22:07:23.597756',2,'',''),(31,'hepatitis-a','Hepatitis A','',1,'','2025-10-02 22:07:23.605782',2,'',''),(32,'varicella','Varicella','',1,'','2025-10-02 22:07:23.612711',2,'',''),(33,'hepatitis-a-2','Hepatitis A-2**','',1,'','2025-10-02 22:07:23.620167',2,'',''),(34,'hpv','HPV','',1,'','2025-10-02 22:07:23.629682',2,'',''),(35,'tdap-td','Tdap / Td','',1,'','2025-10-02 22:07:23.635344',2,'',''),(36,'annual-influenza-vaccine','Annual Influenza Vaccine','',1,'','2025-10-02 22:07:23.639250',2,'','');
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
  `sequence_index` smallint unsigned NOT NULL,
  `dose_label` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `eligible_gender` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `min_offset_days` int unsigned NOT NULL,
  `max_offset_days` int unsigned DEFAULT NULL,
  `is_booster` tinyint(1) NOT NULL,
  `notes` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `previous_dose_id` bigint DEFAULT NULL,
  `schedule_version_id` bigint NOT NULL,
  `vaccine_id` bigint NOT NULL,
  `anchor_policy` varchar(1) COLLATE utf8mb4_unicode_ci DEFAULT 'L',
  `series_key` varchar(32) COLLATE utf8mb4_unicode_ci DEFAULT '',
  `series_seq` smallint unsigned DEFAULT '1',
  PRIMARY KEY (`id`),
  KEY `vaccine_dos_schedul_5264c4_idx` (`schedule_version_id`,`vaccine_id`,`sequence_index`),
  KEY `vaccine_dos_previou_fb1c9d_idx` (`previous_dose_id`),
  CONSTRAINT `vaccine_dose_chk_1` CHECK ((`sequence_index` >= 0)),
  CONSTRAINT `vaccine_dose_chk_2` CHECK ((`min_offset_days` >= 0)),
  CONSTRAINT `vaccine_dose_chk_3` CHECK ((`max_offset_days` >= 0)),
  CONSTRAINT `vd_offset_range_valid` CHECK (((`max_offset_days` is null) or (`max_offset_days` >= `min_offset_days`)))
) ENGINE=InnoDB AUTO_INCREMENT=98 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vaccine_dose`
--

LOCK TABLES `vaccine_dose` WRITE;
/*!40000 ALTER TABLE `vaccine_dose` DISABLE KEYS */;
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
  `language` varchar(5) NOT NULL,
  `title` varchar(200) NOT NULL,
  `video_url` varchar(200) NOT NULL,
  `platform` varchar(20) NOT NULL,
  `rank` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `vaccine_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vaccine_id` (`vaccine_id`,`video_url`),
  KEY `vaccine_edu_vaccine_f09e3c_idx` (`vaccine_id`,`rank`),
  KEY `vaccine_edu_is_acti_7524ff_idx` (`is_active`),
  KEY `vaccine_education_doctor_language_idx` (`language`),
  CONSTRAINT `vaccine_education_doctor_vaccine_id_fk` FOREIGN KEY (`vaccine_id`) REFERENCES `vaccine` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vaccine_education_doctor`
--

LOCK TABLES `vaccine_education_doctor` WRITE;
/*!40000 ALTER TABLE `vaccine_education_doctor` DISABLE KEYS */;
INSERT INTO `vaccine_education_doctor` VALUES (1,'en','BCG Vaccine -','https://player.vimeo.com/video/949456495?h=15d524fba8&amp','vimeo',1,1,'2025-10-07 07:33:37.879572','2025-10-07 07:35:04.849346',19),(2,'en','Hepatitis B Vaccine -','https://player.vimeo.com/video/949456531?h=69e2e95886&amp','vimeo',1,1,'2025-10-07 07:33:37.886313','2025-10-07 07:35:04.963272',20),(3,'en','Polio Vaccine -','https://player.vimeo.com/video/949457948?h=5e2715fda5&amp','vimeo',1,1,'2025-10-07 07:33:37.893293','2025-10-07 07:35:04.859144',21),(4,'en','DTwP/DTaP Vaccine -','https://player.vimeo.com/video/949456505?h=f16d540e8a&amp','vimeo',1,1,'2025-10-07 07:33:37.899687','2025-10-07 07:35:05.053670',22),(5,'en','Hib Vaccine -','https://player.vimeo.com/video/949456549?h=18680bedba&amp','vimeo',1,1,'2025-10-07 07:33:37.900137','2025-10-07 07:35:05.032703',23),(6,'en','Polio Vaccine -','https://player.vimeo.com/video/949457948?h=5e2715fda5&amp','vimeo',1,1,'2025-10-07 07:33:37.909575','2025-10-07 07:35:05.063379',24),(7,'en','PCV Vaccine -','https://player.vimeo.com/video/949457908?h=0e4b1c5108&amp','vimeo',1,1,'2025-10-07 07:33:37.923497','2025-10-07 07:35:05.011481',25),(8,'en','Rotavirus Vaccine -','https://player.vimeo.com/video/949480723?h=aa02736e7a&amp','vimeo',1,1,'2025-10-07 07:33:37.927946','2025-10-07 07:35:04.939126',26),(9,'en','Rotavirus Vaccine -','https://player.vimeo.com/video/949480723?h=aa02736e7a&amp','vimeo',1,1,'2025-10-07 07:33:38.004345','2025-10-07 07:35:04.974573',27),(10,'en','Influenza Vaccine -','https://player.vimeo.com/video/949456654?h=03c752baab&amp','vimeo',1,1,'2025-10-07 07:33:38.010842','2025-10-07 07:35:04.985745',28),(11,'en','Typhoid Vaccine -','https://player.vimeo.com/video/949457995?h=ab4e507a32&amp','vimeo',1,1,'2025-10-07 07:33:38.021195','2025-10-07 07:35:04.992026',29),(12,'en','MMR Vaccine -','https://player.vimeo.com/video/949457887?h=07623d3d60&amp','vimeo',1,1,'2025-10-07 07:33:38.028710','2025-10-07 07:35:05.068469',30),(13,'en','Hepatitis A Vaccine -','https://player.vimeo.com/video/949456529?h=ce857f59b2&amp','vimeo',1,1,'2025-10-07 07:33:38.032149','2025-10-07 07:35:05.004927',31),(14,'en','Varicella Vaccine -','https://player.vimeo.com/video/949458012?h=2c421ad5f4&amp','vimeo',1,1,'2025-10-07 07:33:38.052954','2025-10-07 07:35:05.049484',32),(15,'en','Hepatitis A Vaccine -','https://player.vimeo.com/video/949456529?h=ce857f59b2&amp','vimeo',1,1,'2025-10-07 07:33:38.081634','2025-10-07 07:35:05.046633',33),(16,'en','HPV Vaccine -','https://player.vimeo.com/video/949456621?h=9dda6ebded&amp','vimeo',1,1,'2025-10-07 07:33:38.110061','2025-10-07 07:35:05.074377',34),(17,'en','Tdap/ Td Vaccine -','https://player.vimeo.com/video/949457971?h=77df860042&amp','vimeo',1,1,'2025-10-07 07:33:38.118476','2025-10-07 07:35:05.081872',35),(18,'en','Influenza Vaccine -','https://player.vimeo.com/video/949456654?h=03c752baab&amp','vimeo',1,1,'2025-10-07 07:33:38.123901','2025-10-07 07:35:05.088872',36);
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
  `language` varchar(5) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `video_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `platform` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `thumbnail_url` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `duration_seconds` int unsigned DEFAULT NULL,
  `rank` smallint unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `vaccine_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vaccine_id` (`vaccine_id`,`language`,`video_url`),
  KEY `vaccine_edu_vaccine_a5e22a_idx` (`vaccine_id`,`language`,`rank`),
  KEY `vaccine_edu_is_acti_14108b_idx` (`is_active`),
  KEY `vaccine_education_patient_language_idx` (`language`),
  CONSTRAINT `vaccine_education_patient_vaccine_id_fk` FOREIGN KEY (`vaccine_id`) REFERENCES `vaccine` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=145 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vaccine_education_patient`
--

LOCK TABLES `vaccine_education_patient` WRITE;
/*!40000 ALTER TABLE `vaccine_education_patient` DISABLE KEYS */;
INSERT INTO `vaccine_education_patient` VALUES (1,'en','BCG Vaccine -','https://www.youtube.com/watch?v=_eQYO400CeI','youtube','',NULL,1,1,'2025-10-07 07:33:35.670737','2025-10-07 07:35:02.799114',19),(2,'en','Hepatitis B Vaccine -','https://www.youtube.com/watch?v=RU_RJ-SkNkI','youtube','',NULL,1,1,'2025-10-07 07:33:35.678184','2025-10-07 07:35:02.918379',20),(3,'en','Polio Vaccine -','https://www.youtube.com/watch?v=60WK_NrKZgM','youtube','',NULL,1,1,'2025-10-07 07:33:35.686112','2025-10-07 07:35:02.818591',21),(4,'en','DTwP/DTaP Vaccine -','https://www.youtube.com/watch?v=QZoGZsHEks0','youtube','',NULL,1,1,'2025-10-07 07:33:35.692106','2025-10-07 07:35:03.032930',22),(5,'en','Hib Vaccine -','https://www.youtube.com/watch?v=aN40_AqNMs4','youtube','',NULL,1,1,'2025-10-07 07:33:35.699397','2025-10-07 07:35:03.007125',23),(6,'en','Polio Vaccine -','https://www.youtube.com/watch?v=60WK_NrKZgM','youtube','',NULL,1,1,'2025-10-07 07:33:35.707546','2025-10-07 07:35:03.040309',24),(7,'en','PCV Vaccine -','https://www.youtube.com/watch?v=2PA5VNcX0Sw','youtube','',NULL,1,1,'2025-10-07 07:33:35.719904','2025-10-07 07:35:02.984211',25),(8,'en','Rotavirus Vaccine -','https://www.youtube.com/watch?v=hyZghnV1SyM','youtube','',NULL,1,1,'2025-10-07 07:33:35.761628','2025-10-07 07:35:02.894275',26),(9,'en','Rotavirus Vaccine -','https://www.youtube.com/watch?v=hyZghnV1SyM','youtube','',NULL,1,1,'2025-10-07 07:33:35.838992','2025-10-07 07:35:02.935669',27),(10,'en','Influenza Vaccine -','https://www.youtube.com/watch?v=rr6fJSRVdbc','youtube','',NULL,1,1,'2025-10-07 07:33:35.844721','2025-10-07 07:35:02.949789',28),(11,'en','Typhoid Vaccine -','https://youtu.be/JCx2W16Q_Do','youtube','',NULL,1,1,'2025-10-07 07:33:35.851654','2025-10-07 07:35:02.963395',29),(12,'en','MMR Vaccine -','https://www.youtube.com/watch?v=gDv2ALsa-KE','youtube','',NULL,1,1,'2025-10-07 07:33:35.865057','2025-10-07 07:35:03.046269',30),(13,'en','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=exGZaLv3bKg','youtube','',NULL,1,1,'2025-10-07 07:33:35.871238','2025-10-07 07:35:02.977559',31),(14,'en','Varicella Vaccine -','https://www.youtube.com/watch?v=Qtb9E5wMp6U','youtube','',NULL,1,1,'2025-10-07 07:33:35.889570','2025-10-07 07:35:03.026067',32),(15,'en','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=exGZaLv3bKg','youtube','',NULL,1,1,'2025-10-07 07:33:35.914157','2025-10-07 07:35:03.021130',33),(16,'en','HPV Vaccine -','https://www.youtube.com/watch?v=XYDS8J1nqw0','youtube','',NULL,1,1,'2025-10-07 07:33:35.947377','2025-10-07 07:35:03.053763',34),(17,'en','Tdap/ Td Vaccine -','https://www.youtube.com/watch?v=eXIFZ5KJBfY','youtube','',NULL,1,1,'2025-10-07 07:33:35.949456','2025-10-07 07:35:03.060220',35),(18,'en','Influenza Vaccine -','https://www.youtube.com/watch?v=rr6fJSRVdbc','youtube','',NULL,1,1,'2025-10-07 07:33:35.956488','2025-10-07 07:35:03.067086',36),(19,'hi','BCG Vaccine -','https://www.youtube.com/watch?v=brmzWb_9td8','youtube','',NULL,1,1,'2025-10-07 07:33:35.962748','2025-10-07 07:35:03.071318',19),(20,'hi','Hepatitis B Vaccine -','https://www.youtube.com/watch?v=FOHBUEtED1A','youtube','',NULL,1,1,'2025-10-07 07:33:35.971737','2025-10-07 07:35:03.184253',20),(21,'hi','Polio Vaccine -','https://www.youtube.com/watch?v=VmjTWdo5J7o','youtube','',NULL,1,1,'2025-10-07 07:33:35.976793','2025-10-07 07:35:03.081552',21),(22,'hi','DTwP/DTaP Vaccine -','https://www.youtube.com/watch?v=-nvqEoTgYME','youtube','',NULL,1,1,'2025-10-07 07:33:35.983649','2025-10-07 07:35:03.282879',22),(23,'hi','Hib Vaccine -','https://www.youtube.com/watch?v=zSsHvuq6hhs','youtube','',NULL,1,1,'2025-10-07 07:33:35.990527','2025-10-07 07:35:03.257038',23),(24,'hi','Polio Vaccine -','https://www.youtube.com/watch?v=VmjTWdo5J7o','youtube','',NULL,1,1,'2025-10-07 07:33:35.997542','2025-10-07 07:35:03.288771',24),(25,'hi','PCV Vaccine -','https://www.youtube.com/watch?v=sV8JtOMwtt4','youtube','',NULL,1,1,'2025-10-07 07:33:36.010884','2025-10-07 07:35:03.231698',25),(26,'hi','Rotavirus Vaccine -','https://www.youtube.com/watch?v=xWDBsVJno3U','youtube','',NULL,1,1,'2025-10-07 07:33:36.016797','2025-10-07 07:35:03.157955',26),(27,'hi','Rotavirus Vaccine -','https://www.youtube.com/watch?v=xWDBsVJno3U','youtube','',NULL,1,1,'2025-10-07 07:33:36.089306','2025-10-07 07:35:03.196874',27),(28,'hi','Influenza Vaccine -','https://www.youtube.com/watch?v=9UiR6RJQo78','youtube','',NULL,1,1,'2025-10-07 07:33:36.096784','2025-10-07 07:35:03.206458',28),(29,'hi','Typhoid Vaccine -','https://www.youtube.com/watch?v=3sM45uCgSnU','youtube','',NULL,1,1,'2025-10-07 07:33:36.108498','2025-10-07 07:35:03.213472',29),(30,'hi','MMR Vaccine -','https://www.youtube.com/watch?v=JIHdiWIrfms','youtube','',NULL,1,1,'2025-10-07 07:33:36.116525','2025-10-07 07:35:03.292107',30),(31,'hi','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=iSGilrqVbdQ','youtube','',NULL,1,1,'2025-10-07 07:33:36.124122','2025-10-07 07:35:03.226831',31),(32,'hi','Varicella Vaccine -','https://www.youtube.com/watch?v=A0I978oLRs8','youtube','',NULL,1,1,'2025-10-07 07:33:36.142854','2025-10-07 07:35:03.276038',32),(33,'hi','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=iSGilrqVbdQ','youtube','',NULL,1,1,'2025-10-07 07:33:36.166613','2025-10-07 07:35:03.268948',33),(34,'hi','HPV Vaccine -','https://www.youtube.com/watch?v=AR4QKd7fnSY','youtube','',NULL,1,1,'2025-10-07 07:33:36.199439','2025-10-07 07:35:03.299535',34),(35,'hi','Tdap/ Td Vaccine -','https://www.youtube.com/watch?v=gH87V2nsBPA','youtube','',NULL,1,1,'2025-10-07 07:33:36.206367','2025-10-07 07:35:03.307105',35),(36,'hi','Influenza Vaccine -','https://www.youtube.com/watch?v=9UiR6RJQo78','youtube','',NULL,1,1,'2025-10-07 07:33:36.212823','2025-10-07 07:35:03.310632',36),(37,'mr','BCG Vaccine -','https://www.youtube.com/watch?v=VpcK2e3136M','youtube','',NULL,1,1,'2025-10-07 07:33:36.219194','2025-10-07 07:35:03.318673',19),(38,'mr','Hepatitis B Vaccine -','https://www.youtube.com/watch?v=lvbIl7ZY4Qs','youtube','',NULL,1,1,'2025-10-07 07:33:36.224489','2025-10-07 07:35:03.435720',20),(39,'mr','Polio Vaccine -','https://www.youtube.com/watch?v=bAunAm4lIto','youtube','',NULL,1,1,'2025-10-07 07:33:36.232356','2025-10-07 07:35:03.331477',21),(40,'mr','DTwP/DTaP Vaccine -','https://youtu.be/vo0zZeZUhxE','youtube','',NULL,1,1,'2025-10-07 07:33:36.238754','2025-10-07 07:35:03.535666',22),(41,'mr','Hib Vaccine -','https://www.youtube.com/watch?v=0RkS3x02iMo','youtube','',NULL,1,1,'2025-10-07 07:33:36.240519','2025-10-07 07:35:03.512099',23),(42,'mr','Polio Vaccine -','https://www.youtube.com/watch?v=bAunAm4lIto','youtube','',NULL,1,1,'2025-10-07 07:33:36.249528','2025-10-07 07:35:03.539780',24),(43,'mr','PCV Vaccine -','https://www.youtube.com/watch?v=9VeFfucurtI','youtube','',NULL,1,1,'2025-10-07 07:33:36.261412','2025-10-07 07:35:03.485825',25),(44,'mr','Rotavirus Vaccine -','https://www.youtube.com/watch?v=2ntZkI8ne-s','youtube','',NULL,1,1,'2025-10-07 07:33:36.268311','2025-10-07 07:35:03.408053',26),(45,'mr','Rotavirus Vaccine -','https://www.youtube.com/watch?v=2ntZkI8ne-s','youtube','',NULL,1,1,'2025-10-07 07:33:36.344701','2025-10-07 07:35:03.449605',27),(46,'mr','Influenza Vaccine -','https://www.youtube.com/watch?v=IB82kgAuz_c','youtube','',NULL,1,1,'2025-10-07 07:33:36.351167','2025-10-07 07:35:03.456542',28),(47,'mr','Typhoid Vaccine -','https://www.youtube.com/watch?v=BRoffRhh6RA','youtube','',NULL,1,1,'2025-10-07 07:33:36.365042','2025-10-07 07:35:03.468444',29),(48,'mr','MMR Vaccine -','https://www.youtube.com/watch?v=Nf0Qmk7FkTo','youtube','',NULL,1,1,'2025-10-07 07:33:36.371280','2025-10-07 07:35:03.549348',30),(49,'mr','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=PgJY56sb3PA','youtube','',NULL,1,1,'2025-10-07 07:33:36.374602','2025-10-07 07:35:03.477442',31),(50,'mr','Varicella Vaccine -','https://www.youtube.com/watch?v=Q59x2kIPf3s','youtube','',NULL,1,1,'2025-10-07 07:33:36.393405','2025-10-07 07:35:03.527053',32),(51,'mr','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=PgJY56sb3PA','youtube','',NULL,1,1,'2025-10-07 07:33:36.421098','2025-10-07 07:35:03.523650',33),(52,'mr','HPV Vaccine -','https://www.youtube.com/watch?v=hDW63Iw0dm0','youtube','',NULL,1,1,'2025-10-07 07:33:36.450027','2025-10-07 07:35:03.553700',34),(53,'mr','Tdap/ Td Vaccine -','https://www.youtube.com/watch?v=25JBK2gimHk','youtube','',NULL,1,1,'2025-10-07 07:33:36.456443','2025-10-07 07:35:03.560686',35),(54,'mr','Influenza Vaccine -','https://www.youtube.com/watch?v=IB82kgAuz_c','youtube','',NULL,1,1,'2025-10-07 07:33:36.462787','2025-10-07 07:35:03.567616',36),(55,'ml','BCG Vaccine -','https://www.youtube.com/watch?v=oyAzYh-hIN4','youtube','',NULL,1,1,'2025-10-07 07:33:36.471245','2025-10-07 07:35:03.573781',19),(56,'ml','Hepatitis B Vaccine -','https://www.youtube.com/watch?v=FjO71AdoRFo','youtube','',NULL,1,1,'2025-10-07 07:33:36.477349','2025-10-07 07:35:03.685624',20),(57,'ml','Polio Vaccine -','https://www.youtube.com/watch?v=9D7pMl5fXRQ','youtube','',NULL,1,1,'2025-10-07 07:33:36.485921','2025-10-07 07:35:03.586023',21),(58,'ml','DTwP/DTaP Vaccine -','https://www.youtube.com/watch?v=xT4-gkohKOg','youtube','',NULL,1,1,'2025-10-07 07:33:36.490637','2025-10-07 07:35:03.789904',22),(59,'ml','Hib Vaccine -','https://www.youtube.com/watch?v=RpHS_6ESr6I','youtube','',NULL,1,1,'2025-10-07 07:33:36.499737','2025-10-07 07:35:03.761983',23),(60,'ml','Polio Vaccine -','https://www.youtube.com/watch?v=9D7pMl5fXRQ','youtube','',NULL,1,1,'2025-10-07 07:33:36.504668','2025-10-07 07:35:03.789904',24),(61,'ml','PCV Vaccine -','https://www.youtube.com/watch?v=mqq4-oPRXbw','youtube','',NULL,1,1,'2025-10-07 07:33:36.518288','2025-10-07 07:35:03.738873',25),(62,'ml','Rotavirus Vaccine -','https://www.youtube.com/watch?v=lmpnLd-TGbU','youtube','',NULL,1,1,'2025-10-07 07:33:36.525284','2025-10-07 07:35:03.658112',26),(63,'ml','Rotavirus Vaccine -','https://www.youtube.com/watch?v=lmpnLd-TGbU','youtube','',NULL,1,1,'2025-10-07 07:33:36.631952','2025-10-07 07:35:03.699646',27),(64,'ml','Influenza Vaccine -','https://www.youtube.com/watch?v=SThjDkZfiVM','youtube','',NULL,1,1,'2025-10-07 07:33:36.646713','2025-10-07 07:35:03.712915',28),(65,'ml','Typhoid Vaccine -','https://www.youtube.com/watch?v=5M6GG5wmHME','youtube','',NULL,1,1,'2025-10-07 07:33:36.666642','2025-10-07 07:35:03.718558',29),(66,'ml','MMR Vaccine -','https://www.youtube.com/watch?v=qOcr_QlZdXk','youtube','',NULL,1,1,'2025-10-07 07:33:36.677541','2025-10-07 07:35:03.803245',30),(67,'ml','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=P2NlAlA-7ZA','youtube','',NULL,1,1,'2025-10-07 07:33:36.686005','2025-10-07 07:35:03.731620',31),(68,'ml','Varicella Vaccine -','https://www.youtube.com/watch?v=X1du9nWmhI0','youtube','',NULL,1,1,'2025-10-07 07:33:36.708430','2025-10-07 07:35:03.783005',32),(69,'ml','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=P2NlAlA-7ZA','youtube','',NULL,1,1,'2025-10-07 07:33:36.734507','2025-10-07 07:35:03.776593',33),(70,'ml','HPV Vaccine -','https://www.youtube.com/watch?v=7DBl-Q4zTrM','youtube','',NULL,1,1,'2025-10-07 07:33:36.767413','2025-10-07 07:35:03.806714',34),(71,'ml','Tdap/ Td Vaccine -','https://www.youtube.com/watch?v=48bre88FvaQ','youtube','',NULL,1,1,'2025-10-07 07:33:36.773897','2025-10-07 07:35:03.810934',35),(72,'ml','Influenza Vaccine -','https://www.youtube.com/watch?v=SThjDkZfiVM','youtube','',NULL,1,1,'2025-10-07 07:33:36.775315','2025-10-07 07:35:03.821489',36),(73,'te','BCG Vaccine -','https://www.youtube.com/watch?v=MkeuXBDM5XE','youtube','',NULL,1,1,'2025-10-07 07:33:36.785964','2025-10-07 07:35:03.826687',19),(74,'te','Hepatitis B Vaccine -','https://www.youtube.com/watch?v=CdyqusA3y7g','youtube','',NULL,1,1,'2025-10-07 07:33:36.789186','2025-10-07 07:35:03.942628',20),(75,'te','Polio Vaccine -','https://www.youtube.com/watch?v=XWInzB578GY','youtube','',NULL,1,1,'2025-10-07 07:33:36.799273','2025-10-07 07:35:03.839093',21),(76,'te','DTwP/DTaP Vaccine -','https://www.youtube.com/watch?v=pDJR09etnQA','youtube','',NULL,1,1,'2025-10-07 07:33:36.803180','2025-10-07 07:35:04.046252',22),(77,'te','Hib Vaccine -','https://www.youtube.com/watch?v=ehYm8aij1YE','youtube','',NULL,1,1,'2025-10-07 07:33:36.810088','2025-10-07 07:35:04.021069',23),(78,'te','Polio Vaccine -','https://www.youtube.com/watch?v=XWInzB578GY','youtube','',NULL,1,1,'2025-10-07 07:33:36.818571','2025-10-07 07:35:04.053185',24),(79,'te','PCV Vaccine -','https://www.youtube.com/watch?v=0ivQ0wpLLxs','youtube','',NULL,1,1,'2025-10-07 07:33:36.831870','2025-10-07 07:35:03.998174',25),(80,'te','Rotavirus Vaccine -','https://www.youtube.com/watch?v=hTK6QhceQes','youtube','',NULL,1,1,'2025-10-07 07:33:36.838697','2025-10-07 07:35:03.914388',26),(81,'te','Rotavirus Vaccine -','https://www.youtube.com/watch?v=hTK6QhceQes','youtube','',NULL,1,1,'2025-10-07 07:33:36.917100','2025-10-07 07:35:03.956509',27),(82,'te','Influenza Vaccine -','https://www.youtube.com/watch?v=lrURICX4xr4','youtube','',NULL,1,1,'2025-10-07 07:33:36.923470','2025-10-07 07:35:03.968347',28),(83,'te','Typhoid Vaccine -','https://www.youtube.com/watch?v=MkeuXBDM5XE','youtube','',NULL,1,1,'2025-10-07 07:33:36.936028','2025-10-07 07:35:03.974561',29),(84,'te','MMR Vaccine -','https://www.youtube.com/watch?v=CrmEVKawmlU','youtube','',NULL,1,1,'2025-10-07 07:33:36.941950','2025-10-07 07:35:04.056628',30),(85,'te','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=a6DggiSTKoE','youtube','',NULL,1,1,'2025-10-07 07:33:36.949426','2025-10-07 07:35:03.988210',31),(86,'te','Varicella Vaccine -','https://www.youtube.com/watch?v=Y5_0LnaXLDY','youtube','',NULL,1,1,'2025-10-07 07:33:36.997570','2025-10-07 07:35:04.039699',32),(87,'te','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=a6DggiSTKoE','youtube','',NULL,1,1,'2025-10-07 07:33:37.021261','2025-10-07 07:35:04.032910',33),(88,'te','HPV Vaccine -','https://www.youtube.com/watch?v=boj9a95yO1Y','youtube','',NULL,1,1,'2025-10-07 07:33:37.053258','2025-10-07 07:35:04.060584',34),(89,'te','Tdap/ Td Vaccine -','https://www.youtube.com/watch?v=vmNGp71cL8c','youtube','',NULL,1,1,'2025-10-07 07:33:37.060003','2025-10-07 07:35:04.071113',35),(90,'te','Influenza Vaccine -','https://www.youtube.com/watch?v=lrURICX4xr4','youtube','',NULL,1,1,'2025-10-07 07:33:37.067181','2025-10-07 07:35:04.076889',36),(91,'bn','BCG Vaccine -','https://www.youtube.com/watch?v=AdWYHsUAo7o','youtube','',NULL,1,1,'2025-10-07 07:33:37.074470','2025-10-07 07:35:04.081885',19),(92,'bn','Hepatitis B Vaccine -','https://www.youtube.com/watch?v=vDts5jV97ng','youtube','',NULL,1,1,'2025-10-07 07:33:37.081766','2025-10-07 07:35:04.192575',20),(93,'bn','Polio Vaccine -','https://www.youtube.com/watch?v=LqYx0qaZi-4','youtube','',NULL,1,1,'2025-10-07 07:33:37.088982','2025-10-07 07:35:04.095404',21),(94,'bn','DTwP/DTaP Vaccine -','https://www.youtube.com/watch?v=-Q8WNyPdE6k','youtube','',NULL,1,1,'2025-10-07 07:33:37.094727','2025-10-07 07:35:04.299576',22),(95,'bn','Hib Vaccine -','https://www.youtube.com/watch?v=Vr_BkZX_36Y','youtube','',NULL,1,1,'2025-10-07 07:33:37.101573','2025-10-07 07:35:04.269987',23),(96,'bn','Polio Vaccine -','https://www.youtube.com/watch?v=LqYx0qaZi-4','youtube','',NULL,1,1,'2025-10-07 07:33:37.108062','2025-10-07 07:35:04.306361',24),(97,'bn','PCV Vaccine -','https://www.youtube.com/watch?v=QP55NA8B05o','youtube','',NULL,1,1,'2025-10-07 07:33:37.121201','2025-10-07 07:35:04.241279',25),(98,'bn','Rotavirus Vaccine -','https://www.youtube.com/watch?v=mkPUQQH10PI','youtube','',NULL,1,1,'2025-10-07 07:33:37.124579','2025-10-07 07:35:04.168387',26),(99,'bn','Rotavirus Vaccine -','https://www.youtube.com/watch?v=mkPUQQH10PI','youtube','',NULL,1,1,'2025-10-07 07:33:37.199115','2025-10-07 07:35:04.206497',27),(100,'bn','Influenza Vaccine -','https://www.youtube.com/watch?v=TrdLY73VbTQ','youtube','',NULL,1,1,'2025-10-07 07:33:37.205979','2025-10-07 07:35:04.216311',28),(101,'bn','Typhoid Vaccine -','https://www.youtube.com/watch?v=2ta4OSxlrYU','youtube','',NULL,1,1,'2025-10-07 07:33:37.221138','2025-10-07 07:35:04.221384',29),(102,'bn','MMR Vaccine -','https://www.youtube.com/watch?v=SgJF9aPukOI','youtube','',NULL,1,1,'2025-10-07 07:33:37.226590','2025-10-07 07:35:04.312368',30),(103,'bn','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=bbXTKslALbA','youtube','',NULL,1,1,'2025-10-07 07:33:37.233577','2025-10-07 07:35:04.235924',31),(104,'bn','Varicella Vaccine -','https://www.youtube.com/watch?v=lnoNYe1gQZc','youtube','',NULL,1,1,'2025-10-07 07:33:37.253948','2025-10-07 07:35:04.292095',32),(105,'bn','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=bbXTKslALbA','youtube','',NULL,1,1,'2025-10-07 07:33:37.275341','2025-10-07 07:35:04.284986',33),(106,'bn','HPV Vaccine -','https://www.youtube.com/watch?v=CRLKqWu7fGc','youtube','',NULL,1,1,'2025-10-07 07:33:37.309965','2025-10-07 07:35:04.318474',34),(107,'bn','Tdap/ Td Vaccine -','https://youtu.be/OUWVfAwdgDY','youtube','',NULL,1,1,'2025-10-07 07:33:37.316952','2025-10-07 07:35:04.324517',35),(108,'bn','Influenza Vaccine -','https://www.youtube.com/watch?v=TrdLY73VbTQ','youtube','',NULL,1,1,'2025-10-07 07:33:37.321061','2025-10-07 07:35:04.331928',36),(109,'kn','BCG Vaccine -','https://www.youtube.com/watch?v=FCtWHkvAFds','youtube','',NULL,1,1,'2025-10-07 07:33:37.326508','2025-10-07 07:35:04.339956',19),(110,'kn','Hepatitis B Vaccine -','https://www.youtube.com/watch?v=W-9nPjdxkZQ','youtube','',NULL,1,1,'2025-10-07 07:33:37.335808','2025-10-07 07:35:04.450052',20),(111,'kn','Polio Vaccine -','https://www.youtube.com/watch?v=xX1iqkxlQFM','youtube','',NULL,1,1,'2025-10-07 07:33:37.342156','2025-10-07 07:35:04.352757',21),(112,'kn','DTwP/DTaP Vaccine -','https://www.youtube.com/watch?v=Tqw66Myx_X4','youtube','',NULL,1,1,'2025-10-07 07:33:37.349331','2025-10-07 07:35:04.549316',22),(113,'kn','Hib Vaccine -','https://www.youtube.com/watch?v=BXYYW4Sx_50','youtube','',NULL,1,1,'2025-10-07 07:33:37.351617','2025-10-07 07:35:04.525949',23),(114,'kn','Polio Vaccine -','https://www.youtube.com/watch?v=xX1iqkxlQFM','youtube','',NULL,1,1,'2025-10-07 07:33:37.361051','2025-10-07 07:35:04.557168',24),(115,'kn','PCV Vaccine -','https://www.youtube.com/watch?v=JaZvUnav5fk','youtube','',NULL,1,1,'2025-10-07 07:33:37.375039','2025-10-07 07:35:04.499529',25),(116,'kn','Rotavirus Vaccine -','https://www.youtube.com/watch?v=vj2jnsh6vPA','youtube','',NULL,1,1,'2025-10-07 07:33:37.381878','2025-10-07 07:35:04.426847',26),(117,'kn','Rotavirus Vaccine -','https://www.youtube.com/watch?v=vj2jnsh6vPA','youtube','',NULL,1,1,'2025-10-07 07:33:37.455816','2025-10-07 07:35:04.463609',27),(118,'kn','Influenza Vaccine -','https://www.youtube.com/watch?v=L8NbpSfFbUk','youtube','',NULL,1,1,'2025-10-07 07:33:37.462735','2025-10-07 07:35:04.477266',28),(119,'kn','Typhoid Vaccine -','https://www.youtube.com/watch?v=pt8o3WJ2GS8','youtube','',NULL,1,1,'2025-10-07 07:33:37.476714','2025-10-07 07:35:04.484446',29),(120,'kn','MMR Vaccine -','https://www.youtube.com/watch?v=aC3sf3axowI','youtube','',NULL,1,1,'2025-10-07 07:33:37.486090','2025-10-07 07:35:04.560756',30),(121,'kn','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=72evvMcmBE0','youtube','',NULL,1,1,'2025-10-07 07:33:37.490689','2025-10-07 07:35:04.497548',31),(122,'kn','Varicella Vaccine -','https://www.youtube.com/watch?v=CqujMH65n4E','youtube','',NULL,1,1,'2025-10-07 07:33:37.511472','2025-10-07 07:35:04.546269',32),(123,'kn','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=72evvMcmBE0','youtube','',NULL,1,1,'2025-10-07 07:33:37.539182','2025-10-07 07:35:04.539743',33),(124,'kn','HPV Vaccine -','https://www.youtube.com/watch?v=5JqA5GyiMf8','youtube','',NULL,1,1,'2025-10-07 07:33:37.581832','2025-10-07 07:35:04.571097',34),(125,'kn','Tdap/ Td Vaccine -','https://www.youtube.com/watch?v=9koc4KTgj3k','youtube','',NULL,1,1,'2025-10-07 07:33:37.589837','2025-10-07 07:35:04.577132',35),(126,'kn','Influenza Vaccine -','https://www.youtube.com/watch?v=L8NbpSfFbUk','youtube','',NULL,1,1,'2025-10-07 07:33:37.597629','2025-10-07 07:35:04.581957',36),(127,'ta','BCG Vaccine -','https://www.youtube.com/watch?v=1WGsY-WLWEw','youtube','',NULL,1,1,'2025-10-07 07:33:37.604271','2025-10-07 07:35:04.589303',19),(128,'ta','Hepatitis B Vaccine -','https://www.youtube.com/watch?v=ZhjwNlvFj6M','youtube','',NULL,1,1,'2025-10-07 07:33:37.610208','2025-10-07 07:35:04.699600',20),(129,'ta','Polio Vaccine -','https://www.youtube.com/watch?v=TN5O2xlmxIw','youtube','',NULL,1,1,'2025-10-07 07:33:37.618457','2025-10-07 07:35:04.602326',21),(130,'ta','DTwP/DTaP Vaccine -','https://www.youtube.com/watch?v=0OOXSQagiZQ','youtube','',NULL,1,1,'2025-10-07 07:33:37.624938','2025-10-07 07:35:04.796668',22),(131,'ta','Hib Vaccine -','https://www.youtube.com/watch?v=GlReMD-J4sw','youtube','',NULL,1,1,'2025-10-07 07:33:37.631532','2025-10-07 07:35:04.774554',23),(132,'ta','Polio Vaccine -','https://www.youtube.com/watch?v=TN5O2xlmxIw','youtube','',NULL,1,1,'2025-10-07 07:33:37.639053','2025-10-07 07:35:04.803606',24),(133,'ta','PCV Vaccine -','https://www.youtube.com/watch?v=yIpyP3_0Vi8','youtube','',NULL,1,1,'2025-10-07 07:33:37.651054','2025-10-07 07:35:04.749108',25),(134,'ta','Rotavirus Vaccine -','https://www.youtube.com/watch?v=mCXLtRgUozI','youtube','',NULL,1,1,'2025-10-07 07:33:37.657312','2025-10-07 07:35:04.678584',26),(135,'ta','Rotavirus Vaccine -','https://www.youtube.com/watch?v=mCXLtRgUozI','youtube','',NULL,1,1,'2025-10-07 07:33:37.736046','2025-10-07 07:35:04.713317',27),(136,'ta','Influenza Vaccine -','https://www.youtube.com/watch?v=7DoRKhHZ8xk','youtube','',NULL,1,1,'2025-10-07 07:33:37.743239','2025-10-07 07:35:04.727182',28),(137,'ta','Typhoid Vaccine -','https://www.youtube.com/watch?v=M1D6HFf_RJE','youtube','',NULL,1,1,'2025-10-07 07:33:37.754468','2025-10-07 07:35:04.731594',29),(138,'ta','MMR Vaccine -','https://www.youtube.com/watch?v=Hg7uZM9uKyM','youtube','',NULL,1,1,'2025-10-07 07:33:37.761253','2025-10-07 07:35:04.810543',30),(139,'ta','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=a8GMOBt6mIU','youtube','',NULL,1,1,'2025-10-07 07:33:37.768222','2025-10-07 07:35:04.741158',31),(140,'ta','Varicella Vaccine -','https://www.youtube.com/watch?v=rhbxyLjzgaw','youtube','',NULL,1,1,'2025-10-07 07:33:37.789065','2025-10-07 07:35:04.792206',32),(141,'ta','Hepatitis A Vaccine -','https://www.youtube.com/watch?v=a8GMOBt6mIU','youtube','',NULL,1,1,'2025-10-07 07:33:37.809891','2025-10-07 07:35:04.785891',33),(142,'ta','HPV Vaccine -','https://www.youtube.com/watch?v=haYJ_xjMzMs','youtube','',NULL,1,1,'2025-10-07 07:33:37.844849','2025-10-07 07:35:04.817050',34),(143,'ta','Tdap/ Td Vaccine -','https://www.youtube.com/watch?v=5G_pF7_8KfA','youtube','',NULL,1,1,'2025-10-07 07:33:37.851666','2025-10-07 07:35:04.824457',35),(144,'ta','Influenza Vaccine -','https://www.youtube.com/watch?v=7DoRKhHZ8xk','youtube','',NULL,1,1,'2025-10-07 07:33:37.858657','2025-10-07 07:35:04.827789',36);
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

-- Dump completed on 2026-02-18 12:46:44
