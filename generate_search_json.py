#-*- coding: utf-8 -*-

import os
import sqlite3
import argparse
import json

default_out = os.path.join(os.path.dirname(__file__), 'sitio/db.json')
default_db = os.path.join(os.path.dirname(__file__), 'db.db')

parser = argparse.ArgumentParser(description='Genera un fichero JSON para que use el buscador JS')
parser.add_argument('-f', '--db-file', default = default_db, help = 'Fichero SQLite')
parser.add_argument('-o', '--output', default = default_out, help = 'Fichero de salida del json. Por defecto %s' % default_out)

args = parser.parse_args()

con = sqlite3.connect(args.db_file)
cur = con.cursor()

artistas = dict()
q = """ SELECT
            slug, nombre
        FROM artista """
for slug, nombre in cur.execute(q):
    artistas[slug] = nombre

canciones = dict()
q = """ SELECT
            slug_artista,
            slug,
            titulo
        FROM cancion """
for slug_artista, slug_cancion, titulo in cur.execute(q):
    anterior = canciones.get(slug_artista, []) # Conservo la lista si existe
    anterior.append(dict(
        slug = slug_cancion,
        titulo = titulo
        ))
    canciones[slug_artista] = anterior

f = open(args.output, 'w')
f.write(json.dumps(dict(
    artistas = artistas,
    canciones = canciones)))
f.close()

print args.output, 'generado correctamente!'