import pymysql
import sqlparse
from dotenv import dotenv_values

config = dotenv_values('.flaskenv')
# MySql配置信息
HOST = config.get('MYSQL_HOST') or '127.0.0.1'
PORT = config.get('MYSQL_PORT') or 3306
DATABASE = config.get('MYSQL_DATABASE') or 'AdminFlask'
USERNAME = config.get('MYSQL_USERNAME') or 'root'
PASSWORD = config.get('MYSQL_PASSWORD') or '123456'


def is_exist_database():
    db = pymysql.connect(
        host=HOST,
        port=int(PORT),
        user=USERNAME,
        password=PASSWORD,
        charset='utf8mb4')
    cursor = db.cursor()
    sql = "SELECT COUNT(DISTINCT `TABLE_NAME`) AS anyAliasName FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `table_schema` = '%s';" % DATABASE
    res = cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results


def init_database():
    db = pymysql.connect(
        host=HOST,
        port=int(PORT),
        user=USERNAME,
        password=PASSWORD,
        charset='utf8mb4')
    cursor = db.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS %s CHARSET=utf8 COLLATE=utf8_general_ci;" % DATABASE
    res = cursor.execute(sql)
    db.close()
    return res


def execute_fromfile(filename):
    db = pymysql.connect(
        host=HOST,
        port=int(PORT),
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE,
        charset='utf8')
    fd = open(filename, 'r', encoding='utf-8')
    cursor = db.cursor()
    sqlfile = fd.read()
    sqlfile = sqlparse.format(sqlfile, strip_comments=True).strip()

    sqlcommamds = sqlfile.split(';')

    for command in sqlcommamds:
        try:
            cursor.execute(command)
            db.commit()

        except Exception as msg:

            db.rollback()
    db.close()


def init_db():
    if is_exist_database()[0][0] > 0:
        print('数据库%s不为空，不进行初始化操作' % str(DATABASE))
        return
    if init_database():
        print('数据库%s创建成功' % str(DATABASE))
    execute_fromfile('init_db.sql')
    print('表创建成功')
