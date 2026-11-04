-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: school_imentor
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

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
-- Table structure for table `auditlog_logentry`
--

DROP TABLE IF EXISTS `auditlog_logentry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auditlog_logentry` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_pk` varchar(255) NOT NULL,
  `object_id` bigint(20) DEFAULT NULL,
  `object_repr` longtext NOT NULL,
  `action` smallint(5) unsigned NOT NULL CHECK (`action` >= 0),
  `changes` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`changes`)),
  `timestamp` datetime(6) NOT NULL,
  `actor_id` int(11) DEFAULT NULL,
  `content_type_id` int(11) NOT NULL,
  `remote_addr` char(39) DEFAULT NULL,
  `additional_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`additional_data`)),
  `serialized_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`serialized_data`)),
  `cid` varchar(255) DEFAULT NULL,
  `changes_text` longtext NOT NULL,
  `remote_port` int(10) unsigned DEFAULT NULL CHECK (`remote_port` >= 0),
  `actor_email` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `auditlog_logentry_actor_id_959271d2_fk_main_app_customuser_id` (`actor_id`),
  KEY `auditlog_logentry_content_type_id_75830218_fk_django_co` (`content_type_id`),
  KEY `auditlog_logentry_object_id_09c2eee8` (`object_id`),
  KEY `auditlog_logentry_object_pk_6e3219c0` (`object_pk`),
  KEY `auditlog_logentry_action_229afe39` (`action`),
  KEY `auditlog_logentry_timestamp_37867bb0` (`timestamp`),
  KEY `auditlog_logentry_cid_9f467263` (`cid`),
  CONSTRAINT `auditlog_logentry_actor_id_959271d2_fk_main_app_customuser_id` FOREIGN KEY (`actor_id`) REFERENCES `main_app_customuser` (`id`),
  CONSTRAINT `auditlog_logentry_content_type_id_75830218_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=222 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditlog_logentry`
--

LOCK TABLES `auditlog_logentry` WRITE;
/*!40000 ALTER TABLE `auditlog_logentry` DISABLE KEYS */;
INSERT INTO `auditlog_logentry` VALUES (1,'4',4,'7 - C',0,'{\"division\": [\"None\", \"C\"], \"id\": [\"None\", \"4\"], \"name\": [\"None\", \"7\"], \"created_at\": [\"None\", \"2025-06-20 07:22:34.608336\"], \"updated_at\": [\"None\", \"2025-06-20 07:22:34.608336\"]}','2025-06-20 07:22:34.616335',1,8,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(2,'2',2,'JOHN, JOSEPH',1,'{\"password\": [\"pbkdf2_sha256$216000$4irfda5ttavN$SMaEv0oh0CHrYP/9wUW28vOcrAE/s8g8mjxTQiAOBL8=\", \"pbkdf2_sha256$390000$k1w9GKCj3ko8lxZFcVKxE2$VCJbbZRk+IB5B5Jcn8ECmkZwxSGO+jZ9DTY2ZBXh3Ro=\"]}','2025-06-20 07:27:18.131110',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(3,'2',2,'JOHN, JOSEPH',1,'{\"last_login\": [\"2025-06-19 11:00:30.980567\", \"2025-06-20 07:27:18.146528\"]}','2025-06-20 07:27:18.148527',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(4,'1',1,'1. REAL NUMBER (15) PERIODS\nFUNDAMENTAL THEOREM OF ARITHMETIC - STATEMENTS AFTER REVIEWING WORK DONE EARLIER AND\nAFTER ILLUSTRATING AND MOTIVATING THROUGH EXAMPLES, PROOFS OF IRRATIONALITY OF SQUARE ROOT OF 2,3,5\n - 9 - B - Subject object (1)',0,'{\"id\": [\"None\", \"1\"], \"title\": [\"None\", \"UNIT I: NUMBER SYSTEMS\"], \"status\": [\"None\", \"False\"], \"course\": [\"None\", \"2\"], \"subject\": [\"None\", \"1\"], \"lesson\": [\"None\", \"1. REAL NUMBER (15) PERIODS\\nFUNDAMENTAL THEOREM OF ARITHMETIC - STATEMENTS AFTER REVIEWING WORK DONE EARLIER AND\\nAFTER ILLUSTRATING AND MOTIVATING THROUGH EXAMPLES, PROOFS OF IRRATIONALITY OF SQUARE ROOT OF 2,3,5\\n\"], \"term\": [\"None\", \"Term-1\"], \"notificaton\": [\"None\", \"False\"]}','2025-06-20 07:40:56.161393',2,24,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(5,'6',6,'ABC, X',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"6\"], \"admin\": [\"None\", \"24\"]}','2025-06-20 10:36:44.547212',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(6,'24',24,'ABC, X',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABC\"], \"last_name\": [\"None\", \"X\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:36:44.521934\"], \"email\": [\"None\", \"abc.x.d8d032@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:36:44.521934\"], \"updated_at\": [\"None\", \"2025-06-20 10:36:44.521934\"], \"student\": [\"None\", \"ABC, X\"], \"id\": [\"None\", \"24\"]}','2025-06-20 10:36:44.567406',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(7,'6',6,'ABC, X',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:36:44.581057',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(8,'7',7,'XYZ, A',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"7\"], \"admin\": [\"None\", \"25\"]}','2025-06-20 10:36:44.594016',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(9,'25',25,'XYZ, A',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"XYZ\"], \"last_name\": [\"None\", \"A\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:36:44.592092\"], \"email\": [\"None\", \"xyz.a.bb63b2@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:36:44.593056\"], \"updated_at\": [\"None\", \"2025-06-20 10:36:44.593056\"], \"student\": [\"None\", \"XYZ, A\"], \"id\": [\"None\", \"25\"]}','2025-06-20 10:36:44.600029',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(10,'7',7,'XYZ, A',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:36:44.607893',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(11,'8',8,'AKHIL , K A',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"8\"], \"admin\": [\"None\", \"26\"]}','2025-06-20 10:49:15.990893',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(12,'26',26,'AKHIL , K A',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"AKHIL \"], \"last_name\": [\"None\", \"K A\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:49:15.985895\"], \"email\": [\"None\", \"akhil .k a.1@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:49:15.985895\"], \"updated_at\": [\"None\", \"2025-06-20 10:49:15.985895\"], \"id\": [\"None\", \"26\"], \"student\": [\"None\", \"AKHIL , K A\"]}','2025-06-20 10:49:16.004899',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(13,'8',8,'AKHIL , K A',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:49:16.021928',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(14,'9',9,'ARATHY, KRISHNA',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"9\"], \"admin\": [\"None\", \"27\"]}','2025-06-20 10:49:16.051194',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(15,'27',27,'ARATHY, KRISHNA',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ARATHY\"], \"last_name\": [\"None\", \"KRISHNA\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:49:16.043193\"], \"email\": [\"None\", \"arathy.krishna.2@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:49:16.043193\"], \"updated_at\": [\"None\", \"2025-06-20 10:49:16.043193\"], \"id\": [\"None\", \"27\"], \"student\": [\"None\", \"ARATHY, KRISHNA\"]}','2025-06-20 10:49:16.060206',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(16,'9',9,'ARATHY, KRISHNA',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:49:16.086191',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(17,'10',10,'PRAKASH, JOSE',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"10\"], \"admin\": [\"None\", \"28\"]}','2025-06-20 10:53:26.514777',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(18,'28',28,'PRAKASH, JOSE',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"PRAKASH\"], \"last_name\": [\"None\", \"JOSE\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:53:26.510838\"], \"email\": [\"None\", \"prakashjose1@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"PRAKASH, JOSE\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:53:26.510838\"], \"updated_at\": [\"None\", \"2025-06-20 10:53:26.510838\"], \"id\": [\"None\", \"28\"]}','2025-06-20 10:53:26.520746',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(19,'10',10,'PRAKASH, JOSE',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:53:26.527023',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(20,'11',11,'BINCY, JOHN',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"11\"], \"admin\": [\"None\", \"29\"]}','2025-06-20 10:53:26.539913',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(21,'29',29,'BINCY, JOHN',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"BINCY\"], \"last_name\": [\"None\", \"JOHN\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:53:26.537916\"], \"email\": [\"None\", \"bincyjohn2@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"BINCY, JOHN\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:53:26.538920\"], \"updated_at\": [\"None\", \"2025-06-20 10:53:26.538920\"], \"id\": [\"None\", \"29\"]}','2025-06-20 10:53:26.548939',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(22,'11',11,'BINCY, JOHN',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:53:26.557456',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(23,'12',12,'ABHINAV ,  P S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"12\"], \"admin\": [\"None\", \"30\"]}','2025-06-20 10:59:25.560586',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(24,'30',30,'ABHINAV ,  P S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABHINAV \"], \"last_name\": [\"None\", \" P S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.550107\"], \"email\": [\"None\", \"abhinav  p s1@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"ABHINAV ,  P S\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.551105\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.551105\"], \"id\": [\"None\", \"30\"]}','2025-06-20 10:59:25.575586',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(25,'12',12,'ABHINAV ,  P S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.581586',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(26,'13',13,'AGRAJ , A',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"13\"], \"admin\": [\"None\", \"31\"]}','2025-06-20 10:59:25.589588',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(27,'31',31,'AGRAJ , A',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"AGRAJ \"], \"last_name\": [\"None\", \"A\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.588589\"], \"email\": [\"None\", \"agraj a2@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"AGRAJ , A\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.588589\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.588589\"], \"id\": [\"None\", \"31\"]}','2025-06-20 10:59:25.593586',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(28,'13',13,'AGRAJ , A',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.601593',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(29,'14',14,'ANSON , JOSE',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"14\"], \"admin\": [\"None\", \"32\"]}','2025-06-20 10:59:25.610102',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(30,'32',32,'ANSON , JOSE',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ANSON \"], \"last_name\": [\"None\", \"JOSE\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.608593\"], \"email\": [\"None\", \"anson jose3@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"ANSON , JOSE\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.608593\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.608593\"], \"id\": [\"None\", \"32\"]}','2025-06-20 10:59:25.614111',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(31,'14',14,'ANSON , JOSE',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.625308',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(32,'15',15,'ARJUN  , BINOY',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"15\"], \"admin\": [\"None\", \"33\"]}','2025-06-20 10:59:25.633308',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(33,'33',33,'ARJUN  , BINOY',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ARJUN  \"], \"last_name\": [\"None\", \"BINOY\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.632307\"], \"email\": [\"None\", \"arjun  binoy4@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"ARJUN  , BINOY\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.632307\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.632307\"], \"id\": [\"None\", \"33\"]}','2025-06-20 10:59:25.642308',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(34,'15',15,'ARJUN  , BINOY',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.654880',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(35,'16',16,'DIVINE , A J',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"16\"], \"admin\": [\"None\", \"34\"]}','2025-06-20 10:59:25.661800',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(36,'34',34,'DIVINE , A J',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"DIVINE \"], \"last_name\": [\"None\", \"A J\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.659799\"], \"email\": [\"None\", \"divine a j5@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"DIVINE , A J\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.659799\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.659799\"], \"id\": [\"None\", \"34\"]}','2025-06-20 10:59:25.666796',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(37,'16',16,'DIVINE , A J',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.675179',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(38,'17',17,'EDWIN , BENADICT',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"17\"], \"admin\": [\"None\", \"35\"]}','2025-06-20 10:59:25.682254',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(39,'35',35,'EDWIN , BENADICT',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"EDWIN \"], \"last_name\": [\"None\", \"BENADICT\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.679257\"], \"email\": [\"None\", \"edwin benadict6@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"EDWIN , BENADICT\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.680256\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.680256\"], \"id\": [\"None\", \"35\"]}','2025-06-20 10:59:25.688257',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(40,'17',17,'EDWIN , BENADICT',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.696973',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(41,'18',18,'GANESHKUMAR , S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"18\"], \"admin\": [\"None\", \"36\"]}','2025-06-20 10:59:25.704972',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(42,'36',36,'GANESHKUMAR , S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"GANESHKUMAR \"], \"last_name\": [\"None\", \"S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.701973\"], \"email\": [\"None\", \"ganeshkumar s7@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"GANESHKUMAR , S\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.701973\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.701973\"], \"id\": [\"None\", \"36\"]}','2025-06-20 10:59:25.709974',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(43,'18',18,'GANESHKUMAR , S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.716315',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(44,'19',19,'JOHN , PIO VARGHESE',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"19\"], \"admin\": [\"None\", \"37\"]}','2025-06-20 10:59:25.724314',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(45,'37',37,'JOHN , PIO VARGHESE',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"JOHN \"], \"last_name\": [\"None\", \"PIO VARGHESE\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.722318\"], \"email\": [\"None\", \"john pio varghese8@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"JOHN , PIO VARGHESE\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.722318\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.722318\"], \"id\": [\"None\", \"37\"]}','2025-06-20 10:59:25.728313',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(46,'19',19,'JOHN , PIO VARGHESE',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.734314',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(47,'20',20,'PAVANENDH,  S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"20\"], \"admin\": [\"None\", \"38\"]}','2025-06-20 10:59:25.741313',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(48,'38',38,'PAVANENDH,  S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"PAVANENDH\"], \"last_name\": [\"None\", \" S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.739317\"], \"email\": [\"None\", \"pavanendh s9@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"PAVANENDH,  S\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.739317\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.739317\"], \"id\": [\"None\", \"38\"]}','2025-06-20 10:59:25.745318',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(49,'20',20,'PAVANENDH,  S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.753316',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(50,'21',21,'SANJAY , KRISHNA',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"21\"], \"admin\": [\"None\", \"39\"]}','2025-06-20 10:59:25.762313',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(51,'39',39,'SANJAY , KRISHNA',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"SANJAY \"], \"last_name\": [\"None\", \"KRISHNA\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.760316\"], \"email\": [\"None\", \"sanjay krishna10@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"SANJAY , KRISHNA\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.760316\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.760316\"], \"id\": [\"None\", \"39\"]}','2025-06-20 10:59:25.767318',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(52,'21',21,'SANJAY , KRISHNA',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.773318',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(53,'22',22,'SNEHADATHAN , S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"22\"], \"admin\": [\"None\", \"40\"]}','2025-06-20 10:59:25.779995',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(54,'40',40,'SNEHADATHAN , S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"SNEHADATHAN \"], \"last_name\": [\"None\", \"S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.777996\"], \"email\": [\"None\", \"snehadathan s11@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"SNEHADATHAN , S\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.777996\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.777996\"], \"id\": [\"None\", \"40\"]}','2025-06-20 10:59:25.784009',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(55,'22',22,'SNEHADATHAN , S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.789995',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(56,'23',23,'THANSEEM , NIYAS',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"23\"], \"admin\": [\"None\", \"41\"]}','2025-06-20 10:59:25.795798',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(57,'41',41,'THANSEEM , NIYAS',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"THANSEEM \"], \"last_name\": [\"None\", \"NIYAS\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.793789\"], \"email\": [\"None\", \"thanseem niyas12@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"THANSEEM , NIYAS\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.793789\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.793789\"], \"id\": [\"None\", \"41\"]}','2025-06-20 10:59:25.799798',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(58,'23',23,'THANSEEM , NIYAS',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.806803',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(59,'24',24,'ABHIRAMI , SUDEESH',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"24\"], \"admin\": [\"None\", \"42\"]}','2025-06-20 10:59:25.813355',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(60,'42',42,'ABHIRAMI , SUDEESH',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABHIRAMI \"], \"last_name\": [\"None\", \"SUDEESH\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.811357\"], \"email\": [\"None\", \"abhirami sudeesh13@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"ABHIRAMI , SUDEESH\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.811357\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.811357\"], \"id\": [\"None\", \"42\"]}','2025-06-20 10:59:25.817355',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(61,'24',24,'ABHIRAMI , SUDEESH',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.824316',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(62,'25',25,'ALEEVIA , ASHOK K',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"25\"], \"admin\": [\"None\", \"43\"]}','2025-06-20 10:59:25.831319',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(63,'43',43,'ALEEVIA , ASHOK K',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ALEEVIA \"], \"last_name\": [\"None\", \"ASHOK K\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.829319\"], \"email\": [\"None\", \"aleevia ashok k14@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"ALEEVIA , ASHOK K\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.829319\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.829319\"], \"id\": [\"None\", \"43\"]}','2025-06-20 10:59:25.835319',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(64,'25',25,'ALEEVIA , ASHOK K',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.842786',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(65,'26',26,'DARSANA , U NAIR',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"26\"], \"admin\": [\"None\", \"44\"]}','2025-06-20 10:59:25.849452',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(66,'44',44,'DARSANA , U NAIR',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"DARSANA \"], \"last_name\": [\"None\", \"U NAIR\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.847449\"], \"email\": [\"None\", \"darsana u nair15@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"DARSANA , U NAIR\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.848452\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.848452\"], \"id\": [\"None\", \"44\"]}','2025-06-20 10:59:25.855448',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(67,'26',26,'DARSANA , U NAIR',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.863810',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(68,'27',27,'DINCIYA , PETER',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"27\"], \"admin\": [\"None\", \"45\"]}','2025-06-20 10:59:25.871835',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(69,'45',45,'DINCIYA , PETER',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"DINCIYA \"], \"last_name\": [\"None\", \"PETER\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.869841\"], \"email\": [\"None\", \"dinciya peter16@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"DINCIYA , PETER\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.869841\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.869841\"], \"id\": [\"None\", \"45\"]}','2025-06-20 10:59:25.877836',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(70,'27',27,'DINCIYA , PETER',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.884833',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(71,'28',28,'MALAVIKA , MANOJ',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"28\"], \"admin\": [\"None\", \"46\"]}','2025-06-20 10:59:25.892836',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(72,'46',46,'MALAVIKA , MANOJ',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"MALAVIKA \"], \"last_name\": [\"None\", \"MANOJ\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.890837\"], \"email\": [\"None\", \"malavika manoj17@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"MALAVIKA , MANOJ\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.890837\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.890837\"], \"id\": [\"None\", \"46\"]}','2025-06-20 10:59:25.897859',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(73,'28',28,'MALAVIKA , MANOJ',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.904026',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(74,'29',29,'SERA , C THOMAS',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"29\"], \"admin\": [\"None\", \"47\"]}','2025-06-20 10:59:25.908791',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(75,'47',47,'SERA , C THOMAS',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"SERA \"], \"last_name\": [\"None\", \"C THOMAS\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.907785\"], \"email\": [\"None\", \"sera c thomas18@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"SERA , C THOMAS\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.908791\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.908791\"], \"id\": [\"None\", \"47\"]}','2025-06-20 10:59:25.913315',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(76,'29',29,'SERA , C THOMAS',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.922131',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(77,'30',30,'SREENANDA , V S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"30\"], \"admin\": [\"None\", \"48\"]}','2025-06-20 10:59:25.928141',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(78,'48',48,'SREENANDA , V S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"SREENANDA \"], \"last_name\": [\"None\", \"V S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.927138\"], \"email\": [\"None\", \"sreenanda v s19@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"SREENANDA , V S\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.927138\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.927138\"], \"id\": [\"None\", \"48\"]}','2025-06-20 10:59:25.932142',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(79,'30',30,'SREENANDA , V S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.940664',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(80,'31',31,'VYSHNAVI , RAJ',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"31\"], \"admin\": [\"None\", \"49\"]}','2025-06-20 10:59:25.947665',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(81,'49',49,'VYSHNAVI , RAJ',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"VYSHNAVI \"], \"last_name\": [\"None\", \"RAJ\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 10:59:25.946667\"], \"email\": [\"None\", \"vyshnavi raj20@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"student\": [\"None\", \"VYSHNAVI , RAJ\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 10:59:25.946667\"], \"updated_at\": [\"None\", \"2025-06-20 10:59:25.946667\"], \"id\": [\"None\", \"49\"]}','2025-06-20 10:59:25.952665',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(82,'31',31,'VYSHNAVI , RAJ',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 10:59:25.965687',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(83,'32',32,'ABHINAV ,  P S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"32\"], \"admin\": [\"None\", \"50\"]}','2025-06-20 11:03:39.537007',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(84,'50',50,'ABHINAV ,  P S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABHINAV \"], \"last_name\": [\"None\", \" P S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.532220\"], \"email\": [\"None\", \"abhinav _1@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"ABHINAV ,  P S\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.532220\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.532220\"], \"id\": [\"None\", \"50\"]}','2025-06-20 11:03:39.547992',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(85,'32',32,'ABHINAV ,  P S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.563273',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(86,'33',33,'AGRAJ , A',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"33\"], \"admin\": [\"None\", \"51\"]}','2025-06-20 11:03:39.572483',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(87,'51',51,'AGRAJ , A',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"AGRAJ \"], \"last_name\": [\"None\", \"A\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.570480\"], \"email\": [\"None\", \"agraj _2@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"AGRAJ , A\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.571483\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.571483\"], \"id\": [\"None\", \"51\"]}','2025-06-20 11:03:39.579001',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(88,'33',33,'AGRAJ , A',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.589009',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(89,'34',34,'ANSON , JOSE',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"34\"], \"admin\": [\"None\", \"52\"]}','2025-06-20 11:03:39.600594',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(90,'52',52,'ANSON , JOSE',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ANSON \"], \"last_name\": [\"None\", \"JOSE\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.598596\"], \"email\": [\"None\", \"anson _3@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"ANSON , JOSE\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.598596\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.598596\"], \"id\": [\"None\", \"52\"]}','2025-06-20 11:03:39.614749',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(91,'34',34,'ANSON , JOSE',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.621719',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(92,'35',35,'ARJUN  , BINOY',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"35\"], \"admin\": [\"None\", \"53\"]}','2025-06-20 11:03:39.631720',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(93,'53',53,'ARJUN  , BINOY',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ARJUN  \"], \"last_name\": [\"None\", \"BINOY\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.630720\"], \"email\": [\"None\", \"arjun  _4@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"ARJUN  , BINOY\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.630720\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.630720\"], \"id\": [\"None\", \"53\"]}','2025-06-20 11:03:39.636714',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(94,'35',35,'ARJUN  , BINOY',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.651713',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(95,'36',36,'DIVINE , A J',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"36\"], \"admin\": [\"None\", \"54\"]}','2025-06-20 11:03:39.661565',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(96,'54',54,'DIVINE , A J',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"DIVINE \"], \"last_name\": [\"None\", \"A J\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.657544\"], \"email\": [\"None\", \"divine _5@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"DIVINE , A J\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.658547\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.658547\"], \"id\": [\"None\", \"54\"]}','2025-06-20 11:03:39.666565',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(97,'36',36,'DIVINE , A J',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.681076',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(98,'37',37,'EDWIN , BENADICT',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"37\"], \"admin\": [\"None\", \"55\"]}','2025-06-20 11:03:39.689073',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(99,'55',55,'EDWIN , BENADICT',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"EDWIN \"], \"last_name\": [\"None\", \"BENADICT\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.687074\"], \"email\": [\"None\", \"edwin _6@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"EDWIN , BENADICT\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.687074\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.687074\"], \"id\": [\"None\", \"55\"]}','2025-06-20 11:03:39.697074',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(100,'37',37,'EDWIN , BENADICT',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.703075',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(101,'38',38,'GANESHKUMAR , S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"38\"], \"admin\": [\"None\", \"56\"]}','2025-06-20 11:03:39.712089',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(102,'56',56,'GANESHKUMAR , S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"GANESHKUMAR \"], \"last_name\": [\"None\", \"S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.710079\"], \"email\": [\"None\", \"ganeshkumar _7@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"GANESHKUMAR , S\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.710079\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.710079\"], \"id\": [\"None\", \"56\"]}','2025-06-20 11:03:39.716075',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(103,'38',38,'GANESHKUMAR , S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.722075',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(104,'39',39,'JOHN , PIO VARGHESE',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"39\"], \"admin\": [\"None\", \"57\"]}','2025-06-20 11:03:39.732076',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(105,'57',57,'JOHN , PIO VARGHESE',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"JOHN \"], \"last_name\": [\"None\", \"PIO VARGHESE\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.730075\"], \"email\": [\"None\", \"john _8@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"JOHN , PIO VARGHESE\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.730075\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.730075\"], \"id\": [\"None\", \"57\"]}','2025-06-20 11:03:39.737076',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(106,'39',39,'JOHN , PIO VARGHESE',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.749076',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(107,'40',40,'PAVANENDH,  S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"40\"], \"admin\": [\"None\", \"58\"]}','2025-06-20 11:03:39.756077',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(108,'58',58,'PAVANENDH,  S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"PAVANENDH\"], \"last_name\": [\"None\", \" S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.754076\"], \"email\": [\"None\", \"pavanendh_9@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"PAVANENDH,  S\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.754076\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.754076\"], \"id\": [\"None\", \"58\"]}','2025-06-20 11:03:39.763092',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(109,'40',40,'PAVANENDH,  S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.768090',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(110,'41',41,'SANJAY , KRISHNA',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"41\"], \"admin\": [\"None\", \"59\"]}','2025-06-20 11:03:39.777621',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(111,'59',59,'SANJAY , KRISHNA',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"SANJAY \"], \"last_name\": [\"None\", \"KRISHNA\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.774089\"], \"email\": [\"None\", \"sanjay _10@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"SANJAY , KRISHNA\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.774599\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.774599\"], \"id\": [\"None\", \"59\"]}','2025-06-20 11:03:39.781611',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(112,'41',41,'SANJAY , KRISHNA',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.787611',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(113,'42',42,'SNEHADATHAN , S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"42\"], \"admin\": [\"None\", \"60\"]}','2025-06-20 11:03:39.797611',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(114,'60',60,'SNEHADATHAN , S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"SNEHADATHAN \"], \"last_name\": [\"None\", \"S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.795613\"], \"email\": [\"None\", \"snehadathan _11@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"SNEHADATHAN , S\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.795613\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.795613\"], \"id\": [\"None\", \"60\"]}','2025-06-20 11:03:39.801611',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(115,'42',42,'SNEHADATHAN , S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.812612',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(116,'43',43,'THANSEEM , NIYAS',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"43\"], \"admin\": [\"None\", \"61\"]}','2025-06-20 11:03:39.819609',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(117,'61',61,'THANSEEM , NIYAS',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"THANSEEM \"], \"last_name\": [\"None\", \"NIYAS\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.817614\"], \"email\": [\"None\", \"thanseem _12@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"THANSEEM , NIYAS\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.817614\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.817614\"], \"id\": [\"None\", \"61\"]}','2025-06-20 11:03:39.825611',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(118,'43',43,'THANSEEM , NIYAS',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.831611',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(119,'44',44,'ABHIRAMI , SUDEESH',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"44\"], \"admin\": [\"None\", \"62\"]}','2025-06-20 11:03:39.838612',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(120,'62',62,'ABHIRAMI , SUDEESH',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABHIRAMI \"], \"last_name\": [\"None\", \"SUDEESH\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.836612\"], \"email\": [\"None\", \"abhirami _13@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"ABHIRAMI , SUDEESH\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.836612\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.836612\"], \"id\": [\"None\", \"62\"]}','2025-06-20 11:03:39.845614',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(121,'44',44,'ABHIRAMI , SUDEESH',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.850611',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(122,'45',45,'ALEEVIA , ASHOK K',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"45\"], \"admin\": [\"None\", \"63\"]}','2025-06-20 11:03:39.859629',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(123,'63',63,'ALEEVIA , ASHOK K',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ALEEVIA \"], \"last_name\": [\"None\", \"ASHOK K\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.855612\"], \"email\": [\"None\", \"aleevia _14@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"ALEEVIA , ASHOK K\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.855612\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.855612\"], \"id\": [\"None\", \"63\"]}','2025-06-20 11:03:39.864626',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(124,'45',45,'ALEEVIA , ASHOK K',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.870626',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(125,'46',46,'DARSANA , U NAIR',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"46\"], \"admin\": [\"None\", \"64\"]}','2025-06-20 11:03:39.879145',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(126,'64',64,'DARSANA , U NAIR',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"DARSANA \"], \"last_name\": [\"None\", \"U NAIR\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.878158\"], \"email\": [\"None\", \"darsana _15@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"DARSANA , U NAIR\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.878158\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.878158\"], \"id\": [\"None\", \"64\"]}','2025-06-20 11:03:39.883145',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(127,'46',46,'DARSANA , U NAIR',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.889145',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(128,'47',47,'DINCIYA , PETER',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"47\"], \"admin\": [\"None\", \"65\"]}','2025-06-20 11:03:39.898148',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(129,'65',65,'DINCIYA , PETER',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"DINCIYA \"], \"last_name\": [\"None\", \"PETER\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.896143\"], \"email\": [\"None\", \"dinciya _16@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"DINCIYA , PETER\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.896143\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.896143\"], \"id\": [\"None\", \"65\"]}','2025-06-20 11:03:39.902147',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(130,'47',47,'DINCIYA , PETER',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.910141',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(131,'48',48,'MALAVIKA , MANOJ',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"48\"], \"admin\": [\"None\", \"66\"]}','2025-06-20 11:03:39.919147',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(132,'66',66,'MALAVIKA , MANOJ',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"MALAVIKA \"], \"last_name\": [\"None\", \"MANOJ\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.917145\"], \"email\": [\"None\", \"malavika _17@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"MALAVIKA , MANOJ\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.918144\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.918144\"], \"id\": [\"None\", \"66\"]}','2025-06-20 11:03:39.922147',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(133,'48',48,'MALAVIKA , MANOJ',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.930144',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(134,'49',49,'SERA , C THOMAS',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"49\"], \"admin\": [\"None\", \"67\"]}','2025-06-20 11:03:39.937143',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(135,'67',67,'SERA , C THOMAS',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"SERA \"], \"last_name\": [\"None\", \"C THOMAS\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.935143\"], \"email\": [\"None\", \"sera _18@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"SERA , C THOMAS\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.936144\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.936144\"], \"id\": [\"None\", \"67\"]}','2025-06-20 11:03:39.944148',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(136,'49',49,'SERA , C THOMAS',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.950144',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(137,'50',50,'SREENANDA , V S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"50\"], \"admin\": [\"None\", \"68\"]}','2025-06-20 11:03:39.956146',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(138,'68',68,'SREENANDA , V S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"SREENANDA \"], \"last_name\": [\"None\", \"V S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.954146\"], \"email\": [\"None\", \"sreenanda _19@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"SREENANDA , V S\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.955144\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.955144\"], \"id\": [\"None\", \"68\"]}','2025-06-20 11:03:39.964478',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(139,'50',50,'SREENANDA , V S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.972478',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(140,'51',51,'VYSHNAVI , RAJ',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"51\"], \"admin\": [\"None\", \"69\"]}','2025-06-20 11:03:39.980995',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(141,'69',69,'VYSHNAVI , RAJ',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"VYSHNAVI \"], \"last_name\": [\"None\", \"RAJ\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:03:39.978994\"], \"email\": [\"None\", \"vyshnavi _20@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"student\": [\"None\", \"VYSHNAVI , RAJ\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:03:39.979997\"], \"updated_at\": [\"None\", \"2025-06-20 11:03:39.979997\"], \"id\": [\"None\", \"69\"]}','2025-06-20 11:03:39.984997',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(142,'51',51,'VYSHNAVI , RAJ',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"3\"]}','2025-06-20 11:03:39.991996',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(143,'52',52,'ABEL, FERNANDEZ',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"52\"], \"admin\": [\"None\", \"70\"]}','2025-06-20 11:49:30.237977',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(144,'70',70,'ABEL, FERNANDEZ',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABEL\"], \"last_name\": [\"None\", \"FERNANDEZ\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:49:30.231976\"], \"email\": [\"None\", \"abel1@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:49:30.231976\"], \"updated_at\": [\"None\", \"2025-06-20 11:49:30.231976\"], \"student\": [\"None\", \"ABEL, FERNANDEZ\"], \"id\": [\"None\", \"70\"]}','2025-06-20 11:49:30.250131',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(145,'53',53,'ABHINAV, VA',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"53\"], \"admin\": [\"None\", \"71\"]}','2025-06-20 11:49:30.299668',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(146,'71',71,'ABHINAV, VA',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABHINAV\"], \"last_name\": [\"None\", \"VA\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:49:30.297626\"], \"email\": [\"None\", \"abhinav2@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:49:30.297626\"], \"updated_at\": [\"None\", \"2025-06-20 11:49:30.297626\"], \"student\": [\"None\", \"ABHINAV, VA\"], \"id\": [\"None\", \"71\"]}','2025-06-20 11:49:30.310148',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(147,'54',54,'ABIHAIL, PJ',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"54\"], \"admin\": [\"None\", \"72\"]}','2025-06-20 11:49:30.329023',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(148,'72',72,'ABIHAIL, PJ',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABIHAIL\"], \"last_name\": [\"None\", \"PJ\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:49:30.324972\"], \"email\": [\"None\", \"abihail3@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:49:30.325986\"], \"updated_at\": [\"None\", \"2025-06-20 11:49:30.325986\"], \"student\": [\"None\", \"ABIHAIL, PJ\"], \"id\": [\"None\", \"72\"]}','2025-06-20 11:49:30.338097',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(149,'55',55,'ARNAV, MS',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"55\"], \"admin\": [\"None\", \"73\"]}','2025-06-20 11:49:30.355451',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(150,'73',73,'ARNAV, MS',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ARNAV\"], \"last_name\": [\"None\", \"MS\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:49:30.352110\"], \"email\": [\"None\", \"arnav4@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:49:30.352110\"], \"updated_at\": [\"None\", \"2025-06-20 11:49:30.352110\"], \"student\": [\"None\", \"ARNAV, MS\"], \"id\": [\"None\", \"73\"]}','2025-06-20 11:49:30.364984',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(151,'56',56,'GAGANKRISHNA, S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"56\"], \"admin\": [\"None\", \"74\"]}','2025-06-20 11:49:30.385024',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(152,'74',74,'GAGANKRISHNA, S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"GAGANKRISHNA\"], \"last_name\": [\"None\", \"S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:49:30.382033\"], \"email\": [\"None\", \"gagankrishna5@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:49:30.382033\"], \"updated_at\": [\"None\", \"2025-06-20 11:49:30.382033\"], \"student\": [\"None\", \"GAGANKRISHNA, S\"], \"id\": [\"None\", \"74\"]}','2025-06-20 11:49:30.394622',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(153,'57',57,'HARSHAL, CHANDRAS',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"57\"], \"admin\": [\"None\", \"75\"]}','2025-06-20 11:49:30.414866',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(154,'75',75,'HARSHAL, CHANDRAS',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"HARSHAL\"], \"last_name\": [\"None\", \"CHANDRAS\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:49:30.411866\"], \"email\": [\"None\", \"harshal6@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:49:30.412903\"], \"updated_at\": [\"None\", \"2025-06-20 11:49:30.412903\"], \"student\": [\"None\", \"HARSHAL, CHANDRAS\"], \"id\": [\"None\", \"75\"]}','2025-06-20 11:49:30.424320',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(155,'58',58,'JOEL, JOSE',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"58\"], \"admin\": [\"None\", \"76\"]}','2025-06-20 11:49:30.441317',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(156,'76',76,'JOEL, JOSE',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"JOEL\"], \"last_name\": [\"None\", \"JOSE\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:49:30.438317\"], \"email\": [\"None\", \"joel7@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:49:30.438317\"], \"updated_at\": [\"None\", \"2025-06-20 11:49:30.438317\"], \"student\": [\"None\", \"JOEL, JOSE\"], \"id\": [\"None\", \"76\"]}','2025-06-20 11:49:30.467074',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(157,'59',59,'MADHAV, R',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"59\"], \"admin\": [\"None\", \"77\"]}','2025-06-20 11:49:30.513387',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(158,'77',77,'MADHAV, R',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"MADHAV\"], \"last_name\": [\"None\", \"R\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:49:30.488491\"], \"email\": [\"None\", \"madhav8@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:49:30.488491\"], \"updated_at\": [\"None\", \"2025-06-20 11:49:30.488491\"], \"student\": [\"None\", \"MADHAV, R\"], \"id\": [\"None\", \"77\"]}','2025-06-20 11:49:30.526394',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(159,'60',60,'RIYAN, VB',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"60\"], \"admin\": [\"None\", \"78\"]}','2025-06-20 11:49:30.566043',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(160,'78',78,'RIYAN, VB',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"RIYAN\"], \"last_name\": [\"None\", \"VB\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 11:49:30.563095\"], \"email\": [\"None\", \"riyan9@imentor.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 11:49:30.563095\"], \"updated_at\": [\"None\", \"2025-06-20 11:49:30.563095\"], \"student\": [\"None\", \"RIYAN, VB\"], \"id\": [\"None\", \"78\"]}','2025-06-20 11:49:30.593019',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(161,'1',1,', ',1,'{\"password\": [\"pbkdf2_sha256$216000$3AG3xUjhSsnI$mvpziKISQAp87oBbIpnwrZXc9rywxeu0EXbQsLgKmF4=\", \"pbkdf2_sha256$390000$t6794OeI1lu194GjrezbOI$4yjTphVD9c1/Ug1/8Ng1ATL/hx8xHiVTDH+SeJBTBo4=\"]}','2025-06-20 11:53:38.520903',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(162,'1',1,', ',1,'{\"last_login\": [\"2025-06-20 04:54:07.660159\", \"2025-06-20 11:53:38.587310\"]}','2025-06-20 11:53:38.598663',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(163,'5',5,'7 - B',0,'{\"created_at\": [\"None\", \"2025-06-20 12:03:58.709835\"], \"id\": [\"None\", \"5\"], \"updated_at\": [\"None\", \"2025-06-20 12:03:58.709835\"], \"name\": [\"None\", \"7\"], \"division\": [\"None\", \"B\"]}','2025-06-20 12:03:58.726418',1,8,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(164,'2',2,'JOHN, JOSEPH',1,'{\"last_login\": [\"2025-06-20 07:27:18.146528\", \"2025-06-20 12:04:45.490950\"]}','2025-06-20 12:04:45.495975',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(165,'61',61,'ABEL, FERNANDEZ',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"61\"], \"admin\": [\"None\", \"79\"]}','2025-06-20 12:05:01.871883',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(166,'79',79,'ABEL, FERNANDEZ',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABEL\"], \"last_name\": [\"None\", \"FERNANDEZ\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 12:05:01.863578\"], \"email\": [\"None\", \"abelfernandez1@littleflower.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 12:05:01.863578\"], \"updated_at\": [\"None\", \"2025-06-20 12:05:01.863578\"], \"student\": [\"None\", \"ABEL, FERNANDEZ\"], \"id\": [\"None\", \"79\"]}','2025-06-20 12:05:01.882037',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(167,'61',61,'ABEL, FERNANDEZ',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"5\"]}','2025-06-20 12:05:01.912584',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(168,'62',62,'ABHINAV, VA',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"62\"], \"admin\": [\"None\", \"80\"]}','2025-06-20 12:05:01.924027',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(169,'80',80,'ABHINAV, VA',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABHINAV\"], \"last_name\": [\"None\", \"VA\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 12:05:01.922028\"], \"email\": [\"None\", \"abhinavva2@littleflower.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 12:05:01.923025\"], \"updated_at\": [\"None\", \"2025-06-20 12:05:01.923025\"], \"student\": [\"None\", \"ABHINAV, VA\"], \"id\": [\"None\", \"80\"]}','2025-06-20 12:05:01.932230',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(170,'62',62,'ABHINAV, VA',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"5\"]}','2025-06-20 12:05:01.942452',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(171,'63',63,'ABIHAIL, PJ',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"63\"], \"admin\": [\"None\", \"81\"]}','2025-06-20 12:05:01.955350',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(172,'81',81,'ABIHAIL, PJ',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"ABIHAIL\"], \"last_name\": [\"None\", \"PJ\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 12:05:01.948176\"], \"email\": [\"None\", \"abihailpj3@littleflower.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 12:05:01.949271\"], \"updated_at\": [\"None\", \"2025-06-20 12:05:01.949271\"], \"student\": [\"None\", \"ABIHAIL, PJ\"], \"id\": [\"None\", \"81\"]}','2025-06-20 12:05:01.961836',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(173,'63',63,'ABIHAIL, PJ',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"5\"]}','2025-06-20 12:05:01.975212',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(174,'64',64,'SIVADEV, S',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"64\"], \"admin\": [\"None\", \"82\"]}','2025-06-20 12:07:41.446831',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(175,'82',82,'SIVADEV, S',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"SIVADEV\"], \"last_name\": [\"None\", \"S\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 12:07:41.439831\"], \"email\": [\"None\", \"sivadevs1@littleflower.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 12:07:41.440827\"], \"updated_at\": [\"None\", \"2025-06-20 12:07:41.440827\"], \"student\": [\"None\", \"SIVADEV, S\"], \"id\": [\"None\", \"82\"]}','2025-06-20 12:07:41.462043',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(176,'64',64,'SIVADEV, S',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"5\"]}','2025-06-20 12:07:41.510838',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(177,'65',65,'THEJUS, KRISH',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"65\"], \"admin\": [\"None\", \"83\"]}','2025-06-20 12:07:41.536252',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(178,'83',83,'THEJUS, KRISH',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"THEJUS\"], \"last_name\": [\"None\", \"KRISH\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 12:07:41.532250\"], \"email\": [\"None\", \"thejuskrish2@littleflower.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 12:07:41.533260\"], \"updated_at\": [\"None\", \"2025-06-20 12:07:41.533260\"], \"student\": [\"None\", \"THEJUS, KRISH\"], \"id\": [\"None\", \"83\"]}','2025-06-20 12:07:41.549954',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(179,'65',65,'THEJUS, KRISH',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"5\"]}','2025-06-20 12:07:41.587108',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(180,'66',66,'VIHAAN, RAJ',0,'{\"admission_number\": [\"None\", \"\"], \"parent_name\": [\"None\", \"\"], \"guardian_contact_number\": [\"None\", \"\"], \"mother_name\": [\"None\", \"\"], \"blood_group\": [\"None\", \"\"], \"mother_tongue\": [\"None\", \"\"], \"file_type\": [\"None\", \"\"], \"id\": [\"None\", \"66\"], \"admin\": [\"None\", \"84\"]}','2025-06-20 12:07:41.610591',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(181,'84',84,'VIHAAN, RAJ',0,'{\"password\": [\"None\", \"\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"VIHAAN\"], \"last_name\": [\"None\", \"RAJ\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-20 12:07:41.607586\"], \"email\": [\"None\", \"vihaanraj3@littleflower.school\"], \"user_type\": [\"None\", \"3\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-20 12:07:41.607586\"], \"updated_at\": [\"None\", \"2025-06-20 12:07:41.607586\"], \"student\": [\"None\", \"VIHAAN, RAJ\"], \"id\": [\"None\", \"84\"]}','2025-06-20 12:07:41.617880',2,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(182,'66',66,'VIHAAN, RAJ',1,'{\"file_type\": [\"\", \"1\"], \"course\": [\"None\", \"5\"]}','2025-06-20 12:07:41.637896',2,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(183,'1',1,', ',1,'{\"last_login\": [\"2025-06-20 11:53:38.587310\", \"2025-06-20 12:08:39.068405\"]}','2025-06-20 12:08:39.074691',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(184,'83',83,'THEJUS, KRISH',1,'{\"password\": [\"\", \"pbkdf2_sha256$390000$hgQwB54d2dJ6PzMlG7pwYt$VeKys6OwMnWWvddVsIUOXE6GXtBLHqMDjvM99QiAbjI=\"], \"email\": [\"thejuskrish2@littleflower.school\", \"thejus1020@gmail.com\"], \"gender\": [\"\", \"M\"], \"profile_pic\": [\"\", \"/media/avatar2_vlqOzcQ.png\"], \"city\": [\"\", \"Vaikom\"], \"state\": [\"\", \"Kerala\"], \"street_address\": [\"\", \"C K Road\"], \"district_name\": [\"\", \"kottayam\"], \"country\": [\"\", \"India\"]}','2025-06-21 06:41:27.325544',1,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(185,'65',65,'THEJUS, KRISH',1,'{\"session\": [\"None\", \"1\"], \"admission_number\": [\"\", \"1020\"], \"parent_name\": [\"\", \"Krishnan\"], \"guardian_contact_number\": [\"\", \"9786452319\"], \"mother_name\": [\"\", \"Priya Menon\"], \"blood_group\": [\"\", \"B+\"], \"mother_tongue\": [\"\", \"Malayalam\"]}','2025-06-21 06:41:27.372110',1,11,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(186,'2',2,'JOHN, JOSEPH',1,'{\"last_login\": [\"2025-06-20 12:04:45.490950\", \"2025-06-21 07:02:36.610745\"]}','2025-06-21 07:02:36.614846',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(187,'2',2,'POLYNOMIALS (8) PERIODS\nZEROS OF A POLYNOMIAL. RELATIONSHIP BETWEEN ZEROS AND COEFFICIENTS OF QUADRATIC\nPOLYNOMIALS.\n2. PAIR OF LINEAR EQUATIONS IN TWO VARIABLES (15) PERIODS\nPAIR OF LINEAR EQUATIONS IN TWO VARIABLES AND GRAPHICAL METHOD OF THEIR\nSOLUTION, CONSISTENCY/INCONSISTENCY.\nALGEBRAIC CONDITIONS FOR NUMBER OF SOLUTIONS. SOLUTION OF A PAIR OF LINEAR EQUATIONS IN TWO\nVARIABLES ALGEBRAICALLY - BY SUBSTITUTION, BY ELIMINATION. SIMPLE SITUATIONAL PROBLEMS. - 9 - B - Subject object (1)',0,'{\"id\": [\"None\", \"2\"], \"title\": [\"None\", \"UNIT II: ALGEBRA \"], \"status\": [\"None\", \"False\"], \"course\": [\"None\", \"2\"], \"subject\": [\"None\", \"1\"], \"lesson\": [\"None\", \"POLYNOMIALS (8) PERIODS\\nZEROS OF A POLYNOMIAL. RELATIONSHIP BETWEEN ZEROS AND COEFFICIENTS OF QUADRATIC\\nPOLYNOMIALS.\\n2. PAIR OF LINEAR EQUATIONS IN TWO VARIABLES (15) PERIODS\\nPAIR OF LINEAR EQUATIONS IN TWO VARIABLES AND GRAPHICAL METHOD OF THEIR\\nSOLUTION, CONSISTENCY/INCONSISTENCY.\\nALGEBRAIC CONDITIONS FOR NUMBER OF SOLUTIONS. SOLUTION OF A PAIR OF LINEAR EQUATIONS IN TWO\\nVARIABLES ALGEBRAICALLY - BY SUBSTITUTION, BY ELIMINATION. SIMPLE SITUATIONAL PROBLEMS.\"], \"term\": [\"None\", \"Term-1\"], \"notificaton\": [\"None\", \"False\"]}','2025-06-21 07:05:05.958334',2,24,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(188,'1',1,', ',1,'{\"last_login\": [\"2025-06-20 12:08:39.068405\", \"2025-06-23 05:35:18.935346\"]}','2025-06-23 05:35:18.974094',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(189,'1',1,', ',1,'{\"last_login\": [\"2025-06-23 05:35:18.935346\", \"2025-06-24 09:27:11.108276\"]}','2025-06-24 09:27:11.147300',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(190,'2',2,'JOHN, JOSEPH',1,'{\"last_login\": [\"2025-06-21 07:02:36.610745\", \"2025-06-24 09:28:44.173881\"]}','2025-06-24 09:28:44.176885',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(191,'1',1,'Terminal Exam',0,'{\"exam_type\": [\"None\", \"Terminal Exam\"], \"exam_name\": [\"None\", \"TERMINAL EXAM 1\"], \"term\": [\"None\", \"Term-1\"], \"max_marks\": [\"None\", \"50.0\"], \"created_at\": [\"None\", \"2025-06-24 11:53:23.515047\"], \"updated_at\": [\"None\", \"2025-06-24 11:53:23.515047\"], \"id\": [\"None\", \"1\"]}','2025-06-24 11:53:23.552044',2,35,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(192,'1',1,'Terminal Exam',1,'{\"term\": [\"Term-1\", \"Term-2\"]}','2025-06-24 11:53:39.885862',2,35,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(193,'1',1,'Terminal Exam',1,'{\"max_marks\": [\"50.0\", \"100.0\"]}','2025-06-24 11:53:51.568158',2,35,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(194,'1',1,'AccAdmin object (1)',0,'{\"accadmin\": [\"None\", \"2\"], \"id\": [\"None\", \"1\"]}','2025-06-24 11:54:12.497076',2,23,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(195,'1',1,', ',1,'{\"last_login\": [\"2025-06-24 09:27:11.108276\", \"2025-06-24 11:54:58.084861\"]}','2025-06-24 11:54:58.113321',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(196,'1',1,'ANISHA G',0,'{\"image\": [\"None\", \"/media/avatar1_s8lLRpI.png\"], \"gender\": [\"None\", \"F\"], \"email\": [\"None\", \"anisha@gmail.com\"], \"mobile\": [\"None\", \"9497008255\"], \"permanent_locality\": [\"None\", \"Harippad\"], \"permanent_district\": [\"None\", \"Alleppey\"], \"permanent_state\": [\"None\", \"Kerala\"], \"current_locality\": [\"None\", \"Harippad\"], \"current_district\": [\"None\", \"Alleppey\"], \"current_state\": [\"None\", \"Kerala\"], \"course_studied\": [\"None\", \"BCA\"], \"period_of_study\": [\"None\", \"2017 - 2020\"], \"current_status\": [\"None\", \"E\"], \"is_active\": [\"None\", \"True\"], \"id\": [\"None\", \"1\"], \"studentname\": [\"None\", \"ANISHA G\"]}','2025-06-24 11:57:28.876742',1,30,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(197,'2',2,'TIBIN THOMAS',0,'{\"image\": [\"None\", \"/media/avatar2_8etWfqa.png\"], \"gender\": [\"None\", \"M\"], \"email\": [\"None\", \"tibin@gmail.com\"], \"mobile\": [\"None\", \"9497003245\"], \"permanent_locality\": [\"None\", \"Fort Kochi\"], \"permanent_district\": [\"None\", \"Ernakulam\"], \"permanent_state\": [\"None\", \"Kerala\"], \"current_locality\": [\"None\", \"Fort Kochi\"], \"current_district\": [\"None\", \"Ernakulam\"], \"current_state\": [\"None\", \"Kerala\"], \"course_studied\": [\"None\", \"MCA\"], \"period_of_study\": [\"None\", \"2016 - 2020\"], \"current_status\": [\"None\", \"U\"], \"is_active\": [\"None\", \"True\"], \"id\": [\"None\", \"2\"], \"studentname\": [\"None\", \"TIBIN THOMAS\"]}','2025-06-24 11:58:40.528067',1,30,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(198,'2',2,'JOHN, JOSEPH',1,'{\"last_login\": [\"2025-06-24 09:28:44.173881\", \"2025-06-24 12:07:13.760699\"]}','2025-06-24 12:07:13.764142',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(199,'1',1,', ',1,'{\"last_login\": [\"2025-06-24 11:54:58.084861\", \"2025-06-24 23:55:39.321230\"]}','2025-06-24 23:55:39.361586',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(200,'4',4,'BLESSY, THOMAS',1,'{\"password\": [\"pbkdf2_sha256$216000$Sbr6GUaPZm9k$XL9zqBwyFmrFMCUwBqJ1EyZREuV8/C9VDIvGwonoAdg=\", \"pbkdf2_sha256$390000$GObcY01xzNwcbsPTuwQ2uX$7cEMSA+feY+d/r2l4SQJDlAFSlHNgQdT88Snp0t/e6U=\"]}','2025-06-24 23:56:10.295865',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(201,'4',4,'BLESSY, THOMAS',1,'{\"last_login\": [\"2025-06-15 12:33:08.432502\", \"2025-06-24 23:56:10.381415\"]}','2025-06-24 23:56:10.389747',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(202,'1',1,'StudentResult object (1)',1,'{\"test\": [\"40.0\", \"40\"], \"exam\": [\"50.0\", \"50\"]}','2025-06-25 00:26:13.589567',4,13,'127.0.0.1',NULL,NULL,NULL,'',NULL,'blessy@gmail.com'),(203,'1',1,'StudentResult object (1)',1,'{\"test\": [\"40.0\", \"42.0\"]}','2025-06-25 00:43:29.759614',4,13,'127.0.0.1',NULL,NULL,NULL,'',NULL,'blessy@gmail.com'),(204,'1',1,', ',1,'{\"last_login\": [\"2025-06-24 23:55:39.321230\", \"2025-06-25 03:47:16.809566\"]}','2025-06-25 03:47:16.860922',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(205,'1',1,'NotificationStaff object (1)',0,'{\"id\": [\"None\", \"1\"], \"staff\": [\"None\", \"1\"], \"message\": [\"None\", \"Coming Saturday (28/06/2025) will be a working day.\"], \"created_at\": [\"None\", \"2025-06-25 03:48:22.539944\"], \"updated_at\": [\"None\", \"2025-06-25 03:48:22.539944\"]}','2025-06-25 03:48:22.594982',1,15,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(206,'4',4,'BLESSY, THOMAS',1,'{\"last_login\": [\"2025-06-24 23:56:10.381415\", \"2025-06-25 03:48:40.332719\"]}','2025-06-25 03:48:40.335208',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(207,'4',4,'BLESSY, THOMAS',1,'{\"fcm_token\": [\"dRiwuPqvkXKiTajqmD4Kgj:APA91bHfxH3X7oiYIg7sLnSLWN78r4UBDn5il2v8IKB9JpiYA8LRbWa9qNGmJFRJUcIBITNhJ6wJ96Mpvnh5DIrXxFC8QwHuUJShqPYW-IWyee5CyuEqudo\", \"cTSV0pzncARpop4_GkyA2v:APA91bG6k0vkKSphdPgTkv3nISvuQwnHZa2D4bE9wl2iuk552E_uEKAXqNC7CCQIu4fL_yETz5Fza8p5o54Jw8oPT-JsArhjciyJSYeb0mj1A8Jbi8ZzUJo\"]}','2025-06-25 03:48:44.897584',4,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'blessy@gmail.com'),(208,'1',1,'LeaveReportStaff object (1)',0,'{\"id\": [\"None\", \"1\"], \"staff\": [\"None\", \"1\"], \"date\": [\"None\", \"2025-06-26\"], \"message\": [\"None\", \"Kindly grant leave on 26/06/2025 since I have to attend a PSC exam.\"], \"status\": [\"None\", \"0\"], \"created_at\": [\"None\", \"2025-06-25 03:57:29.334191\"], \"updated_at\": [\"None\", \"2025-06-25 03:57:29.334191\"], \"image\": [\"None\", \"leave_images/emblom.jpg\"]}','2025-06-25 03:57:29.360250',4,17,'127.0.0.1',NULL,NULL,NULL,'',NULL,'blessy@gmail.com'),(209,'1',1,', ',1,'{\"last_login\": [\"2025-06-25 03:47:16.809566\", \"2025-06-25 04:19:47.858366\"]}','2025-06-25 04:19:47.894919',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(210,'2',2,'JOHN, JOSEPH',1,'{\"last_login\": [\"2025-06-24 12:07:13.760699\", \"2025-06-25 04:20:16.225133\"]}','2025-06-25 04:20:16.231390',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(211,'3',3,'POLYNOMIALS (26) PERIODS\nDEFINITION OF A POLYNOMIAL IN ONE VARIABLE, WITH EXAMPLES AND COUNTER EXAMPLES. COEFFICIENTS\nOF A POLYNOMIAL, TERMS OF A POLYNOMIAL AND ZERO POLYNOMIAL. DEGREE OF A POLYNOMIAL. CONSTANT,\nLINEAR, QUADRATIC AND CUBIC POLYNOMIALS. MONOMIALS, BINOMIALS, TRINOMIALS. FACTORS AND\nMULTIPLES. ZEROS OF A POLYNOMIAL. MOTIVATE AND STATE THE REMAINDER THEOREM WITH EXAMPLES.\nSTATEMENT AND PROOF OF THE FACTOR THEOREM. FACTORIZATION OF AX2 + BX + C, A ≠ 0 WHERE A, B AND\nC ARE REAL NUMBERS, AND OF CUBIC POLYNOMIALS USING THE FACTOR THEOREM.\n - 9 - B - Subject object (1)',0,'{\"id\": [\"None\", \"3\"], \"title\": [\"None\", \"UNIT I: ALGEBRA \"], \"status\": [\"None\", \"False\"], \"course\": [\"None\", \"2\"], \"subject\": [\"None\", \"1\"], \"lesson\": [\"None\", \"POLYNOMIALS (26) PERIODS\\nDEFINITION OF A POLYNOMIAL IN ONE VARIABLE, WITH EXAMPLES AND COUNTER EXAMPLES. COEFFICIENTS\\nOF A POLYNOMIAL, TERMS OF A POLYNOMIAL AND ZERO POLYNOMIAL. DEGREE OF A POLYNOMIAL. CONSTANT,\\nLINEAR, QUADRATIC AND CUBIC POLYNOMIALS. MONOMIALS, BINOMIALS, TRINOMIALS. FACTORS AND\\nMULTIPLES. ZEROS OF A POLYNOMIAL. MOTIVATE AND STATE THE REMAINDER THEOREM WITH EXAMPLES.\\nSTATEMENT AND PROOF OF THE FACTOR THEOREM. FACTORIZATION OF AX2 + BX + C, A \\u2260 0 WHERE A, B AND\\nC ARE REAL NUMBERS, AND OF CUBIC POLYNOMIALS USING THE FACTOR THEOREM.\\n\"], \"term\": [\"None\", \"Term-1\"], \"notificaton\": [\"None\", \"False\"]}','2025-06-25 04:22:41.115990',2,24,'127.0.0.1',NULL,NULL,NULL,'',NULL,'john@gmail.com'),(212,'1',1,', ',1,'{\"last_login\": [\"2025-06-25 04:19:47.858366\", \"2025-06-25 04:23:12.152961\"]}','2025-06-25 04:23:12.174151',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(213,'2',2,'BEENA MATHEW',0,'{\"admin\": [\"None\", \"85\"], \"contact_number\": [\"None\", \"\"], \"id\": [\"None\", \"2\"]}','2025-06-25 04:25:14.065270',1,10,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(214,'85',85,'BEENA, MATHEW',0,'{\"password\": [\"None\", \"pbkdf2_sha256$390000$IyATDZ3hDJcMJRjMhaVP7h$gJUAY6rWfj+/9u32Lla9mxG3ilE9nrQNUW0I1l8IB+c=\"], \"staff\": [\"None\", \"BEENA MATHEW\"], \"is_superuser\": [\"None\", \"False\"], \"first_name\": [\"None\", \"BEENA\"], \"last_name\": [\"None\", \"MATHEW\"], \"is_staff\": [\"None\", \"False\"], \"is_active\": [\"None\", \"True\"], \"date_joined\": [\"None\", \"2025-06-25 04:25:12.891347\"], \"email\": [\"None\", \"beena@gmail.com\"], \"user_type\": [\"None\", \"2\"], \"gender\": [\"None\", \"\"], \"profile_pic\": [\"None\", \"/media/avatar1_vJ0Fs97.png\"], \"city\": [\"None\", \"\"], \"state\": [\"None\", \"\"], \"street_address\": [\"None\", \"\"], \"district_name\": [\"None\", \"\"], \"country\": [\"None\", \"\"], \"date_of_birth\": [\"None\", \"1985-03-11\"], \"fcm_token\": [\"None\", \"\"], \"created_at\": [\"None\", \"2025-06-25 04:25:13.952872\"], \"updated_at\": [\"None\", \"2025-06-25 04:25:13.952872\"], \"id\": [\"None\", \"85\"]}','2025-06-25 04:25:14.106474',1,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(215,'85',85,'BEENA, MATHEW',1,'{\"gender\": [\"\", \"F\"], \"city\": [\"\", \"Cherthala\"], \"state\": [\"\", \"Kerala\"], \"district_name\": [\"\", \"Alleppey\"], \"country\": [\"\", \"India\"]}','2025-06-25 04:25:14.127328',1,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(216,'2',2,'BEENA MATHEW',1,'{\"department\": [\"None\", \"1\"], \"course\": [\"None\", \"2\"]}','2025-06-25 04:25:14.176864',1,10,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(217,'85',85,'BEENA, MATHEW',1,'{\"last_login\": [\"None\", \"2025-06-25 04:25:51.281154\"]}','2025-06-25 04:25:51.286184',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(218,'85',85,'BEENA, MATHEW',1,'{\"fcm_token\": [\"\", \"cTSV0pzncARpop4_GkyA2v:APA91bG6k0vkKSphdPgTkv3nISvuQwnHZa2D4bE9wl2iuk552E_uEKAXqNC7CCQIu4fL_yETz5Fza8p5o54Jw8oPT-JsArhjciyJSYeb0mj1A8Jbi8ZzUJo\"]}','2025-06-25 04:25:51.927561',85,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,'beena@gmail.com'),(219,'1',1,', ',1,'{\"last_login\": [\"2025-06-25 04:23:12.152961\", \"2025-06-25 04:26:35.530203\"]}','2025-06-25 04:26:35.574285',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL),(220,'3',3,'Subject object (3)',0,'{\"id\": [\"None\", \"3\"], \"subject\": [\"None\", \"1\"], \"staff\": [\"None\", \"2\"], \"course\": [\"None\", \"2\"], \"updated_at\": [\"None\", \"2025-06-25 04:26:57.056393\"], \"created_at\": [\"None\", \"2025-06-25 04:26:57.056393\"]}','2025-06-25 04:26:57.095390',1,12,'127.0.0.1',NULL,NULL,NULL,'',NULL,'anu@gmail.com'),(221,'85',85,'BEENA, MATHEW',1,'{\"last_login\": [\"2025-06-25 04:25:51.281154\", \"2025-06-25 04:27:17.195793\"]}','2025-06-25 04:27:17.198186',NULL,6,'127.0.0.1',NULL,NULL,NULL,'',NULL,NULL);
/*!40000 ALTER TABLE `auditlog_logentry` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=137 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add user',6,'add_customuser'),(22,'Can change user',6,'change_customuser'),(23,'Can delete user',6,'delete_customuser'),(24,'Can view user',6,'view_customuser'),(25,'Can add attendance',7,'add_attendance'),(26,'Can change attendance',7,'change_attendance'),(27,'Can delete attendance',7,'delete_attendance'),(28,'Can view attendance',7,'view_attendance'),(29,'Can add course',8,'add_course'),(30,'Can change course',8,'change_course'),(31,'Can delete course',8,'delete_course'),(32,'Can view course',8,'view_course'),(33,'Can add session',9,'add_session'),(34,'Can change session',9,'change_session'),(35,'Can delete session',9,'delete_session'),(36,'Can view session',9,'view_session'),(37,'Can add staff',10,'add_staff'),(38,'Can change staff',10,'change_staff'),(39,'Can delete staff',10,'delete_staff'),(40,'Can view staff',10,'view_staff'),(41,'Can add student',11,'add_student'),(42,'Can change student',11,'change_student'),(43,'Can delete student',11,'delete_student'),(44,'Can view student',11,'view_student'),(45,'Can add subject',12,'add_subject'),(46,'Can change subject',12,'change_subject'),(47,'Can delete subject',12,'delete_subject'),(48,'Can view subject',12,'view_subject'),(49,'Can add student result',13,'add_studentresult'),(50,'Can change student result',13,'change_studentresult'),(51,'Can delete student result',13,'delete_studentresult'),(52,'Can view student result',13,'view_studentresult'),(53,'Can add notification student',14,'add_notificationstudent'),(54,'Can change notification student',14,'change_notificationstudent'),(55,'Can delete notification student',14,'delete_notificationstudent'),(56,'Can view notification student',14,'view_notificationstudent'),(57,'Can add notification staff',15,'add_notificationstaff'),(58,'Can change notification staff',15,'change_notificationstaff'),(59,'Can delete notification staff',15,'delete_notificationstaff'),(60,'Can view notification staff',15,'view_notificationstaff'),(61,'Can add leave report student',16,'add_leavereportstudent'),(62,'Can change leave report student',16,'change_leavereportstudent'),(63,'Can delete leave report student',16,'delete_leavereportstudent'),(64,'Can view leave report student',16,'view_leavereportstudent'),(65,'Can add leave report staff',17,'add_leavereportstaff'),(66,'Can change leave report staff',17,'change_leavereportstaff'),(67,'Can delete leave report staff',17,'delete_leavereportstaff'),(68,'Can view leave report staff',17,'view_leavereportstaff'),(69,'Can add feedback student',18,'add_feedbackstudent'),(70,'Can change feedback student',18,'change_feedbackstudent'),(71,'Can delete feedback student',18,'delete_feedbackstudent'),(72,'Can view feedback student',18,'view_feedbackstudent'),(73,'Can add feedback staff',19,'add_feedbackstaff'),(74,'Can change feedback staff',19,'change_feedbackstaff'),(75,'Can delete feedback staff',19,'delete_feedbackstaff'),(76,'Can view feedback staff',19,'view_feedbackstaff'),(77,'Can add attendance report',20,'add_attendancereport'),(78,'Can change attendance report',20,'change_attendancereport'),(79,'Can delete attendance report',20,'delete_attendancereport'),(80,'Can view attendance report',20,'view_attendancereport'),(81,'Can add admin',21,'add_admin'),(82,'Can change admin',21,'change_admin'),(83,'Can delete admin',21,'delete_admin'),(84,'Can view admin',21,'view_admin'),(85,'Can add exam form',22,'add_examform'),(86,'Can change exam form',22,'change_examform'),(87,'Can delete exam form',22,'delete_examform'),(88,'Can view exam form',22,'view_examform'),(89,'Can add acc admin',23,'add_accadmin'),(90,'Can change acc admin',23,'change_accadmin'),(91,'Can delete acc admin',23,'delete_accadmin'),(92,'Can view acc admin',23,'view_accadmin'),(93,'Can add curriculam',24,'add_curriculam'),(94,'Can change curriculam',24,'change_curriculam'),(95,'Can delete curriculam',24,'delete_curriculam'),(96,'Can view curriculam',24,'view_curriculam'),(97,'Can add subjectmaster',25,'add_subjectmaster'),(98,'Can change subjectmaster',25,'change_subjectmaster'),(99,'Can delete subjectmaster',25,'delete_subjectmaster'),(100,'Can view subjectmaster',25,'view_subjectmaster'),(101,'Can add department',26,'add_department'),(102,'Can change department',26,'change_department'),(103,'Can delete department',26,'delete_department'),(104,'Can view department',26,'view_department'),(105,'Can add school',27,'add_school'),(106,'Can change school',27,'change_school'),(107,'Can delete school',27,'delete_school'),(108,'Can view school',27,'view_school'),(109,'Can add file',28,'add_file'),(110,'Can change file',28,'change_file'),(111,'Can delete file',28,'delete_file'),(112,'Can view file',28,'view_file'),(113,'Can add fee settings',29,'add_feesettings'),(114,'Can change fee settings',29,'change_feesettings'),(115,'Can delete fee settings',29,'delete_feesettings'),(116,'Can view fee settings',29,'view_feesettings'),(117,'Can add alumini settings',30,'add_aluminisettings'),(118,'Can change alumini settings',30,'change_aluminisettings'),(119,'Can delete alumini settings',30,'delete_aluminisettings'),(120,'Can view alumini settings',30,'view_aluminisettings'),(121,'Can add fee amount settings',31,'add_feeamountsettings'),(122,'Can change fee amount settings',31,'change_feeamountsettings'),(123,'Can delete fee amount settings',31,'delete_feeamountsettings'),(124,'Can view fee amount settings',31,'view_feeamountsettings'),(125,'Can add lesson settings',32,'add_lessonsettings'),(126,'Can change lesson settings',32,'change_lessonsettings'),(127,'Can delete lesson settings',32,'delete_lessonsettings'),(128,'Can view lesson settings',32,'view_lessonsettings'),(129,'Can add staff attendance',33,'add_staffattendance'),(130,'Can change staff attendance',33,'change_staffattendance'),(131,'Can delete staff attendance',33,'delete_staffattendance'),(132,'Can view staff attendance',33,'view_staffattendance'),(133,'Can add log entry',34,'add_logentry'),(134,'Can change log entry',34,'change_logentry'),(135,'Can delete log entry',34,'delete_logentry'),(136,'Can view log entry',34,'view_logentry');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_main_app_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_main_app_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `main_app_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(34,'auditlog','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(23,'main_app','accadmin'),(21,'main_app','admin'),(30,'main_app','aluminisettings'),(7,'main_app','attendance'),(20,'main_app','attendancereport'),(8,'main_app','course'),(24,'main_app','curriculam'),(6,'main_app','customuser'),(26,'main_app','department'),(22,'main_app','examform'),(35,'main_app','examtypesettings'),(31,'main_app','feeamountsettings'),(19,'main_app','feedbackstaff'),(18,'main_app','feedbackstudent'),(29,'main_app','feesettings'),(28,'main_app','file'),(17,'main_app','leavereportstaff'),(16,'main_app','leavereportstudent'),(32,'main_app','lessonsettings'),(15,'main_app','notificationstaff'),(14,'main_app','notificationstudent'),(27,'main_app','school'),(9,'main_app','session'),(10,'main_app','staff'),(33,'main_app','staffattendance'),(11,'main_app','student'),(13,'main_app','studentresult'),(12,'main_app','subject'),(25,'main_app','subjectmaster'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-06-13 15:27:03.829279'),(2,'contenttypes','0002_remove_content_type_name','2025-06-13 15:27:03.911510'),(3,'auth','0001_initial','2025-06-13 15:27:04.018221'),(4,'auth','0002_alter_permission_name_max_length','2025-06-13 15:27:04.308745'),(5,'auth','0003_alter_user_email_max_length','2025-06-13 15:27:04.326837'),(6,'auth','0004_alter_user_username_opts','2025-06-13 15:27:04.342463'),(7,'auth','0005_alter_user_last_login_null','2025-06-13 15:27:04.358636'),(8,'auth','0006_require_contenttypes_0002','2025-06-13 15:27:04.363637'),(9,'auth','0007_alter_validators_add_error_messages','2025-06-13 15:27:04.378286'),(10,'auth','0008_alter_user_username_max_length','2025-06-13 15:27:04.392133'),(11,'auth','0009_alter_user_last_name_max_length','2025-06-13 15:27:04.411332'),(12,'auth','0010_alter_group_name_max_length','2025-06-13 15:27:04.445366'),(13,'auth','0011_update_proxy_permissions','2025-06-13 15:27:04.461521'),(14,'auth','0012_alter_user_first_name_max_length','2025-06-13 15:27:04.475381'),(15,'main_app','0001_initial','2025-06-13 15:27:05.576180'),(16,'admin','0001_initial','2025-06-13 15:27:07.163357'),(17,'admin','0002_logentry_remove_auto_add','2025-06-13 15:27:07.330344'),(18,'admin','0003_logentry_add_action_flag_choices','2025-06-13 15:27:07.367250'),(19,'main_app','0002_student_admission_number','2025-06-13 15:27:07.445938'),(20,'main_app','0003_student_admission_date_student_age','2025-06-13 15:27:07.508331'),(21,'main_app','0004_student_parent_name','2025-06-13 15:27:07.557944'),(22,'main_app','0005_student_parent_address','2025-06-13 15:27:07.604343'),(23,'main_app','0006_student_parent_phone_number','2025-06-13 15:27:07.661326'),(24,'main_app','0007_student_parent_email','2025-06-13 15:27:07.728520'),(25,'main_app','0008_student_religion','2025-06-13 15:27:07.781423'),(26,'main_app','0009_student_caste','2025-06-13 15:27:07.846315'),(27,'main_app','0010_student_state','2025-06-13 15:27:07.914467'),(28,'main_app','0011_student_mother_tongue','2025-06-13 15:27:07.973225'),(29,'main_app','0012_student_identification_mark1_and_more','2025-06-13 15:27:08.093043'),(30,'main_app','0013_remove_student_admission_date_remove_student_age_and_more','2025-06-13 15:27:08.490285'),(31,'main_app','0014_alter_customuser_user_type_parent','2025-06-13 15:27:08.573515'),(32,'main_app','0015_alter_customuser_user_type_delete_parent','2025-06-13 15:27:08.668217'),(33,'main_app','0016_remove_student_admission_date_student_parent_name','2025-06-13 15:27:08.725141'),(34,'main_app','0017_student_mother_tongue','2025-06-13 15:27:08.778594'),(35,'main_app','0018_customuser_date_of_birth','2025-06-13 15:27:08.821239'),(36,'main_app','0019_alter_customuser_date_of_birth','2025-06-13 15:27:08.831721'),(37,'main_app','0020_alter_customuser_profile_pic','2025-06-13 15:27:08.880039'),(38,'main_app','0021_alter_customuser_profile_pic','2025-06-13 15:27:08.977180'),(39,'main_app','0022_examform_studentresult_remarks_and_more','2025-06-13 15:27:09.155597'),(40,'main_app','0023_alter_customuser_date_of_birth','2025-06-13 15:27:09.266614'),(41,'main_app','0024_studentresult_term','2025-06-13 15:27:09.339239'),(42,'main_app','0025_auto_20240807_1232','2025-06-13 15:27:09.620167'),(43,'main_app','0026_alter_customuser_user_type_accadmin','2025-06-13 15:27:09.911651'),(44,'main_app','0027_alter_customuser_user_type','2025-06-13 15:27:10.012535'),(45,'main_app','0026_remove_staff_course_course_division_staff_department','2025-06-13 15:27:10.110309'),(46,'main_app','0028_merge_20240911_1347','2025-06-13 15:27:10.120340'),(47,'main_app','0029_curriculam','2025-06-13 15:27:10.181692'),(48,'main_app','0030_curriculam_course_curriculam_subject','2025-06-13 15:27:10.419402'),(49,'main_app','0031_curriculam_status','2025-06-13 15:27:10.479055'),(50,'main_app','0032_curriculam_term_alter_curriculam_lesson','2025-06-13 15:27:10.606241'),(51,'main_app','0033_alter_curriculam_term','2025-06-13 15:27:10.639937'),(52,'main_app','0034_curriculam_staff','2025-06-13 15:27:10.767532'),(53,'main_app','0035_remove_curriculam_staff','2025-06-13 15:27:10.920190'),(54,'main_app','0036_subjectmaster','2025-06-13 15:27:10.966978'),(55,'main_app','0037_rename_sub_name_subjectmaster_name','2025-06-13 15:27:10.992474'),(56,'main_app','0038_department','2025-06-13 15:27:11.034969'),(57,'main_app','0039_remove_staff_department_staff_deptmnt_and_more','2025-06-13 15:27:11.358359'),(58,'main_app','0040_rename_deptmnt_staff_department','2025-06-13 15:27:11.529355'),(59,'main_app','0041_remove_subject_name_subject_subject','2025-06-13 15:27:11.675275'),(60,'main_app','0042_alter_studentresult_subject','2025-06-13 15:27:11.825533'),(61,'main_app','0043_alter_studentresult_subject','2025-06-13 15:27:12.104894'),(62,'main_app','0044_student_file_type','2025-06-13 15:27:12.157818'),(63,'main_app','0045_alter_student_file_type','2025-06-13 15:27:12.207350'),(64,'main_app','0046_alter_student_file_type','2025-06-13 15:27:12.251826'),(65,'main_app','0047_school','2025-06-13 15:27:12.311622'),(66,'main_app','0048_alter_school_address','2025-06-13 15:27:12.379204'),(67,'main_app','0049_alter_school_email','2025-06-13 15:27:12.449253'),(68,'main_app','0050_alter_school_address_alter_school_email_and_more','2025-06-13 15:27:12.498892'),(69,'main_app','0051_alter_school_image','2025-06-13 15:27:12.529369'),(70,'main_app','0052_curriculam_notificaton','2025-06-13 15:27:12.594435'),(71,'main_app','0053_leavereportstaff_image','2025-06-13 15:27:12.633326'),(72,'main_app','0054_file','2025-06-13 15:27:12.668199'),(73,'main_app','0055_feesettings','2025-06-13 15:27:12.716944'),(74,'main_app','0056_remove_feesettings_academic_year','2025-06-13 15:27:12.752184'),(75,'main_app','0055_aluminisettings','2025-06-13 15:27:12.841978'),(76,'main_app','0057_merge_20250205_1041','2025-06-13 15:27:12.856959'),(77,'main_app','0058_district_state_alter_curriculam_lesson_locality_and_more','2025-06-13 15:27:12.884738'),(78,'main_app','0059_leavereportstudent_image','2025-06-13 15:27:12.945592'),(79,'main_app','0059_alter_student_admission_number_and_more','2025-06-13 15:27:13.047924'),(80,'main_app','0060_merge_20250225_1129','2025-06-13 15:27:13.057274'),(81,'main_app','0061_auto_20250306_1112','2025-06-13 15:27:13.206420'),(82,'main_app','0062_staff_contact_number','2025-06-13 15:27:13.275510'),(83,'main_app','0061_auto_20250305_0849','2025-06-13 15:27:13.398525'),(84,'main_app','0062_aluminisettings_image','2025-06-13 15:27:13.457185'),(85,'main_app','0061_remove_locality_district_alter_studentresult_term_and_more','2025-06-13 15:27:13.599533'),(86,'main_app','0062_alter_studentresult_term','2025-06-13 15:27:13.656382'),(87,'main_app','0063_merge_20250312_1828','2025-06-13 15:27:13.673642'),(88,'main_app','0064_feeamountsettings','2025-06-13 15:27:13.773275'),(89,'main_app','0065_studentresult_subjectmaster_and_more','2025-06-13 15:27:14.362188'),(90,'main_app','0066_lessonsettings','2025-06-13 15:27:14.455205'),(91,'main_app','0067_alter_lessonsettings_date','2025-06-13 15:27:14.781256'),(92,'main_app','0068_curriculam_title','2025-06-13 15:27:14.822172'),(93,'main_app','0069_rename_curriculam_lessonsettings_title','2025-06-13 15:27:14.978264'),(94,'main_app','0070_rename_title_lessonsettings_curriculam','2025-06-13 15:27:15.181447'),(95,'main_app','0063_merge_20250311_1641','2025-06-13 15:27:15.195509'),(96,'main_app','0065_merge_0063_merge_20250311_1641_0064_feeamountsettings','2025-06-13 15:27:15.216297'),(97,'main_app','0064_aluminisettings_is_active','2025-06-13 15:27:15.251656'),(98,'main_app','0066_merge_20250325_1624','2025-06-13 15:27:15.269300'),(99,'main_app','0056_merge_20250207_1424','2025-06-13 15:27:15.295429'),(100,'main_app','0071_merge_20250401_1238','2025-06-13 15:27:15.328027'),(101,'main_app','0072_file','2025-06-13 15:27:15.344562'),(102,'main_app','0073_auto_20250407_1316','2025-06-13 15:27:15.395619'),(103,'main_app','0063_merge_20250319_1519','2025-06-13 15:27:15.418253'),(104,'main_app','0064_staffattendance','2025-06-13 15:27:15.516396'),(105,'main_app','0074_merge_20250611_1232','2025-06-13 15:27:15.587112'),(106,'main_app','0075_staffattendance_is_active','2025-06-13 15:27:15.638656'),(107,'sessions','0001_initial','2025-06-13 15:27:15.675140'),(108,'auditlog','0001_initial','2025-06-20 07:19:19.551142'),(109,'auditlog','0002_auto_support_long_primary_keys','2025-06-20 07:19:20.631271'),(110,'auditlog','0003_logentry_remote_addr','2025-06-20 07:19:20.649221'),(111,'auditlog','0004_logentry_detailed_object_repr','2025-06-20 07:19:20.681338'),(112,'auditlog','0005_logentry_additional_data_verbose_name','2025-06-20 07:19:20.726383'),(113,'auditlog','0006_object_pk_index','2025-06-20 07:19:20.838904'),(114,'auditlog','0007_object_pk_type','2025-06-20 07:19:20.850291'),(115,'auditlog','0008_action_index','2025-06-20 07:19:20.907655'),(116,'auditlog','0009_alter_logentry_additional_data','2025-06-20 07:19:20.931664'),(117,'auditlog','0010_alter_logentry_timestamp','2025-06-20 07:19:20.968382'),(118,'auditlog','0011_logentry_serialized_data','2025-06-20 07:19:21.011392'),(119,'auditlog','0012_add_logentry_action_access','2025-06-20 07:19:21.041789'),(120,'auditlog','0013_alter_logentry_timestamp','2025-06-20 07:19:21.079972'),(121,'auditlog','0014_logentry_cid','2025-06-20 07:19:21.149667'),(122,'auditlog','0015_alter_logentry_changes','2025-06-20 07:19:21.378351'),(123,'auditlog','0016_logentry_remote_port','2025-06-20 07:19:21.414354'),(124,'auditlog','0017_add_actor_email','2025-06-20 07:19:21.460028'),(125,'main_app','0074_merge_0064_staffattendance_0073_auto_20250407_1316','2025-06-20 07:19:21.477037'),(126,'main_app','0075_examtypesettings_userloginrecord_delete_examform_and_more','2025-06-24 11:49:59.971486'),(127,'main_app','0074_file','2025-06-24 12:33:04.549819');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('dfb104co30uk7m61t6xq1fcrouaxliwb','.eJxViz0OwjAMRu-SGSGI48RmROIckd06SgVUFaVT1bsTxEK39_281WVZ3jUvs73y0LuLI3SH_1Klu9v4XZ4yjFmm6Xhr9Lj--l3Ym1Xm2jSvMYIoeGLD_gycLHgoFBsJABdNemIq0DGlkFjbERkFAxqRJLd9ABqENBk:1uUHjB:VOMUhMRUV3VUHPEC27F6-OTqJqBgEfwZQ8hOjUo0t1I','2025-07-09 04:27:17.249120'),('o644zbmhwhx2utph6okvoyzc9bhuu07v','.eJxVi0EKwjAQRe-StUjGTDKJS8FzhF8nIUUtxdqVeHcr3bS7_9_jfUzG_G55nsor92rOhsxhyzrc7mX4iyf6IWMcj9dlPS4r35192TC1JXOsNUR2Hqynqr6QhdWQSLkoRY9YbA3JsbhEqQrYC1EnBAkS4M33BwjeND0:1uTZpv:tqwPLIKa2n3G7khloNGexG0xRj2zsUMtk4cnp6NZ2aE','2025-07-07 05:35:19.003470');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_accadmin`
--

DROP TABLE IF EXISTS `main_app_accadmin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_accadmin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `accadmin_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accadmin_id` (`accadmin_id`),
  CONSTRAINT `main_app_accadmin_accadmin_id_bf23001a_fk_main_app_customuser_id` FOREIGN KEY (`accadmin_id`) REFERENCES `main_app_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_accadmin`
--

LOCK TABLES `main_app_accadmin` WRITE;
/*!40000 ALTER TABLE `main_app_accadmin` DISABLE KEYS */;
INSERT INTO `main_app_accadmin` VALUES (1,2);
/*!40000 ALTER TABLE `main_app_accadmin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_admin`
--

DROP TABLE IF EXISTS `main_app_admin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `admin_id` (`admin_id`),
  CONSTRAINT `main_app_admin_admin_id_677566c2_fk_main_app_customuser_id` FOREIGN KEY (`admin_id`) REFERENCES `main_app_customuser` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_admin`
--

LOCK TABLES `main_app_admin` WRITE;
/*!40000 ALTER TABLE `main_app_admin` DISABLE KEYS */;
INSERT INTO `main_app_admin` VALUES (1,1);
/*!40000 ALTER TABLE `main_app_admin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_aluminisettings`
--

DROP TABLE IF EXISTS `main_app_aluminisettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_aluminisettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `studentname` varchar(40) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `mobile` varchar(10) NOT NULL,
  `permanent_locality` varchar(30) NOT NULL,
  `permanent_district` varchar(30) NOT NULL,
  `permanent_state` varchar(30) NOT NULL,
  `current_locality` varchar(30) NOT NULL,
  `current_district` varchar(30) NOT NULL,
  `current_state` varchar(30) NOT NULL,
  `course_studied` varchar(50) NOT NULL,
  `period_of_study` varchar(50) NOT NULL,
  `current_status` varchar(1) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_aluminisettings`
--

LOCK TABLES `main_app_aluminisettings` WRITE;
/*!40000 ALTER TABLE `main_app_aluminisettings` DISABLE KEYS */;
INSERT INTO `main_app_aluminisettings` VALUES (1,'ANISHA G','F','anisha@gmail.com','9497008255','Harippad','Alleppey','Kerala','Harippad','Alleppey','Kerala','BCA','2017 - 2020','E','/media/avatar1_s8lLRpI.png',1),(2,'TIBIN THOMAS','M','tibin@gmail.com','9497003245','Fort Kochi','Ernakulam','Kerala','Fort Kochi','Ernakulam','Kerala','MCA','2016 - 2020','U','/media/avatar2_8etWfqa.png',1);
/*!40000 ALTER TABLE `main_app_aluminisettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_attendance`
--

DROP TABLE IF EXISTS `main_app_attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_attendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `session_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_attendance_session_id_b5e3071a_fk_main_app_session_id` (`session_id`),
  KEY `main_app_attendance_subject_id_4de67085_fk_main_app_subject_id` (`subject_id`),
  CONSTRAINT `main_app_attendance_session_id_b5e3071a_fk_main_app_session_id` FOREIGN KEY (`session_id`) REFERENCES `main_app_session` (`id`),
  CONSTRAINT `main_app_attendance_subject_id_4de67085_fk_main_app_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `main_app_subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_attendance`
--

LOCK TABLES `main_app_attendance` WRITE;
/*!40000 ALTER TABLE `main_app_attendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_attendancereport`
--

DROP TABLE IF EXISTS `main_app_attendancereport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_attendancereport` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `attendance_id` int(11) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_attendancer_attendance_id_8102922e_fk_main_app_` (`attendance_id`),
  KEY `main_app_attendancer_student_id_0957b64c_fk_main_app_` (`student_id`),
  CONSTRAINT `main_app_attendancer_attendance_id_8102922e_fk_main_app_` FOREIGN KEY (`attendance_id`) REFERENCES `main_app_attendance` (`id`),
  CONSTRAINT `main_app_attendancer_student_id_0957b64c_fk_main_app_` FOREIGN KEY (`student_id`) REFERENCES `main_app_student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_attendancereport`
--

LOCK TABLES `main_app_attendancereport` WRITE;
/*!40000 ALTER TABLE `main_app_attendancereport` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_attendancereport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_course`
--

DROP TABLE IF EXISTS `main_app_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `division` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_course`
--

LOCK TABLES `main_app_course` WRITE;
/*!40000 ALTER TABLE `main_app_course` DISABLE KEYS */;
INSERT INTO `main_app_course` VALUES (1,'8','2025-06-15 12:14:26.932665','2025-06-15 12:14:26.932665','A'),(2,'9','2025-06-15 12:14:39.569166','2025-06-15 12:14:39.569166','B'),(3,'11','2025-06-19 00:02:55.471408','2025-06-19 00:02:55.471408','A'),(4,'7','2025-06-20 07:22:34.608336','2025-06-20 07:22:34.608336','C'),(5,'7','2025-06-20 12:03:58.709835','2025-06-20 12:03:58.709835','B');
/*!40000 ALTER TABLE `main_app_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_curriculam`
--

DROP TABLE IF EXISTS `main_app_curriculam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_curriculam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `lesson` longtext NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `term` longtext NOT NULL,
  `notificaton` longtext NOT NULL,
  `title` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_curriculam_course_id_cd599b63_fk_main_app_course_id` (`course_id`),
  KEY `main_app_curriculam_subject_id_7e56013a_fk_main_app_subject_id` (`subject_id`),
  CONSTRAINT `main_app_curriculam_course_id_cd599b63_fk_main_app_course_id` FOREIGN KEY (`course_id`) REFERENCES `main_app_course` (`id`),
  CONSTRAINT `main_app_curriculam_subject_id_7e56013a_fk_main_app_subject_id` FOREIGN KEY (`subject_id`) REFERENCES `main_app_subject` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_curriculam`
--

LOCK TABLES `main_app_curriculam` WRITE;
/*!40000 ALTER TABLE `main_app_curriculam` DISABLE KEYS */;
INSERT INTO `main_app_curriculam` VALUES (1,'1. REAL NUMBER (15) PERIODS\nFUNDAMENTAL THEOREM OF ARITHMETIC - STATEMENTS AFTER REVIEWING WORK DONE EARLIER AND\nAFTER ILLUSTRATING AND MOTIVATING THROUGH EXAMPLES, PROOFS OF IRRATIONALITY OF SQUARE ROOT OF 2,3,5\n',2,1,1,'Term-1','False','UNIT I: NUMBER SYSTEMS'),(2,'POLYNOMIALS (8) PERIODS\nZEROS OF A POLYNOMIAL. RELATIONSHIP BETWEEN ZEROS AND COEFFICIENTS OF QUADRATIC\nPOLYNOMIALS.\n2. PAIR OF LINEAR EQUATIONS IN TWO VARIABLES (15) PERIODS\nPAIR OF LINEAR EQUATIONS IN TWO VARIABLES AND GRAPHICAL METHOD OF THEIR\nSOLUTION, CONSISTENCY/INCONSISTENCY.\nALGEBRAIC CONDITIONS FOR NUMBER OF SOLUTIONS. SOLUTION OF A PAIR OF LINEAR EQUATIONS IN TWO\nVARIABLES ALGEBRAICALLY - BY SUBSTITUTION, BY ELIMINATION. SIMPLE SITUATIONAL PROBLEMS.',2,1,0,'Term-1','False','UNIT II: ALGEBRA '),(3,'POLYNOMIALS (26) PERIODS\nDEFINITION OF A POLYNOMIAL IN ONE VARIABLE, WITH EXAMPLES AND COUNTER EXAMPLES. COEFFICIENTS\nOF A POLYNOMIAL, TERMS OF A POLYNOMIAL AND ZERO POLYNOMIAL. DEGREE OF A POLYNOMIAL. CONSTANT,\nLINEAR, QUADRATIC AND CUBIC POLYNOMIALS. MONOMIALS, BINOMIALS, TRINOMIALS. FACTORS AND\nMULTIPLES. ZEROS OF A POLYNOMIAL. MOTIVATE AND STATE THE REMAINDER THEOREM WITH EXAMPLES.\nSTATEMENT AND PROOF OF THE FACTOR THEOREM. FACTORIZATION OF AX2 + BX + C, A ≠ 0 WHERE A, B AND\nC ARE REAL NUMBERS, AND OF CUBIC POLYNOMIALS USING THE FACTOR THEOREM.\n',2,1,0,'Term-1','False','UNIT I: ALGEBRA ');
/*!40000 ALTER TABLE `main_app_curriculam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_customuser`
--

DROP TABLE IF EXISTS `main_app_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_customuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `user_type` varchar(1) NOT NULL,
  `gender` varchar(1) NOT NULL,
  `profile_pic` varchar(100) DEFAULT NULL,
  `fcm_token` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `city` longtext NOT NULL,
  `country` longtext NOT NULL,
  `district_name` longtext NOT NULL,
  `state` longtext NOT NULL,
  `street_address` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_customuser`
--

LOCK TABLES `main_app_customuser` WRITE;
/*!40000 ALTER TABLE `main_app_customuser` DISABLE KEYS */;
INSERT INTO `main_app_customuser` VALUES (1,'pbkdf2_sha256$390000$t6794OeI1lu194GjrezbOI$4yjTphVD9c1/Ug1/8Ng1ATL/hx8xHiVTDH+SeJBTBo4=','2025-06-25 04:26:35.530203',1,'','',1,1,'2025-06-13 15:33:30.296712','anu@gmail.com','1','','','','2025-06-13 15:33:30.535005','2025-06-13 15:33:30.535005',NULL,'','','','',''),(2,'pbkdf2_sha256$390000$k1w9GKCj3ko8lxZFcVKxE2$VCJbbZRk+IB5B5Jcn8ECmkZwxSGO+jZ9DTY2ZBXh3Ro=','2025-06-25 04:20:16.225133',0,'JOHN','JOSEPH',0,1,'2025-06-15 12:16:45.508030','john@gmail.com','4','','/media/avatar2.png','','2025-06-15 12:16:45.680247','2025-06-15 12:16:45.680247',NULL,'','','','',''),(3,'pbkdf2_sha256$216000$zesY2xApzncL$BYy9KrzLmDTjZ0r/nAK+LjHjf5qgbeNeUxEi9kbZ5iA=',NULL,0,'JOHN','JOSEPH',0,1,'2025-06-15 12:18:23.087432','johnjoseph@gmail.com','4','','/media/avatar2_UftA4Fm.png','','2025-06-15 12:18:23.294618','2025-06-15 12:18:23.294618',NULL,'','','','',''),(4,'pbkdf2_sha256$390000$GObcY01xzNwcbsPTuwQ2uX$7cEMSA+feY+d/r2l4SQJDlAFSlHNgQdT88Snp0t/e6U=','2025-06-25 03:48:40.332719',0,'BLESSY','THOMAS',0,1,'2025-06-15 12:22:23.495956','blessy@gmail.com','2','F','/media/avatar1.png','cTSV0pzncARpop4_GkyA2v:APA91bG6k0vkKSphdPgTkv3nISvuQwnHZa2D4bE9wl2iuk552E_uEKAXqNC7CCQIu4fL_yETz5Fza8p5o54Jw8oPT-JsArhjciyJSYeb0mj1A8Jbi8ZzUJo','2025-06-15 12:22:23.699062','2025-06-25 03:48:44.963823','1988-05-11','Kochi','India','ERNAKULAM','Kerala',''),(5,'pbkdf2_sha256$216000$oHkO9lrPq1gZ$KhwSSLiMY1STfUiDYcfqbrDuesGTJL9Qdbh6uBCYXiE=',NULL,0,'ALAN','MATHEW',0,1,'2025-06-15 12:29:25.945335','alan101@gmail.com','3','M','/media/avatar2_LRA1tQ1.png','','2025-06-15 12:29:26.145491','2025-06-15 12:29:26.157017','2014-09-18','Cherthala','India','Alappuzha','Kerala','Market Road'),(6,'pbkdf2_sha256$216000$WkIo9HXQGvSL$EAC9etDrg/cDBujHWoJmb6Qh4CrmZkNPuwUA8wmjkGE=',NULL,0,'PRIYA','SURESH',0,1,'2025-06-15 12:32:29.864910','priya102@gmail.com','3','F','/media/avatar1_ZRjadtB.png','','2025-06-15 12:32:30.063054','2025-06-15 12:32:30.072488','2013-08-16','Kochi','India','Ernakulam','Kerala','Church Road'),(7,'',NULL,0,'AKHILA1','PRADEEP',0,1,'2025-06-19 10:32:13.101459','','3','','','','2025-06-19 10:32:13.102458','2025-06-19 10:32:13.102458',NULL,'','','','',''),(22,'',NULL,0,'ABC','X',0,1,'2025-06-20 04:53:03.214834','abcx@gmail.com','3','','','','2025-06-20 04:53:03.214834','2025-06-20 04:53:03.214834',NULL,'','','','',''),(23,'',NULL,0,'XYZ','A',0,1,'2025-06-20 04:53:03.253359','xyza@gmail.com','3','','','','2025-06-20 04:53:03.254362','2025-06-20 04:53:03.254362',NULL,'','','','',''),(24,'',NULL,0,'ABC','X',0,1,'2025-06-20 10:36:44.521934','abc.x.d8d032@imentor.school','3','','','','2025-06-20 10:36:44.521934','2025-06-20 10:36:44.521934',NULL,'','','','',''),(25,'',NULL,0,'XYZ','A',0,1,'2025-06-20 10:36:44.592092','xyz.a.bb63b2@imentor.school','3','','','','2025-06-20 10:36:44.593056','2025-06-20 10:36:44.593056',NULL,'','','','',''),(26,'',NULL,0,'AKHIL ','K A',0,1,'2025-06-20 10:49:15.985895','akhil .k a.1@imentor.school','3','','','','2025-06-20 10:49:15.985895','2025-06-20 10:49:15.985895',NULL,'','','','',''),(27,'',NULL,0,'ARATHY','KRISHNA',0,1,'2025-06-20 10:49:16.043193','arathy.krishna.2@imentor.school','3','','','','2025-06-20 10:49:16.043193','2025-06-20 10:49:16.043193',NULL,'','','','',''),(28,'',NULL,0,'PRAKASH','JOSE',0,1,'2025-06-20 10:53:26.510838','prakashjose1@imentor.school','3','','','','2025-06-20 10:53:26.510838','2025-06-20 10:53:26.510838',NULL,'','','','',''),(29,'',NULL,0,'BINCY','JOHN',0,1,'2025-06-20 10:53:26.537916','bincyjohn2@imentor.school','3','','','','2025-06-20 10:53:26.538920','2025-06-20 10:53:26.538920',NULL,'','','','',''),(30,'',NULL,0,'ABHINAV ',' P S',0,1,'2025-06-20 10:59:25.550107','abhinav  p s1@imentor.school','3','','','','2025-06-20 10:59:25.551105','2025-06-20 10:59:25.551105',NULL,'','','','',''),(31,'',NULL,0,'AGRAJ ','A',0,1,'2025-06-20 10:59:25.588589','agraj a2@imentor.school','3','','','','2025-06-20 10:59:25.588589','2025-06-20 10:59:25.588589',NULL,'','','','',''),(32,'',NULL,0,'ANSON ','JOSE',0,1,'2025-06-20 10:59:25.608593','anson jose3@imentor.school','3','','','','2025-06-20 10:59:25.608593','2025-06-20 10:59:25.608593',NULL,'','','','',''),(33,'',NULL,0,'ARJUN  ','BINOY',0,1,'2025-06-20 10:59:25.632307','arjun  binoy4@imentor.school','3','','','','2025-06-20 10:59:25.632307','2025-06-20 10:59:25.632307',NULL,'','','','',''),(34,'',NULL,0,'DIVINE ','A J',0,1,'2025-06-20 10:59:25.659799','divine a j5@imentor.school','3','','','','2025-06-20 10:59:25.659799','2025-06-20 10:59:25.659799',NULL,'','','','',''),(35,'',NULL,0,'EDWIN ','BENADICT',0,1,'2025-06-20 10:59:25.679257','edwin benadict6@imentor.school','3','','','','2025-06-20 10:59:25.680256','2025-06-20 10:59:25.680256',NULL,'','','','',''),(36,'',NULL,0,'GANESHKUMAR ','S',0,1,'2025-06-20 10:59:25.701973','ganeshkumar s7@imentor.school','3','','','','2025-06-20 10:59:25.701973','2025-06-20 10:59:25.701973',NULL,'','','','',''),(37,'',NULL,0,'JOHN ','PIO VARGHESE',0,1,'2025-06-20 10:59:25.722318','john pio varghese8@imentor.school','3','','','','2025-06-20 10:59:25.722318','2025-06-20 10:59:25.722318',NULL,'','','','',''),(38,'',NULL,0,'PAVANENDH',' S',0,1,'2025-06-20 10:59:25.739317','pavanendh s9@imentor.school','3','','','','2025-06-20 10:59:25.739317','2025-06-20 10:59:25.739317',NULL,'','','','',''),(39,'',NULL,0,'SANJAY ','KRISHNA',0,1,'2025-06-20 10:59:25.760316','sanjay krishna10@imentor.school','3','','','','2025-06-20 10:59:25.760316','2025-06-20 10:59:25.760316',NULL,'','','','',''),(40,'',NULL,0,'SNEHADATHAN ','S',0,1,'2025-06-20 10:59:25.777996','snehadathan s11@imentor.school','3','','','','2025-06-20 10:59:25.777996','2025-06-20 10:59:25.777996',NULL,'','','','',''),(41,'',NULL,0,'THANSEEM ','NIYAS',0,1,'2025-06-20 10:59:25.793789','thanseem niyas12@imentor.school','3','','','','2025-06-20 10:59:25.793789','2025-06-20 10:59:25.793789',NULL,'','','','',''),(42,'',NULL,0,'ABHIRAMI ','SUDEESH',0,1,'2025-06-20 10:59:25.811357','abhirami sudeesh13@imentor.school','3','','','','2025-06-20 10:59:25.811357','2025-06-20 10:59:25.811357',NULL,'','','','',''),(43,'',NULL,0,'ALEEVIA ','ASHOK K',0,1,'2025-06-20 10:59:25.829319','aleevia ashok k14@imentor.school','3','','','','2025-06-20 10:59:25.829319','2025-06-20 10:59:25.829319',NULL,'','','','',''),(44,'',NULL,0,'DARSANA ','U NAIR',0,1,'2025-06-20 10:59:25.847449','darsana u nair15@imentor.school','3','','','','2025-06-20 10:59:25.848452','2025-06-20 10:59:25.848452',NULL,'','','','',''),(45,'',NULL,0,'DINCIYA ','PETER',0,1,'2025-06-20 10:59:25.869841','dinciya peter16@imentor.school','3','','','','2025-06-20 10:59:25.869841','2025-06-20 10:59:25.869841',NULL,'','','','',''),(46,'',NULL,0,'MALAVIKA ','MANOJ',0,1,'2025-06-20 10:59:25.890837','malavika manoj17@imentor.school','3','','','','2025-06-20 10:59:25.890837','2025-06-20 10:59:25.890837',NULL,'','','','',''),(47,'',NULL,0,'SERA ','C THOMAS',0,1,'2025-06-20 10:59:25.907785','sera c thomas18@imentor.school','3','','','','2025-06-20 10:59:25.908791','2025-06-20 10:59:25.908791',NULL,'','','','',''),(48,'',NULL,0,'SREENANDA ','V S',0,1,'2025-06-20 10:59:25.927138','sreenanda v s19@imentor.school','3','','','','2025-06-20 10:59:25.927138','2025-06-20 10:59:25.927138',NULL,'','','','',''),(49,'',NULL,0,'VYSHNAVI ','RAJ',0,1,'2025-06-20 10:59:25.946667','vyshnavi raj20@imentor.school','3','','','','2025-06-20 10:59:25.946667','2025-06-20 10:59:25.946667',NULL,'','','','',''),(50,'',NULL,0,'ABHINAV ',' P S',0,1,'2025-06-20 11:03:39.532220','abhinav _1@imentor.school','3','','','','2025-06-20 11:03:39.532220','2025-06-20 11:03:39.532220',NULL,'','','','',''),(51,'',NULL,0,'AGRAJ ','A',0,1,'2025-06-20 11:03:39.570480','agraj _2@imentor.school','3','','','','2025-06-20 11:03:39.571483','2025-06-20 11:03:39.571483',NULL,'','','','',''),(52,'',NULL,0,'ANSON ','JOSE',0,1,'2025-06-20 11:03:39.598596','anson _3@imentor.school','3','','','','2025-06-20 11:03:39.598596','2025-06-20 11:03:39.598596',NULL,'','','','',''),(53,'',NULL,0,'ARJUN  ','BINOY',0,1,'2025-06-20 11:03:39.630720','arjun  _4@imentor.school','3','','','','2025-06-20 11:03:39.630720','2025-06-20 11:03:39.630720',NULL,'','','','',''),(54,'',NULL,0,'DIVINE ','A J',0,1,'2025-06-20 11:03:39.657544','divine _5@imentor.school','3','','','','2025-06-20 11:03:39.658547','2025-06-20 11:03:39.658547',NULL,'','','','',''),(55,'',NULL,0,'EDWIN ','BENADICT',0,1,'2025-06-20 11:03:39.687074','edwin _6@imentor.school','3','','','','2025-06-20 11:03:39.687074','2025-06-20 11:03:39.687074',NULL,'','','','',''),(56,'',NULL,0,'GANESHKUMAR ','S',0,1,'2025-06-20 11:03:39.710079','ganeshkumar _7@imentor.school','3','','','','2025-06-20 11:03:39.710079','2025-06-20 11:03:39.710079',NULL,'','','','',''),(57,'',NULL,0,'JOHN ','PIO VARGHESE',0,1,'2025-06-20 11:03:39.730075','john _8@imentor.school','3','','','','2025-06-20 11:03:39.730075','2025-06-20 11:03:39.730075',NULL,'','','','',''),(58,'',NULL,0,'PAVANENDH',' S',0,1,'2025-06-20 11:03:39.754076','pavanendh_9@imentor.school','3','','','','2025-06-20 11:03:39.754076','2025-06-20 11:03:39.754076',NULL,'','','','',''),(59,'',NULL,0,'SANJAY ','KRISHNA',0,1,'2025-06-20 11:03:39.774089','sanjay _10@imentor.school','3','','','','2025-06-20 11:03:39.774599','2025-06-20 11:03:39.774599',NULL,'','','','',''),(60,'',NULL,0,'SNEHADATHAN ','S',0,1,'2025-06-20 11:03:39.795613','snehadathan _11@imentor.school','3','','','','2025-06-20 11:03:39.795613','2025-06-20 11:03:39.795613',NULL,'','','','',''),(61,'',NULL,0,'THANSEEM ','NIYAS',0,1,'2025-06-20 11:03:39.817614','thanseem _12@imentor.school','3','','','','2025-06-20 11:03:39.817614','2025-06-20 11:03:39.817614',NULL,'','','','',''),(62,'',NULL,0,'ABHIRAMI ','SUDEESH',0,1,'2025-06-20 11:03:39.836612','abhirami _13@imentor.school','3','','','','2025-06-20 11:03:39.836612','2025-06-20 11:03:39.836612',NULL,'','','','',''),(63,'',NULL,0,'ALEEVIA ','ASHOK K',0,1,'2025-06-20 11:03:39.855612','aleevia _14@imentor.school','3','','','','2025-06-20 11:03:39.855612','2025-06-20 11:03:39.855612',NULL,'','','','',''),(64,'',NULL,0,'DARSANA ','U NAIR',0,1,'2025-06-20 11:03:39.878158','darsana _15@imentor.school','3','','','','2025-06-20 11:03:39.878158','2025-06-20 11:03:39.878158',NULL,'','','','',''),(65,'',NULL,0,'DINCIYA ','PETER',0,1,'2025-06-20 11:03:39.896143','dinciya _16@imentor.school','3','','','','2025-06-20 11:03:39.896143','2025-06-20 11:03:39.896143',NULL,'','','','',''),(66,'',NULL,0,'MALAVIKA ','MANOJ',0,1,'2025-06-20 11:03:39.917145','malavika _17@imentor.school','3','','','','2025-06-20 11:03:39.918144','2025-06-20 11:03:39.918144',NULL,'','','','',''),(67,'',NULL,0,'SERA ','C THOMAS',0,1,'2025-06-20 11:03:39.935143','sera _18@imentor.school','3','','','','2025-06-20 11:03:39.936144','2025-06-20 11:03:39.936144',NULL,'','','','',''),(68,'',NULL,0,'SREENANDA ','V S',0,1,'2025-06-20 11:03:39.954146','sreenanda _19@imentor.school','3','','','','2025-06-20 11:03:39.955144','2025-06-20 11:03:39.955144',NULL,'','','','',''),(69,'',NULL,0,'VYSHNAVI ','RAJ',0,1,'2025-06-20 11:03:39.978994','vyshnavi _20@imentor.school','3','','','','2025-06-20 11:03:39.979997','2025-06-20 11:03:39.979997',NULL,'','','','',''),(70,'',NULL,0,'ABEL','FERNANDEZ',0,1,'2025-06-20 11:49:30.231976','abel1@imentor.school','3','','','','2025-06-20 11:49:30.231976','2025-06-20 11:49:30.231976',NULL,'','','','',''),(71,'',NULL,0,'ABHINAV','VA',0,1,'2025-06-20 11:49:30.297626','abhinav2@imentor.school','3','','','','2025-06-20 11:49:30.297626','2025-06-20 11:49:30.297626',NULL,'','','','',''),(72,'',NULL,0,'ABIHAIL','PJ',0,1,'2025-06-20 11:49:30.324972','abihail3@imentor.school','3','','','','2025-06-20 11:49:30.325986','2025-06-20 11:49:30.325986',NULL,'','','','',''),(73,'',NULL,0,'ARNAV','MS',0,1,'2025-06-20 11:49:30.352110','arnav4@imentor.school','3','','','','2025-06-20 11:49:30.352110','2025-06-20 11:49:30.352110',NULL,'','','','',''),(74,'',NULL,0,'GAGANKRISHNA','S',0,1,'2025-06-20 11:49:30.382033','gagankrishna5@imentor.school','3','','','','2025-06-20 11:49:30.382033','2025-06-20 11:49:30.382033',NULL,'','','','',''),(75,'',NULL,0,'HARSHAL','CHANDRAS',0,1,'2025-06-20 11:49:30.411866','harshal6@imentor.school','3','','','','2025-06-20 11:49:30.412903','2025-06-20 11:49:30.412903',NULL,'','','','',''),(76,'',NULL,0,'JOEL','JOSE',0,1,'2025-06-20 11:49:30.438317','joel7@imentor.school','3','','','','2025-06-20 11:49:30.438317','2025-06-20 11:49:30.438317',NULL,'','','','',''),(77,'',NULL,0,'MADHAV','R',0,1,'2025-06-20 11:49:30.488491','madhav8@imentor.school','3','','','','2025-06-20 11:49:30.488491','2025-06-20 11:49:30.488491',NULL,'','','','',''),(78,'',NULL,0,'RIYAN','VB',0,1,'2025-06-20 11:49:30.563095','riyan9@imentor.school','3','','','','2025-06-20 11:49:30.563095','2025-06-20 11:49:30.563095',NULL,'','','','',''),(79,'',NULL,0,'ABEL','FERNANDEZ',0,1,'2025-06-20 12:05:01.863578','abelfernandez1@littleflower.school','3','','','','2025-06-20 12:05:01.863578','2025-06-20 12:05:01.863578',NULL,'','','','',''),(80,'',NULL,0,'ABHINAV','VA',0,1,'2025-06-20 12:05:01.922028','abhinavva2@littleflower.school','3','','','','2025-06-20 12:05:01.923025','2025-06-20 12:05:01.923025',NULL,'','','','',''),(81,'',NULL,0,'ABIHAIL','PJ',0,1,'2025-06-20 12:05:01.948176','abihailpj3@littleflower.school','3','','','','2025-06-20 12:05:01.949271','2025-06-20 12:05:01.949271',NULL,'','','','',''),(82,'',NULL,0,'SIVADEV','S',0,1,'2025-06-20 12:07:41.439831','sivadevs1@littleflower.school','3','','','','2025-06-20 12:07:41.440827','2025-06-20 12:07:41.440827',NULL,'','','','',''),(83,'pbkdf2_sha256$390000$hgQwB54d2dJ6PzMlG7pwYt$VeKys6OwMnWWvddVsIUOXE6GXtBLHqMDjvM99QiAbjI=',NULL,0,'THEJUS','KRISH',0,1,'2025-06-20 12:07:41.532250','thejus1020@gmail.com','3','M','/media/avatar2_vlqOzcQ.png','','2025-06-20 12:07:41.533260','2025-06-21 06:41:27.335868',NULL,'Vaikom','India','kottayam','Kerala','C K Road'),(84,'',NULL,0,'VIHAAN','RAJ',0,1,'2025-06-20 12:07:41.607586','vihaanraj3@littleflower.school','3','','','','2025-06-20 12:07:41.607586','2025-06-20 12:07:41.607586',NULL,'','','','',''),(85,'pbkdf2_sha256$390000$IyATDZ3hDJcMJRjMhaVP7h$gJUAY6rWfj+/9u32Lla9mxG3ilE9nrQNUW0I1l8IB+c=','2025-06-25 04:27:17.195793',0,'BEENA','MATHEW',0,1,'2025-06-25 04:25:12.891347','beena@gmail.com','2','F','/media/avatar1_vJ0Fs97.png','cTSV0pzncARpop4_GkyA2v:APA91bG6k0vkKSphdPgTkv3nISvuQwnHZa2D4bE9wl2iuk552E_uEKAXqNC7CCQIu4fL_yETz5Fza8p5o54Jw8oPT-JsArhjciyJSYeb0mj1A8Jbi8ZzUJo','2025-06-25 04:25:13.952872','2025-06-25 04:27:17.620030','1985-03-11','Cherthala','India','Alleppey','Kerala','');
/*!40000 ALTER TABLE `main_app_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_customuser_groups`
--

DROP TABLE IF EXISTS `main_app_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_customuser_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_app_customuser_groups_customuser_id_group_id_6dd2b9a7_uniq` (`customuser_id`,`group_id`),
  KEY `main_app_customuser_groups_group_id_9ee498f4_fk_auth_group_id` (`group_id`),
  CONSTRAINT `main_app_customuser__customuser_id_9d75aa94_fk_main_app_` FOREIGN KEY (`customuser_id`) REFERENCES `main_app_customuser` (`id`),
  CONSTRAINT `main_app_customuser_groups_group_id_9ee498f4_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_customuser_groups`
--

LOCK TABLES `main_app_customuser_groups` WRITE;
/*!40000 ALTER TABLE `main_app_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_customuser_user_permissions`
--

DROP TABLE IF EXISTS `main_app_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_customuser_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `main_app_customuser_user_customuser_id_permission_0bd2d638_uniq` (`customuser_id`,`permission_id`),
  KEY `main_app_customuser__permission_id_595e7ce3_fk_auth_perm` (`permission_id`),
  CONSTRAINT `main_app_customuser__customuser_id_b28fdeb1_fk_main_app_` FOREIGN KEY (`customuser_id`) REFERENCES `main_app_customuser` (`id`),
  CONSTRAINT `main_app_customuser__permission_id_595e7ce3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_customuser_user_permissions`
--

LOCK TABLES `main_app_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `main_app_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_department`
--

DROP TABLE IF EXISTS `main_app_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_department` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_department`
--

LOCK TABLES `main_app_department` WRITE;
/*!40000 ALTER TABLE `main_app_department` DISABLE KEYS */;
INSERT INTO `main_app_department` VALUES (1,'HIGH SCHOOL');
/*!40000 ALTER TABLE `main_app_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_examtypesettings`
--

DROP TABLE IF EXISTS `main_app_examtypesettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_examtypesettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_type` varchar(50) NOT NULL,
  `exam_name` varchar(50) NOT NULL,
  `term` varchar(50) NOT NULL,
  `max_marks` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_examtypesettings`
--

LOCK TABLES `main_app_examtypesettings` WRITE;
/*!40000 ALTER TABLE `main_app_examtypesettings` DISABLE KEYS */;
INSERT INTO `main_app_examtypesettings` VALUES (1,'Terminal Exam','TERMINAL EXAM 1','Term-2',100,'2025-06-24 11:53:23.515047','2025-06-24 11:53:51.582249');
/*!40000 ALTER TABLE `main_app_examtypesettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_feeamountsettings`
--

DROP TABLE IF EXISTS `main_app_feeamountsettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_feeamountsettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fee_name` varchar(50) NOT NULL,
  `fee_type` varchar(50) NOT NULL,
  `amount` double NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_feeamountse_course_id_dd014400_fk_main_app_` (`course_id`),
  KEY `main_app_feeamountse_session_id_73d1486a_fk_main_app_` (`session_id`),
  CONSTRAINT `main_app_feeamountse_course_id_dd014400_fk_main_app_` FOREIGN KEY (`course_id`) REFERENCES `main_app_course` (`id`),
  CONSTRAINT `main_app_feeamountse_session_id_73d1486a_fk_main_app_` FOREIGN KEY (`session_id`) REFERENCES `main_app_session` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_feeamountsettings`
--

LOCK TABLES `main_app_feeamountsettings` WRITE;
/*!40000 ALTER TABLE `main_app_feeamountsettings` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_feeamountsettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_feedbackstaff`
--

DROP TABLE IF EXISTS `main_app_feedbackstaff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_feedbackstaff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` longtext NOT NULL,
  `reply` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `staff_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_feedbackstaff_staff_id_b20848bb_fk_main_app_staff_id` (`staff_id`),
  CONSTRAINT `main_app_feedbackstaff_staff_id_b20848bb_fk_main_app_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `main_app_staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_feedbackstaff`
--

LOCK TABLES `main_app_feedbackstaff` WRITE;
/*!40000 ALTER TABLE `main_app_feedbackstaff` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_feedbackstaff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_feedbackstudent`
--

DROP TABLE IF EXISTS `main_app_feedbackstudent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_feedbackstudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` longtext NOT NULL,
  `reply` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_feedbackstu_student_id_7509652e_fk_main_app_` (`student_id`),
  CONSTRAINT `main_app_feedbackstu_student_id_7509652e_fk_main_app_` FOREIGN KEY (`student_id`) REFERENCES `main_app_student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_feedbackstudent`
--

LOCK TABLES `main_app_feedbackstudent` WRITE;
/*!40000 ALTER TABLE `main_app_feedbackstudent` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_feedbackstudent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_feesettings`
--

DROP TABLE IF EXISTS `main_app_feesettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_feesettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fee_name` varchar(50) NOT NULL,
  `fee_type` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_feesettings`
--

LOCK TABLES `main_app_feesettings` WRITE;
/*!40000 ALTER TABLE `main_app_feesettings` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_feesettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_file`
--

DROP TABLE IF EXISTS `main_app_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_file` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_file`
--

LOCK TABLES `main_app_file` WRITE;
/*!40000 ALTER TABLE `main_app_file` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_file` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_leavereportstaff`
--

DROP TABLE IF EXISTS `main_app_leavereportstaff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_leavereportstaff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(60) NOT NULL,
  `message` longtext NOT NULL,
  `status` smallint(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `staff_id` int(11) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_leavereportstaff_staff_id_9c69ba31_fk_main_app_staff_id` (`staff_id`),
  CONSTRAINT `main_app_leavereportstaff_staff_id_9c69ba31_fk_main_app_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `main_app_staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_leavereportstaff`
--

LOCK TABLES `main_app_leavereportstaff` WRITE;
/*!40000 ALTER TABLE `main_app_leavereportstaff` DISABLE KEYS */;
INSERT INTO `main_app_leavereportstaff` VALUES (1,'2025-06-26','Kindly grant leave on 26/06/2025 since I have to attend a PSC exam.',0,'2025-06-25 03:57:29.334191','2025-06-25 03:57:29.334191',1,'leave_images/emblom.jpg');
/*!40000 ALTER TABLE `main_app_leavereportstaff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_leavereportstudent`
--

DROP TABLE IF EXISTS `main_app_leavereportstudent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_leavereportstudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(60) NOT NULL,
  `message` longtext NOT NULL,
  `status` smallint(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id` int(11) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_leavereport_student_id_2d19cc01_fk_main_app_` (`student_id`),
  CONSTRAINT `main_app_leavereport_student_id_2d19cc01_fk_main_app_` FOREIGN KEY (`student_id`) REFERENCES `main_app_student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_leavereportstudent`
--

LOCK TABLES `main_app_leavereportstudent` WRITE;
/*!40000 ALTER TABLE `main_app_leavereportstudent` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_leavereportstudent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_lessonsettings`
--

DROP TABLE IF EXISTS `main_app_lessonsettings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_lessonsettings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `notes` longtext NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `curriculam_id` int(11) DEFAULT NULL,
  `subject_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_lessonsetti_subject_id_8cd3671f_fk_main_app_` (`subject_id`),
  KEY `main_app_lessonsetti_curriculam_id_e2a6ebce_fk_main_app_` (`curriculam_id`),
  CONSTRAINT `main_app_lessonsetti_curriculam_id_e2a6ebce_fk_main_app_` FOREIGN KEY (`curriculam_id`) REFERENCES `main_app_curriculam` (`id`),
  CONSTRAINT `main_app_lessonsetti_subject_id_8cd3671f_fk_main_app_` FOREIGN KEY (`subject_id`) REFERENCES `main_app_subject` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_lessonsettings`
--

LOCK TABLES `main_app_lessonsettings` WRITE;
/*!40000 ALTER TABLE `main_app_lessonsettings` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_lessonsettings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_notificationstaff`
--

DROP TABLE IF EXISTS `main_app_notificationstaff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_notificationstaff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `staff_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_notificatio_staff_id_4170f50c_fk_main_app_` (`staff_id`),
  CONSTRAINT `main_app_notificatio_staff_id_4170f50c_fk_main_app_` FOREIGN KEY (`staff_id`) REFERENCES `main_app_staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_notificationstaff`
--

LOCK TABLES `main_app_notificationstaff` WRITE;
/*!40000 ALTER TABLE `main_app_notificationstaff` DISABLE KEYS */;
INSERT INTO `main_app_notificationstaff` VALUES (1,'Coming Saturday (28/06/2025) will be a working day.','2025-06-25 03:48:22.539944','2025-06-25 03:48:22.539944',1);
/*!40000 ALTER TABLE `main_app_notificationstaff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_notificationstudent`
--

DROP TABLE IF EXISTS `main_app_notificationstudent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_notificationstudent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_notificatio_student_id_dcbe1f25_fk_main_app_` (`student_id`),
  CONSTRAINT `main_app_notificatio_student_id_dcbe1f25_fk_main_app_` FOREIGN KEY (`student_id`) REFERENCES `main_app_student` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_notificationstudent`
--

LOCK TABLES `main_app_notificationstudent` WRITE;
/*!40000 ALTER TABLE `main_app_notificationstudent` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_notificationstudent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_school`
--

DROP TABLE IF EXISTS `main_app_school`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_school` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `address` varchar(200) NOT NULL,
  `city` varchar(100) NOT NULL,
  `state` varchar(100) NOT NULL,
  `country` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_school`
--

LOCK TABLES `main_app_school` WRITE;
/*!40000 ALTER TABLE `main_app_school` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_school` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_session`
--

DROP TABLE IF EXISTS `main_app_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_session` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_year` date NOT NULL,
  `end_year` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_session`
--

LOCK TABLES `main_app_session` WRITE;
/*!40000 ALTER TABLE `main_app_session` DISABLE KEYS */;
INSERT INTO `main_app_session` VALUES (1,'2025-06-02','2026-03-31');
/*!40000 ALTER TABLE `main_app_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_staff`
--

DROP TABLE IF EXISTS `main_app_staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_staff` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `contact_number` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `admin_id` (`admin_id`),
  KEY `main_app_staff_course_id_b4d19096_fk_main_app_course_id` (`course_id`),
  KEY `main_app_staff_department_id_4138bc5d_fk_main_app_department_id` (`department_id`),
  CONSTRAINT `main_app_staff_admin_id_831efa54_fk_main_app_customuser_id` FOREIGN KEY (`admin_id`) REFERENCES `main_app_customuser` (`id`),
  CONSTRAINT `main_app_staff_course_id_b4d19096_fk_main_app_course_id` FOREIGN KEY (`course_id`) REFERENCES `main_app_course` (`id`),
  CONSTRAINT `main_app_staff_department_id_4138bc5d_fk_main_app_department_id` FOREIGN KEY (`department_id`) REFERENCES `main_app_department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_staff`
--

LOCK TABLES `main_app_staff` WRITE;
/*!40000 ALTER TABLE `main_app_staff` DISABLE KEYS */;
INSERT INTO `main_app_staff` VALUES (1,4,1,1,''),(2,85,2,1,'');
/*!40000 ALTER TABLE `main_app_staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_staffattendance`
--

DROP TABLE IF EXISTS `main_app_staffattendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_staffattendance` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fn` tinyint(1) NOT NULL,
  `an` tinyint(1) NOT NULL,
  `date` date NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `staff_id` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_staffattendance_staff_id_e1e9faf4_fk_main_app_staff_id` (`staff_id`),
  CONSTRAINT `main_app_staffattendance_staff_id_e1e9faf4_fk_main_app_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `main_app_staff` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_staffattendance`
--

LOCK TABLES `main_app_staffattendance` WRITE;
/*!40000 ALTER TABLE `main_app_staffattendance` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_staffattendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_student`
--

DROP TABLE IF EXISTS `main_app_student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_student` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) NOT NULL,
  `course_id` int(11) DEFAULT NULL,
  `session_id` int(11) DEFAULT NULL,
  `admission_number` longtext NOT NULL,
  `parent_name` longtext NOT NULL,
  `mother_tongue` longtext NOT NULL,
  `file_type` longtext NOT NULL,
  `blood_group` longtext NOT NULL,
  `guardian_contact_number` varchar(10) NOT NULL,
  `mother_name` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `admin_id` (`admin_id`),
  KEY `main_app_student_course_id_8a4c712f_fk_main_app_course_id` (`course_id`),
  KEY `main_app_student_session_id_8f220969_fk_main_app_session_id` (`session_id`),
  CONSTRAINT `main_app_student_admin_id_c8e987bb_fk_main_app_customuser_id` FOREIGN KEY (`admin_id`) REFERENCES `main_app_customuser` (`id`),
  CONSTRAINT `main_app_student_course_id_8a4c712f_fk_main_app_course_id` FOREIGN KEY (`course_id`) REFERENCES `main_app_course` (`id`),
  CONSTRAINT `main_app_student_session_id_8f220969_fk_main_app_session_id` FOREIGN KEY (`session_id`) REFERENCES `main_app_session` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_student`
--

LOCK TABLES `main_app_student` WRITE;
/*!40000 ALTER TABLE `main_app_student` DISABLE KEYS */;
INSERT INTO `main_app_student` VALUES (1,5,1,1,'101','Mathew John','Malayalam','','B+','9786452312','Mary Mathew'),(2,6,2,1,'102','Suresh S','Malayalam','','A+','9786452300','Aditi S'),(3,7,3,NULL,'','','','1','','',''),(4,22,3,NULL,'','','','1','','',''),(5,23,3,NULL,'','','','1','','',''),(6,24,3,NULL,'','','','1','','',''),(7,25,3,NULL,'','','','1','','',''),(8,26,3,NULL,'','','','1','','',''),(9,27,3,NULL,'','','','1','','',''),(10,28,3,NULL,'','','','1','','',''),(11,29,3,NULL,'','','','1','','',''),(12,30,3,NULL,'','','','1','','',''),(13,31,3,NULL,'','','','1','','',''),(14,32,3,NULL,'','','','1','','',''),(15,33,3,NULL,'','','','1','','',''),(16,34,3,NULL,'','','','1','','',''),(17,35,3,NULL,'','','','1','','',''),(18,36,3,NULL,'','','','1','','',''),(19,37,3,NULL,'','','','1','','',''),(20,38,3,NULL,'','','','1','','',''),(21,39,3,NULL,'','','','1','','',''),(22,40,3,NULL,'','','','1','','',''),(23,41,3,NULL,'','','','1','','',''),(24,42,3,NULL,'','','','1','','',''),(25,43,3,NULL,'','','','1','','',''),(26,44,3,NULL,'','','','1','','',''),(27,45,3,NULL,'','','','1','','',''),(28,46,3,NULL,'','','','1','','',''),(29,47,3,NULL,'','','','1','','',''),(30,48,3,NULL,'','','','1','','',''),(31,49,3,NULL,'','','','1','','',''),(32,50,3,NULL,'','','','1','','',''),(33,51,3,NULL,'','','','1','','',''),(34,52,3,NULL,'','','','1','','',''),(35,53,3,NULL,'','','','1','','',''),(36,54,3,NULL,'','','','1','','',''),(37,55,3,NULL,'','','','1','','',''),(38,56,3,NULL,'','','','1','','',''),(39,57,3,NULL,'','','','1','','',''),(40,58,3,NULL,'','','','1','','',''),(41,59,3,NULL,'','','','1','','',''),(42,60,3,NULL,'','','','1','','',''),(43,61,3,NULL,'','','','1','','',''),(44,62,3,NULL,'','','','1','','',''),(45,63,3,NULL,'','','','1','','',''),(46,64,3,NULL,'','','','1','','',''),(47,65,3,NULL,'','','','1','','',''),(48,66,3,NULL,'','','','1','','',''),(49,67,3,NULL,'','','','1','','',''),(50,68,3,NULL,'','','','1','','',''),(51,69,3,NULL,'','','','1','','',''),(52,70,NULL,NULL,'','','','','','',''),(53,71,NULL,NULL,'','','','','','',''),(54,72,NULL,NULL,'','','','','','',''),(55,73,NULL,NULL,'','','','','','',''),(56,74,NULL,NULL,'','','','','','',''),(57,75,NULL,NULL,'','','','','','',''),(58,76,NULL,NULL,'','','','','','',''),(59,77,NULL,NULL,'','','','','','',''),(60,78,NULL,NULL,'','','','','','',''),(61,79,5,NULL,'','','','1','','',''),(62,80,5,NULL,'','','','1','','',''),(63,81,5,NULL,'','','','1','','',''),(64,82,5,NULL,'','','','1','','',''),(65,83,5,1,'1020','Krishnan','Malayalam','1','B+','9786452319','Priya Menon'),(66,84,5,NULL,'','','','1','','','');
/*!40000 ALTER TABLE `main_app_student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_studentresult`
--

DROP TABLE IF EXISTS `main_app_studentresult`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_studentresult` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `test` double NOT NULL,
  `exam` double NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `student_id` int(11) NOT NULL,
  `subject_id` int(11) NOT NULL,
  `remarks` longtext NOT NULL,
  `term` varchar(50) NOT NULL,
  `subjectmaster_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_studentresu_student_id_e57bb0c5_fk_main_app_` (`student_id`),
  KEY `main_app_studentresu_subjectmaster_id_d161f273_fk_main_app_` (`subjectmaster_id`),
  KEY `main_app_studentresu_subject_id_6abff4dc_fk_main_app_` (`subject_id`),
  CONSTRAINT `main_app_studentresu_student_id_e57bb0c5_fk_main_app_` FOREIGN KEY (`student_id`) REFERENCES `main_app_student` (`id`),
  CONSTRAINT `main_app_studentresu_subject_id_6abff4dc_fk_main_app_` FOREIGN KEY (`subject_id`) REFERENCES `main_app_subject` (`id`),
  CONSTRAINT `main_app_studentresu_subjectmaster_id_d161f273_fk_main_app_` FOREIGN KEY (`subjectmaster_id`) REFERENCES `main_app_subjectmaster` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_studentresult`
--

LOCK TABLES `main_app_studentresult` WRITE;
/*!40000 ALTER TABLE `main_app_studentresult` DISABLE KEYS */;
INSERT INTO `main_app_studentresult` VALUES (1,42,50,'2025-06-15 12:33:58.949331','2025-06-25 00:43:29.790724',1,1,'Good','Term-1',1),(2,38,45,'2025-06-15 12:34:34.738908','2025-06-15 12:34:34.738908',2,2,'Good','Term-1',1);
/*!40000 ALTER TABLE `main_app_studentresult` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_subject`
--

DROP TABLE IF EXISTS `main_app_subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_subject` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `course_id` int(11) NOT NULL,
  `staff_id` int(11) NOT NULL,
  `subject_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_subject_course_id_e94ba4e3_fk_main_app_course_id` (`course_id`),
  KEY `main_app_subject_staff_id_f1d6d399_fk_main_app_staff_id` (`staff_id`),
  KEY `main_app_subject_subject_id_55bad52b_fk_main_app_` (`subject_id`),
  CONSTRAINT `main_app_subject_course_id_e94ba4e3_fk_main_app_course_id` FOREIGN KEY (`course_id`) REFERENCES `main_app_course` (`id`),
  CONSTRAINT `main_app_subject_staff_id_f1d6d399_fk_main_app_staff_id` FOREIGN KEY (`staff_id`) REFERENCES `main_app_staff` (`id`),
  CONSTRAINT `main_app_subject_subject_id_55bad52b_fk_main_app_` FOREIGN KEY (`subject_id`) REFERENCES `main_app_subjectmaster` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_subject`
--

LOCK TABLES `main_app_subject` WRITE;
/*!40000 ALTER TABLE `main_app_subject` DISABLE KEYS */;
INSERT INTO `main_app_subject` VALUES (1,'2025-06-15 12:22:58.350372','2025-06-15 12:22:58.350372',1,1,1),(2,'2025-06-15 12:23:19.175618','2025-06-15 12:23:19.175618',2,1,1),(3,'2025-06-25 04:26:57.056393','2025-06-25 04:26:57.056393',2,2,1);
/*!40000 ALTER TABLE `main_app_subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_subjectmaster`
--

DROP TABLE IF EXISTS `main_app_subjectmaster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_subjectmaster` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `main_app_subjectmast_department_id_cb9e7056_fk_main_app_` (`department_id`),
  CONSTRAINT `main_app_subjectmast_department_id_cb9e7056_fk_main_app_` FOREIGN KEY (`department_id`) REFERENCES `main_app_department` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_subjectmaster`
--

LOCK TABLES `main_app_subjectmaster` WRITE;
/*!40000 ALTER TABLE `main_app_subjectmaster` DISABLE KEYS */;
INSERT INTO `main_app_subjectmaster` VALUES (1,'MATHS','2025-06-15 12:19:51.904717','2025-06-15 12:19:51.904717',1);
/*!40000 ALTER TABLE `main_app_subjectmaster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_app_userloginrecord`
--

DROP TABLE IF EXISTS `main_app_userloginrecord`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `main_app_userloginrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_time` datetime(6) NOT NULL,
  `CustomUser_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_app_userloginrecord`
--

LOCK TABLES `main_app_userloginrecord` WRITE;
/*!40000 ALTER TABLE `main_app_userloginrecord` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_app_userloginrecord` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-25 11:23:57
