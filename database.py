import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'library_b'
TABLE = {}
TABLE['book'] = (
    "CREATE TABLE `book` ("
    "   `id` int(15) NOT NULL AUTO_INCREMENT,"
    "   `book_name` varchar(45) NOT NULL,"
    "   `book_description` varchar(100) NOT NULL,"
    "   `book_code` varchar(45) NOT NULL,"
    "   `book_category` varchar(30) NOT NULL,"
    "   `book_author` varchar(30) NOT NULL,"
    "   `book_publisher` varchar(30) NOT NULL,"
    "   `book_price` int(15) NOT NULL,"
    "   primary key (`id`)"
    ") ENGINE=InnoDB")

TABLE['clients'] = (
    "CREATE TABLE `clients` ("
    "   `id` int(15) NOT NULL AUTO_INCREMENT,"
    "   `client_name` varchar(50) NOT NULL,"
    "   `client_email` varchar(50) NOT NULL,"
    "   `client_national_id` varchar(20) NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLE['users'] = (
    "CREATE TABLE `users` ("
    "   `id` int(15) NOT NULL AUTO_INCREMENT,"
    "   `user_name` varchar(50) NOT NULL,"
    "   `user_email` varchar(50) NOT NULL,"
    "   `user_password` varchar(50) NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLE['dayoperations'] = (
    "CREATE TABLE `dayoperations` ("
    "   `id` int(15) NOT NULL AUTO_INCREMENT,"
    "   `book_code` varchar(20) NOT NULL,"
    "   `type` varchar(20) NOT NULL,"
    "   `days` int(15) NOT NULL,"
    "   `date` DATE NOT NULL,"
    "   `client_national_id` varchar(45) NOT NULL,"
    "   `to_date` DATE NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLE['category'] = (
    "CREATE TABLE `category` ("
    "   `id` int(15) NOT NULL AUTO_INCREMENT,"
    "   `category_name` varchar(45) NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLE['authors'] = (
    "CREATE TABLE `authors` ("
    "   `id` int(15) NOT NULL AUTO_INCREMENT,"
    "   `author_name` varchar(40) NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLE['publisher'] = (
    "CREATE TABLE `publisher` ("
    "   `id` int(15) NOT NULL AUTO_INCREMENT,"
    "   `publisher_name` varchar(45) NOT NULL,"
    "   PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

db = mysql.connector.connect(host='127.0.0.1', user='root', password='@615$011m9841k@')
cursor = db.cursor()


def create_database(cursor):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print('Failed Creating Database: {}'.format(err))
        exit(1)


try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        db.database = DB_NAME
    else:
        print(err)
        exit(1)

for table_name in TABLE:
    table_description = TABLE[table_name]
    try:
        print("Creating table {}".format(table_name), end='')
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Already exists!")
        else:
            print(err.msg)
    else:
        print('Ok')

cursor.close()
db.close()
