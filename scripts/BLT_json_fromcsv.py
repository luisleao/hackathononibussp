#!/usr/bin/python

import csv
import sys
import os
import json
import pyes, pprint
import codecs

from datetime import datetime, timedelta
from time import strptime
from os import listdir
from StringIO import StringIO

def save_file(filename, json_data):
  print "salvando '%s'..." % filename
  with open(filename, "w") as the_file:
    the_file.write(json.dumps(json_data, encoding="utf-8")) #iso-8859-1"))
    the_file.close()
  print "file saved"


# read the presidents.csv file using the python
# csv module http://docs.python.org/library/csv.html
csv_data = csv.reader(file(sys.argv[1]), delimiter='|')
# execute the for clicle and insert the csv into the
# database.

blt_hshmap = {}

i = 0
for row in csv_data:
  i = i+1

  data = datetime(*strptime(row[0], "%d/%m/%Y %H:%M:%S")[0:6]).strftime("%s")
  cod_linha = row[5] + ('0' if row[2] == "TP_TS" else '1')
  veiculo = str(row[3])

  blt_hshmap

  if not blt_hshmap.has_key(cod_linha):
    blt_hshmap[cod_linha] = { "veiculos" : {} }

  if not blt_hshmap[cod_linha]["veiculos"].has_key(veiculo):
    blt_hshmap[cod_linha]["veiculos"][veiculo] = {}

  if not blt_hshmap[cod_linha]["veiculos"][veiculo].has_key(data):
    blt_hshmap[cod_linha]["veiculos"][veiculo][data] = 0

  blt_hshmap[cod_linha]["veiculos"][veiculo][data] = blt_hshmap[cod_linha]["veiculos"][veiculo][data] + 1

  #print blt_hshmap
  #raw_input("continue...")
  if i % 100000 == 0: print "%d rows processed" % i

  #if i > 10000: break

for linha in blt_hshmap:
  save_file("../web/data/linhas/blt/%s_blt.json" % linha, blt_hshmap[linha])






