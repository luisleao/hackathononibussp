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

countQryString = "SELECT COUNT( * ) FROM BLT"

#qryString = '\
#SELECT BLT.data, BLT.hash, BLT.veiculo, CONCAT( AL.linha,  "", AL.tipo,  "", AL.sentido -1 ) AS cod_linha \
#FROM BLT \
#JOIN AL ON ( BLT.linha = CONCAT(AL.linha, AL.tipo ) ) \
#WHERE 1 \
#LIMIT %d \
#OFFSET %d \
#;'

qryString = '\
SELECT BLT.data, count(BLT.hash), BLT.veiculo, CONCAT( AL.linha,  "", AL.tipo,  "", AL.sentido -1 ) AS cod_linha \
FROM BLT \
JOIN AL ON ( BLT.linha = CONCAT(AL.linha, AL.tipo ) ) \
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
  # 0 data
  # 1 hash
  # 2 veiculo  
  # 3 cod_linha

  for r in cursor:
    
    #print r
    #sys.exit(0)
    data = r[0]
    hhash = r[1]
    veiculo   = str(r[2])
    cod_linha = r[3]

    try:      
      blt_json = open("../web/data/linhas/blt/%s_blt.json" % cod_linha)
      blt_linha = json.load(blt_json)
      open_files.append(blt_json)
      #blt_linha["veiculos"].values()[0].append([123,123,123])
      #print blt_linha["veiculos"].values()[0]
      #raw_input("continue...")
      #print 'arquivo blt da linha %s encontrado, carregando...' % cod_linha   
    except IOError:
      #print 'nova linha %s encontrada, criando arquivo...' % cod_linha
      blt_linha={}
      blt_linha["cod_linha"] = cod_linha
      blt_linha["veiculos"] = {}

    save_json.append(blt_linha)

    if not blt_linha["veiculos"].has_key(veiculo):
      #print blt_linha["veiculos"]
      #print veiculo
      #raw_input("continue...")

      blt_linha["veiculos"][veiculo] = []
    #else:
      #print blt_linha["veiculos"][veiculo]
      #raw_input("continue...")

    blt_linha["veiculos"][veiculo].append([data.strftime("%s"), hhash])
  
  print "salvando %d arquivos" % (len(save_json))
  for j in save_json:
    #print j
    save_file("../web/data/linhas/blt/%s_blt.json" % j['cod_linha'], j)
  save_json = []

  print "fechando %d arquivos" % (len(open_files))
  for f in open_files:
    f.close()
  open_files = []

cursor.close()