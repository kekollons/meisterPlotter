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

import sched, time, subprocess, sys, os, threading, psutil
from datetime import datetime
from pathlib import Path
import json
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')

rutatxt = open ('rutaChia.txt','r')
ruta_chia = rutatxt.read()

k = ''
inparallel = ''
queue = ''
threads = ''
ram = ''
bitfield = ''
excludefinaldir = ''
tempdir1 = ''
tempdir2 = ''
finaldirs = ''
autosched = ''
relativetimes = ''
startat = ''
startdatetime = ''
delay1 = 0
delay2 = 0
delay3 = 0
delay4 = 0
delay5 = 0
delay6 = 0
delay7 = 0
delay8 = 0
delay9 = 0
delay10 = 0
delay11 = 0
delay12 = 0
secuencia = []
sequence = []
sequeuence = []
nplots = 0
farmerkey = ''
poolkey = ''
fecha_form = '%Y/%m/%d %H:%M:%S'

def timecalc():
        if startat is True:
            timestart = datetime.strptime(startdatetime, fecha_form)
            if timestart > datetime.now():
                delay1 = timestart - datetime.now()
                delay1 = delay1.total_seconds()
            else:
                delay1 = 0
        else:
            delay1 = 0
        if relativetimes == False:
            sequence.append(delay1)
            sequence.append(delay1 + (delay2*60))
            sequence.append(delay1 + (delay3*60))
            sequence.append(delay1 + (delay4*60))
            sequence.append(delay1 + (delay5*60))
            sequence.append(delay1 + (delay6*60))
            sequence.append(delay1 + (delay7*60))
            sequence.append(delay1 + (delay8*60))
            sequence.append(delay1 + (delay9*60))
            sequence.append(delay1 + (delay10*60))
            sequence.append(delay1 + (delay11*60))
            sequence.append(delay1 + (delay12*60))
            return sequence[0:inparallel+1]
        elif relativetimes == True:
            sequence.append(delay1)
            sumadelay = delay1 + (delay2*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay3*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay4*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay5*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay6*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay7*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay8*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay9*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay10*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay11*60)
            sequence.append(sumadelay)
            sumadelay = sumadelay + (delay12*60)
            sequence.append(sumadelay)
            return sequence[0:inparallel+1]
        else:
            logging.info('ERROR')

def queuecalc():
    letter_dir = []
    letter_free = []
    
    for ruta in finaldirs:
        letter_dir.append(ruta[0:2])
       
    #letter_dir = list(set(letter_dir))
    for letra in letter_dir:
        hdd = psutil.disk_usage(letra)
        letter_free.append(((hdd.free // (2**30))) // 102)
        
    free_plots = dict(zip(letter_dir, letter_free))
    #print(free_plots)
    
    xqueue = queue // (inparallel+1)
    xqueue_float = queue / (inparallel+1)
    xqueue_dif = int(((xqueue_float - xqueue) + 0.01) * (inparallel+1))
    for unit in range(inparallel+1):
        if unit < xqueue_dif:
            sequeuence.append(xqueue+1)
        else:
            sequeuence.append(xqueue)
    #print(sequeuence)
    
    n=0
    acarreo = 0
    #try:
    for cola in sequeuence:
        xlist = []
        for x in letter_free:
            xlist.append(0)
        if cola >= letter_free[n] - acarreo:
            acarreo = cola - letter_free[n]
            xlist[n] = letter_free[n]
            n = n + 1 
            if acarreo != 0:
                if acarreo >= letter_free[n] - acarreo:
                    acarreo = acarreo - letter_free[n]
                    xlist[n] = letter_free[n]
                    n = n + 1
                    if acarreo != 0:
                        if acarreo >= letter_free[n] - acarreo:
                            acarreo = acarreo - letter_free[n]
                            xlist[n] = letter_free[n]
                            n = n + 1
                            if acarreo != 0:
                                if acarreo > letter_free[n] - acarreo:
                                    acarreo = acarreo - letter_free[n]
                                    xlist[n] = letter_free[n]
                                    n = n + 1
                                else:
                                    xlist[n] = acarreo
                        else:
                            xlist[n] = acarreo
                else:
                    xlist[n] = acarreo
        else:
            xlist[n] = cola
        secuencia.append(xlist)
                
    #except:
        #logging.info('Calculate space ERROR!')
    #print(secuencia)
    return secuencia
                
def read_data():
    global k, inparallel, queue, threads, ram, bitfield, excludefinaldir, tempdir1, tempdir2, finaldirs, autosched, relativetimes, startat, startdatetime, delay2, delay3, delay4, delay5, delay6, delay7, delay8, delay9, delay10, delay11, delay12, farmerkey, poolkey
        
    with open('newplot.newplot') as json_file:
        data = json.load(json_file)
        for param in data['cfg']:
            k = param['k']
            inparallel = param['inparallel']
            queue = param['queue']
            threads = param['threads']
            ram = param['ram']
            bitfield = param['bitfield']
            excludefinaldir = param['excludefinaldir']
            tempdir1 = param['tempdir1']
            tempdir2 = param['tempdir2']
            finaldirs = param['finaldirs']
            autosched = param['autosched']
            relativetimes = param['relativetimes']
            startat = param['startat']
            startdatetime = param['datetime']
            delay2 = param['delay2']
            delay3 = param['delay3']
            delay4 = param['delay4']
            delay5 = param['delay5']
            delay6 = param['delay6']
            delay7 = param['delay7']
            delay8 = param['delay8']
            delay9 = param['delay9']
            delay10 = param['delay10']
            delay11 = param['delay11']
            delay12 = param['delay12']
            farmerkey = param['farmerkey']
            poolkey = param['poolkey']

def createplot(pr_queue, pr_time, pr_hilo):
    global k, inparallel, queue, threads, ram, bitfield, excludefinaldir, tempdir1, tempdir2, finaldirs, autosched, relativetimes, startat, startdatetime, delay2, delay3, delay4, delay5, delay6, delay7, delay8, delay9, delay10, delay11, delay12, farmerkey, poolkey, ruta_chia
    nqueue = pr_queue
    ntime = pr_time
    nhilo = str(pr_hilo)
    ptempdir1 = Path(tempdir1)
    ptempdir2 = Path(tempdir2)
    
    if k == 1:
        kn = '33'
    elif k == 2:
        kn = '34'
    else:
        kn = '32'

    def th_plotting():
        if tempdir2 == "":
            command = ['start', 'cmd', '/c', 'chia', 'plots', 'create',
                    '-k', kn, '-b', str(ram), '-r',str(threads+1),
                    '-f', farmerkey, '-p', poolkey,
                    '-t', ptempdir1]
        else:
            command = ['start', 'cmd', '/c', 'chia', 'plots', 'create',
                    '-k', kn, '-b', str(ram), '-r', str(threads+1),
                    '-f', farmerkey, '-p', poolkey,
                    '-t', ptempdir1, '-2', ptempdir2]
                
        if bitfield is True:
            command.append('-e')
        if excludefinaldir is True:
            command.append('-x')
        
        command.extend(['-d', 'borrar', '-n', 'borrar'])    
        logging.info('Plotting starting in queque ' + nhilo)
        y = 0
        for ncola in nqueue:
            if ncola != 0:
                command = command[0:-4]
                command.append('-d')
                command.append(Path(finaldirs[y]))
                command.append('-n')
                command.append(str(ncola))
               
            y = y + 1
            #print(command)
            #prueba = subprocess.check_output(['start', 'cmd', '/c', 'chia', 'wallet', 'show'], cwd=ruta_chia, shell=True)
            subprocess.Popen(command, cwd=ruta_chia, shell=True)
            
        logging.info('Finished plot in queue ' + nhilo)
    
    #th_plotting()
    th_createplot = threading.Thread(target=th_plotting)
    th_createplot.start()

def programer():
    global seqtime, sequeue
    schedmod = sched.scheduler(time.time, time.sleep)
    
    for hilo in range(len(sequeue)):
        schedmod.enter(seqtime[hilo], 1, createplot, (sequeue[hilo], seqtime[hilo], hilo+1))
        logging.info('Create queue ' + str(hilo+1) + ', start in ' + str(seqtime[hilo]) + ' seconds')
    schedmod.run()
    
def main():
    global seqtime, sequeue
    read_data()
    seqtime = timecalc()
    sequeue = queuecalc()
    th_program = threading.Thread(target=programer)
    th_program.start()
    #createplot(sequeue[0], seqtime[0], 1)
    
    
if __name__ == '__main__':
    main()