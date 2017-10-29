/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50617
Source Host           : localhost:3306
Source Database       : college

Target Server Type    : MYSQL
Target Server Version : 50617
File Encoding         : 65001

Date: 2017-10-24 20:06:38
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `type_of_table`
-- ----------------------------
DROP TABLE IF EXISTS `type_of_table`;
CREATE TABLE `type_of_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_cn` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_cn` (`name_cn`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of type_of_table
-- ----------------------------
INSERT INTO `type_of_table` VALUES ('2', '人才');
INSERT INTO `type_of_table` VALUES ('1', '榜单');
