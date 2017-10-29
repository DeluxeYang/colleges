/*
 Navicat PostgreSQL Data Transfer

 Source Server         : localhost
 Source Server Type    : PostgreSQL
 Source Server Version : 100000
 Source Host           : localhost:5432
 Source Catalog        : college
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 100000
 File Encoding         : 65001

 Date: 24/10/2017 20:08:35
*/


-- ----------------------------
-- Table structure for area
-- ----------------------------
DROP TABLE IF EXISTS "public"."area";
CREATE TABLE "public"."area" (
  "id" int4 NOT NULL DEFAULT nextval('area_id_seq'::regclass),
  "name_cn" varchar(30) COLLATE "pg_catalog"."default" NOT NULL,
  "nation_code_2" varchar(2) COLLATE "pg_catalog"."default",
  "is_index" bool NOT NULL
)
;

-- ----------------------------
-- Records of area
-- ----------------------------
INSERT INTO "public"."area" VALUES (1, '华北', '11', 'f');
INSERT INTO "public"."area" VALUES (2, '华北', '12', 'f');
INSERT INTO "public"."area" VALUES (3, '华北', '14', 'f');
INSERT INTO "public"."area" VALUES (4, '华北', '13', 'f');
INSERT INTO "public"."area" VALUES (5, '华北', '15', 'f');
INSERT INTO "public"."area" VALUES (6, '华东', '31', 'f');
INSERT INTO "public"."area" VALUES (7, '华东', '32', 'f');
INSERT INTO "public"."area" VALUES (8, '华东', '33', 'f');
INSERT INTO "public"."area" VALUES (9, '华东', '34', 'f');
INSERT INTO "public"."area" VALUES (10, '华东', '35', 'f');
INSERT INTO "public"."area" VALUES (11, '华东', '36', 'f');
INSERT INTO "public"."area" VALUES (12, '华东', '37', 'f');
INSERT INTO "public"."area" VALUES (13, '华中', '41', 'f');
INSERT INTO "public"."area" VALUES (14, '华中', '42', 'f');
INSERT INTO "public"."area" VALUES (15, '华中', '43', 'f');
INSERT INTO "public"."area" VALUES (16, '华南', '44', 'f');
INSERT INTO "public"."area" VALUES (17, '华南', '45', 'f');
INSERT INTO "public"."area" VALUES (18, '华南', '46', 'f');
INSERT INTO "public"."area" VALUES (19, '西南', '51', 'f');
INSERT INTO "public"."area" VALUES (20, '西南', '52', 'f');
INSERT INTO "public"."area" VALUES (21, '西南', '53', 'f');
INSERT INTO "public"."area" VALUES (22, '西南', '50', 'f');
INSERT INTO "public"."area" VALUES (23, '西南', '54', 'f');
INSERT INTO "public"."area" VALUES (24, '西北', '61', 'f');
INSERT INTO "public"."area" VALUES (25, '西北', '62', 'f');
INSERT INTO "public"."area" VALUES (26, '西北', '63', 'f');
INSERT INTO "public"."area" VALUES (27, '西北', '64', 'f');
INSERT INTO "public"."area" VALUES (28, '西北', '65', 'f');
INSERT INTO "public"."area" VALUES (29, '东北', '21', 'f');
INSERT INTO "public"."area" VALUES (30, '东北', '22', 'f');
INSERT INTO "public"."area" VALUES (31, '东北', '23', 'f');
INSERT INTO "public"."area" VALUES (32, '港澳台', '71', 'f');
INSERT INTO "public"."area" VALUES (33, '港澳台', '81', 'f');
INSERT INTO "public"."area" VALUES (34, '港澳台', '82', 'f');
INSERT INTO "public"."area" VALUES (35, '华北', '', 't');
INSERT INTO "public"."area" VALUES (36, '东北', '', 't');
INSERT INTO "public"."area" VALUES (37, '华东', '', 't');
INSERT INTO "public"."area" VALUES (38, '华中', '', 't');
INSERT INTO "public"."area" VALUES (39, '华南', '', 't');
INSERT INTO "public"."area" VALUES (40, '西南', '', 't');
INSERT INTO "public"."area" VALUES (41, '西北', '', 't');
INSERT INTO "public"."area" VALUES (42, '港澳台', '', 't');

-- ----------------------------
-- Primary Key structure for table area
-- ----------------------------
ALTER TABLE "public"."area" ADD CONSTRAINT "area_pkey" PRIMARY KEY ("id");
