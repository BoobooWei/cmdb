-- MySQL dump 10.13  Distrib 5.7.11, for osx10.9 (x86_64)
--
-- Host: localhost    Database: cmdb
-- ------------------------------------------------------
-- Server version	5.7.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
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
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('32d8e7250ca6');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assets`
--

DROP TABLE IF EXISTS `assets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classType_id` int(11) DEFAULT NULL,
  `an` varchar(64) DEFAULT NULL,
  `sn` varchar(64) DEFAULT NULL,
  `onstatus` int(11) DEFAULT NULL,
  `dateofmanufacture` datetime DEFAULT NULL,
  `manufacturer` varchar(64) DEFAULT NULL,
  `brand` varchar(64) DEFAULT NULL,
  `model` varchar(64) DEFAULT NULL,
  `usedept` varchar(64) DEFAULT NULL,
  `usestaff` varchar(64) DEFAULT NULL,
  `mainuses` varchar(128) DEFAULT NULL,
  `managedept` varchar(64) DEFAULT NULL,
  `managestaff` varchar(64) DEFAULT NULL,
  `koriyasustarttime` datetime DEFAULT NULL,
  `koriyasuendtime` datetime DEFAULT NULL,
  `equipprice` int(11) DEFAULT NULL,
  `auto_discover` tinyint(1) DEFAULT NULL,
  `isdelete` tinyint(1) DEFAULT NULL,
  `remarks` text,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_assets_an` (`an`),
  UNIQUE KEY `ix_assets_sn` (`sn`),
  KEY `classType_id` (`classType_id`),
  CONSTRAINT `assets_ibfk_1` FOREIGN KEY (`classType_id`) REFERENCES `classType` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assets`
--

LOCK TABLES `assets` WRITE;
/*!40000 ALTER TABLE `assets` DISABLE KEYS */;
INSERT INTO `assets` VALUES (1,1,'SERVER001','SERVER001',1,'2016-01-01 00:00:00','DELL','PowerEdge','R720','运维部','柯发通','官网','运维部','柯发通','2016-01-01 00:00:00','2016-01-01 00:00:00',36000,NULL,0,'',NULL,'2016-07-30 19:03:00'),(2,4,'VIRT001','VIRT001',1,'2016-01-01 00:00:00','DELL','PowerEdge','R720','运维部','柯发通','虚拟化','运维部','柯发通','2016-01-01 00:00:00','2016-01-01 00:00:00',38000,NULL,0,'',NULL,'2016-07-31 10:20:38'),(3,2,'SW001','SW001',1,'2016-01-01 00:00:00','CISCO','SWITCH','2960s','运维部','柯发通','接入','运维部','柯发通','2016-01-01 00:00:00','2016-01-01 00:00:00',5000,NULL,0,'',NULL,'2016-07-31 10:26:58');
/*!40000 ALTER TABLE `assets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `classType`
--

DROP TABLE IF EXISTS `classType`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `classType` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `isdelete` tinyint(1) DEFAULT NULL,
  `remarks` text,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_classType_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `classType`
--

LOCK TABLES `classType` WRITE;
/*!40000 ALTER TABLE `classType` DISABLE KEYS */;
INSERT INTO `classType` VALUES (1,'物理机',1,0,'',NULL,'2016-07-30 19:00:41'),(2,'二层交换机',2,0,'',NULL,'2016-07-31 10:15:03'),(3,'DELL刀片',1,0,'',NULL,'2016-07-31 10:16:11'),(4,'虚拟化',1,0,'',NULL,'2016-07-31 10:18:37');
/*!40000 ALTER TABLE `classType` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deviceDisks`
--

DROP TABLE IF EXISTS `deviceDisks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deviceDisks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot_id` int(11) DEFAULT NULL,
  `sn` varchar(64) DEFAULT NULL,
  `size` varchar(32) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `raid` int(11) DEFAULT NULL,
  `revolutions` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `physics_error` int(11) DEFAULT NULL,
  `logic_error` int(11) DEFAULT NULL,
  `device_id` int(11) DEFAULT NULL,
  `isdelete` tinyint(1) DEFAULT NULL,
  `remarks` text,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `devicedisks_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deviceDisks`
--

LOCK TABLES `deviceDisks` WRITE;
/*!40000 ALTER TABLE `deviceDisks` DISABLE KEYS */;
/*!40000 ALTER TABLE `deviceDisks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deviceMemorys`
--

DROP TABLE IF EXISTS `deviceMemorys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deviceMemorys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slot_id` int(11) DEFAULT NULL,
  `sn` varchar(64) DEFAULT NULL,
  `size` int(11) DEFAULT NULL,
  `device_id` int(11) DEFAULT NULL,
  `remarks` text,
  `isdelete` tinyint(1) DEFAULT NULL,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `devicememorys_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deviceMemorys`
--

LOCK TABLES `deviceMemorys` WRITE;
/*!40000 ALTER TABLE `deviceMemorys` DISABLE KEYS */;
/*!40000 ALTER TABLE `deviceMemorys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deviceModel`
--

DROP TABLE IF EXISTS `deviceModel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deviceModel` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `portcount` int(11) DEFAULT NULL,
  `slot_id` int(11) DEFAULT NULL,
  `sn` varchar(64) DEFAULT NULL,
  `device_id` int(11) DEFAULT NULL,
  `isdelete` tinyint(1) DEFAULT NULL,
  `remarks` text,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `devicemodel_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deviceModel`
--

LOCK TABLES `deviceModel` WRITE;
/*!40000 ALTER TABLE `deviceModel` DISABLE KEYS */;
INSERT INTO `deviceModel` VALUES (4,'网卡1',1,2,1,'MODEL1',1,0,'',NULL,'2016-07-30 19:15:35'),(5,'网卡1',1,8,1,'',2,0,'',NULL,'2016-07-31 12:20:12'),(6,'网卡2',1,8,2,'',1,0,'',NULL,'2016-08-01 15:09:30'),(7,'test',2,2,1,'333333',1,0,'',NULL,'2016-08-31 22:07:14');
/*!40000 ALTER TABLE `deviceModel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deviceNetwork`
--

DROP TABLE IF EXISTS `deviceNetwork`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deviceNetwork` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `classType_id` int(11) DEFAULT NULL,
  `asset_id` int(11) DEFAULT NULL,
  `rack_id` int(11) DEFAULT NULL,
  `model_id` int(11) DEFAULT NULL,
  `firmversion` varchar(64) DEFAULT NULL,
  `enginecount` int(11) DEFAULT NULL,
  `powercount` int(11) DEFAULT NULL,
  `powertype` int(11) DEFAULT NULL,
  `fancount` int(11) DEFAULT NULL,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  `remarks` text,
  `hostname` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `classType_id` (`classType_id`),
  KEY `asset_id` (`asset_id`),
  KEY `rack_id` (`rack_id`),
  KEY `model_id` (`model_id`),
  CONSTRAINT `devicenetwork_ibfk_1` FOREIGN KEY (`classType_id`) REFERENCES `classType` (`id`),
  CONSTRAINT `devicenetwork_ibfk_2` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`),
  CONSTRAINT `devicenetwork_ibfk_3` FOREIGN KEY (`rack_id`) REFERENCES `racks` (`id`),
  CONSTRAINT `devicenetwork_ibfk_4` FOREIGN KEY (`model_id`) REFERENCES `deviceModel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deviceNetwork`
--

LOCK TABLES `deviceNetwork` WRITE;
/*!40000 ALTER TABLE `deviceNetwork` DISABLE KEYS */;
INSERT INTO `deviceNetwork` VALUES (1,2,3,1,NULL,'1.0',2,2,1,4,NULL,'2016-08-02 15:03:12',NULL,'SWITCH01');
/*!40000 ALTER TABLE `deviceNetwork` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devicePools`
--

DROP TABLE IF EXISTS `devicePools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devicePools` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `usedept` varchar(64) DEFAULT NULL,
  `isdelete` tinyint(1) DEFAULT NULL,
  `remarks` text,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devicePools`
--

LOCK TABLES `devicePools` WRITE;
/*!40000 ALTER TABLE `devicePools` DISABLE KEYS */;
INSERT INTO `devicePools` VALUES (1,'运维',1,'运维部',0,'',NULL,'2016-07-31 10:16:43'),(2,'研发',1,'研发部',0,'开发',NULL,'2016-07-31 10:17:31'),(3,'测试',1,'研发部',0,'',NULL,'2016-07-31 10:18:06');
/*!40000 ALTER TABLE `devicePools` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devicePortMap`
--

DROP TABLE IF EXISTS `devicePortMap`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devicePortMap` (
  `source_id` int(11) NOT NULL,
  `target_id` int(11) NOT NULL,
  `use` varchar(64) DEFAULT NULL,
  `isbond` tinyint(1) DEFAULT NULL,
  `remarks` text,
  `isdelete` tinyint(1) DEFAULT NULL,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  PRIMARY KEY (`source_id`,`target_id`),
  KEY `target_id` (`target_id`),
  CONSTRAINT `deviceportmap_ibfk_1` FOREIGN KEY (`source_id`) REFERENCES `devicePorts` (`id`),
  CONSTRAINT `deviceportmap_ibfk_2` FOREIGN KEY (`target_id`) REFERENCES `devicePorts` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devicePortMap`
--

LOCK TABLES `devicePortMap` WRITE;
/*!40000 ALTER TABLE `devicePortMap` DISABLE KEYS */;
/*!40000 ALTER TABLE `devicePortMap` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devicePorts`
--

DROP TABLE IF EXISTS `devicePorts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devicePorts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `ip` varchar(32) DEFAULT NULL,
  `netmask` varchar(32) DEFAULT NULL,
  `gateway` varchar(32) DEFAULT NULL,
  `mac` varchar(64) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `mode` int(11) DEFAULT NULL,
  `rate` int(11) DEFAULT NULL,
  `vlanid` int(11) DEFAULT NULL,
  `model_id` int(11) DEFAULT NULL,
  `display` tinyint(1) DEFAULT NULL,
  `remarks` text,
  `isdelete` tinyint(1) DEFAULT NULL,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_devicePorts_ip` (`ip`),
  UNIQUE KEY `ix_devicePorts_mac` (`mac`),
  KEY `model_id` (`model_id`),
  CONSTRAINT `deviceports_ibfk_1` FOREIGN KEY (`model_id`) REFERENCES `deviceModel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devicePorts`
--

LOCK TABLES `devicePorts` WRITE;
/*!40000 ALTER TABLE `devicePorts` DISABLE KEYS */;
INSERT INTO `devicePorts` VALUES (1,'eth0','192.168.1.1','255.255.255.0','192.168.1.254','aa:bb:cc:dd:ee:',2,1,2,1,4,1,'',0,NULL,'2016-07-30 19:16:47'),(2,'eth1','192.168.1.6','255.255.255.0','192.168.1.1','aa:bb:cc:dd:ee:ff',1,1,2,1,4,0,'',0,NULL,'2016-07-30 21:30:17'),(4,'eth2','192.168.2.100','255.255.255.0','192.168.2.254','aa:bb:cc:dd:ef',1,1,2,1,6,1,'',0,NULL,'2016-07-31 12:22:03'),(5,'eth3','192.168.4.22','255.255.255.0','192.168.4.254','aa:bb:cc',1,1,2,4,5,1,'',0,NULL,'2016-08-03 15:04:17'),(6,'geth0','192.168.1.8','255.255.255.0','192.168.1.1','33:33:33:33:33',1,1,2,22,7,0,'',0,NULL,'2016-08-31 22:10:10');
/*!40000 ALTER TABLE `devicePorts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devicePowers`
--

DROP TABLE IF EXISTS `devicePowers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devicePowers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` int(11) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT NULL,
  `ip` varchar(64) DEFAULT NULL,
  `user` varchar(64) DEFAULT NULL,
  `password_hash` varchar(256) DEFAULT NULL,
  `powerid` varchar(256) DEFAULT NULL,
  `device_id` int(11) DEFAULT NULL,
  `isdelete` tinyint(1) DEFAULT NULL,
  `remarks` text,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  CONSTRAINT `devicepowers_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devicePowers`
--

LOCK TABLES `devicePowers` WRITE;
/*!40000 ALTER TABLE `devicePowers` DISABLE KEYS */;
INSERT INTO `devicePowers` VALUES (2,1,1,'192.168.1.20','root','eyJhbGciOiJIUzI1NiJ9.eyJjb25maXJtIjoiMTIzNDU2In0.kMK2FgZWE5b9kBRUngoU6XfoKNdsLUN-TnbXq1qM3Mg','1',1,0,'',NULL,'2016-07-30 20:54:38');
/*!40000 ALTER TABLE `devicePowers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `devices`
--

DROP TABLE IF EXISTS `devices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `asset_id` int(11) DEFAULT NULL,
  `rack_id` int(11) DEFAULT NULL,
  `classType_id` int(11) DEFAULT NULL,
  `hostname` varchar(64) DEFAULT NULL,
  `is_virtualization` tinyint(1) DEFAULT NULL,
  `os` varchar(64) DEFAULT NULL,
  `cpumodel` varchar(64) DEFAULT NULL,
  `cpucount` int(11) DEFAULT NULL,
  `memsize` int(11) DEFAULT NULL,
  `disksize` varchar(64) DEFAULT NULL,
  `use` varchar(64) DEFAULT NULL,
  `business` int(11) DEFAULT NULL,
  `powerstatus` int(11) DEFAULT NULL,
  `uuid` varchar(64) DEFAULT NULL,
  `auto_discover` tinyint(1) DEFAULT NULL,
  `isdelete` int(11) DEFAULT NULL,
  `remarks` text,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  `useracksize` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `asset_id` (`asset_id`),
  KEY `rack_id` (`rack_id`),
  KEY `classType_id` (`classType_id`),
  CONSTRAINT `devices_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `devices_ibfk_2` FOREIGN KEY (`rack_id`) REFERENCES `racks` (`id`),
  CONSTRAINT `devices_ibfk_3` FOREIGN KEY (`classType_id`) REFERENCES `classType` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `devices`
--

LOCK TABLES `devices` WRITE;
/*!40000 ALTER TABLE `devices` DISABLE KEYS */;
INSERT INTO `devices` VALUES (1,1,1,1,'web001',0,'','intel',24,64,'1000','官网',2,1,NULL,NULL,NULL,'',NULL,'2016-07-30 19:13:17',2),(2,2,1,4,'virtual001',1,'','intel',24,128,'2000','虚拟化',1,1,NULL,NULL,NULL,'',NULL,'2016-07-31 12:18:35',NULL),(3,1,2,1,'172.16.46.128',0,'','intel',2,4,'500','ansible测试',1,1,NULL,NULL,NULL,'',NULL,'2016-08-07 21:00:58',2);
/*!40000 ALTER TABLE `devices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `idcs`
--

DROP TABLE IF EXISTS `idcs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `idcs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `ispid` varchar(64) DEFAULT NULL,
  `contactname` varchar(64) DEFAULT NULL,
  `contactphone` varchar(64) DEFAULT NULL,
  `isdelete` tinyint(1) DEFAULT NULL,
  `nettype` int(11) DEFAULT NULL,
  `netout` varchar(64) DEFAULT NULL,
  `address` varchar(128) DEFAULT NULL,
  `city` varchar(64) DEFAULT NULL,
  `adnature` int(11) DEFAULT NULL,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `idcs`
--

LOCK TABLES `idcs` WRITE;
/*!40000 ALTER TABLE `idcs` DISABLE KEYS */;
INSERT INTO `idcs` VALUES (1,'上海移动机房','中国移动','柯发通','18516891830',0,3,'1000','上海金桥路636','上海',1,NULL,'2016-07-30 19:04:08','');
/*!40000 ALTER TABLE `idcs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ipResourceManage`
--

DROP TABLE IF EXISTS `ipResourceManage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ipResourceManage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ipPool_id` int(11) DEFAULT NULL,
  `ip` varchar(20) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `devicePort_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ipPool_id` (`ipPool_id`),
  KEY `devicePort_id` (`devicePort_id`),
  CONSTRAINT `ipresourcemanage_ibfk_1` FOREIGN KEY (`ipPool_id`) REFERENCES `ipResourcePools` (`id`),
  CONSTRAINT `ipresourcemanage_ibfk_2` FOREIGN KEY (`devicePort_id`) REFERENCES `devicePorts` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=763 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ipResourceManage`
--

LOCK TABLES `ipResourceManage` WRITE;
/*!40000 ALTER TABLE `ipResourceManage` DISABLE KEYS */;
INSERT INTO `ipResourceManage` VALUES (1,1,'192.168.1.1',1,1),(2,1,'192.168.1.2',0,NULL),(3,1,'192.168.1.3',0,NULL),(4,1,'192.168.1.4',0,NULL),(5,1,'192.168.1.5',0,NULL),(6,1,'192.168.1.6',1,2),(7,1,'192.168.1.7',0,NULL),(8,1,'192.168.1.8',1,6),(9,1,'192.168.1.9',0,NULL),(10,1,'192.168.1.10',0,NULL),(11,1,'192.168.1.11',0,NULL),(12,1,'192.168.1.12',0,NULL),(13,1,'192.168.1.13',0,NULL),(14,1,'192.168.1.14',0,NULL),(15,1,'192.168.1.15',0,NULL),(16,1,'192.168.1.16',0,NULL),(17,1,'192.168.1.17',0,NULL),(18,1,'192.168.1.18',0,NULL),(19,1,'192.168.1.19',0,NULL),(20,1,'192.168.1.20',0,NULL),(21,1,'192.168.1.21',0,NULL),(22,1,'192.168.1.22',0,NULL),(23,1,'192.168.1.23',0,NULL),(24,1,'192.168.1.24',0,NULL),(25,1,'192.168.1.25',0,NULL),(26,1,'192.168.1.26',0,NULL),(27,1,'192.168.1.27',0,NULL),(28,1,'192.168.1.28',0,NULL),(29,1,'192.168.1.29',0,NULL),(30,1,'192.168.1.30',0,NULL),(31,1,'192.168.1.31',0,NULL),(32,1,'192.168.1.32',0,NULL),(33,1,'192.168.1.33',0,NULL),(34,1,'192.168.1.34',0,NULL),(35,1,'192.168.1.35',0,NULL),(36,1,'192.168.1.36',0,NULL),(37,1,'192.168.1.37',0,NULL),(38,1,'192.168.1.38',0,NULL),(39,1,'192.168.1.39',0,NULL),(40,1,'192.168.1.40',0,NULL),(41,1,'192.168.1.41',0,NULL),(42,1,'192.168.1.42',0,NULL),(43,1,'192.168.1.43',0,NULL),(44,1,'192.168.1.44',0,NULL),(45,1,'192.168.1.45',0,NULL),(46,1,'192.168.1.46',0,NULL),(47,1,'192.168.1.47',0,NULL),(48,1,'192.168.1.48',0,NULL),(49,1,'192.168.1.49',0,NULL),(50,1,'192.168.1.50',0,NULL),(51,1,'192.168.1.51',0,NULL),(52,1,'192.168.1.52',0,NULL),(53,1,'192.168.1.53',0,NULL),(54,1,'192.168.1.54',0,NULL),(55,1,'192.168.1.55',0,NULL),(56,1,'192.168.1.56',0,NULL),(57,1,'192.168.1.57',0,NULL),(58,1,'192.168.1.58',0,NULL),(59,1,'192.168.1.59',0,NULL),(60,1,'192.168.1.60',0,NULL),(61,1,'192.168.1.61',0,NULL),(62,1,'192.168.1.62',0,NULL),(63,1,'192.168.1.63',0,NULL),(64,1,'192.168.1.64',0,NULL),(65,1,'192.168.1.65',0,NULL),(66,1,'192.168.1.66',0,NULL),(67,1,'192.168.1.67',0,NULL),(68,1,'192.168.1.68',0,NULL),(69,1,'192.168.1.69',0,NULL),(70,1,'192.168.1.70',0,NULL),(71,1,'192.168.1.71',0,NULL),(72,1,'192.168.1.72',0,NULL),(73,1,'192.168.1.73',0,NULL),(74,1,'192.168.1.74',0,NULL),(75,1,'192.168.1.75',0,NULL),(76,1,'192.168.1.76',0,NULL),(77,1,'192.168.1.77',0,NULL),(78,1,'192.168.1.78',0,NULL),(79,1,'192.168.1.79',0,NULL),(80,1,'192.168.1.80',0,NULL),(81,1,'192.168.1.81',0,NULL),(82,1,'192.168.1.82',0,NULL),(83,1,'192.168.1.83',0,NULL),(84,1,'192.168.1.84',0,NULL),(85,1,'192.168.1.85',0,NULL),(86,1,'192.168.1.86',0,NULL),(87,1,'192.168.1.87',0,NULL),(88,1,'192.168.1.88',0,NULL),(89,1,'192.168.1.89',0,NULL),(90,1,'192.168.1.90',0,NULL),(91,1,'192.168.1.91',0,NULL),(92,1,'192.168.1.92',0,NULL),(93,1,'192.168.1.93',0,NULL),(94,1,'192.168.1.94',0,NULL),(95,1,'192.168.1.95',0,NULL),(96,1,'192.168.1.96',0,NULL),(97,1,'192.168.1.97',0,NULL),(98,1,'192.168.1.98',0,NULL),(99,1,'192.168.1.99',0,NULL),(100,1,'192.168.1.100',0,NULL),(101,1,'192.168.1.101',0,NULL),(102,1,'192.168.1.102',0,NULL),(103,1,'192.168.1.103',0,NULL),(104,1,'192.168.1.104',0,NULL),(105,1,'192.168.1.105',0,NULL),(106,1,'192.168.1.106',0,NULL),(107,1,'192.168.1.107',0,NULL),(108,1,'192.168.1.108',0,NULL),(109,1,'192.168.1.109',0,NULL),(110,1,'192.168.1.110',0,NULL),(111,1,'192.168.1.111',0,NULL),(112,1,'192.168.1.112',0,NULL),(113,1,'192.168.1.113',0,NULL),(114,1,'192.168.1.114',0,NULL),(115,1,'192.168.1.115',0,NULL),(116,1,'192.168.1.116',0,NULL),(117,1,'192.168.1.117',0,NULL),(118,1,'192.168.1.118',0,NULL),(119,1,'192.168.1.119',0,NULL),(120,1,'192.168.1.120',0,NULL),(121,1,'192.168.1.121',0,NULL),(122,1,'192.168.1.122',0,NULL),(123,1,'192.168.1.123',0,NULL),(124,1,'192.168.1.124',0,NULL),(125,1,'192.168.1.125',0,NULL),(126,1,'192.168.1.126',0,NULL),(127,1,'192.168.1.127',0,NULL),(128,1,'192.168.1.128',0,NULL),(129,1,'192.168.1.129',0,NULL),(130,1,'192.168.1.130',0,NULL),(131,1,'192.168.1.131',0,NULL),(132,1,'192.168.1.132',0,NULL),(133,1,'192.168.1.133',0,NULL),(134,1,'192.168.1.134',0,NULL),(135,1,'192.168.1.135',0,NULL),(136,1,'192.168.1.136',0,NULL),(137,1,'192.168.1.137',0,NULL),(138,1,'192.168.1.138',0,NULL),(139,1,'192.168.1.139',0,NULL),(140,1,'192.168.1.140',0,NULL),(141,1,'192.168.1.141',0,NULL),(142,1,'192.168.1.142',0,NULL),(143,1,'192.168.1.143',0,NULL),(144,1,'192.168.1.144',0,NULL),(145,1,'192.168.1.145',0,NULL),(146,1,'192.168.1.146',0,NULL),(147,1,'192.168.1.147',0,NULL),(148,1,'192.168.1.148',0,NULL),(149,1,'192.168.1.149',0,NULL),(150,1,'192.168.1.150',0,NULL),(151,1,'192.168.1.151',0,NULL),(152,1,'192.168.1.152',0,NULL),(153,1,'192.168.1.153',0,NULL),(154,1,'192.168.1.154',0,NULL),(155,1,'192.168.1.155',0,NULL),(156,1,'192.168.1.156',0,NULL),(157,1,'192.168.1.157',0,NULL),(158,1,'192.168.1.158',0,NULL),(159,1,'192.168.1.159',0,NULL),(160,1,'192.168.1.160',0,NULL),(161,1,'192.168.1.161',0,NULL),(162,1,'192.168.1.162',0,NULL),(163,1,'192.168.1.163',0,NULL),(164,1,'192.168.1.164',0,NULL),(165,1,'192.168.1.165',0,NULL),(166,1,'192.168.1.166',0,NULL),(167,1,'192.168.1.167',0,NULL),(168,1,'192.168.1.168',0,NULL),(169,1,'192.168.1.169',0,NULL),(170,1,'192.168.1.170',0,NULL),(171,1,'192.168.1.171',0,NULL),(172,1,'192.168.1.172',0,NULL),(173,1,'192.168.1.173',0,NULL),(174,1,'192.168.1.174',0,NULL),(175,1,'192.168.1.175',0,NULL),(176,1,'192.168.1.176',0,NULL),(177,1,'192.168.1.177',0,NULL),(178,1,'192.168.1.178',0,NULL),(179,1,'192.168.1.179',0,NULL),(180,1,'192.168.1.180',0,NULL),(181,1,'192.168.1.181',0,NULL),(182,1,'192.168.1.182',0,NULL),(183,1,'192.168.1.183',0,NULL),(184,1,'192.168.1.184',0,NULL),(185,1,'192.168.1.185',0,NULL),(186,1,'192.168.1.186',0,NULL),(187,1,'192.168.1.187',0,NULL),(188,1,'192.168.1.188',0,NULL),(189,1,'192.168.1.189',0,NULL),(190,1,'192.168.1.190',0,NULL),(191,1,'192.168.1.191',0,NULL),(192,1,'192.168.1.192',0,NULL),(193,1,'192.168.1.193',0,NULL),(194,1,'192.168.1.194',0,NULL),(195,1,'192.168.1.195',0,NULL),(196,1,'192.168.1.196',0,NULL),(197,1,'192.168.1.197',0,NULL),(198,1,'192.168.1.198',0,NULL),(199,1,'192.168.1.199',0,NULL),(200,1,'192.168.1.200',0,NULL),(201,1,'192.168.1.201',0,NULL),(202,1,'192.168.1.202',0,NULL),(203,1,'192.168.1.203',0,NULL),(204,1,'192.168.1.204',0,NULL),(205,1,'192.168.1.205',0,NULL),(206,1,'192.168.1.206',0,NULL),(207,1,'192.168.1.207',0,NULL),(208,1,'192.168.1.208',0,NULL),(209,1,'192.168.1.209',0,NULL),(210,1,'192.168.1.210',0,NULL),(211,1,'192.168.1.211',0,NULL),(212,1,'192.168.1.212',0,NULL),(213,1,'192.168.1.213',0,NULL),(214,1,'192.168.1.214',0,NULL),(215,1,'192.168.1.215',0,NULL),(216,1,'192.168.1.216',0,NULL),(217,1,'192.168.1.217',0,NULL),(218,1,'192.168.1.218',0,NULL),(219,1,'192.168.1.219',0,NULL),(220,1,'192.168.1.220',0,NULL),(221,1,'192.168.1.221',0,NULL),(222,1,'192.168.1.222',0,NULL),(223,1,'192.168.1.223',0,NULL),(224,1,'192.168.1.224',0,NULL),(225,1,'192.168.1.225',0,NULL),(226,1,'192.168.1.226',0,NULL),(227,1,'192.168.1.227',0,NULL),(228,1,'192.168.1.228',0,NULL),(229,1,'192.168.1.229',0,NULL),(230,1,'192.168.1.230',0,NULL),(231,1,'192.168.1.231',0,NULL),(232,1,'192.168.1.232',0,NULL),(233,1,'192.168.1.233',0,NULL),(234,1,'192.168.1.234',0,NULL),(235,1,'192.168.1.235',0,NULL),(236,1,'192.168.1.236',0,NULL),(237,1,'192.168.1.237',0,NULL),(238,1,'192.168.1.238',0,NULL),(239,1,'192.168.1.239',0,NULL),(240,1,'192.168.1.240',0,NULL),(241,1,'192.168.1.241',0,NULL),(242,1,'192.168.1.242',0,NULL),(243,1,'192.168.1.243',0,NULL),(244,1,'192.168.1.244',0,NULL),(245,1,'192.168.1.245',0,NULL),(246,1,'192.168.1.246',0,NULL),(247,1,'192.168.1.247',0,NULL),(248,1,'192.168.1.248',0,NULL),(249,1,'192.168.1.249',0,NULL),(250,1,'192.168.1.250',0,NULL),(251,1,'192.168.1.251',0,NULL),(252,1,'192.168.1.252',0,NULL),(253,1,'192.168.1.253',0,NULL),(254,1,'192.168.1.254',0,NULL),(255,2,'192.168.2.1',0,NULL),(256,2,'192.168.2.2',0,NULL),(257,2,'192.168.2.3',0,NULL),(258,2,'192.168.2.4',0,NULL),(259,2,'192.168.2.5',0,NULL),(260,2,'192.168.2.6',0,NULL),(261,2,'192.168.2.7',0,NULL),(262,2,'192.168.2.8',0,NULL),(263,2,'192.168.2.9',0,NULL),(264,2,'192.168.2.10',0,NULL),(265,2,'192.168.2.11',0,NULL),(266,2,'192.168.2.12',0,NULL),(267,2,'192.168.2.13',0,NULL),(268,2,'192.168.2.14',0,NULL),(269,2,'192.168.2.15',0,NULL),(270,2,'192.168.2.16',0,NULL),(271,2,'192.168.2.17',0,NULL),(272,2,'192.168.2.18',0,NULL),(273,2,'192.168.2.19',0,NULL),(274,2,'192.168.2.20',0,NULL),(275,2,'192.168.2.21',0,NULL),(276,2,'192.168.2.22',0,NULL),(277,2,'192.168.2.23',0,NULL),(278,2,'192.168.2.24',0,NULL),(279,2,'192.168.2.25',0,NULL),(280,2,'192.168.2.26',0,NULL),(281,2,'192.168.2.27',0,NULL),(282,2,'192.168.2.28',0,NULL),(283,2,'192.168.2.29',0,NULL),(284,2,'192.168.2.30',0,NULL),(285,2,'192.168.2.31',0,NULL),(286,2,'192.168.2.32',0,NULL),(287,2,'192.168.2.33',0,NULL),(288,2,'192.168.2.34',0,NULL),(289,2,'192.168.2.35',0,NULL),(290,2,'192.168.2.36',0,NULL),(291,2,'192.168.2.37',0,NULL),(292,2,'192.168.2.38',0,NULL),(293,2,'192.168.2.39',0,NULL),(294,2,'192.168.2.40',0,NULL),(295,2,'192.168.2.41',0,NULL),(296,2,'192.168.2.42',0,NULL),(297,2,'192.168.2.43',0,NULL),(298,2,'192.168.2.44',0,NULL),(299,2,'192.168.2.45',0,NULL),(300,2,'192.168.2.46',0,NULL),(301,2,'192.168.2.47',0,NULL),(302,2,'192.168.2.48',0,NULL),(303,2,'192.168.2.49',0,NULL),(304,2,'192.168.2.50',0,NULL),(305,2,'192.168.2.51',0,NULL),(306,2,'192.168.2.52',0,NULL),(307,2,'192.168.2.53',0,NULL),(308,2,'192.168.2.54',0,NULL),(309,2,'192.168.2.55',0,NULL),(310,2,'192.168.2.56',0,NULL),(311,2,'192.168.2.57',0,NULL),(312,2,'192.168.2.58',0,NULL),(313,2,'192.168.2.59',0,NULL),(314,2,'192.168.2.60',0,NULL),(315,2,'192.168.2.61',0,NULL),(316,2,'192.168.2.62',0,NULL),(317,2,'192.168.2.63',0,NULL),(318,2,'192.168.2.64',0,NULL),(319,2,'192.168.2.65',0,NULL),(320,2,'192.168.2.66',0,NULL),(321,2,'192.168.2.67',0,NULL),(322,2,'192.168.2.68',0,NULL),(323,2,'192.168.2.69',0,NULL),(324,2,'192.168.2.70',0,NULL),(325,2,'192.168.2.71',0,NULL),(326,2,'192.168.2.72',0,NULL),(327,2,'192.168.2.73',0,NULL),(328,2,'192.168.2.74',0,NULL),(329,2,'192.168.2.75',0,NULL),(330,2,'192.168.2.76',0,NULL),(331,2,'192.168.2.77',0,NULL),(332,2,'192.168.2.78',0,NULL),(333,2,'192.168.2.79',0,NULL),(334,2,'192.168.2.80',0,NULL),(335,2,'192.168.2.81',0,NULL),(336,2,'192.168.2.82',0,NULL),(337,2,'192.168.2.83',0,NULL),(338,2,'192.168.2.84',0,NULL),(339,2,'192.168.2.85',0,NULL),(340,2,'192.168.2.86',0,NULL),(341,2,'192.168.2.87',0,NULL),(342,2,'192.168.2.88',0,NULL),(343,2,'192.168.2.89',0,NULL),(344,2,'192.168.2.90',0,NULL),(345,2,'192.168.2.91',0,NULL),(346,2,'192.168.2.92',0,NULL),(347,2,'192.168.2.93',0,NULL),(348,2,'192.168.2.94',0,NULL),(349,2,'192.168.2.95',0,NULL),(350,2,'192.168.2.96',0,NULL),(351,2,'192.168.2.97',0,NULL),(352,2,'192.168.2.98',0,NULL),(353,2,'192.168.2.99',0,NULL),(354,2,'192.168.2.100',1,4),(355,2,'192.168.2.101',0,NULL),(356,2,'192.168.2.102',0,NULL),(357,2,'192.168.2.103',0,NULL),(358,2,'192.168.2.104',0,NULL),(359,2,'192.168.2.105',0,NULL),(360,2,'192.168.2.106',0,NULL),(361,2,'192.168.2.107',0,NULL),(362,2,'192.168.2.108',0,NULL),(363,2,'192.168.2.109',0,NULL),(364,2,'192.168.2.110',0,NULL),(365,2,'192.168.2.111',0,NULL),(366,2,'192.168.2.112',0,NULL),(367,2,'192.168.2.113',0,NULL),(368,2,'192.168.2.114',0,NULL),(369,2,'192.168.2.115',0,NULL),(370,2,'192.168.2.116',0,NULL),(371,2,'192.168.2.117',0,NULL),(372,2,'192.168.2.118',0,NULL),(373,2,'192.168.2.119',0,NULL),(374,2,'192.168.2.120',0,NULL),(375,2,'192.168.2.121',0,NULL),(376,2,'192.168.2.122',0,NULL),(377,2,'192.168.2.123',0,NULL),(378,2,'192.168.2.124',0,NULL),(379,2,'192.168.2.125',0,NULL),(380,2,'192.168.2.126',0,NULL),(381,2,'192.168.2.127',0,NULL),(382,2,'192.168.2.128',0,NULL),(383,2,'192.168.2.129',0,NULL),(384,2,'192.168.2.130',0,NULL),(385,2,'192.168.2.131',0,NULL),(386,2,'192.168.2.132',0,NULL),(387,2,'192.168.2.133',0,NULL),(388,2,'192.168.2.134',0,NULL),(389,2,'192.168.2.135',0,NULL),(390,2,'192.168.2.136',0,NULL),(391,2,'192.168.2.137',0,NULL),(392,2,'192.168.2.138',0,NULL),(393,2,'192.168.2.139',0,NULL),(394,2,'192.168.2.140',0,NULL),(395,2,'192.168.2.141',0,NULL),(396,2,'192.168.2.142',0,NULL),(397,2,'192.168.2.143',0,NULL),(398,2,'192.168.2.144',0,NULL),(399,2,'192.168.2.145',0,NULL),(400,2,'192.168.2.146',0,NULL),(401,2,'192.168.2.147',0,NULL),(402,2,'192.168.2.148',0,NULL),(403,2,'192.168.2.149',0,NULL),(404,2,'192.168.2.150',0,NULL),(405,2,'192.168.2.151',0,NULL),(406,2,'192.168.2.152',0,NULL),(407,2,'192.168.2.153',0,NULL),(408,2,'192.168.2.154',0,NULL),(409,2,'192.168.2.155',0,NULL),(410,2,'192.168.2.156',0,NULL),(411,2,'192.168.2.157',0,NULL),(412,2,'192.168.2.158',0,NULL),(413,2,'192.168.2.159',0,NULL),(414,2,'192.168.2.160',0,NULL),(415,2,'192.168.2.161',0,NULL),(416,2,'192.168.2.162',0,NULL),(417,2,'192.168.2.163',0,NULL),(418,2,'192.168.2.164',0,NULL),(419,2,'192.168.2.165',0,NULL),(420,2,'192.168.2.166',0,NULL),(421,2,'192.168.2.167',0,NULL),(422,2,'192.168.2.168',0,NULL),(423,2,'192.168.2.169',0,NULL),(424,2,'192.168.2.170',0,NULL),(425,2,'192.168.2.171',0,NULL),(426,2,'192.168.2.172',0,NULL),(427,2,'192.168.2.173',0,NULL),(428,2,'192.168.2.174',0,NULL),(429,2,'192.168.2.175',0,NULL),(430,2,'192.168.2.176',0,NULL),(431,2,'192.168.2.177',0,NULL),(432,2,'192.168.2.178',0,NULL),(433,2,'192.168.2.179',0,NULL),(434,2,'192.168.2.180',0,NULL),(435,2,'192.168.2.181',0,NULL),(436,2,'192.168.2.182',0,NULL),(437,2,'192.168.2.183',0,NULL),(438,2,'192.168.2.184',0,NULL),(439,2,'192.168.2.185',0,NULL),(440,2,'192.168.2.186',0,NULL),(441,2,'192.168.2.187',0,NULL),(442,2,'192.168.2.188',0,NULL),(443,2,'192.168.2.189',0,NULL),(444,2,'192.168.2.190',0,NULL),(445,2,'192.168.2.191',0,NULL),(446,2,'192.168.2.192',0,NULL),(447,2,'192.168.2.193',0,NULL),(448,2,'192.168.2.194',0,NULL),(449,2,'192.168.2.195',0,NULL),(450,2,'192.168.2.196',0,NULL),(451,2,'192.168.2.197',0,NULL),(452,2,'192.168.2.198',0,NULL),(453,2,'192.168.2.199',0,NULL),(454,2,'192.168.2.200',0,NULL),(455,2,'192.168.2.201',0,NULL),(456,2,'192.168.2.202',0,NULL),(457,2,'192.168.2.203',0,NULL),(458,2,'192.168.2.204',0,NULL),(459,2,'192.168.2.205',0,NULL),(460,2,'192.168.2.206',0,NULL),(461,2,'192.168.2.207',0,NULL),(462,2,'192.168.2.208',0,NULL),(463,2,'192.168.2.209',0,NULL),(464,2,'192.168.2.210',0,NULL),(465,2,'192.168.2.211',0,NULL),(466,2,'192.168.2.212',0,NULL),(467,2,'192.168.2.213',0,NULL),(468,2,'192.168.2.214',0,NULL),(469,2,'192.168.2.215',0,NULL),(470,2,'192.168.2.216',0,NULL),(471,2,'192.168.2.217',0,NULL),(472,2,'192.168.2.218',0,NULL),(473,2,'192.168.2.219',0,NULL),(474,2,'192.168.2.220',0,NULL),(475,2,'192.168.2.221',0,NULL),(476,2,'192.168.2.222',0,NULL),(477,2,'192.168.2.223',0,NULL),(478,2,'192.168.2.224',0,NULL),(479,2,'192.168.2.225',0,NULL),(480,2,'192.168.2.226',0,NULL),(481,2,'192.168.2.227',0,NULL),(482,2,'192.168.2.228',0,NULL),(483,2,'192.168.2.229',0,NULL),(484,2,'192.168.2.230',0,NULL),(485,2,'192.168.2.231',0,NULL),(486,2,'192.168.2.232',0,NULL),(487,2,'192.168.2.233',0,NULL),(488,2,'192.168.2.234',0,NULL),(489,2,'192.168.2.235',0,NULL),(490,2,'192.168.2.236',0,NULL),(491,2,'192.168.2.237',0,NULL),(492,2,'192.168.2.238',0,NULL),(493,2,'192.168.2.239',0,NULL),(494,2,'192.168.2.240',0,NULL),(495,2,'192.168.2.241',0,NULL),(496,2,'192.168.2.242',0,NULL),(497,2,'192.168.2.243',0,NULL),(498,2,'192.168.2.244',0,NULL),(499,2,'192.168.2.245',0,NULL),(500,2,'192.168.2.246',0,NULL),(501,2,'192.168.2.247',0,NULL),(502,2,'192.168.2.248',0,NULL),(503,2,'192.168.2.249',0,NULL),(504,2,'192.168.2.250',0,NULL),(505,2,'192.168.2.251',0,NULL),(506,2,'192.168.2.252',0,NULL),(507,2,'192.168.2.253',0,NULL),(508,2,'192.168.2.254',0,NULL),(509,3,'192.168.4.1',0,NULL),(510,3,'192.168.4.2',0,NULL),(511,3,'192.168.4.3',0,NULL),(512,3,'192.168.4.4',0,NULL),(513,3,'192.168.4.5',0,NULL),(514,3,'192.168.4.6',0,NULL),(515,3,'192.168.4.7',0,NULL),(516,3,'192.168.4.8',0,NULL),(517,3,'192.168.4.9',0,NULL),(518,3,'192.168.4.10',0,NULL),(519,3,'192.168.4.11',0,NULL),(520,3,'192.168.4.12',0,NULL),(521,3,'192.168.4.13',0,NULL),(522,3,'192.168.4.14',0,NULL),(523,3,'192.168.4.15',0,NULL),(524,3,'192.168.4.16',0,NULL),(525,3,'192.168.4.17',0,NULL),(526,3,'192.168.4.18',0,NULL),(527,3,'192.168.4.19',0,NULL),(528,3,'192.168.4.20',0,NULL),(529,3,'192.168.4.21',0,NULL),(530,3,'192.168.4.22',1,5),(531,3,'192.168.4.23',0,NULL),(532,3,'192.168.4.24',0,NULL),(533,3,'192.168.4.25',0,NULL),(534,3,'192.168.4.26',0,NULL),(535,3,'192.168.4.27',0,NULL),(536,3,'192.168.4.28',0,NULL),(537,3,'192.168.4.29',0,NULL),(538,3,'192.168.4.30',0,NULL),(539,3,'192.168.4.31',0,NULL),(540,3,'192.168.4.32',0,NULL),(541,3,'192.168.4.33',0,NULL),(542,3,'192.168.4.34',0,NULL),(543,3,'192.168.4.35',0,NULL),(544,3,'192.168.4.36',0,NULL),(545,3,'192.168.4.37',0,NULL),(546,3,'192.168.4.38',0,NULL),(547,3,'192.168.4.39',0,NULL),(548,3,'192.168.4.40',0,NULL),(549,3,'192.168.4.41',0,NULL),(550,3,'192.168.4.42',0,NULL),(551,3,'192.168.4.43',0,NULL),(552,3,'192.168.4.44',0,NULL),(553,3,'192.168.4.45',0,NULL),(554,3,'192.168.4.46',0,NULL),(555,3,'192.168.4.47',0,NULL),(556,3,'192.168.4.48',0,NULL),(557,3,'192.168.4.49',0,NULL),(558,3,'192.168.4.50',0,NULL),(559,3,'192.168.4.51',0,NULL),(560,3,'192.168.4.52',0,NULL),(561,3,'192.168.4.53',0,NULL),(562,3,'192.168.4.54',0,NULL),(563,3,'192.168.4.55',0,NULL),(564,3,'192.168.4.56',0,NULL),(565,3,'192.168.4.57',0,NULL),(566,3,'192.168.4.58',0,NULL),(567,3,'192.168.4.59',0,NULL),(568,3,'192.168.4.60',0,NULL),(569,3,'192.168.4.61',0,NULL),(570,3,'192.168.4.62',0,NULL),(571,3,'192.168.4.63',0,NULL),(572,3,'192.168.4.64',0,NULL),(573,3,'192.168.4.65',0,NULL),(574,3,'192.168.4.66',0,NULL),(575,3,'192.168.4.67',0,NULL),(576,3,'192.168.4.68',0,NULL),(577,3,'192.168.4.69',0,NULL),(578,3,'192.168.4.70',0,NULL),(579,3,'192.168.4.71',0,NULL),(580,3,'192.168.4.72',0,NULL),(581,3,'192.168.4.73',0,NULL),(582,3,'192.168.4.74',0,NULL),(583,3,'192.168.4.75',0,NULL),(584,3,'192.168.4.76',0,NULL),(585,3,'192.168.4.77',0,NULL),(586,3,'192.168.4.78',0,NULL),(587,3,'192.168.4.79',0,NULL),(588,3,'192.168.4.80',0,NULL),(589,3,'192.168.4.81',0,NULL),(590,3,'192.168.4.82',0,NULL),(591,3,'192.168.4.83',0,NULL),(592,3,'192.168.4.84',0,NULL),(593,3,'192.168.4.85',0,NULL),(594,3,'192.168.4.86',0,NULL),(595,3,'192.168.4.87',0,NULL),(596,3,'192.168.4.88',0,NULL),(597,3,'192.168.4.89',0,NULL),(598,3,'192.168.4.90',0,NULL),(599,3,'192.168.4.91',0,NULL),(600,3,'192.168.4.92',0,NULL),(601,3,'192.168.4.93',0,NULL),(602,3,'192.168.4.94',0,NULL),(603,3,'192.168.4.95',0,NULL),(604,3,'192.168.4.96',0,NULL),(605,3,'192.168.4.97',0,NULL),(606,3,'192.168.4.98',0,NULL),(607,3,'192.168.4.99',0,NULL),(608,3,'192.168.4.100',0,NULL),(609,3,'192.168.4.101',0,NULL),(610,3,'192.168.4.102',0,NULL),(611,3,'192.168.4.103',0,NULL),(612,3,'192.168.4.104',0,NULL),(613,3,'192.168.4.105',0,NULL),(614,3,'192.168.4.106',0,NULL),(615,3,'192.168.4.107',0,NULL),(616,3,'192.168.4.108',0,NULL),(617,3,'192.168.4.109',0,NULL),(618,3,'192.168.4.110',0,NULL),(619,3,'192.168.4.111',0,NULL),(620,3,'192.168.4.112',0,NULL),(621,3,'192.168.4.113',0,NULL),(622,3,'192.168.4.114',0,NULL),(623,3,'192.168.4.115',0,NULL),(624,3,'192.168.4.116',0,NULL),(625,3,'192.168.4.117',0,NULL),(626,3,'192.168.4.118',0,NULL),(627,3,'192.168.4.119',0,NULL),(628,3,'192.168.4.120',0,NULL),(629,3,'192.168.4.121',0,NULL),(630,3,'192.168.4.122',0,NULL),(631,3,'192.168.4.123',0,NULL),(632,3,'192.168.4.124',0,NULL),(633,3,'192.168.4.125',0,NULL),(634,3,'192.168.4.126',0,NULL),(635,3,'192.168.4.127',0,NULL),(636,3,'192.168.4.128',0,NULL),(637,3,'192.168.4.129',0,NULL),(638,3,'192.168.4.130',0,NULL),(639,3,'192.168.4.131',0,NULL),(640,3,'192.168.4.132',0,NULL),(641,3,'192.168.4.133',0,NULL),(642,3,'192.168.4.134',0,NULL),(643,3,'192.168.4.135',0,NULL),(644,3,'192.168.4.136',0,NULL),(645,3,'192.168.4.137',0,NULL),(646,3,'192.168.4.138',0,NULL),(647,3,'192.168.4.139',0,NULL),(648,3,'192.168.4.140',0,NULL),(649,3,'192.168.4.141',0,NULL),(650,3,'192.168.4.142',0,NULL),(651,3,'192.168.4.143',0,NULL),(652,3,'192.168.4.144',0,NULL),(653,3,'192.168.4.145',0,NULL),(654,3,'192.168.4.146',0,NULL),(655,3,'192.168.4.147',0,NULL),(656,3,'192.168.4.148',0,NULL),(657,3,'192.168.4.149',0,NULL),(658,3,'192.168.4.150',0,NULL),(659,3,'192.168.4.151',0,NULL),(660,3,'192.168.4.152',0,NULL),(661,3,'192.168.4.153',0,NULL),(662,3,'192.168.4.154',0,NULL),(663,3,'192.168.4.155',0,NULL),(664,3,'192.168.4.156',0,NULL),(665,3,'192.168.4.157',0,NULL),(666,3,'192.168.4.158',0,NULL),(667,3,'192.168.4.159',0,NULL),(668,3,'192.168.4.160',0,NULL),(669,3,'192.168.4.161',0,NULL),(670,3,'192.168.4.162',0,NULL),(671,3,'192.168.4.163',0,NULL),(672,3,'192.168.4.164',0,NULL),(673,3,'192.168.4.165',0,NULL),(674,3,'192.168.4.166',0,NULL),(675,3,'192.168.4.167',0,NULL),(676,3,'192.168.4.168',0,NULL),(677,3,'192.168.4.169',0,NULL),(678,3,'192.168.4.170',0,NULL),(679,3,'192.168.4.171',0,NULL),(680,3,'192.168.4.172',0,NULL),(681,3,'192.168.4.173',0,NULL),(682,3,'192.168.4.174',0,NULL),(683,3,'192.168.4.175',0,NULL),(684,3,'192.168.4.176',0,NULL),(685,3,'192.168.4.177',0,NULL),(686,3,'192.168.4.178',0,NULL),(687,3,'192.168.4.179',0,NULL),(688,3,'192.168.4.180',0,NULL),(689,3,'192.168.4.181',0,NULL),(690,3,'192.168.4.182',0,NULL),(691,3,'192.168.4.183',0,NULL),(692,3,'192.168.4.184',0,NULL),(693,3,'192.168.4.185',0,NULL),(694,3,'192.168.4.186',0,NULL),(695,3,'192.168.4.187',0,NULL),(696,3,'192.168.4.188',0,NULL),(697,3,'192.168.4.189',0,NULL),(698,3,'192.168.4.190',0,NULL),(699,3,'192.168.4.191',0,NULL),(700,3,'192.168.4.192',0,NULL),(701,3,'192.168.4.193',0,NULL),(702,3,'192.168.4.194',0,NULL),(703,3,'192.168.4.195',0,NULL),(704,3,'192.168.4.196',0,NULL),(705,3,'192.168.4.197',0,NULL),(706,3,'192.168.4.198',0,NULL),(707,3,'192.168.4.199',0,NULL),(708,3,'192.168.4.200',0,NULL),(709,3,'192.168.4.201',0,NULL),(710,3,'192.168.4.202',0,NULL),(711,3,'192.168.4.203',0,NULL),(712,3,'192.168.4.204',0,NULL),(713,3,'192.168.4.205',0,NULL),(714,3,'192.168.4.206',0,NULL),(715,3,'192.168.4.207',0,NULL),(716,3,'192.168.4.208',0,NULL),(717,3,'192.168.4.209',0,NULL),(718,3,'192.168.4.210',0,NULL),(719,3,'192.168.4.211',0,NULL),(720,3,'192.168.4.212',0,NULL),(721,3,'192.168.4.213',0,NULL),(722,3,'192.168.4.214',0,NULL),(723,3,'192.168.4.215',0,NULL),(724,3,'192.168.4.216',0,NULL),(725,3,'192.168.4.217',0,NULL),(726,3,'192.168.4.218',0,NULL),(727,3,'192.168.4.219',0,NULL),(728,3,'192.168.4.220',0,NULL),(729,3,'192.168.4.221',0,NULL),(730,3,'192.168.4.222',0,NULL),(731,3,'192.168.4.223',0,NULL),(732,3,'192.168.4.224',0,NULL),(733,3,'192.168.4.225',0,NULL),(734,3,'192.168.4.226',0,NULL),(735,3,'192.168.4.227',0,NULL),(736,3,'192.168.4.228',0,NULL),(737,3,'192.168.4.229',0,NULL),(738,3,'192.168.4.230',0,NULL),(739,3,'192.168.4.231',0,NULL),(740,3,'192.168.4.232',0,NULL),(741,3,'192.168.4.233',0,NULL),(742,3,'192.168.4.234',0,NULL),(743,3,'192.168.4.235',0,NULL),(744,3,'192.168.4.236',0,NULL),(745,3,'192.168.4.237',0,NULL),(746,3,'192.168.4.238',0,NULL),(747,3,'192.168.4.239',0,NULL),(748,3,'192.168.4.240',0,NULL),(749,3,'192.168.4.241',0,NULL),(750,3,'192.168.4.242',0,NULL),(751,3,'192.168.4.243',0,NULL),(752,3,'192.168.4.244',0,NULL),(753,3,'192.168.4.245',0,NULL),(754,3,'192.168.4.246',0,NULL),(755,3,'192.168.4.247',0,NULL),(756,3,'192.168.4.248',0,NULL),(757,3,'192.168.4.249',0,NULL),(758,3,'192.168.4.250',0,NULL),(759,3,'192.168.4.251',0,NULL),(760,3,'192.168.4.252',0,NULL),(761,3,'192.168.4.253',0,NULL),(762,3,'192.168.4.254',0,NULL);
/*!40000 ALTER TABLE `ipResourceManage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ipResourcePools`
--

DROP TABLE IF EXISTS `ipResourcePools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ipResourcePools` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `idc_id` int(11) DEFAULT NULL,
  `netmask` varchar(32) DEFAULT NULL,
  `gateway` varchar(32) DEFAULT NULL,
  `range` varchar(64) DEFAULT NULL,
  `type` int(11) DEFAULT NULL,
  `vlan` varchar(10) DEFAULT NULL,
  `remarks` text,
  PRIMARY KEY (`id`),
  KEY `idc_id` (`idc_id`),
  CONSTRAINT `ipresourcepools_ibfk_1` FOREIGN KEY (`idc_id`) REFERENCES `idcs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ipResourcePools`
--

LOCK TABLES `ipResourcePools` WRITE;
/*!40000 ALTER TABLE `ipResourcePools` DISABLE KEYS */;
INSERT INTO `ipResourcePools` VALUES (1,1,'255.255.255.0','192.168.1.254','192.168.1.0/24',1,'1',''),(2,1,'255.255.255.0','192.168.2.254','192.168.2.0/24',1,'',''),(3,NULL,'255.255.255.0','192.168.4.254','192.168.4.0/24',1,NULL,NULL);
/*!40000 ALTER TABLE `ipResourcePools` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `logtime` datetime DEFAULT NULL,
  `content` varchar(256) DEFAULT NULL,
  `action` varchar(32) DEFAULT NULL,
  `logobjtype` varchar(64) DEFAULT NULL,
  `logobj_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `racks`
--

DROP TABLE IF EXISTS `racks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `racks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `staff` varchar(64) DEFAULT NULL,
  `site` varchar(64) DEFAULT NULL,
  `racktype` varchar(64) DEFAULT NULL,
  `usesize` int(11) DEFAULT NULL,
  `remainsize` int(11) DEFAULT NULL,
  `electrictype` varchar(32) DEFAULT NULL,
  `electricno` varchar(32) DEFAULT NULL,
  `electriccapacity` int(11) DEFAULT NULL,
  `leftelectric` int(11) DEFAULT NULL,
  `renttime` datetime DEFAULT NULL,
  `expiretime` datetime DEFAULT NULL,
  `nextpaytime` datetime DEFAULT NULL,
  `money` int(11) DEFAULT NULL,
  `isdelete` tinyint(1) DEFAULT NULL,
  `remarks` text,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  `idc_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idc_id` (`idc_id`),
  CONSTRAINT `racks_ibfk_1` FOREIGN KEY (`idc_id`) REFERENCES `idcs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `racks`
--

LOCK TABLES `racks` WRITE;
/*!40000 ALTER TABLE `racks` DISABLE KEYS */;
INSERT INTO `racks` VALUES (1,'F01','柯发通','二楼A区F01','1',2,18,'1','1',20,20,'2016-01-01 00:00:00','2016-01-01 00:00:00','2016-01-01 00:00:00',6000,0,'',NULL,'2016-07-30 19:05:00',1),(2,'A02','柯发通','二楼A区A02','1',2,18,'1','1',NULL,20,'2016-01-01 00:00:00','2016-01-01 00:00:00','2016-01-01 00:00:00',6000,0,'',NULL,'2016-08-02 15:05:54',1);
/*!40000 ALTER TABLE `racks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) DEFAULT NULL,
  `default` tinyint(1) DEFAULT NULL,
  `permissions` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_roles_default` (`default`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'manager',0,536870910),(2,'User',1,306783378),(3,'Administrator',0,2147483647);
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) DEFAULT NULL,
  `username` varchar(64) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `name` varchar(64) DEFAULT NULL,
  `location` varchar(64) DEFAULT NULL,
  `position` varchar(64) DEFAULT NULL,
  `about_me` text,
  `phone` varchar(11) DEFAULT NULL,
  `qq` varchar(13) DEFAULT NULL,
  `member_since` datetime DEFAULT NULL,
  `last_seen` datetime DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT NULL,
  `avatar_hash` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  UNIQUE KEY `ix_users_username` (`username`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'kefatong@qq.com','administrator','pbkdf2:sha1:1000$yfBNFRNu$ec871e4d9f563c319dc677f7917c0f0faebe7e6f',3,'Admin','shanghai','python',NULL,'11111',NULL,'2016-07-30 10:58:41','2016-09-22 03:20:53',1,NULL);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `virtMachine`
--

DROP TABLE IF EXISTS `virtMachine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `virtMachine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` int(11) DEFAULT NULL,
  `deviceType` varchar(64) DEFAULT NULL,
  `virtType` int(11) DEFAULT NULL,
  `pool_id` int(11) DEFAULT NULL,
  `hostname` varchar(64) DEFAULT NULL,
  `os` varchar(64) DEFAULT NULL,
  `cpumodel` varchar(64) DEFAULT NULL,
  `cpucount` int(11) DEFAULT NULL,
  `memsize` int(11) DEFAULT NULL,
  `disksize` varchar(64) DEFAULT NULL,
  `business` int(11) DEFAULT NULL,
  `powerstatus` int(11) DEFAULT NULL,
  `onstatus` int(11) DEFAULT NULL,
  `usedept` varchar(64) DEFAULT NULL,
  `usestaff` varchar(64) DEFAULT NULL,
  `mainuses` varchar(128) DEFAULT NULL,
  `managedept` varchar(64) DEFAULT NULL,
  `managestaff` varchar(64) DEFAULT NULL,
  `isdelete` tinyint(1) DEFAULT NULL,
  `instaff` varchar(64) DEFAULT NULL,
  `inputtime` datetime DEFAULT NULL,
  `remarks` text,
  `uuid` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `device_id` (`device_id`),
  KEY `pool_id` (`pool_id`),
  CONSTRAINT `virtmachine_ibfk_1` FOREIGN KEY (`device_id`) REFERENCES `devices` (`id`),
  CONSTRAINT `virtmachine_ibfk_2` FOREIGN KEY (`pool_id`) REFERENCES `devicePools` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `virtMachine`
--

LOCK TABLES `virtMachine` WRITE;
/*!40000 ALTER TABLE `virtMachine` DISABLE KEYS */;
INSERT INTO `virtMachine` VALUES (1,2,'1',NULL,3,'test01','centos6.5','intel',24,4,'50',1,1,1,'运维部','柯发通','测试','运维部','柯发通',NULL,NULL,'2016-07-31 14:24:33','',NULL);
/*!40000 ALTER TABLE `virtMachine` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-09-22 12:41:46
