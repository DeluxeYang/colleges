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

 Date: 24/10/2017 20:08:51
*/


-- ----------------------------
-- Table structure for type_of_table
-- ----------------------------
DROP TABLE IF EXISTS "public"."type_of_table";
CREATE TABLE "public"."type_of_table" (
  "id" int4 NOT NULL DEFAULT nextval('type_of_table_id_seq'::regclass),
  "name_cn" varchar(30) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of type_of_table
-- ----------------------------
INSERT INTO "public"."type_of_table" VALUES (2, '人才');
INSERT INTO "public"."type_of_table" VALUES (1, '榜单');

-- ----------------------------
-- Indexes structure for table type_of_table
-- ----------------------------
CREATE INDEX "type_of_table_name_cn_71778b5e7afa19dd_like" ON "public"."type_of_table" USING btree (
  "name_cn" COLLATE "pg_catalog"."default" "pg_catalog"."varchar_pattern_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table type_of_table
-- ----------------------------
ALTER TABLE "public"."type_of_table" ADD CONSTRAINT "type_of_table_name_cn_key" UNIQUE ("name_cn");

-- ----------------------------
-- Primary Key structure for table type_of_table
-- ----------------------------
ALTER TABLE "public"."type_of_table" ADD CONSTRAINT "type_of_table_pkey" PRIMARY KEY ("id");
