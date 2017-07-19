#!/usr/bin/env python
# encoding: utf-8

import pymysql
import pymysql.cursors
import os
import django
import sys

from basic.utils.logger import logger
from college.settings import DATABASES

MYSQL_CONFIG = DATABASES["default"]


def sql_init(db_host, db_user, db_passwd, db_name, db_port=3306):
    # conn = None
    # cursor = None
    if db_name is None:
        """
        通过查看api 参数cursorclass应该在connect中，
        如果放在conn.cursor()中，应该是参数应该是cursor   modifed by ck
        """
        conn = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, port=db_port,
                               cursorclass=pymysql.cursors.DictCursor)  # connect to MySQL
        cursor = conn.cursor()  # get the cursor
    else:
        # 同上 modifed by ck
        conn = pymysql.connect(host=db_host, user=db_user, passwd=db_passwd, db=db_name,
                               port=db_port, cursorclass=pymysql.cursors.DictCursor)  # connect to MySQL
        cursor = conn.cursor()  # get the cursor
    return conn, cursor


# Function:  close MySQL cursor and connect.
# Parameter: conn: MySQL connection; cursor: MySQL cursor.
def sql_close(conn, cursor):
    try:
        cursor.close()      # close cursor
        conn.close()        # close connection
    except pymysql.Error as e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))


# Function:  configure django database settings.
# Parameter: file_path: settings.py; db_engine: type of database.
def django_db_configure(file_path, db_engine, db_name, db_user, db_passwd, db_host, db_port=3306):
    db_dict = {}        # dictionary assigned to DATABASES of settings.py
    db_conf = {'ENGINE': db_engine, 'NAME': db_name, 'USER': db_user, 'PASSWORD': db_passwd, 'HOST': db_host,
               'PORT': db_port}  # dictionary assigned to database configure

    db_dict['default'] = db_conf

    reader = open(file_path, 'r')
    lines = reader.readlines()
    reader.close()
    writer = open('settings.py', 'w')

    # delete DATABASES line.
    for line in lines:
        if 'DATABASES' not in line:
            writer.write(line)

    writer.write('DATABASES = ' + str(db_dict))   # update new DATABASES of settings.py
    writer.close()
    return


# Function:  setup django environment. You should setup django before using ORM standalone.
# Parameter: poj_directory: django project directory; settings: django settings module
def django_setup(poj_directory, settings):  # configure project directory
    sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), poj_directory))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)               # configure django settings
    django.setup()
    return


# Function:  execute orginal sql return insert_id and sql-execute results
# Parameter: conn: MySQL connection; cursor: MySQL cursor; sql: orginal SQL; args: SQL's arguments used by INSERT.
# Return:    primary keys of the table and sql-execute results.
def sql_execute(conn, cursor, sql, args):
    try:
        cursor.execute(sql, args)           # execute orginal SQL, with args or none.
        if conn is not None:
            conn.commit()                   # DELETE, INSERT, UPDATE operations should commit.
        ret = cursor.fetchall()
    except pymysql.Error as e:
        logger.error("mysql_base_api sql_execute Error %d: %s" % (e.args[0], e.args[1]))
        ret = (e.args[0], e.args[1])
    return ret         # sql-execute results.


# Function:  execute orginal sql return primary keys.
# Parameter: conn: MySQL connection; cursor: MySQL cursor; sql: orginal SQL; args: SQL's arguments used by INSERT.
# Return:    primary keys.
def sql_execute_keyreturn(conn, cursor, sql, args):
    pmkey = None                             # store primary keys
    try:
        cursor.execute(sql, args)           # execute orginal SQL, with args or none.
        pmkey = cursor.lastrowid
        if conn is not None:
            conn.commit()                   # DELETE, INSERT, UPDATE operations should commit.
    except pymysql.Error as e:
        logger.error("mysql_base_api sql_execute Error %d: %s" % (e.args[0], e.args[1]))

    return pmkey         # primary keys and sql-execute results.


# Function:  execute orginal sql without return.
# Parameter: cursor: MySQL cursor; sql: orginal SQL; args: SQL's arguments used by INSERT.
# Return:    None.
def sql_execute_noreturn(cursor, sql, args):
    try:
        cursor.execute(sql, args)
    except pymysql.Error as e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))


# Function:  executemany
# Parameter: conn: db connection; cursor: MySQL cursor; sql: orginal SQL; args: SQL's arguments used by INSERT.
# Return:    last row's pmkey.
def sql_executemany(conn, cursor, sql, args):
    pmkey = None                             # store primary keys
    try:
        cursor.executemany(sql, args)           # execute orginal SQL, with args or none.
        pmkey = cursor.lastrowid
        if conn is not None:
            conn.commit()                   # DELETE, INSERT, UPDATE operations should commit.
    except pymysql.Error as e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))

    return pmkey            # sql-execute results.


# Function:  create database
# Parameter: cursor: MySQL cursor; db_name: database name
# Format:    db_name: {"create_db":"base_api_test"}
# Return:    None.
def create_database(conn, cursor, db_name):
    r = 1
    try:
        sql = "CREATE DATABASE IF NOT EXISTS %s" % db_name      # orginal database-create sql
        r = sql_execute(conn, cursor, sql, None)
    except pymysql.Error as e:
        logger.error("------------Error %d: %s" % (e.args[0], e.args[1]))
    return r


# Function:  drop database
# Parameter: cursor: MySQL cursor; db_name: database name
# Format:    db_name: {"drop_db":"base_api_test"}
# Return:    None.
def drop_database(cursor, db_name):
    sql = "DROP DATABASE IF EXISTS %s" % db_name            # orginal drop-database sql
    sql_execute_noreturn(cursor, sql, None)


# Function:  create tables
# Parameter: cursor: MySQL cursor; create_scripts: orignal create tables sql
# Format:    create_scripts: {"create_tb":["script1","script2"]}, scripts is ordered according to foreign key
# Return:    None.
def create_tables(cursor, create_scripts):
    if len(create_scripts) == 0:            # none sql script
        logger.info("None table to create.")
        return -1

    try:
        for script in create_scripts:       # fetch one table-create script a time
            cursor.execute(script)
            logger.error("SQL Result: %s", cursor.fetchone())
    except pymysql.Error as e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))
        return 0
    return 1


# Function:  drop tables list, ordered by foreign key dependence
# Parameter: cursor: MySQL cursor; tables_list: tables to be dropt
# Format:    tables_list: {"drop_tb":["table1","table2"]}
# Return:    None.
def drop_tables(cursor, tables_list):
    if len(tables_list) == 0:               # none table to drop
        logger.error("None table to drop.")
        return -1

    try:
        for table in tables_list:           # fetch one table a time
            cursor.execute("DROP TABLE %s" % table)
            logger.debug("SQL Result: %s", cursor.fetchone())
    except pymysql.Error as e:
        logger.error("Error %d: %s" % (e.args[0], e.args[1]))

    return 1


# Function:  build INSERT orignal SQL: INSERT INTO table (col1, col2, ..) VALUES (%s, %s, ...)
# Parameter: table: table name; row_data: columns and coresponding values
# Return:    INSERT orignal SQL
def build_insertsql(table, row_data):
    qmarks = ','.join(["%s"] * len(row_data))         # build VALUES sub string: "%s, %s, ..."
    cols = ','.join(row_data.keys())                  # build COLUMNS sub string: "col1, col2, ..."
    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, qmarks)  # build orginal INSERT SQL with table, columns and %s for values
    return sql


# Function:  insert
# Parameter: conn: MySQL connection; cursor: MySQL cursor; insert_data: table name and data to be inserted.
# Format:    tables_list: {"insert":{"table_name":["col1":val1, "col2":val2]}}
# Return:    Primary keys list.
def insert_row(conn, cursor, insert_data):
    if len(insert_data) == 0:               # none data to insert
        logger.debug("None data to insert.")
        return []

    pmkey = []              # store inserted row id
    for table, data in insert_data.items():     # fetch table name and data list
        for one_script in data:                 # fetch a row, keys coresponding to column name
            # qmarks = ','.join(["%s"] * len(one_script))         # build VALUES sub string: "%s, %s, ..."
            # cols = ','.join(one_script.keys())                  # build COLUMNS sub string: "col1, col2, ..."
            # sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, qmarks)
            #  build orginal INSERT SQL with table, columns and %s
            sql = build_insertsql(table, one_script)
            # execute INSERT SQL, values of dict as the arguments
            pmkey.append(sql_execute_keyreturn(None, cursor, sql, one_script.values()))

    conn.commit()

    return pmkey            # return rows' primary keys list


# Function:  insert without commit.
# Parameter: cursor: MySQL cursor; insert_data: table name and data to be inserted.
# Format:    tables_list: {"insert_nocmt":{"table_name":["col1":val1, "col2":val2]}}
# Return:    Primary keys list.
def insert_row_nocommit(cursor, insert_data):
    if len(insert_data) == 0:               # none data to insert
        logger.debug("None data to insert.")
        return []
    pmkey = []              # store inserted row id
    for table, data in insert_data.items():     # fetch table name and data list
        for one_script in data:                 # fetch a row, keys coresponding to column name
            sql = build_insertsql(table, one_script)
            # execute INSERT SQL, values of dict as the arguments
            pmkey.append(sql_execute_keyreturn(None, cursor, sql, one_script.values()))
    return pmkey            # return rows' primary keys list


# Function:  insert one sql with multi arguments.
# Parameter: cursor: MySQL cursor; insert_data: table name and data to be inserted.
# Format:    tables_list: {"insert_many":{"table_name":["col1":val1, "col2":val2]}}
# Return:    Primary keys list.
def insert_many(cursor, insert_data):
    if len(insert_data) == 0:               # none data to insert
        logger.debug("None data to insert.")
        return []

    args = []
    pmkey = []
    # sql= ""
    for table, data in insert_data.items():     # fetch table name and data list
        if len(data) == 0:
            return []
        else:
            sql = build_insertsql(table, data[0])

        for one_script in data:                 # fetch a row, keys coresponding to column name
            args.append(one_script.values())    # build arguments list

        pmkey.append(sql_executemany(None, cursor, sql, args))

    return pmkey        # return rows' primary keys list


# Function:  insert row table one by one with foreignkey
# Parameter: conn: MySQL connection; cursor: MySQL cursor; insert_data: table name and data to be inserted.
# Format:    tables_list: {"insert_fk":[{"table_name":{"data":{"col1":val1, "col2":val2}, "foreignkey":"col"}}]}
# Return:    Last inserted primary key.
def insert_row_foreignkey(conn, cursor, insert_data):
    if len(insert_data) == 0:               # none data to insert
        logger.debug("None data to insert.")
        return -1

    row_id = 0              # row primary key id
    # fetch each table's data: {"table_name":{"data":{"col1":val1, "col2":val2}, "foreignkey":"col"}}]}
    for one_script in insert_data:
        for table, one_row in one_script.items():       # fetch table name and row data
            data_dict = one_row             # copy data for adding foreignkey key-val pair
            if "foreignkey" in one_row:     # check if table has a foreign key
                data_dict = one_row["data"]
                data_dict[one_row["foreignkey"]] = row_id       # last table's insert-row id as foreignkey value

            sql = build_insertsql(table, data_dict)
            logger.debug(data_dict)
            pmkey = sql_execute_keyreturn(conn, cursor, sql, data_dict.values())
            row_id = pmkey               # store insert-row id
            logger.debug(pmkey)

    return row_id           # last inserted primary key


# Function:  UPDATE & DELETE operation using orignal SQL
# Parameter: conn: MySQL connection; cursor: MySQL cursor; sql_list: SQL script list
# Format:    sql_list: UPDATE-{"update":["sql1"]}, DELETE-{"delete":["sql1"]}
# Return:    sql result
def update_row(conn, cursor, sql_list):
    ret = ["success"]
    for sql in sql_list:
        sql_result = sql_execute(conn, cursor, sql, None)
        if len(sql_result) > 0:
            ret = ["fail", sql_result]
    return ret


# Function:  SELECT operation using orignal SQL
# Parameter: cursor: MySQL cursor; sql_list: SQL script list
# Format:    sql_list: {"select":["sql1"]}
# Return:    sql result
def select_row(cursor, sql_list):
    ret = []
    for sql in sql_list:
        sql_result = sql_execute(None, cursor, sql, None)
        if len(sql_result) > 0:
            ret.append(sql_result)
    return ret


# Function: Querying with original SQL and fetch one result
# Parameter: cursor: MySQL Cursor; sql: SQL script; param: Query parameter
def select_one_row(cursor, sql, param=None):
    cursor.execute(sql, param)
    return cursor.fetchone()


# Function:  SELECT operation using orignal SQL, with only 1 sql as parameter
# Parameter: cursor: MySQL cursor; sql: SQL script
# Format:    sql_list: {"select":"sql1"}
# Return:    sql result
def select_onesql(cursor, sql):
    ret = sql_execute(None, cursor, sql, None)
    return ret


# Function:  create user
# Parameter: conn: MySQL connection; cursor: MySQL cursor; user_info: user name and password
# Format:    tables_list: {"create_user":{"user":"finger", "password":"ca$hc0w"}}
# Return:    sql result
def db_user_create(conn, cursor, user_info):
    sql = "CREATE USER %s IDENTIFIED BY %s"
    args = [user_info["user"], user_info["password"]]       # build sql arguments

    ret = sql_execute(conn, cursor, sql, args)
    logger.debug("User: %s is created." % user_info["user"])
    return ret


# Function:  delete user
# Parameter: conn: MySQL connection; cursor: MySQL cursor; user_name: user name
# Format:    tables_list: {"delete_user":"finger"}
# Return:    sql result
def db_user_delete(conn, cursor, user):
    sql = "DROP USER %s"
    args = [user]

    sql_execute(conn, cursor, sql, args)
    logger.debug("User: %s is deleted." % user)


# Function:  reset user's password
# Parameter: conn: MySQL connection; cursor: MySQL cursor; user_info: user name and password
# Format:    tables_list: {"set_passwd":{"user":"finger", "password":"finger"}}
# Return:    sql result
def set_passwd(conn, cursor, user_info):
    sql = "SET PASSWORD FOR %s = PASSWORD(%s)"
    args = [user_info["user"], user_info["password"]]       # build sql arguments

    sql_execute(conn, cursor, sql, args)
    logger.debug("Password of user: %s has changed." % user_info["user"])


# Function:  backup databases using mysqldump
# Parameter: backup_info: arguments needed by mysqldump
# Format:    tables_list: {"backup_db":{"user":"", "password":"", "file":"", "dblist":[db1]}}
# Return:    sql result
def db_backup(backup_info):
    db_user = backup_info["user"]
    db_passwd = backup_info["password"]
    backup_file = backup_info["file"]
    db_list = backup_info["dblist"]
    if len(db_list) == 0:
        logger.debug("None db to backup.")
        return -1

    db_join = ' '.join(db_list)             # build database list as "db1 db2 ..."
    logger.debug(db_join)
    # use mysqldump to backup databases. use "--password" to assign password without inputting while mysqldump
    cmd = "mysqldump -u %s --password=%s --databases %s > %s" % (db_user, db_passwd, db_join, backup_file)
    os.system(cmd)

    return 1


# Function:  restore databases from backup file
# Parameter: restore_info: arguments needed by mysqldump
# Format:    tables_list: {"restore_db":{"user":"", "password":"", "file":"", "dblist":[db1]}}
# Return:    sql result
def db_restore(restore_info):
    db_user = restore_info["user"]
    db_passwd = restore_info["password"]
    backup_file = restore_info["file"]
    db_list = restore_info["dblist"]
    if len(db_list) == 0:           # None database to restore
        logger.debug("None database to resotre.")
        return
    elif len(db_list) == 1:         # Only 1 database to restore
        cmd = "mysql -u %s --password=%s %s < %s" % (db_user, db_passwd, db_list[0], backup_file)
    else:                           # multi databases to restore
        cmd = "mysql -u %s --password=%s < %s" % (db_user, db_passwd, backup_file)
    os.system(cmd)
