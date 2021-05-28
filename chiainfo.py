'''
    This file is part of meisterPlotter.

    meisterPlotter is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    meisterPlotter is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with meisterPlotter.  If not, see <https://www.gnu.org/licenses/>.
'''

__title__ = 'meisterPlotter'
__version__ = '0.1b'
__author__ = 'Kekollons'
__license__ = 'GPLv3'
__copyright__ = 'Esta obra está licenciada bajo la Licencia Creative Commons Atribución-NoComercial-SinDerivadas 4.0 Internacional.Para ver una copia de esta licencia, visite http://creativecommons.org/licenses/by-nc-nd/4.0/ o envíe una carta a Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.'

import os
import subprocess

rutatxt = open ('rutaChia.txt','r')
ruta_chia = rutatxt.read()
    
dinero = []
allkeys = []
llavepalabra = ''
llaves = []
directoriosplot = []

def info():
    directoriosplot = []
    output_directorios = subprocess.check_output(['chia', 'plots', 'show'], cwd=ruta_chia, shell=True)
    estado_directorios = output_directorios.decode('UTF-8').split('\n')
    for linea in estado_directorios:
        if linea.find(':\\') > 0:
            directoriosplot.append(linea[0:-1])

    output_keys = subprocess.check_output(['chia', 'keys', 'show'], cwd=ruta_chia, shell=True)
    estado_keys = output_keys.decode('UTF-8').split(' ')
    for palabra in estado_keys:
        if len(palabra) > 30:
            llavepalabra = palabra.split('\n')
            llavepalabra = llavepalabra[0]
            allkeys.append(llavepalabra[0:-1])
    llaves = [allkeys[1], allkeys[2]]
    
    output_nodo = subprocess.check_output(['chia', 'show', '-s'], cwd=ruta_chia, shell=True)
    output_granja = subprocess.check_output(['chia', 'farm', 'summary'], cwd=ruta_chia, shell=True)
    output_cartera = subprocess.check_output(['chia', 'wallet', 'show'], cwd=ruta_chia, shell=True)
    output_nodo = output_nodo.decode('UTF-8')
    output_granja = output_granja.decode('UTF-8')
    output_cartera = output_cartera.decode('UTF-8')
    
    if output_nodo[27] == 'F':
        estado_nodo = 'Sincronizado'
    elif output_nodo[27] == 'N':
        estado_nodo = 'No sincronizado'
    else:
        estado_nodo = 'ERROR'
        
    if output_granja[16] == 'F':
        estado_granja = 'Farmeando'
    elif output_granja[16] == 'S':
        estado_granja = 'Sincronizando'
    elif output_granja[16] == 'N':
        estado_granja = 'No sincronizado'
    else:
        estado_granja = 'ERROR'
    
    if output_cartera[36] == 'S':
        estado_cartera = 'Sincronizado'
        dinero = []
        modoutput = output_cartera.split('\n')
        for cifra in modoutput:
            if cifra.find(' -') > 0:
                pos_cifra = cifra.find(': ') + 2
                xch_cifra = cifra[pos_cifra:-1].split(' (')
                dinero.append(xch_cifra[0])
            
    elif output_cartera[36] == 'N':
        dinero = ['0', '0', '0']
        estado_cartera = 'No sincronizado'
    else:
        dinero = ['0', '0', '0']
        estado_cartera = 'ERROR'
   
    return estado_nodo, estado_cartera, estado_granja, dinero, directoriosplot, llaves
info()