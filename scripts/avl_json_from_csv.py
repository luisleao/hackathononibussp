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
  #print "salvando '%s'..." % filename
  with open(filename, "w") as the_file:
    the_file.write(json.dumps(json_data, encoding="utf-8")) #iso-8859-1"))
    the_file.close()
 # print "file saved"


av_map = {}
al_map = {}
avl_linha = {}


# carrega AV
csv_data = csv.reader(file(sys.argv[1]), delimiter=',')
for row in csv_data:
  av_map[row[0]] = row[1]
print "AV carregado."


# carrega AL
csv_data = csv.reader(file(sys.argv[2]), delimiter=',')
for row in csv_data:
  al_map[row[2]] = str(row[0])+str(row[1])+str((int(row[3])-1))
print "AL carregado."


# monta MO
csv_data = csv.reader(file(sys.argv[3]), delimiter=',')

i = 0
for row in csv_data:
  i = i+1

  dt_movto = datetime(*strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")[0:6]).strftime("%s")
  try:
    cod_linha = al_map[row[2]]
  except KeyError:
    pass
    #print "inconsistencia identificada: cod_linha %s da tabela MO nao consta na tabela AL" %(row[2],)

  try:
    veiculo = int(av_map[row[5]])
  except KeyError:
    pass
    #print "inconsistencia identificada: nr_identificador %s da tabela MO nao consta na tabela AV" %(row[5],)

  nr_latitude_grau = float(row[3])
  nr_longitude_grau = float(row[4])

  if not avl_linha.has_key(cod_linha):
    avl_linha[cod_linha] = { "cod_linha" : cod_linha, "veiculos" : {} }

  if not avl_linha[cod_linha]["veiculos"].has_key(veiculo):
      avl_linha[cod_linha]["veiculos"][veiculo] = []

  avl_linha[cod_linha]["veiculos"][veiculo].append([dt_movto, nr_latitude_grau, nr_longitude_grau])

  #print avl_linha
  #raw_input("continue...")
  if i % 100000 == 0: print "%d rows processed" % i

  #if i > 10000: break

for linha in avl_linha:
  save_file("../web/data/linhas/avl2/%s_avl.json" % linha, avl_linha[linha])






