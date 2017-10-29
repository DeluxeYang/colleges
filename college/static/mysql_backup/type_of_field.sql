/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50617
Source Host           : localhost:3306
Source Database       : college

Target Server Type    : MYSQL
Target Server Version : 50617
File Encoding         : 65001

Date: 2017-10-24 20:06:47
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `type_of_field`
-- ----------------------------
DROP TABLE IF EXISTS `type_of_field`;
CREATE TABLE `type_of_field` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `size` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of type_of_field
-- ----------------------------
INSERT INTO `type_of_field` VALUES ('1', 'int', null);
INSERT INTO `type_of_field` VALUES ('2', 'varchar', '255');
INSERT INTO `type_of_field` VALUES ('3', 'float', null);
INSERT INTO `type_of_field` VALUES ('4', 'text', null);
