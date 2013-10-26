#!/usr/bin/python
#simple python csv parser that export Comma
#Separated Value data into a MySQL database.
#phillip@bailey.st
import csv
import MySQLdb
import sys

#if(not(sys.argv[1] and sys.argv[2])):
#  print "usage: <script> <file name> <table name>"
#  sys.exit(0)

# open the connection to the MySQL server.
# using MySQLdb
mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='muggler',
    db='hackatonsptrans2013')
cursor = mydb.cursor()
# read the presidents.csv file using the python
# csv module http://docs.python.org/library/csv.html
csv_data = csv.reader(file(sys.argv[1]), delimiter=',')
# execute the for clicle and insert the csv into the
# database.

#i = 0;
for row in csv_data:
    #i=i+1
    #print str(i)+":"
    #print row
    #sys.exit(0)
    cursor.execute('INSERT INTO AL (linha, tipo, cd_linha, sentido)' \
            ' VALUES(%s, %s, %s, %s);', row)
    print cursor._last_executed
    #raw_input("Press Enter to continue...")

#close the connection to the database.
mydb.commit()
cursor.close()
print "Import to MySQL is over"

