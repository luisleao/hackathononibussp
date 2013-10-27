#!/usr/bin/python
import csv
import sys
import datetime
from time import strptime

#TABELA;ATRIBUTOS;DESCRIÇÃO
#;;
#B_AAMMDD;;Registro de bilhetagem
#;data;data da utilização
#;hash;hash bilhete
#;sentido;sentido trajeto
#;veiculo;prefixo do veículo
#;validador;código do validador
#;linha;número e tipo de linha

# read the presidents.csv file using the python
# csv module http://docs.python.org/library/csv.html
csv_data = csv.reader(file(sys.argv[1]), delimiter='|')
# execute the for clicle and insert the csv into the
# database.

i = 0
for row in csv_data:
  i = i+1
  d = datetime.datetime(*strptime(row[0], "%d/%m/%Y %H:%M:%S")[0:6])
  row[0] = d
  #print row[0]
  #sys.exit(0)
  cursor.execute('INSERT INTO BLT (data ,hash \
                ,sentido ,veiculo ,validador ,linha)' \
                ' VALUES(%s, %s, %s, %s, %s, %s);', row)
  #print cursor._last_executed
  if (i%1000 == 0):
    mydb.commit()
    sys.stdout.write(str(i))
    sys.stdout.write('\r')
    #print cursor._last_executed
#close the connection to the database.
mydb.commit()
cursor.close()
print "Import to MySQL is over"

