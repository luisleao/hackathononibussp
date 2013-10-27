#!/usr/bin/python

import sys
import os
import json
import pyes, pprint
import codecs
import MySQLdb

from datetime import datetime, timedelta
from os import listdir
from StringIO import StringIO


def save_file(filename, json_data):
  #print "salvando '%s'..." % filename
  with open(filename, "w") as the_file:
    the_file.write(json.dumps(json_data, encoding="utf-8")) #iso-8859-1"))
    the_file.close()
  #print "file saved"

pagesizelimit = 1000

countQryString = "SELECT COUNT( * ) FROM MO"

qryString = '\
       SELECT MO.dt_movto, MO.dt_avl, MO.nr_latitude_grau, MO.nr_longitude_grau, AV.veiculo, CONCAT( AL.linha,  "", AL.tipo,  "", AL.sentido -1 ) AS cod_linha \
FROM MO \
JOIN AL ON ( AL.cd_linha = MO.cd_linha ) \
JOIN AV ON ( AV.nr_identificador = MO.nr_identificador ) \
WHERE 1 \
LIMIT %d \
OFFSET %d \
;'

mydb = MySQLdb.connect(host='localhost',
    user='root',
    passwd='muggler',
    db='hackatonsptrans2013')
cursor = mydb.cursor()

cursor.execute(countQryString)
count_records = int(cursor.fetchone()[0])

print "processando %d registros" % count_records
#sys.exit(0)

offset = 0
while offset <= count_records:
  
  cursor.execute(qryString % (pagesizelimit, offset))
  print "selecionados registros %d-%d de %d" % (offset+1, offset+pagesizelimit, count_records)
  offset+=pagesizelimit
  
  #print cursor.fetchone()
  #sys.exit(0)

  open_files = []
  save_json = []

  # resultados:
  # 0 dt_movto
  # 1 dt_avl
  # 2 nr_lat_grau
  # 3 nr_long_grau  
  # 4 veiculo
  # 5 cod_linha
  for r in cursor:
    
    #print r
    dt_movto = r[0]
    dt_avl = r[1]
    nr_lat_grau = r[2]
    nr_long_grau   = r[3]
    veiculo = str(r[4])
    cod_linha = r[5]

    try:      
      avl_json = open("../web/data/linhas/avl/%s_avl.json" % cod_linha)
      avl_linha = json.load(avl_json)
      open_files.append(avl_json)
      #avl_linha["veiculos"].values()[0].append([123,123,123])
      #print avl_linha["veiculos"].values()[0]
      #raw_input("continue...")
      #print 'arquivo avl da linha %s encontrado, carregando...' % cod_linha   
    except IOError:
      #print 'nova linha %s encontrada, criando arquivo...' % cod_linha
      avl_linha={}
      avl_linha["cod_linha"] = cod_linha
      avl_linha["veiculos"] = {}

    save_json.append(avl_linha)

    if not avl_linha["veiculos"].has_key(veiculo):
      #print avl_linha["veiculos"]
      #print veiculo
      #raw_input("continue...")

      avl_linha["veiculos"][veiculo] = []
    #else:
      #print avl_linha["veiculos"][veiculo]
      #raw_input("continue...")


    #avl_linha["veiculos"][veiculo].append((dt_movto.strftime("%s"), dt_avl.strftime("%s"), nr_lat_grau, nr_long_grau))
    avl_linha["veiculos"][veiculo].append([dt_movto.strftime("%s"), nr_lat_grau, nr_long_grau])

    #avl_linha["veiculos"][veiculo]["avl"]["dt_movto"] = dt_movto.strftime("%s")
    #avl_linha["veiculos"][veiculo]["avl"]["dt_avl"] = dt_avl.strftime("%s")
    #avl_linha["veiculos"][veiculo]["avl"]["nr_lat_grau"] = nr_lat_grau
    #avl_linha["veiculos"][veiculo]["avl"]["nr_long_grau"] = nr_long_grau
  
  print "salvando %d arquivos" % (len(save_json))
  for j in save_json:
    #print j
    save_file("../web/data/linhas/avl/%s_avl.json" % j['cod_linha'], j)
  save_json = []

  print "fechando %d arquivos" % (len(open_files))
  for f in open_files:
    f.close()
  open_files = []

cursor.close()