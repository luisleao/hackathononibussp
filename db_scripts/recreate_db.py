#!/usr/bin/python

import MySQLdb
import sys

# open the connection to the MySQL server.
# using MySQLdb
mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='muggler',
    db='hackatonsptrans2013')
cursor = mydb.cursor()

cursor.execute('DROP TABLE IF EXISTS AL')
cursor.execute('DROP TABLE IF EXISTS AV')
cursor.execute('DROP TABLE IF EXISTS MO')
cursor.execute('DROP TABLE IF EXISTS BLT')

cursor.execute ('DROP DATABASE `hackatonsptrans2013`')

cursor.execute('CREATE DATABASE IF NOT EXISTS `hackatonsptrans2013` CHARACTER SET = utf8 COLLATE utf8_general_ci;')

cursor.execute('USE hackatonsptrans2013')

cursor.execute('CREATE TABLE IF NOT EXISTS `AV` \
			   ( \
			    `nr_identificador` INT(11) unsigned NOT NULL, \
				`veiculo` INT(11) unsigned NOT NULL \
				, PRIMARY KEY (`nr_identificador`) \
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
				)

cursor.execute('CREATE TABLE IF NOT EXISTS `AL` \
				( \
				`linha` VARCHAR(255) NOT NULL, \
				`tipo` INT(11) unsigned NOT NULL, \
				`cd_linha` INT(11) unsigned NOT NULL, \
				`sentido` INT(11) unsigned NOT NULL\
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
				)

cursor.execute('CREATE TABLE IF NOT EXISTS `MO` \
				( \
				`dt_movto` DATETIME NOT NULL,  \
				`dt_avl` DATETIME NOT NULL, \
				`cd_linha` INT(11) unsigned NOT NULL, \
				`nr_latitude_grau` FLOAT NOT NULL, \
				`nr_longitude_grau` FLOAT NOT NULL, \
				`nr_identificador` INT(11) unsigned NOT NULL \
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
				)

cursor.execute('CREATE TABLE IF NOT EXISTS `BLT` \
				( \
				`data` DATETIME NOT NULL,  \
				`hash` INT(11) unsigned NOT NULL, \
				`sentido` VARCHAR(255) NOT NULL, \
				`veiculo` INT(11) unsigned NOT NULL, \
				`validador` INT(11) unsigned NOT NULL, \
				`linha` VARCHAR(255) NOT NULL \
				) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
				)


#close the connection to the database.
cursor.close()
print "All tables created"