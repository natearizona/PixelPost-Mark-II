-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: pixelpost
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `pixelpost_addons`
--

DROP TABLE IF EXISTS `pixelpost_addons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_addons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `addon_name` varchar(66) NOT NULL DEFAULT '',
  `status` varchar(3) NOT NULL DEFAULT 'on',
  `type` varchar(15) NOT NULL DEFAULT 'normal',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pixelpost_banlist`
--

DROP TABLE IF EXISTS `pixelpost_banlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_banlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `moderation_list` mediumtext NOT NULL,
  `blacklist` mediumtext NOT NULL,
  `ref_ban_list` mediumtext NOT NULL,
  `acceptable_num_links` int(3) NOT NULL DEFAULT '2',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pixelpost_catassoc`
--

DROP TABLE IF EXISTS `pixelpost_catassoc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_catassoc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` int(11) NOT NULL DEFAULT '0',
  `image_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `cat_id` (`cat_id`),
  KEY `image_id` (`image_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pixelpost_categories`
--

DROP TABLE IF EXISTS `pixelpost_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL DEFAULT '',
  `alt_name` varchar(100) NOT NULL DEFAULT 'DEFAULT',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pixelpost_comments`
--

DROP TABLE IF EXISTS `pixelpost_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL DEFAULT '0',
  `datetime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ip` varchar(20) NOT NULL DEFAULT '',
  `message` text NOT NULL,
  `name` varchar(30) DEFAULT NULL,
  `url` varchar(70) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `publish` varchar(3) NOT NULL DEFAULT 'yes',
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pixelpost_config`
--

DROP TABLE IF EXISTS `pixelpost_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_config` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `admin` varchar(20) NOT NULL DEFAULT '',
  `password` varchar(90) NOT NULL DEFAULT '',
  `email` varchar(90) NOT NULL DEFAULT '',
  `commentemail` varchar(3) NOT NULL DEFAULT '',
  `template` varchar(150) NOT NULL DEFAULT '',
  `imagepath` varchar(150) NOT NULL DEFAULT '',
  `thumbnailpath` varchar(150) NOT NULL DEFAULT '../thumbnails/',
  `siteurl` varchar(100) NOT NULL DEFAULT '',
  `sitetitle` varchar(100) NOT NULL DEFAULT '',
  `subtitle` varchar(100) NOT NULL DEFAULT 'Authentic photoblog flavour',
  `langfile` varchar(100) NOT NULL DEFAULT '',
  `calendar` varchar(30) NOT NULL DEFAULT '',
  `crop` varchar(3) NOT NULL DEFAULT '',
  `thumbwidth` int(11) NOT NULL,
  `thumbheight` int(11) NOT NULL,
  `thumbnumber` int(11) NOT NULL,
  `compression` int(11) NOT NULL,
  `dateformat` varchar(30) NOT NULL DEFAULT '',
  `timezone` float NOT NULL DEFAULT '-7',
  `catgluestart` varchar(5) NOT NULL DEFAULT '[',
  `catglueend` varchar(5) NOT NULL DEFAULT ']',
  `htmlemailnote` char(3) DEFAULT 'yes',
  `timestamp` varchar(4) NOT NULL DEFAULT 'yes',
  `visitorbooking` varchar(4) NOT NULL DEFAULT 'yes',
  `altlangfile` varchar(100) NOT NULL DEFAULT 'Off',
  `global_comments` enum('A','M','F') NOT NULL DEFAULT 'A',
  `markdown` enum('F','T') NOT NULL DEFAULT 'F',
  `exif` enum('F','T') NOT NULL DEFAULT 'T',
  `token` enum('F','T') NOT NULL DEFAULT 'F',
  `token_time` varchar(2) NOT NULL DEFAULT '5',
  `comment_timebetween` varchar(3) NOT NULL DEFAULT '30',
  `feeditems` varchar(3) NOT NULL DEFAULT '10',
  `max_uri_comments` varchar(3) NOT NULL DEFAULT '5',
  `rsstype` enum('F','FO','T','O','N') NOT NULL DEFAULT 'T',
  `feed_discovery` enum('RA','R','A','E','N') NOT NULL DEFAULT 'RA',
  `feed_title` varchar(100) NOT NULL DEFAULT 'Pixelpost',
  `feed_description` varchar(100) NOT NULL DEFAULT 'Authentic photoblog flavour',
  `feed_copyright` varchar(100) NOT NULL DEFAULT 'Copyright 2007 yoursite.com, All Rights Reserved',
  `allow_comment_feed` enum('Y','N') NOT NULL DEFAULT 'Y',
  `feed_external` varchar(150) NOT NULL DEFAULT '',
  `feed_external_type` enum('ER','EA') NOT NULL DEFAULT 'ER',
  `admin_langfile` varchar(100) NOT NULL DEFAULT 'english',
  `display_order` enum('default','reversed') NOT NULL DEFAULT 'default',
  `display_sort_by` varchar(150) NOT NULL DEFAULT 'datetime',
  `thumb_sharpening` varchar(1) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pixelpost_pixelpost`
--

DROP TABLE IF EXISTS `pixelpost_pixelpost`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_pixelpost` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `headline` varchar(150) NOT NULL DEFAULT '',
  `body` text NOT NULL,
  `image` text NOT NULL,
  `category` varchar(150) NOT NULL DEFAULT '',
  `alt_headline` varchar(150) NOT NULL DEFAULT '',
  `alt_body` text,
  `comments` enum('A','M','F') NOT NULL DEFAULT 'A',
  `exif_info` text,
  PRIMARY KEY (`id`),
  KEY `datetime` (`datetime`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pixelpost_tags`
--

DROP TABLE IF EXISTS `pixelpost_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_tags` (
  `img_id` int(11) NOT NULL,
  `tag` tinytext NOT NULL,
  `alt_tag` tinytext NOT NULL,
  PRIMARY KEY (`img_id`,`tag`(128),`alt_tag`(128))
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pixelpost_version`
--

DROP TABLE IF EXISTS `pixelpost_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_version` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `upgrade_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `version` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `version` (`version`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `pixelpost_visitors`
--

DROP TABLE IF EXISTS `pixelpost_visitors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `pixelpost_visitors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datetime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `host` varchar(100) NOT NULL DEFAULT '',
  `referer` varchar(255) NOT NULL DEFAULT '',
  `ua` varchar(255) NOT NULL DEFAULT '',
  `ip` varchar(255) NOT NULL DEFAULT '',
  `ruri` varchar(150) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `datetime` (`datetime`),
  KEY `referer` (`referer`),
  KEY `ip` (`ip`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-31 17:25:21
