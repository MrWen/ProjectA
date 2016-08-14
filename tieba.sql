/*
SQLyog Ultimate v11.33 (64 bit)
MySQL - 5.6.28-0ubuntu0.14.04.1 : Database - tieba
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`tieba` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `tieba`;

/*Table structure for table `tieba_attention` */

DROP TABLE IF EXISTS `tieba_attention`;

CREATE TABLE `tieba_attention` (
  `user_id` int(11) NOT NULL,
  `attention` varchar(512) DEFAULT NULL,
  `peoples` int(11) DEFAULT NULL,
  `url` varchar(512) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `tieba_coef` */

DROP TABLE IF EXISTS `tieba_coef`;

CREATE TABLE `tieba_coef` (
  `name` char(32) NOT NULL,
  `name_type` int(11) DEFAULT NULL,
  `cur_index` int(11) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `tieba_name` */

DROP TABLE IF EXISTS `tieba_name`;

CREATE TABLE `tieba_name` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `table_name` char(32) DEFAULT NULL,
  `tieba_name` varchar(256) DEFAULT NULL,
  `sub_name` varchar(2048) DEFAULT NULL,
  `url` varchar(1024) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8;

/*Table structure for table `tieba_template` */

DROP TABLE IF EXISTS `tieba_template`;

CREATE TABLE `tieba_template` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `context` text,
  `cur_time` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `tieba_user` */

DROP TABLE IF EXISTS `tieba_user`;

CREATE TABLE `tieba_user` (
  `userid` int(11) NOT NULL,
  `user_name` varchar(256) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `use_year` float DEFAULT NULL COMMENT 'Y',
  `invitation` float DEFAULT NULL COMMENT 'W',
  `url` varchar(1024) DEFAULT NULL,
  `user_star` varchar(32) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `user_dynamics` */

DROP TABLE IF EXISTS `user_dynamics`;

CREATE TABLE `user_dynamics` (
  `user_id` int(11) DEFAULT NULL,
  `tieba_name` varchar(256) DEFAULT NULL,
  `context` text,
  `url` varchar(512) DEFAULT NULL,
  `titil` varchar(256) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `update_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
