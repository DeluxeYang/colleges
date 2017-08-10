/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50617
Source Host           : localhost:3306
Source Database       : college

Target Server Type    : MYSQL
Target Server Version : 50617
File Encoding         : 65001

Date: 2017-08-10 15:35:49
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `area`
-- ----------------------------
DROP TABLE IF EXISTS `area`;
CREATE TABLE `area` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name_cn` varchar(30) NOT NULL,
  `nation_code_2` varchar(2) DEFAULT NULL,
  `is_index` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of area
-- ----------------------------
INSERT INTO `area` VALUES ('1', '华北', '11', '0');
INSERT INTO `area` VALUES ('2', '华北', '12', '0');
INSERT INTO `area` VALUES ('3', '华北', '14', '0');
INSERT INTO `area` VALUES ('4', '华北', '13', '0');
INSERT INTO `area` VALUES ('5', '华北', '15', '0');
INSERT INTO `area` VALUES ('6', '华东', '31', '0');
INSERT INTO `area` VALUES ('7', '华东', '32', '0');
INSERT INTO `area` VALUES ('8', '华东', '33', '0');
INSERT INTO `area` VALUES ('9', '华东', '34', '0');
INSERT INTO `area` VALUES ('10', '华东', '35', '0');
INSERT INTO `area` VALUES ('11', '华东', '36', '0');
INSERT INTO `area` VALUES ('12', '华东', '37', '0');
INSERT INTO `area` VALUES ('13', '华中', '41', '0');
INSERT INTO `area` VALUES ('14', '华中', '42', '0');
INSERT INTO `area` VALUES ('15', '华中', '43', '0');
INSERT INTO `area` VALUES ('16', '华南', '44', '0');
INSERT INTO `area` VALUES ('17', '华南', '45', '0');
INSERT INTO `area` VALUES ('18', '华南', '46', '0');
INSERT INTO `area` VALUES ('19', '西南', '51', '0');
INSERT INTO `area` VALUES ('20', '西南', '52', '0');
INSERT INTO `area` VALUES ('21', '西南', '53', '0');
INSERT INTO `area` VALUES ('22', '西南', '50', '0');
INSERT INTO `area` VALUES ('23', '西南', '54', '0');
INSERT INTO `area` VALUES ('24', '西北', '61', '0');
INSERT INTO `area` VALUES ('25', '西北', '62', '0');
INSERT INTO `area` VALUES ('26', '西北', '63', '0');
INSERT INTO `area` VALUES ('27', '西北', '64', '0');
INSERT INTO `area` VALUES ('28', '西北', '65', '0');
INSERT INTO `area` VALUES ('29', '东北', '21', '0');
INSERT INTO `area` VALUES ('30', '东北', '22', '0');
INSERT INTO `area` VALUES ('31', '东北', '23', '0');
INSERT INTO `area` VALUES ('32', '港澳台', '71', '0');
INSERT INTO `area` VALUES ('33', '港澳台', '81', '0');
INSERT INTO `area` VALUES ('34', '港澳台', '82', '0');
INSERT INTO `area` VALUES ('35', '华北', '', '1');
INSERT INTO `area` VALUES ('36', '东北', '', '1');
INSERT INTO `area` VALUES ('37', '华东', '', '1');
INSERT INTO `area` VALUES ('38', '华中', '', '1');
INSERT INTO `area` VALUES ('39', '华南', '', '1');
INSERT INTO `area` VALUES ('40', '西南', '', '1');
INSERT INTO `area` VALUES ('41', '西北', '', '1');
INSERT INTO `area` VALUES ('42', '港澳台', '', '1');
