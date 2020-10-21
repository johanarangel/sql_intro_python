#! usr/bin/env python
'''SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Johana Rangel"
__email__ = "johanarang@hotmail.com"
__version__ = "1.1"

import sqlite3
import csv

def create_schema():
     
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()

    c.execute("""
                DROP TABLE IF EXISTS libro;
            """)

    c.execute("""
            CREATE TABLE libro(
                [id] INTEGER PRIMARY KEY AUTOINCREMENT,
                [titulo] TEXT NOT NULL,
                [pags] INTEGER NOT NULL,
                [author] TEXT 
            );
            """)

    conn.commit()
    conn.close()

def fill():

    with open('libreria.csv', 'r') as archivo:
        data = list(csv.DictReader(archivo))
    
        libros = []
        for x in range(len(data)):    
            titulo = data[x]['titulo']
            pags = int(data[x]['cantidad_paginas'])
            author = data[x]['autor']
            libros.append((titulo, pags, author))
    
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()

    for x in libros:
        c.execute("""
            INSERT INTO libro (titulo, pags, author)
            VALUES(?,?,?);""", x)

    conn.commit()
    conn.close()

def fetch(id):
      
    if id == 0:
        
        conn = sqlite3.connect('libreria.db')
        c = conn.cursor()
        c.execute("""SELECT * FROM libro;""")
        
        while True:
            row = c.fetchone()
            if row is None:
                break
            print(row)

        conn.commit()
        conn.close()

    elif id > 0:
        
        conn = sqlite3.connect('libreria.db')
        c = conn.cursor()

        for row in c.execute("""SELECT titulo, pags, author FROM libro WHERE id=?;""", (id,)):
            print('Fila:', id, 'resultado:', row)
          
        conn.commit()
        conn.close()  

def search_author(titulo):

    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()

    for row in c.execute("""SELECT author FROM libro WHERE titulo=?;""", (titulo,)):
        print('El autor de:', titulo, 'es:', row)
        
    conn.commit()
    conn.close() 

def update(id, titulo):
    
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()

    rowcount = c.execute("UPDATE libro SET titulo = ? WHERE id =?",
                         (titulo, id)).rowcount

    print('Filas actualizadas:', rowcount)
    
    for row in c.execute("""SELECT * FROM libro;"""):
        print(row)
        
    conn.commit()
    conn.close()

def delete(titulo):
    
    conn = sqlite3.connect('libreria.db')
    c = conn.cursor()

    rowcount = c.execute("DELETE FROM libro WHERE titulo = ?", (titulo,)).rowcount            

    print('Filas actualizadas:', rowcount)
    
    for row in c.execute("""SELECT * FROM libro;"""):
        print(row)
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    
    create_schema()
    fill()
    fetch(0)
    fetch(3)
    fetch(20)
    search_author('Relato de un naufrago')
    update(3, 'La culpa es de la pereza')
    delete('Boquitas pintadas')