/*
SQLyog Community Edition- MySQL GUI v7.01 
MySQL - 5.0.27-community-nt : Database - 0035_health_insurance
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`0035_health_insurance` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `0035_health_insurance`;

/*Table structure for table `insurance` */

DROP TABLE IF EXISTS `insurance`;

CREATE TABLE `insurance` (
  `ID` int(255) NOT NULL auto_increment,
  `name` varchar(255) default NULL,
  `insurancecost` varchar(255) default NULL,
  `insurancetype` varchar(255) default NULL,
  `Phone` varchar(255) default NULL,
  `Address` varchar(255) default NULL,
  `usermassge` longtext,
  `filenamepath` varchar(255) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `insurance` */

insert  into `insurance`(`ID`,`name`,`insurancecost`,`insurancetype`,`Phone`,`Address`,`usermassge`,`filenamepath`) values (1,'sahil disusa','6000','Life Insurance','7894561231','mumbai','dfsdf','static/Insurance/1.jpg'),(2,'skin lacto','2000','Life Insurance','7894561231','mumbai','dsgdv sdgsd sd sdg sgsdg fh gfj kugjkgjhgh','static/Insurance/2.jpg'),(3,'amok gore','10000','Homeowners/Renters Insurance','9632589632','ghatkoper','If you want to fetch all insurance records','static/Insurance/3.jpg');

/*Table structure for table `registration` */

DROP TABLE IF EXISTS `registration`;

CREATE TABLE `registration` (
  `Id` int(255) NOT NULL auto_increment,
  `Name` varchar(255) default NULL,
  `Email` varchar(255) default NULL,
  `Phone` varchar(255) default NULL,
  `Password` varchar(255) default NULL,
  `Address` varchar(255) default NULL,
  `Profile_img` varchar(255) default NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `registration` */

insert  into `registration`(`Id`,`Name`,`Email`,`Phone`,`Password`,`Address`,`Profile_img`) values (1,'a','roshu@gmail.com','7894561231','a','mumbai','static/facedata/a/a_12.jpg'),(2,'kalpesh','y@gmail.com','7894561231','b','mumbai','static/facedata/kalpesh/kalpesh_6.jpg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
